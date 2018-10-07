# coding:utf-8

# *****************************************************************************
# 模块说明：利用 pack 方法，模拟构建人工智能的定制平台界面，只用于界面制作的学习参考
#          界面代码进行了分层编写，在容器层，设置子组件的pack()，
#          在子组件层， 创建自身框架，布局自己的子组件， 并返回自身，供容器布局
#          界面的结构层次比较清晰，修改调整会方便些
# 开发人员: Edwin.Zhang
# 开发时间: 2018-09-28
# *****************************************************************************

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk


def center_window(win, width=None, height=None):
	""" 将窗口屏幕居中 """
	screenwidth = win.winfo_screenwidth()
	screenheight = win.winfo_screenheight()
	if width is None:
		width, height = get_window_size(win)[:2]
	size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/3)
	win.geometry(size)


def get_window_size(win, update=True):
	""" 获得窗体的尺寸 """
	if update:
		win.update()
	return win.winfo_width(), win.winfo_height(), win.winfo_x(), win.winfo_y()


def tkimg_resized(img, w_box, h_box, keep_ratio=True):
	"""对图片进行按比例缩放处理"""
	w, h = img.size

	if keep_ratio:
		if w > h:
			width = w_box
			height = int(h_box * (1.0 * h / w))

		if h >= w:
			height = h_box
			width = int(w_box * (1.0 * w / h))
	else:
		width = w_box
		height = h_box

	img1 = img.resize((width, height), Image.ANTIALIAS)
	tkimg = ImageTk.PhotoImage(img1)
	return tkimg


def image_label(frame, img, width, height, keep_ratio=True):
	"""输入图片信息，及尺寸，返回界面组件"""
	if isinstance(img, str):
		_img = Image.open(img)
	else:
		_img = img
	lbl_image = tk.Label(frame, width=width, height=height)

	tk_img = tkimg_resized(_img, width, height, keep_ratio)
	lbl_image.image = tk_img
	lbl_image.config(image=tk_img)
	return lbl_image


def _font(fname="微软雅黑", size=12, bold=tkFont.NORMAL):
	"""设置字体"""
	ft = tkFont.Font(family=fname, size=size, weight=bold)
	return ft


def _ft(size=12, bold=False):
	"""极简字体设置函数"""
	if bold:
		return _font(size=size, bold=tkFont.BOLD)
	else:
		return _font(size=size, bold=tkFont.NORMAL)


def h_seperator(parent, height=2):  # height 单位为像素值
	"""水平分割线, 水平填充 """
	tk.Frame(parent, height=height, bg="whitesmoke").pack(fill=tk.X)


def v_seperator(parent, width, bg="whitesmoke"):  # width 单位为像素值
	"""垂直分割线 , fill=tk.Y, 但如何定位不确定，直接返回对象，由容器决定 """
	frame = tk.Frame(parent, width=width, bg=bg)
	return frame


