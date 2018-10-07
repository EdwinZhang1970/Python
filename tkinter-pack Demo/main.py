# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import tkutils as tku
import win_ai
import win_single
import win_multi


class App:
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("%dx%d" % (700, 400))   # 窗体尺寸
		tku.center_window(self.root)               # 将窗体移动到屏幕中央
		self.root.iconbitmap("images\\Money.ico")  # 窗体图标
		self.root.title("Python pack 布局演示")
		self.root.resizable(False, False)          # 设置窗体不可改变大小
		self.no_title = True
		self.show_title()
		self.body()

	def body(self):
		# ---------------------------------------------------------------------
		# 背景图片
		# ---------------------------------------------------------------------
		self.img = ImageTk.PhotoImage(file="images\\bg1.png")
		canvas = tk.Canvas(self.root, width=720, height=420)
		canvas.create_image(300, 200, image=self.img)
		canvas.pack(expand=tk.YES, fill=tk.BOTH)

		# ---------------------------------------------------------------------
		# 标题栏
		# ---------------------------------------------------------------------
		f1 = tk.Frame(canvas)

		im1 = tku.image_label(f1, "images\\python.png", 86, 86, False)
		im1.configure(bg="Teal")
		im1.bind('<Button-1>', self.show_title)
		im1.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y)

		ft1 = tkFont.Font(family="微软雅黑", size=24, weight=tkFont.BOLD)
		tk.Label(f1, text="Pack 布局演示", height=2, fg="white", font=ft1, bg="Teal")\
			.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

		im2 = tku.image_label(f1, "images\\close.png", 86, 86, False)
		im2.configure(bg="Teal")
		im2.bind('<Button-1>', self.close)
		im2.pack(side=tk.RIGHT, anchor=tk.NW, fill=tk.Y)

		f1.pack(fill=tk.X)

		# ---------------------------------------------------------------------
		# 功能按钮组
		# ---------------------------------------------------------------------
		ft2 = tkFont.Font(family="微软雅黑", size=14, weight=tkFont.BOLD)
		tk.Button(canvas, text="单组件演示", bg="cadetblue", command=self.show_single, font=ft2, height=2, fg="white", width=15)\
			.pack(side=tk.LEFT, expand=tk.YES, anchor=tk.CENTER, padx=5)
		tk.Button(canvas, text="多组件演示", bg="cadetblue", command=self.show_multi, font=ft2, height=2, fg="white", width=15)\
			.pack(side=tk.LEFT, expand=tk.YES, anchor=tk.CENTER, padx=5)
		tk.Button(canvas, text="应用平台界面", bg="cadetblue", command=self.show_ai, font=ft2, height=2, fg="white", width=15)\
			.pack(side=tk.RIGHT, expand=tk.YES, anchor=tk.CENTER, padx=5)

	def show_title(self, *args):
		self.root.overrideredirect(self.no_title)
		self.no_title = not self.no_title

	def show_single(self):
		win_single.Window(self.root)

	def show_multi(self):
		win_multi.Window(self.root)

	def show_ai(self):
		win_ai.Window(self.root)

	def close(self, *arg):
		if tku.show_confirm("确认退出吗 ?"):
			self.root.destroy()


if __name__ == "__main__":
	app = App()
	app.root.mainloop()
