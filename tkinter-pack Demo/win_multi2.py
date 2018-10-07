# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
import tkutils as tku

colors = ['red', 'yellow', 'blue', 'green', 'pink', 'slateblue', 'lawngreen', 'orange', 'gold', 'cyan',
		  'cyan', 'brown', 'gray', 'royalblue', 'magenta', 'olive', 'black']


class Window:
	def __init__(self, parent, pack_code):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (600, 400))
		tku.center_window(self.root)
		self.root.title("多组件的pack布局, 改变窗体大小，观察组件的变化")
		self.root.grab_set()
		self.root.resizable(True, True)
		self.pack_code = pack_code
		self.body()

	# 绘制窗体组件
	def body(self):
		all_code = self.pack_code
		len_color = len(colors) - 1
		all_error = ""
		ft = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
		for i, one in enumerate(all_code.split("\n")):
			if one is not None and one.strip() != "":
				color = colors[i % len_color]
				desc = one.split(".")[0]
				pack = one.split(".")[1:][0]
				pack_code = "tk.Label(self.root, font=ft, text='{}', width=10, height=3, bg='{}')".format(desc, color)
				pack_code += "." + pack
				try:
					exec(pack_code)
				except Exception as err:
					all_error += one + "\n"
		if all_error != "":
			message = "以下布局设置语法有错误，请检查:\n\n"
			message += all_error
			tku.show_info(message)
