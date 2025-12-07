@ECHO OFF

REM 设置 python.exe 的位置
if not defined PYTHON (set PYTHON="C:\ProgramData\Anaconda3\envs\tf_gpu\python.exe")

REM 创建虚拟环境, 目录名为 .venv
%PYTHON% -m venv .venv

REM  更新升级 pip
.venv\scripts\python.exe -m pip install --upgrade pip

REM 根据 requirements.txt , 从国内镜像网站安装依赖模块
.venv\scripts\pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
