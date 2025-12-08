# coding:utf-8

""" 利用 tkinter.Canvas 实现推箱子游戏

基本说明：
    1. 参考game_maps.py 中的现有游戏场景，自己设计新的游戏关卡（可借鉴其他推箱子游戏的场景，自定义模仿设置）
    2. 设置 push_box_game.BOX_SIZE, 设置箱子大小，缺省为64， 理论上，可按自己需要，任意设置， 一般大小为 32, 64, 96, 128
    3. 设置 push_box_game.start_index, 设置开始关卡数， 进行游戏
    4. 该程序仅用于演示参考，不是完整的商业游戏，大家可以自行扩展功能，如实时调整大小，回退功能等。

开发人员: Edwin.Zhang
开发时间: 2019-6-28
"""

import PIL as pil
from PIL import ImageTk
from tkinter import *
from tkinter.messagebox import *
import numpy as np
from game_maps import basic_maps

root = Tk()
TOTAL_GAMES = len(basic_maps)  # 总的游戏关数
BOX_SIZE = 64    # 游戏的方块大小, 可设置访问(32, 64, 96, 128) 其实，可以任意


DIRECTIONS = {
    "Up": (-1, 0, -2, 0),
    "Down": (1, 0, 2, 0),
    "Left": (0, -1, 0, -2),
    "Right": (0, 1, 0, 2),
}


def resized_image(img_name, w_box=BOX_SIZE, h_box=BOX_SIZE):
    """ 对图片进行按比例缩放处理, 返回tk支持的图片对象"""
    img = pil.Image.open(img_name)
    w, h = img.size
    if w > h:
        width = w_box
        height = int(h_box * (1.0 * h / w))
    else:
        height = h_box
        width = int(w_box * (1.0 * w / h))
    img1 = img.resize((width, height), pil.Image.ANTIALIAS)
    return ImageTk.PhotoImage(img1)


def create_game_window(width, height):
    """ 创建游戏窗口，并使其屏幕居中 """
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/3)
    root.geometry(size)


# 加载游戏中用到的所有图片
imgs = [resized_image('images\\Wall.jpg'),
        {
            'Stop': (resized_image('images\\Worker.jpg'), resized_image('images\\WorkerInDest.jpg')),
            'Up': (resized_image('images\\w_up.jpg'), resized_image('images\\w_up_in.jpg')),
            'Down': (resized_image('images\\w_down.jpg'), resized_image('images\\w_down_in.jpg')),
            'Left': (resized_image('images\\w_left.jpg'), resized_image('images\\w_left_in.jpg')),
            'Right': (resized_image('images\\w_right.jpg'), resized_image('images\\w_right_in.jpg'))
        },
        resized_image('images\\Box.jpg'),
        resized_image('images\\Passageway.jpg'),
        resized_image('images\\Destination.jpg'),
        resized_image('images\\WorkerInDest.jpg'),
        resized_image('images\\redbox.jpg')]

# 0-墙，1-人，2-箱子，3-路，4-目的地, 5-人在目的地，6-箱子在目的地
Wall, Worker, Box, Passageway, Destination, WorkerInDest, BoxInDest = (0, 1, 2, 3, 4, 5, 6)


