# 一. 项目说明
该项目是一些Python程序的源代码，用于学习

## 1. California Housing Prices
是一个机器学习的项目级演示代码，实现机器学习的全自动化处理。 详细描述，可参考CSDN博客相关文章
https://blog.csdn.net/superfanstoprogram/article/details/80413639

## 2. tkinter-pack Demo
用TKInter编写的演示程序，主要演示pack()定位的参数设置。 详细描述，可参考本CSDN博客相关文章
https://blog.csdn.net/superfanstoprogram/article/details/83713196

## 3. Neural Style Transfer
是一个用Keras实现的，利用神经网络进行图像风格迁移的工具， GUI用tkinter完成。可参考CSDN博客相关文章
https://blog.csdn.net/superfanstoprogram/article/details/90239343


## 4. Boxman
利用 tkinter.Canvas 实现的推箱子游戏, 核心代码 play.py 精简为200多行，可以参考game_maps.py中的地图设置方式，自己设计新的游戏关卡。



# 二. 安装说明
该项目用的Python版本是 3.6.7; 根据以下安装说明创建虚拟环境后，可直接运行

1. 下载并安装 [Python 3.6.7](https://www.python.org/downloads/windows)。

2. 复制所有源代码到本地目录

- 手工编辑 setup.bat 文件，设置PYTHON变量为本地 python 3.6.7 安装目录下的 python.exe 的全称文件名。 
    ```
    if not defined PYTHON (set PYTHON="C:\Program Files\Python36\python.exe")
    ```
- 打开命令行窗口，并定位以上源代码目录

  **小技巧：** 用资源管理器定位以上目录，然后清空地址栏，输入 cmd , 按回车，可打开命令行窗口，并定位当前目录

- 在命令行窗口中，运行 setup.bat, 完成虚拟环境的搭建和依赖模块的安装

- 运行相关子目录下的 run.bat，可启动相应程序


# 三. keras 预训练模型的权重系数下载：
[Neural Style Transfer] 需用到 keras的预训练模型，可通过以下链接下载
https://pan.baidu.com/s/1pYEKpQ48TabncoMy2btBLQ
提取码: rao4

下载后的模型参数文件，请复制到用户目录下的 .keras\models 中，以便keras进行读取
如： C:\Users\Edwin\.keras\models
