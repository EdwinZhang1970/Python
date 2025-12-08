# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
import tkutils as tku
import win_multi2

colors = ['red', 'yellow', 'blue', 'green', 'pink', 'slateblue', 'lawngreen', 'orange', 'gold', 'cyan',
		  'cyan', 'brown', 'gray', 'royalblue', 'magenta', 'olive', 'black']


class Window:
	def __init__(self, parent):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (1000, 700))  # 窗体尺寸
		tku.center_window(self.root)               # 将窗体移动到屏幕中央
		self.root.title("多组件的pack布局演示")                 # 窗体标题
		self.root.grab_set()
		self.root.resizable(False, False)
		self.default_code = "1.pack(side='left', expand='no', anchor='w', fill='y', padx=5, pady=5)\n"
		self.default_code += "2.pack(side='top')\n"
		self.default_code += "3.pack(side='right')\n"
		self.default_code += "4.pack(side='bottom')\n"
		self.body()      # 绘制窗体组件
		self.reset()

	# 绘制窗体组件
	def body(self):
		self.title(self.root).pack(fill=tk.X)
		tk.Frame(self.root, height=2).pack(fill=tk.X)

		self.parameters(self.root).pack(side=tk.LEFT, fill=tk.Y)

		tk.Frame(self.root, width=5, bg="blue").pack(side=tk.LEFT, fill=tk.Y)
		tk.Frame(self.root, height=5,  bg="blue").pack(side=tk.TOP, fill=tk.X)
		self.box = tk.Frame(self.root, height=5,  bg="blue")
		self.box.pack(side=tk.BOTTOM, fill=tk.X)

		self.frame_main = tk.Frame(self.root, bg="white", bd=2)
		self.frame_main.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

		self.bottom = tk.Frame(self.root, width=5, bg="blue")
		self.bottom.pack(side=tk.LEFT, fill=tk.Y)

	def title(self, parent):
		frame = tk.Frame(parent, height=50, bg="black")

		ft0 = tkFont.Font(family="微软雅黑", size=14, weight=tkFont.BOLD)
		tk.Label(frame, font=ft0, bg="black", fg="white", text="设置范例：")\
			.pack(side=tk.LEFT, padx=10)

		ft1 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
		tk.Label(frame, height=2, font=ft1, bg="black", fg="white",
				 text="n.pack(side='left', expand='no', anchor='w', fill='y', padx=5, pady=5)     (全小写字母 + 单引号)")\
			.pack(side=tk.LEFT, padx=5)

		frame.propagate = False
		return frame

	def parameters(self, parent):
		frame = tk.Frame(parent, width=500)

		ft1 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
		ft2 = tkFont.Font(family="微软雅黑", size=10, weight=tkFont.BOLD)

		f_side = tk.Frame(frame)
		tk.Button(f_side, text="复位", width=10, height=1, bg="cadetblue", font=ft1, command=self.reset)\
			.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)

		tk.Button(f_side, text="刷新", width=10, height=1, bg="cadetblue", font=ft1, command=self.refresh)\
			.pack(side=tk.LEFT, anchor=tk.W, padx=10)

		tk.Button(f_side, text="弹窗显示", width=10, height=1, bg="cadetblue", font=ft1, command=self.popup)\
			.pack(side=tk.LEFT, anchor=tk.W, padx=10)

		f_side.pack(fill=tk.X, anchor=tk.W)

		self.controls = tk.Text(frame, font=ft2)
		self.controls.pack(expand='yes', fill='both', padx=5, pady='10')
		self.controls.insert(tk.END, self.default_code)

		frame.propagate(False)
		return frame

	def reset(self):
		self.controls.delete(0.0, tk.END)
		self.controls.insert(tk.END, self.default_code)
		self.refresh()

	def refresh(self):
		self.frame_main.forget()
		del self.frame_main

		self.bottom.forget()
		del self.bottom

		self.frame_main = tk.Frame(self.root, bg="white", bd=2)
		self.frame_main.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

		self.bottom = tk.Frame(self.root, width=5, bg="blue")
		self.bottom.pack(side=tk.LEFT, fill=tk.Y)

		ft = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
		all_code = self.controls.get(0.0, tk.END)
		len_color = len(colors) - 1
		all_error = ""
		for i, one in enumerate(all_code.split("\n")):
			if one is not None and one.strip() != "":
				color = colors[i % len_color]
				desc = one.split(".")[0]
				pack = one.split(".")[1:][0]
				pack_code = "tk.Label(self.frame_main, font=ft, text='{}', width=10, height=3, bg='{}')".format(desc, color)
				pack_code += "." + pack
				try:
					exec(pack_code)
				except Exception as err:
					print(pack_code)
					all_error += one + "\n"
		if all_error != "":
			message = "以下布局设置语法有错误，请检查:\n\n"
			message += all_error
			tku.show_info(message)

	def popup(self):
		all_code = self.controls.get(0.0, tk.END)
		win_multi2.Window(self.root, all_code)