class Window:
	def __init__(self, parent):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (1200, 800))  # 窗体尺寸
		center_window(self.root)                   # 将窗体移动到屏幕中央
		self.root.title("人工智能")                 # 窗体标题
		self.root.iconbitmap("images\\Money.ico")  # 窗体图标
		self.root.grab_set()
		self.body()      # 绘制窗体组件

	# 绘制窗体组件
	def body(self):
		self.title(self.root).pack(fill=tk.X)

		self.main(self.root).pack(expand=tk.YES, fill=tk.BOTH)

		self.bottom(self.root).pack(fill=tk.X)

	def title(self, parent):
		""" 标题栏 """

		def label(frame, text, size, bold=False):
			return tk.Label(frame, text=text, bg="black", fg="white", height=2, font=_ft(size, bold))

		frame = tk.Frame(parent, bg="black")

		label(frame, "人工智能应用平台", 16, True).pack(side=tk.LEFT, padx=10)
		label(frame, "图像模型定制", 12).pack(side=tk.LEFT, padx=100)
		label(frame, "声音模型定制", 12).pack(side=tk.LEFT, padx=0)
		label(frame, "定制模型", 12).pack(side=tk.LEFT, padx=100)
		label(frame, "", 12).pack(side=tk.RIGHT, padx=20)
		label(frame, "登录用户", 12).pack(side=tk.RIGHT, padx=20)
		image_label(frame, "images\\user.png", 40, 40, False).pack(side=tk.RIGHT)

		return frame

	def bottom(self, parent):
		""" 窗体最下面留空白 """

		frame = tk.Frame(parent, height=10, bg="whitesmoke")
		frame.propagate(True)
		return frame

	def main(self, parent):
		""" 窗体主体 """

		frame = tk.Frame(parent, bg="whitesmoke")

		self.main_top(frame).pack(fill=tk.X, padx=30, pady=15)
		self.main_left(frame).pack(side=tk.LEFT, fill=tk.Y, padx=30)
		v_seperator(frame, 30).pack(side=tk.RIGHT, fill=tk.Y)
		self.main_right(frame).pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

		return frame

	def main_top(self, parent):
		def label(frame, text, size=12):
			return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(size))

		frame = tk.Frame(parent, bg="white", height=150)

		image_label(frame, "images\\img_title.png", width=240, height=120, keep_ratio=False) \
			.pack(side=tk.LEFT, padx=10, pady=10)

		self.main_top_middle(frame).pack(side=tk.LEFT)

		label(frame, "收起^").pack(side=tk.RIGHT, padx=10)

		frame.propagate(False)
		return frame

	def main_top_middle(self, parent):
		str1 = "定制图像分类模型，可以识别一张图整体是什么物体/状态/场景。"
		str2 = "在各分类图片之间差异明显的情况下，训练数据每类仅需20-100张，最快10分钟可训练完毕"

		def label(frame, text):
			return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(12))

		frame = tk.Frame(parent, bg="white")

		self.main_top_middle_top(frame).pack(anchor=tk.NW)

		label(frame, str1).pack(anchor=tk.W, padx=10, pady=2)
		label(frame, str2).pack(anchor=tk.W, padx=10)

		return frame

	def main_top_middle_top(self, parent):
		def label(frame, text, size=12, bold=True, fg="blue"):
			return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))

		frame = tk.Frame(parent, bg="white")

		label(frame, "图像分类模型", 20, True, "black").pack(side=tk.LEFT, padx=10)
		label(frame, "操作文档").pack(side=tk.LEFT, padx=10)
		label(frame, "教学视频").pack(side=tk.LEFT, padx=10)
		label(frame, "常见问题").pack(side=tk.LEFT, padx=10)

		return frame

	def main_left(self, parent):
		def label(frame, text, size=10, bold=False, bg="white"):
			return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))

		frame = tk.Frame(parent, width=180, bg="white")

		label(frame, "模型中心", 12, True).pack(anchor=tk.W, padx=20, pady=10)
		label(frame, "我的模型").pack(anchor=tk.W, padx=40, pady=5)

		f1 = tk.Frame(frame, bg="whitesmoke")
		v_seperator(f1, width=5, bg="blue").pack(side=tk.LEFT, fill=tk.Y)
		label(f1, "创建模型", bg="whitesmoke").pack(side=tk.LEFT, anchor=tk.W, padx=35, pady=5)
		f1.pack(fill=tk.X)

		label(frame, "训练模型").pack(anchor=tk.W, padx=40, pady=5)
		label(frame, "校验模型").pack(anchor=tk.W, padx=40, pady=5)
		label(frame, "发布模型").pack(anchor=tk.W, padx=40, pady=5)

		h_seperator(frame, 10)

		label(frame, "数据中心", 12, True).pack(anchor=tk.W, padx=20, pady=10)
		label(frame, "数据集管理").pack(anchor=tk.W, padx=40, pady=5)
		label(frame, "创建数据集").pack(anchor=tk.W, padx=40, pady=5)

		frame.propagate(False)
		return frame

	def main_right(self, parent):
		def label(frame, text, size=10, bold=False, fg="black"):
			return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))

		def space(n):
			s = " "
			r = ""
			for i in range(n):
				r += s
			return r

		frame = tk.Frame(parent, width=200, bg="white")

		label(frame, "创建模型", 12, True).pack(anchor=tk.W, padx=20, pady=5)

		h_seperator(frame)

		f1 = tk.Frame(frame, bg="white")
		label(f1, space(8) + "模型类别:").pack(side=tk.LEFT, pady=5)
		label(f1, "图像分类").pack(side=tk.LEFT, padx=20)
		f1.pack(fill=tk.X)

		f2 = tk.Frame(frame, bg="white")
		label(f2, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
		label(f2, "模型名称:").pack(side=tk.LEFT)
		tk.Entry(f2, bg="white", font=_ft(10), width=25).pack(side=tk.LEFT, padx=20)
		f2.pack(fill=tk.X)

		f3 = tk.Frame(frame, bg="white")
		label(f3, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
		label(f3, "联系方式:").pack(side=tk.LEFT)
		tk.Entry(f3, bg="white", font=_ft(10), width=25).pack(side=tk.LEFT, padx=20)
		f3.pack(fill=tk.X)

		f4 = tk.Frame(frame, bg="white")
		label(f4, space(5) + "*", fg="red").pack(side=tk.LEFT, anchor=tk.N, pady=5)
		label(f4, "功能描述:").pack(side=tk.LEFT, anchor=tk.N, pady=5)
		tk.Text(f4, bg="white", font=_ft(10), height=10, width=40).pack(side=tk.LEFT, padx=20, pady=5)
		f4.pack(fill=tk.X)

		ttk.Button(frame, text="下一步", width=12).pack(anchor=tk.W, padx=112, pady=5)

		return frame