class BoxGame:
    def __init__(self, game_index=1):
        """
            game_index : 游戏关数, 从1开始
        """
        self.game_index = max([1, game_index])
        self.game_steps = 0
        self.screen = None
        self.direction = "Stop"

    def start_game(self, *args):
        if self.screen is not None:
            self.screen.forget()
            del self.screen

            self.btn_refresh.forget()
            del self.btn_refresh

        # 获得当前关卡的地图
        self.cur_map = np.asarray(basic_maps[self.game_index-1], dtype=np.int)
        self.rows, self.cols = self.cur_map.shape[0:2]   # 地图的行数, 列数
        self.x, self.y = 0, 0                            # 推箱工人的位置 (self.x, self.y)
        self.game_steps = 0                              # 当前关的步数
        self.direction = "Stop"

        # 创建并刷新游戏界面
        win_width = self.cols * BOX_SIZE + BOX_SIZE/2 + 40
        win_height = self.rows * BOX_SIZE + BOX_SIZE/2 + 100
        create_game_window(win_width, win_height)

        self.game_title()
        self.screen = Canvas(root, bg='white', width=BOX_SIZE * self.cols, height=BOX_SIZE * self.rows)
        self.screen.configure(highlightthickness=0)      # 去掉画布的边框
        self.refresh_screen()                            # 动态刷新游戏界面
        self.screen.bind("<KeyPress>", self.play_game)   # 绑定键盘事件，进行游戏操作
        self.screen.pack(pady=20)
        self.screen.focus_set()

        self.btn_refresh = Label(root, width=150, height=50)
        tk_img = resized_image('images\\restart.png', 120, 120)
        self.btn_refresh.image = tk_img
        self.btn_refresh.config(image=tk_img)
        self.btn_refresh.bind("<Button-1>", self.start_game)  # 重新开始游戏，可以按“空格”来完成
        self.btn_refresh.pack()

    # 刷新绘制整个游戏区域图形
    def refresh_screen(self):
        self.screen.delete('all')    # 先清空画布，这句话很重要，否则，大的游戏界面刷新会越来越慢
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.cur_map[i, j] == Worker:
                    self.x, self.y = i, j
                    _img = imgs[Worker][self.direction][0]
                elif self.cur_map[i, j] == WorkerInDest:
                    self.x, self.y = i, j
                    _img = imgs[Worker][self.direction][1]
                elif self.cur_map[i, j] == -1:
                    _img = None
                else:
                    _img = imgs[self.cur_map[i, j]]  # 获得对应位置的图片，并进行绘制
                if _img:
                    self.screen.create_image((j * BOX_SIZE + BOX_SIZE / 2, i * BOX_SIZE + BOX_SIZE / 2), image=_img)
        root.update()
        self.screen.focus_set()

    def play_game(self, event):
        key_code = event.keysym

        if key_code in DIRECTIONS.keys():  # 按方向键 "Up", "Down", "Left", "Right" 键的方向，进行移动
            self.move_to(key_code)
        elif key_code == "space":          # 按空格键，重新开始游戏
            self.start_game()

    def move_to(self, move_direct):
        self.direction = move_direct   # 记录移动方向，可用来绘制搬运工人的不同方向上的图像
        m = DIRECTIONS[move_direct]    # 获得移动方向的位移信息
        x1, y1, x2, y2 = (self.x + m[0], self.y + m[1], self.x + m[2], self.y + m[3])  # 获得移动方向的后2个位置的坐标

        p1, p2 = None, None   # 按某方向移动前，需要判断该方向前2个格子的状态，才能决定下一步行为
        if self.is_valid_position(x1, y1):  # 判断是否在游戏区域
            p1 = self.cur_map[x1, y1]
        if self.is_valid_position(x2, y2):
            p2 = self.cur_map[x2, y2]

        if p1 == Wall or not self.is_valid_position(x1, y1):  # p1 是墙
            return

        if p1 == Passageway:      # P1处为通道
            self.move_workman()
            self.x = x1
            self.y = y1
            self.cur_map[x1, y1] = Worker
        if p1 == Destination:     # P1处为目的地
            self.move_workman()
            self.x = x1
            self.y = y1
            self.cur_map[x1, y1] = WorkerInDest
        if p1 == Box:
            if p2 == Wall or not self.is_valid_position(x2, y2) or p2 == Box:  # P2是墙 或 出界 或为箱子
                return
        if p1 == Box and p2 == Passageway:
            self.move_workman()
            self.x = x1
            self.y = y1
            self.cur_map[x2, y2] = Box
            self.cur_map[x1, y1] = Worker
        if p1 == Box and p2 == Destination:
            self.move_workman()
            self.x = x1
            self.y = y1
            self.cur_map[x2, y2] = BoxInDest
            self.cur_map[x1, y1] = Worker
        if p1 == BoxInDest and p2 == Passageway:
            self.move_workman()
            self.x = x1
            self.y = y1
            self.cur_map[x2, y2] = Box
            self.cur_map[x1, y1] = WorkerInDest
        if p1 == BoxInDest and p2 == Destination:
            self.move_workman()
            self.x = x1
            self.y = y1
            self.cur_map[x2, y2] = BoxInDest
            self.cur_map[x1, y1] = WorkerInDest

        self.game_steps += 1  # 统计已经用的步数
        self.game_title()
        self.refresh_screen()

        if self.is_passed():
            showinfo(title="提示", message=" 恭喜你顺利通过第({})关! \n\n一共用了({})步".format(self.game_index, self.game_steps))
            self.game_index = self.game_index % TOTAL_GAMES + 1
            self.start_game()

    def move_workman(self):
        if self.cur_map[self.x, self.y] == Worker:
            self.cur_map[self.x, self.y] = Passageway
        elif self.cur_map[self.x, self.y] == WorkerInDest:
            self.cur_map[self.x, self.y] = Destination

    def is_valid_position(self, row, col):  # 判断坐标是否在地图范围内
        return 0 <= row < self.rows and 0 <= col < self.cols

    def game_title(self):  # 为简化，直接在窗体标题中，显示游戏进度信息
        root.title("推箱子 - 第({}/{})关    总步数: {}".format(self.game_index, TOTAL_GAMES, self.game_steps))

    def is_passed(self):  # 过关条件: 不存在空目的地 及 人在目的地的格子
        return not np.any([self.cur_map == Destination, self.cur_map == WorkerInDest])


if __name__ == "__main__":
    start_index = 1   # 自己设置要开始玩完的关卡
    BoxGame(game_index=start_index).start_game()
    root.mainloop()
