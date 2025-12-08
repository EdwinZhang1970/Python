# coding:utf-8

# -----------------------------------------------------------------------------
# 模块说明：基于 tkinter 框架下，提供一些简单易用的界面处理函数
# 开发人员：Edwin.Zhang
# 开发时间：2018-09-28
# 更新日期：2018-10-20
# 更新日期：2018-11-03
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

from PIL import ImageTk
import PIL as pil
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.simpledialog import *
import tkinter.colorchooser as color_chooser

import re
import os

# 在模块级创建一个 tk.Tk() 很重要， 否则很多 tkinter的功能不能用，如 tkinter.font
root = tk.Tk()

# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
THEME = None

_styles = {
    "default": {"family": "微软雅黑", "size": 10, "bold": False, "bg": None, "fg": None},
    "default-font": {"family": "微软雅黑", "size": 12, "bold": True},
    "default-label": {"size": 12, "bold": False},
    "default-button": {"size": 12, "bold": True, "bg": "CadetBlue", "fg": "white", "width": 12},
    "bold-label": {"size": 12, "bold": True}
}


def get_cfd():
    """ 获得当前python文件所在的目录
        get_current_file_directory
    输入:
        __f  : 应该输入系统变量 __file__
    """
    return os.path.dirname(os.path.abspath(__file__))


def parse_style(family=None, size=None, bold=None, width=None, height=None, bg=None, fg=None,
                style=None, styles=None):
    styles = styles if styles is not None else _styles
    style = style if style is not None and style in styles else "default"
    
    if style in styles:
        family = family if family is not None else styles[style].get("family")
        size = size if size is not None else styles[style].get("size")
        bold = bold if bold is not None else styles[style].get("bold")
        width = width if width is not None else styles[style].get("width")
        height = height if height is not None else styles[style].get("height")
        bg = bg if bg is not None else styles[style].get("bg")
        fg = fg if fg is not None else styles[style].get("fg")
    
    family = family if family is not None else "微软雅黑"
    size = size if size is not None else 10
    bold = bold if bold is not None else False
    bg = bg if bg is not None else "white"
    fg = fg if fg is not None else "black"
    
    if bold:
        bold = tkfont.BOLD
    else:
        bold = tkfont.NORMAL
    
    return {"family": family, "size": size, "bold": bold, "width": width, "height": height, "bg": bg, "fg": fg}


def style_label(master, text, size=None, bold=None, family=None, width=None, height=None, bg=None, fg=None, style=None, styles=None):
    """ 启用样式的标签 """
    style = style if style is not None else "default-label"
    _ = parse_style(family, size, bold, width, height, bg, fg, style, styles)
    return tk.Label(master, text=text, font=tkfont.Font(family=_["family"], size=_["size"], weight=_["bold"]),
                    height=_["height"], bg=_["bg"], fg=_["fg"])


def style_font(size=None, bold=None, family=None, style=None, styles=None):
    """ 启用样式的字体 """
    styles = styles if styles is not None else _styles
    _style = style if style is not None and style in styles else "default-font"
    
    _family = family if family is not None else styles[_style].get("family")
    _size = size if size is not None else styles[_style].get("size")
    _bold = bold if bold is not None else styles[_style].get("bold")
    
    _family = _family if _family is not None else "微软雅黑"
    _size = _size if _size is not None else 10
    _bold = _bold if _bold is not None else False
    
    if _bold:
        _bold = tkfont.BOLD
    else:
        _bold = tkfont.NORMAL
    
    return tkfont.Font(family=_family, size=_size, weight=_bold)


def style_button(master, text, command, family=None, size=None, bold=None, width=None, height=None, bg=None, fg=None,
                 style=None, styles=None):
    """ 启动样式的按钮 """
    style = style if style is not None else "default-button"
    _ = parse_style(family, size, bold, width, height, bg, fg, style, styles)
    return tk.Button(master, text=text, command=command, bg=_["bg"], fg=_["fg"],
                     font=tkfont.Font(family=_["family"], size=_["size"], weight=_["bold"]),
                     width=_["width"], height=_["height"])


# def os_execute(command):
#     import win32process
#     win32process.CreateProcess(command, '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None,
#                                win32process.STARTUPINFO())
#

def process_message(message, *args):
    para = list(args)
    para.extend("".rjust(10))   # 将参数个数扩大10个，避免参数个数不够，造成下标溢出的异常
    return message.format(*para)


def show_message(message="", *args):
    messagebox.showinfo("提示", process_message(message, *args))


def show_info(message="", *args):
    messagebox.showinfo("提示", process_message(message, *args))


def show_error(message="", *args):
    messagebox.showerror("错误", process_message(message, *args))


