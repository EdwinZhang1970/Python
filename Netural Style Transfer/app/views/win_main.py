# coding:utf-8
# -----------------------------------------------------------------------------
# 所有窗体，以 WinBase() 为基类,  WinBase.win 为 tk 的源组件；加一层，是为了防止命令冲突

# 引用时，用 parent, parent.win
# 扩展子组件，返回的实际的控件类型，如 self.widget_label, self.widget_frame
# 组件的容器，一律取 master
# label, button , 可通过 style name 来进行设置和渲染
# -----------------------------------------------------------------------------

from keras.preprocessing.image import load_img, img_to_array
from keras import backend as K

import numpy as np
from keras.applications import vgg19

from scipy.optimize import fmin_l_bfgs_b
from scipy.misc import imsave
import time

import os
import tkinter as tk
from tkinter import ttk
import tensorflow as tf

from framework import tk_utils as tku
from framework import utils
from app import my

from app.my import session
from app.my import img
from app.my import Color
from app.my import String
from app.my import Font


# 设置 GPU 的占用率，以免全部占用
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

workspace_dir = "workspace"
result_prefix = 'style_transfer_'
iterations = 5

style_weight = 1.
content_weight = 0.025

def preprocess_image(image_path, img_height, img_width):
    img = load_img(image_path, target_size=(img_height, img_width))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return img


def deprocess_image(x):
    # Remove zero-center by mean pixel
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    # 'BGR'->'RGB'
    x = x[:, :, ::-1]
    x = np.clip(x, 0, 255).astype('uint8')
    return x


def content_loss(base, combination):
    return K.sum(K.square(combination - base))


def gram_matrix(x):
    features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram


def style_loss(style, combination, img_height, img_width):
    S = gram_matrix(style)
    C = gram_matrix(combination)
    channels = 3
    size = img_height * img_width
    return K.sum(K.square(S - C)) / (4. * (channels ** 2) * (size ** 2))


def total_variation_loss(x, img_height, img_width):
    a = K.square(
        x[:, :img_height - 1, :img_width - 1, :] - x[:, 1:, :img_width - 1, :])
    b = K.square(
        x[:, :img_height - 1, :img_width - 1, :] - x[:, :img_height - 1, 1:, :])
    return K.sum(K.pow(a + b, 1.25))


class Evaluator(object):

    def __init__(self, img_height, img_width, fetch_loss_and_grads):
        self.loss_value = None
        self.grads_values = None
        self.img_height = img_height
        self.img_width = img_width
        self.fetch_loss_and_grads = fetch_loss_and_grads

    def loss(self, x):
        assert self.loss_value is None
        x = x.reshape((1, self.img_height, self.img_width, 3))
        outs = self.fetch_loss_and_grads([x])
        loss_value = outs[0]
        grad_values = outs[1].flatten().astype('float64')
        self.loss_value = loss_value
        self.grad_values = grad_values
        return self.loss_value

    def grads(self, x):
        assert self.loss_value is not None
        grad_values = np.copy(self.grad_values)
        self.loss_value = None
        self.grad_values = None
        return grad_values


