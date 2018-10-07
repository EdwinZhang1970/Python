# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
import tkutils as tku


class Window:
	def __init__(self, parent):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (1000, 700))  # 窗体尺寸
		tku.center_window(self.root)               # 将窗体移动到屏幕中央
		self.root.title("单组件的pack布局演示")                 # 窗体标题
		self.root.grab_set()
		self.root.resizable(False, False)

		self.v_code_pack = tk.StringVar()
		self.v_code_pack.set(".pack()")

		self.v_side = tk.StringVar()
		self.v_side.set("")
		self.side_name = ("RIGHT", "LEFT", "TOP", "BOTTOM", "NONE")

		self.v_expand = tk.StringVar()
		self.v_expand.set("")
		self.expand_name = ("YES", "NO", "NONE")

		self.v_anchor = tk.StringVar()
		self.v_anchor.set("")
		self.anchor_name = ("W", "E", "N", "S", "CENTER", "NW", "NE", "SW", "SE", "NONE")

		self.v_fill = tk.StringVar()
		self.v_fill.set("")
		self.fill_name = ("X", "Y", "BOTH", "NONE")

		self.v_padx = tk.StringVar()
		self.v_padx.set("0")

		self.v_pady = tk.StringVar()
		self.v_pady.set("0")

		self.body()      # 绘制窗体组件

	# 绘制窗体组件
	def body(self):
		self.title(self.root).pack(fill=tk.X)
		tk.Frame(self.root, height=2).pack(fill=tk.X)

		self.parameters(self.root).pack(side=tk.LEFT, fill=tk.Y)

		tk.Frame(self.root, width=5, bg="blue").pack(side=tk.LEFT, fill=tk.Y)
		tk.Frame(self.root, height=5,  bg="blue").pack(side=tk.TOP, fill=tk.X)
		tk.Frame(self.root, height=5,  bg="blue").pack(side=tk.BOTTOM, fill=tk.X)
		self.main(self.root).pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
		tk.Frame(self.root, width=5, bg="blue").pack(side=tk.LEFT, fill=tk.Y)

	def title(self, parent):
		frame = tk.Frame(parent, height=50, bg="black")

		ft0 = tkFont.Font(family="微软雅黑", size=18, weight=tkFont.BOLD)
		tk.Label(frame, font=ft0, bg="black", fg="white", text="当前设置：")\
			.pack(side=tk.LEFT, padx=20)

		ft1 = tkFont.Font(family="微软雅黑", size=14, weight=tkFont.BOLD)
		tk.Label(frame, height=2, font=ft1, bg="black", fg="white",  textvariable=self.v_code_pack)\
			.pack(side=tk.LEFT, padx=5)

		frame.propagate = False
		return frame

	def parameters(self, parent):
		frame = tk.Frame(parent, width=400)

		ft1 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)

		ft2 = tkFont.Font(family="微软雅黑", size=14, weight=tkFont.BOLD)

		f_side = tk.Frame(frame)
		_var_side = tk.StringVar(value=self.side_name)
		self.p_side = tk.Listbox(f_side, listvariable=_var_side, selectmode='single', width=20, height=5, font=ft1)
		self.p_side.pack(side=tk.RIGHT, padx=10, pady=5)
		self.p_side.bind('<<ListboxSelect>>', self.get_side)
		tk.Label(f_side, font=ft2, text="side:").pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		tk.Button(f_side, text="复位", width=10, height=1, bg="cadetblue", font=ft2, command=self.reset)\
			.pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		f_side.pack(fill=tk.X, anchor=tk.W)

		f_expand = tk.Frame(frame)
		_var_expand = tk.StringVar(value=self.expand_name)
		self.p_expand = tk.Listbox(f_expand, listvariable=_var_expand, selectmode='single', width=20, height=3, font=ft1)
		self.p_expand.pack(side=tk.RIGHT, padx=10)
		self.p_expand.bind('<<ListboxSelect>>', self.get_expand)
		tk.Label(f_expand, font=ft2, text="expand:").pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		f_expand.pack(fill=tk.X, anchor=tk.W,)

		f_anchor = tk.Frame(frame)
		_var_anchor = tk.StringVar(value=self.anchor_name)
		self.p_anchor = tk.Listbox(f_anchor, listvariable=_var_anchor, selectmode='single', width=20, height=10, font=ft1)
		self.p_anchor.pack(side=tk.RIGHT, padx=10)
		self.p_anchor.bind('<<ListboxSelect>>', self.get_anchor)
		tk.Label(f_anchor, font=ft2, text="anchor:").pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		f_anchor.pack(fill=tk.X, anchor=tk.W, pady=5)

		f_fill = tk.Frame(frame)
		_var_fill = tk.StringVar(value=self.fill_name)
		self.p_fill = tk.Listbox(f_fill, listvariable=_var_fill, selectmode='single', width=20, height=4, font=ft1)
		self.p_fill.pack(side=tk.RIGHT, padx=10)
		self.p_fill.bind('<<ListboxSelect>>', self.get_fill)
		tk.Label(f_fill, font=ft2, text="fill:").pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		f_fill.pack(fill=tk.X, anchor=tk.W)

		f_padx = tk.Frame(frame)
		self.p_padx = tk.Spinbox(f_padx, from_=0, to=300, textvariable=self.v_padx, width=19, font=ft1, command=self.layout)
		self.p_padx.pack(side=tk.RIGHT, padx=10)
		tk.Label(f_padx, font=ft2, text="padx:").pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		f_padx.pack(fill=tk.X, anchor=tk.W, pady=5)

		f_pady = tk.Frame(frame)
		self.p_pady = tk.Spinbox(f_pady, from_=0, to=300, textvariable=self.v_pady, width=19, font=ft1, command=self.layout)
		self.p_pady.pack(side=tk.RIGHT, padx=10)
		tk.Label(f_pady, font=ft2, text="pady:").pack(side=tk.RIGHT, anchor=tk.W, padx=10)
		f_pady.pack(fill=tk.X, anchor=tk.W, pady=5)

		frame.propagate(False)
		return frame

	def main(self, parent):
		self.frame_main = tk.Frame(parent, bg="lightgreen", bd=2)
		self.element = tk.Label(self.frame_main, width=15, height=3, bg="red")
		self.element.pack()
		return self.frame_main

	def get_side(self, *arg):
		idxs = self.p_side.curselection()
		if idxs is not None and len(idxs) == 1:
			idx = int(idxs[0])
			self.v_side.set(self.side_name[idx])
		self.layout()

	def get_expand(self, *arg):
		idxs = self.p_expand.curselection()
		if idxs is not None and len(idxs) == 1:
			idx = int(idxs[0])
			self.v_expand.set(self.expand_name[idx])
		self.layout()

	def get_anchor(self, *arg):
		idxs = self.p_anchor.curselection()
		if idxs is not None and len(idxs) == 1:
			idx = int(idxs[0])
			self.v_anchor.set(self.anchor_name[idx])
		self.layout()

	def get_fill(self, *arg):
		idxs = self.p_fill.curselection()
		if idxs is not None and len(idxs) == 1:
			idx = int(idxs[0])
			self.v_fill.set(self.fill_name[idx])
		self.layout()

	def reset(self):
		self.v_side.set("")
		self.v_expand.set("")
		self.v_anchor.set("")
		self.v_fill.set("")
		self.v_padx.set("0")
		self.v_pady.set("0")
		self.layout()

	def layout(self):
		self.element.forget()
		del self.element

		self.element = tk.Label(self.frame_main, width=15, height=3, bg="red")
		self.element.pack()

		code = ".pack("
		is_add = False
		if self.v_side.get() != "":
			if self.v_side.get() != "NONE":
				code += "side=" + self.v_side.get()
				is_add = True
				self.element.pack(side=self.v_side.get().lower())

		if self.v_expand.get() != "":
			if self.v_expand.get() != "NONE":
				if is_add:
					code += ", "
				code += "expand=" + self.v_expand.get()
				is_add = True
				self.element.pack(expand=self.v_expand.get().lower())

		if self.v_anchor.get() != "":
			if self.v_anchor.get() != "NONE":
				if is_add:
					code += ", "
				code += "anchor=" + self.v_anchor.get()
				is_add = True
				self.element.pack(anchor=self.v_anchor.get().lower())

		if self.v_fill.get() != "":
			if self.v_fill.get() != "NONE":
				if is_add:
					code += ", "
				code += "fill=" + self.v_fill.get()
				is_add = True
				self.element.pack(fill=self.v_fill.get().lower())

		x = int(self.v_padx.get())
		if x > 0:
			if is_add:
				code += ", "
			code += "padx= " + str(x)
			is_add = True
			self.element.pack(padx=x)

		y = int(self.v_pady.get())
		if y > 0:
			if is_add:
				code += ", "
			code += "pady= " + str(y)
			is_add = True
			self.element.pack(pady=y)

		code += ")"
		self.v_code_pack.set(code)