def show_warning(message="", *args):
    messagebox.showwarning("警告", process_message(message, *args))


def show_confirm(message="", *args):
    """
        True  : yes
        False : no
    """
    return messagebox.askyesno("确认", process_message(message, *args))


def show_confirm3(message="", *args):
    """
        True : yes
        False: no
        None: cancel
    """
    return messagebox.askyesnocancel("确认", process_message(message, *args))


def ask_for_filename():
    return askopenfilename()


def ask_for_save_filename():
    return asksaveasfilename()


def ask_for_directory():
    return askdirectory()


def ask_for_color():
    return color_chooser.askcolor()


def ask_for_integer(initial_value=0):
    return askinteger("提示", "请输入整数", initialvalue=initial_value)


def ask_for_float(minvalue=None, maxvalue=None):
    if minvalue is None or maxvalue is None:
        return askfloat("提示", "请输入浮点数")
    else:
        prompt = "请输入( {} ~ {} )之间的浮点数".format(minvalue, maxvalue)
        return askfloat("提示", prompt, minvalue=minvalue, maxvalue=maxvalue)


def ask_for_string():
    return askstring("提示", "请输入信息")


def get_screen_size(win):
    return win.winfo_screenwidth(), win.winfo_screenheight()


def get_window_size(win, update=True):
    """ 获得窗体的尺寸 """
    if update:
        win.update()
    return win.winfo_width(), win.winfo_height(), win.winfo_x(), win.winfo_y()


def set_window_style(theme=None):
    """ theme in ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative') """
    if theme is not None:
        style = ttk.Style()
        style.theme_use(theme)


def set_window_title(win, title):
    win.title(title)
 

def set_window_resizeable(win, width, height):
    win.resizable(width, height)


def set_window_fixed(win):
    win.resizable(False, False)


def set_window_before_parent(win, parent):
    win.transient(parent)


def set_window_size(win, width, height, x=None, y=None):
    """ 设置窗口的尺寸 """
    if x is None:
        size = "%dx%d" % (width, height)
    else:
        size = '%dx%d+%d+%d' % (width, height, x, y)
    win.geometry(size)


def set_window_center_screen(win, width=None, height=None):
    """ 将窗口屏幕居中 """
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    if width is None:
        width, height = get_window_size(win)[:2]
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/3)
    win.geometry(size)


def set_window_center_parent(win, parent, width=None, height=None):
    """ 将窗口在其父窗体居中 """
    if parent is None:
        set_window_center_screen(win, width, height)
    else:
        parent_width, parent_height, parent_x, parent_y = get_window_size(parent, False)
        if width is None:
            width, height = get_window_size(win)[:2]
        size = '%dx%d+%d+%d' % (width, height, parent_x + int((parent_width - width) / 2),
                                parent_y + int((parent_height - height) / 2))
        win.geometry(size)


def set_window_maximize(win):
    """ 将窗口最大化 """
    # w = win.winfo_screenwidth()
    # h = win.winfo_screenheight()
    # win.geometry("%dx%d+%d+%d" % (w, h, -10, -10))
    win.state("zoomed")


def set_window_full_screen(win):
    win.attributes("-fullscreen", True)


def set_window_top_most(win):
    win.wm_attributes("-topmost", True)


def hide_window_title(win):
    win.overrideredirect(True)


def show_window_title(win):
    win.overrideredirect(False)


def hide_window(win):
    win.withdraw()


def show_window(win):
    win.update()
    win.deiconify()


def set_window_icon(win, icon):
    win.iconbitmap(icon)


def set_window_bg_color(win, color):
    win.config(bg=color)
    

def join(s=" ", source=list()):
    """ 将列表中的元素用指定分割符连起来 """
    str_source = [str(i) for i in source]
    return s.join(str_source)


def space(n):
    """ 创建 n 个空格，用于定位控制 """
    return ''.rjust(n)


def tkimg_resized(img, w_box, h_box, keep_ratio=True):
    """对图片进行按比例缩放处理"""
    w, h = img.size
    
    if w_box is None or h_box is None:
        img1 = img
    else:
        if keep_ratio:
            if w > h:
                width = w_box
                height = int(h_box * (1.0 * h / w))
            else:
                height = h_box
                width = int(w_box * (1.0 * w / h))
        else:
            width = w_box
            height = h_box
        img1 = img.resize((width, height), pil.Image.ANTIALIAS)
        
    tkimg = ImageTk.PhotoImage(img1)
    return tkimg