# 主应用程序界面
class App(tku.WinBase):

    target_file_name = ""
    style_file_name = ""

    def __init__(self):
        tku.WinBase.__init__(self)

        self.title = String.r_app_title
        self.set_size(1024, 768)
        self.set_icon(img("Money.ico"))

        self.lay_body()

    def lay_body(self):
        self.lay_title(self.win).pack(fill=tk.X)

        self.lay_main(self.win).pack(expand=tk.YES, fill=tk.BOTH)

        self.lay_bottom(self.win).pack(fill=tk.X)

        self.txtIterations.insert('end', iterations)
        self.txtContent.insert('end', content_weight)
        self.txtStyle.insert('end', style_weight)
        return self.win

    def lay_title(self, parent):
        """ 标题栏 """
        frame = tk.Frame(parent, bg="black")

        def _label(_frame, text, size=12, bold=False):
            return tku.label(_frame, text, size=size, bold=bold, bg="black", fg="white")

        def _button(_frame, text, size=12, bold=False, width=12, command=None):   # bg = DarkSlateGray
            return tk.Button(_frame, text=text, bg="black", fg="white",
                             width=width, height=2, font=tku.font(size=size, bold=bold),
                             relief=tk.FLAT, command=command)

        _label(frame, String.r_app_title, 16, True).pack(side=tk.LEFT, padx=10)
        _label(frame, "").pack(side=tk.LEFT, padx=50)  # 用于布局的空字符串
        _label(frame, "").pack(side=tk.RIGHT, padx=5)
        _button(frame, "退出", width=8, command=self.do_close).pack(side=tk.RIGHT, padx=15)
        tku.image_label(frame, img("user.png"), 40, 40, False).pack(side=tk.RIGHT)

        return frame

    def lay_bottom(self, parent):
        """ 窗体最下面留空白 """
        frame = tk.Frame(parent, height=10, bg="whitesmoke")
        frame.propagate(True)
        return frame

    def lay_main(self, parent):
        frame = tk.Frame(parent, bg=Color.r_background)

        self.lay_org_image(frame).pack(side=tk.LEFT, fill=tk.Y)
        self.lay_result_image(frame).pack(expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)

        return frame

    def lay_org_image(self, parent):
        frame = tk.Frame(parent, bg=Color.r_whitesmoke, width=350)

        self.org_img = tku.ImageLabel(frame, width=300, height=300)
        self.org_img.pack(side=tk.TOP, fill=tk.Y, padx=10, pady=5)
        self.org_img.set_image(img("flower.jpg"))
        self.org_img.bind('<Button-1>', self.do_choice_image)
        self.target_file_name = img("flower.jpg")

        self.style_img = tku.ImageLabel(frame, width=300, height=300)
        self.style_img.pack(side=tk.TOP, padx=10, pady=5)
        self.style_img.set_image(img("style.jpg"))
        self.style_img.bind('<Button-1>', self.do_choice_style_image)
        self.style_file_name = img("style.jpg")  # 设置缺省风格格式文件


        tk.Button(frame, text=" 目标图片 ", bg="LightBlue", font=Font.r_normal, command=self.do_choice_image)\
            .pack(side=tk.LEFT, fill=tk.X, padx=20)
        tk.Button(frame, text=" 风格图片 ", bg="LightYellow", font=Font.r_normal, command=self.do_choice_style_image)\
            .pack(side=tk.LEFT, fill=tk.X)
        tk.Button(frame, text="开始转换", bg="LightGreen", font=Font.r_medium_title, command=self.do_transfer)\
            .pack(side=tk.RIGHT, fill=tk.X, padx=20)

        frame.propagate(True)
        frame.pack_propagate(0)
        return frame

    def lay_result_image(self, parent):
        frame = tk.Frame(parent, bg=Color.r_white)

        fra_result = tk.Frame(frame, bg=Color.r_white)
        fra_result.pack(expand=tk.YES, fill=tk.BOTH, pady=5)
        fra_result.pack_propagate(0)

        self.final_img = tku.ImageLabel(fra_result, width=460, height=460)
        self.final_img.pack(side='top', padx=10, pady=10)
        self.final_img.set_image(img("style_flower.png"))
        self.final_img.bind('<Button-1>', self.do_browser_workspace)

        tk.Button(fra_result, text=" 图片生成目录 ", bg="LightBlue", font=Font.r_small_content, command=self.do_browser_workspace)\
            .pack(side=tk.BOTTOM, anchor='se', padx=10)

        # --------------------------------------------------------------
        self.fra_output = tk.Frame(frame, height=200, bg=Color.r_whitesmoke)
        self.fra_output.pack(side=tk.BOTTOM, fill=tk.X)
        self.fra_output.pack_propagate(0)

        # fra_output-tabControl
        self.tabControl = ttk.Notebook(self.fra_output)  # Create Tab Control
        self.tabControl.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW)

        # fra_output - tabControl - tabParameters
        tabParameters = ttk.Frame(self.tabControl)
        self.tabControl.add(tabParameters, text='参数设置')

        f1 = tk.Frame(tabParameters)
        f1.pack(side='top', fill='x', pady=10)
        tk.Label(f1, text="循环次数", font=Font.r_small_title).pack(side='left', anchor='w', pady=3, padx=10)
        txtIterations = tk.Entry(f1, width=40, font=Font.r_normal)
        txtIterations.pack(side='left', anchor='n', padx=30, pady=3)
        self.txtIterations = txtIterations

        f2 = tk.Frame(tabParameters)
        f2.pack(side='top', fill='x')
        tk.Label(f2, text="内容权重", font=Font.r_small_title).pack(side='left', anchor='w', pady=3, padx=10)
        txtContent = tk.Entry(f2, width=40, font=Font.r_normal)
        txtContent.pack(side='left', anchor='n', padx=30, pady=3)
        self.txtContent = txtContent

        f3 = tk.Frame(tabParameters)
        f3.pack(side='top', fill='x', pady=10)
        tk.Label(f3, text="风格权重", font=Font.r_small_title).pack(side='left', anchor='w', pady=3, padx=10)
        txtStyle = tk.Entry(f3, width=40, font=Font.r_normal)
        txtStyle.pack(side='left', anchor='n', padx=30, pady=3)
        self.txtStyle = txtStyle

        # fra_output - tabControl - tabOutput
        self.tabOutput = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.tabOutput, text='处理信息')

        txtOutput = tk.Text(self.tabOutput, font=Font.r_small_content)
        ysb = ttk.Scrollbar(self.tabOutput, orient="vertical", command=txtOutput.yview)  # y滚动条
        ysb.pack(side='right', fill='y')

        txtOutput.configure(yscrollcommand=ysb.set)
        txtOutput.pack(expand='yes', fill='both')
        self.txtOutput = txtOutput

        return frame

    # -------------------------------------------------------------------------
    def do_close(self):
        """ 关闭应用程序 """
        msg = String.r_exit_system
        if tku.show_confirm(msg):
            self.close()

    def do_choice_image(self, *args):
        """ 选择目标图片 """
        img_path = tku.ask_for_filename()
        if img_path is not None and img_path != "":
            self.target_file_name = img_path
            self.org_img.set_image(img_path)

    def do_choice_style_image(self, *args):
        """ 选择风格图片 """
        img_path = tku.ask_for_filename()

        if img_path is not None and img_path != "":
            self.style_file_name = img_path
            self.style_img.set_image(img_path)

    def do_browser_workspace(self, *args):
        """ 浏览新生成的图片 """
        if os.path.exists(workspace_dir):
            os.startfile(workspace_dir)

    def log_message(self, *messages):
        """ 记录处理过程的日志信息 """
        info = utils.strftime(True) + " : "
        for message in messages:
            info += str(message) + "  "
        info += "\n"
        self.txtOutput.insert('end', info)
        self.refresh()  # 这句话很重要
        self.txtOutput.see('end')

    def do_transfer(self):
        """
        根据设置，进行图片的风格转换处理
        输入:
            target_image_path          : 需要进行转换的图片
            style_reference_image_path : 风格参考图片
        """
        # 获得目标图片，风格图片
        target_image_path = self.target_file_name
        style_reference_image_path = self.style_file_name

        # 获得设置的参数：循环次数，内容权重，风格权重
        iterations = int(self.txtIterations.get())
        content_weight = float(self.txtContent.get())
        style_weight = float(self.txtStyle.get())

        if not os.path.exists(target_image_path):
            tku.show_message("请先选择目标图片文件！")
            return

        if not os.path.exists(style_reference_image_path):
            tku.show_message("请先选择风格图片文件！")
            return

        utils.create_folder(workspace_dir)

        self.log_message("开始处理")
        self.refresh()

        self.tabControl.select(self.tabOutput)
        self.txtOutput.delete(0.0, 'end')
        self.final_img.set_image(target_image_path)
        self.refresh()

        if iterations <= 0:
            iterations = 5
        self.log_message("循环处理次数", iterations)

        width, height = load_img(target_image_path).size
        img_height = 400
        img_width = int(width * img_height / height)

        target_image = K.constant(preprocess_image(target_image_path, img_height, img_width))
        style_reference_image = K.constant(preprocess_image(style_reference_image_path, img_height, img_width))

        combination_image = K.placeholder((1, img_height, img_width, 3))

        # 将3个样本数据按指定顺序，构建成一个批次，从而可一次性全部计算处理
        # 然后按指定的序号，取出计算值：第0个数据：目标图片；第1个数据：风格图片；第2个数据：生成图片
        input_tensor = K.concatenate([target_image,
                                      style_reference_image,
                                      combination_image], axis=0)

        self.log_message('获得图片信息.')

        # 打开预训练模型 VGG19
        model = vgg19.VGG19(input_tensor=input_tensor,
                            weights='imagenet',
                            include_top=False)
        self.log_message('VGG19 模型创建完成.')

        # 获得 VGG16的所有层次的名称，用于映射取值
        outputs_dict = dict([(layer.name, layer.output) for layer in model.layers])

        # 用于提取内容特征值
        content_layer = 'block5_conv2'

        # 用于提取风格特征值
        style_layers = ['block1_conv1',
                        'block2_conv1',
                        'block3_conv1',
                        'block4_conv1',
                        'block5_conv1']

        # 损失函数中的权重设置
        total_variation_weight = 1e-4
        # style_weight = 1.
        # content_weight = 0.025

        # 定义损失值函数
        loss = K.variable(0.)
        layer_features = outputs_dict[content_layer]
        target_image_features = layer_features[0, :, :, :]     # 根据输入模型的批次， 第0个数据为目标图片, 第1个数据为风格数据, 第2个数据为生成图片
        combination_features = layer_features[2, :, :, :]
        loss += content_weight * content_loss(target_image_features,
                                              combination_features)
        for layer_name in style_layers:
            layer_features = outputs_dict[layer_name]
            style_reference_features = layer_features[1, :, :, :]
            combination_features = layer_features[2, :, :, :]
            sl = style_loss(style_reference_features, combination_features, img_height, img_width)
            loss += (style_weight / len(style_layers)) * sl
        loss += total_variation_weight * total_variation_loss(combination_image, img_height, img_width)

        # 定义计算梯度值
        grads = K.gradients(loss, combination_image)[0]

        # 基于损失值和梯度值，定义计算生成图数据
        fetch_loss_and_grads = K.function([combination_image], [loss, grads])

        # 构建 fmin_l_bfgs_b() 函数需要的评估参数类
        evaluator = Evaluator(img_height, img_width, fetch_loss_and_grads)

        # 生成图片的初始数据值为目标图片数据
        x = preprocess_image(target_image_path, img_height, img_width)
        x = x.flatten()

        self.log_message('模型参数准备完成.')

        for i in range(iterations):
            self.log_message('开始处理轮次：( ', str(i+1) + " / " + str(iterations) + " )")
            start_time = time.time()
            x, min_val, info = fmin_l_bfgs_b(evaluator.loss, x,
                                             fprime=evaluator.grads, maxfun=20)

            self.log_message('当前图片差异损失值 :', min_val)

            img = x.copy().reshape((img_height, img_width, 3))
            img = deprocess_image(img)

            end_time = time.time()
            self.log_message('第 (%d) 轮处理, 所用时间为 (%ds)' % (i+1, end_time - start_time) + "\n")
            if i == iterations - 1:
                fname = os.path.join(workspace_dir, result_prefix + utils.strftime(False) + ".png")
                imsave(fname, img)
                self.log_message('新生成的风格图片保存为：', fname)
                self.final_img.set_image(fname)
            else:
                temp_filename = os.path.join(workspace_dir, 'temp_result.png')
                imsave(temp_filename, img)
                self.final_img.set_image(temp_filename)