def image_label(frame, img, width, height, keep_ratio=True):
    """ 输入图片信息，及尺寸，返回界面组件
        输入：
            frame      : 容器对象
            img        : 图片文件名 或 PIL image 对象
            width      : 显示宽度
            height     : 显示高度
            keep_ratio : 是否保存图片的长宽比例
        输出：
            tk.Label() : 含图像显示
    """
    if isinstance(img, str):
        _img = pil.Image.open(img)
    else:
        _img = img
    lbl_image = tk.Label(frame, width=width, height=height)

    tk_img = tkimg_resized(_img, width, height, keep_ratio)
    lbl_image.image = tk_img
    lbl_image.config(image=tk_img)
    return lbl_image


def font(family="微软雅黑", size=12, bold=False):
    """设置字体, 含缺省设置"""
    if bold:
        _bold = tkfont.BOLD
    else:
        _bold = tkfont.NORMAL

    ft = tkfont.Font(family=family, size=size, weight=_bold)
    return ft


def label(frame, text, size=12, bold=False, bg="white", fg="blue"):
    return tk.Label(frame, text=text, bg=bg, fg=fg, font=font(size=size, bold=bold))


def h_separator(parent, height=2):  # height 单位为像素值

    """水平分割线, 水平填充 """
    tk.Frame(parent, height=height, bg="whitesmoke").pack(fill=tk.X)


def v_separator(parent, width, bg="whitesmoke"):  # width 单位为像素值

    """垂直分割线 , fill=tk.Y, 但如何定位不确定，直接返回对象，由容器决定 """
    frame = tk.Frame(parent, width=width, bg=bg)
    return frame


class WinBase:
    def __init__(self, parent=None):
        """
            parent : tku.WinBase, 这样容易扩展功能, 而不受限于原来的 tk 对象
            self.win : 为 tkinter 原来的对象，其他方法和属性是扩展处理的
        """
        global root

        self.__dummy = None
        self.__title = ""  # 窗体标题
        
        if parent is None:
            self.win = root    # 主程序窗口，一个应用程序，只应该有一个
            self.parent = None
            self.is_app = True    # True : Application main Window,  False : Dialog sub Window
        else:
            self.win = tk.Toplevel()
            self.parent = parent
            self.is_app = False
        
        self.hide()   # 先隐藏，然后打开时再显示，改进窗体明显移动的现象

        self.callback = dict()       # 专用于调用子窗口时的回调结果，定义为字典，这样可以存放多个键值对。

        # 窗体缺省设置
        self.title = "window"
        if self.is_app:
            self.set_size(800, 600)
        else:
            self.set_size(640, 480)
        
        if THEME is not None:
            style = ttk.Style()
            style.theme_use(THEME)
            
        self.win.grab_set()
        # self.win.protocol("WM_DELETE_WINDOW", self.close)
    
    def dummy(self):
        """ 只用于忽略一些静态函数的格式警告 """
        self.__dummy = None
        
    def open(self):
        """ 打开并显示窗体 """
        if self.is_app:
            self.center_screen()
        else:
            self.center_parent()
            
        self.show()
        if self.is_app:  # 应用程序主程序体
            self.win.mainloop()
        else:
            self.parent.win.wait_window(self.win)       # 一定是父窗体等待子窗体，不能搞错

            # self.win.wait_window(self.parent)         # wrong
            
    def close(self):
        self.win.destroy()

    def show(self):
        show_window(self.win)

    def hide(self):
        hide_window(self.win)

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, value):
        self.__title = value
        self.win.title(value)

    @property
    def layout(self):
        self.win.update()
        return self.win.winfo_x(), self.win.winfo_y(), self.win.winfo_width(), self.win.winfo_height()

    @property
    def x(self):
        return self.layout[0]

    @property
    def y(self):
        return self.layout[1]
    
    @property
    def width(self):
        return self.layout[2]
    
    @property
    def height(self):
        return self.layout[3]

    def set_icon(self, icon):
        """ 设置窗体的图标
            icon : 必须是图标格式件名
        """
        self.win.iconbitmap(icon)
    
    def set_size(self, width, height):
        """
            设置窗体的尺寸
            width : 宽度(单位：像素)
            height: 高度(单位：像素)
        """
        set_window_size(self.win, width, height)
        return self

    def set_resizeable(self, width, height):
        set_window_resizeable(self.win, width, height)

    def set_background_color(self, color):
        set_window_bg_color(self.win, color)
        
    def fixed(self):
        """ 将窗体设置为固定大小 """
        self.set_resizeable(False, False)

    def maximize(self):
        """ 将窗体最大化 """
        set_window_maximize(self.win)
        return self

    def center_screen(self):
        """ 窗体居中显示 """
        set_window_center_screen(self.win)
        return self
    
    def center_parent(self):
        """ 窗体显示在调用窗口中间位置 """
        set_window_center_parent(self.win, self.parent.win)

    def full_screen(self):
        """ 窗体全屏显示 """
        set_window_full_screen(self.win)
        return self

    def top_most(self):
        """ 窗体总在最前面 """
        set_window_top_most(self.win)

    def hide_title(self):
        """ 隐藏窗体标题栏 """
        hide_window_title(self.win)

    def show_title(self):
        """ 显示窗体标题栏 """
        show_window_title(self.win)

    def refresh(self):
        """ 刷新界面 """
        self.win.update()

    # 绘制窗体控件，用子类方法覆盖
    def body(self):
        pass

    # 窗体布局，用子类方法覆盖， 这个名字应该比 body()更加明确，配合子布局都用 lay_sub_frame()
    def lay_body(self):
        pass


class SimpleTable(tk.Frame):
    """ 简单表格
        先初始化表格，设置行列数；然后按行，列序号进行逐一赋值处理
    """
    def __init__(self, parent, rows=10, columns=2):
        """
        输入:
            parent : 容器对象
            row    : 行数设置
            columns: 列数设置
        """
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column),
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    # 对指定行，列进行赋值处理
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


class ImageLabel(tk.Label):
    """ 图像控件 """
    default_img = os.path.join(get_cfd(), "python.PNG")

    def __init__(self, parent, img="", width=None, height=None):
        """
            img : 可以是图片文件名，也可以是pil.Image()对象
            width, height : 图片显示的宽度, 高度； 任何一个为None, 则显示原始尺寸

        """
        tk.Label.__init__(self, parent)
        self.set_image(img, width, height)

    def set_image(self, img, width=None, height=None):
        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if isinstance(img, str):
            if os.path.exists(img):
                _img = pil.Image.open(img)
            else:
                _img = pil.Image.open(self.default_img)
        else:
            _img = img

        tk_img = tkimg_resized(_img, self.width, self.height)
        self.image = tk_img
        self.config(image=tk_img)


class ListTable(tk.Frame):
    def __init__(self, parent, columns=set(), columns_info=None, hide_columns=None):
        """ 数据显示表格控件
        输入：
            parent      : 容器对象
            columns     ：列名集合
            columns_info: 数据column的设置信息列表[(宽度, 对齐方向),(10,'w|e|center')]
            hide_columns: 隐藏列列表

        """
        tk.Frame.__init__(self, parent)
        
        self.columns = columns
        self.col_info = columns_info
        self.hide_columns = hide_columns
        self.display_columns = None
        if self.hide_columns is not None:
            self.display_columns = [item for item in self.columns if item not in self.hide_columns]

        self.columns_count = len(columns)
        self.current_selections = None
        
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        if self.columns_count > 0:
            for i, col in enumerate(self.columns):
                if self.col_info is not None and i < len(self.col_info):
                    _width = self.col_info[i][0]
                    if _width == 0:
                        _width = 10
                    anchor = self.col_info[i][1]
                else:
                    _width = 10
                    anchor = 'w'

                self.tree.column("#" + str(i+1), width=_width, anchor=anchor)
                self.tree.heading(col, text=col)
                
        # self.tree.tag_configure('ttk', font=font(size=15, bold=True))
        
        self.tree['selectmode'] = 'browse'
        if self.display_columns is not None:
            self.tree["displaycolumns"] = self.display_columns
        
        self.tree.bind('<ButtonRelease-1>', self.treeview_click)
        self.tree.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        vbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscrollcommand=vbar.set)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def format_tree(self):
        children = self.tree.get_children()
        for idx, child in enumerate(children):  # 先加标签，然后进行格式设置

            if idx % 2 == 0:
                self.tree.item(children[idx], tags=['oddrow', 'allrow'])
            else:
                self.tree.item(children[idx], tags=['allrow'])
        self.tree.tag_configure('oddrow', background='whitesmoke')
        self.tree.tag_configure('allrow', font=font(size=10, bold=False))

    def clear_all(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        
    def fill_tree(self, records):
        """ records 为 元组列表 [(1,1,1),(2,2,2)...] """
        for item in records:
            item = list(item)
            count = len(item)
            if count > self.columns_count:
                item = item[:self.columns_count]
            elif count < self.columns_count:
                item.extend(" " * (self.columns_count - count))
            self.tree.insert("", "end", values=item, tags=('ttk', 'simple'))
        self.format_tree()
        
    def treeview_click(self, event):
        if self.tree.selection() is not None and len(self.tree.selection()) >= 1:
            item = self.tree.selection()[0]
            if item is not None:
                self.current_selections = self.tree.item(item, "values")
