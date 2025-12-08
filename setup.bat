@ECHO OFF

REM 设置 64位 python 3.6.7 的 python.exe 的全称文件名
if not defined PYTHON (set PYTHON="C:\Users\Edwin\AppData\Local\Programs\Python\Python36\python.exe")

REM 创建虚拟环境, 目录名为 .venv
%PYTHON% -m venv .venv

REM  更新升级 pip
.venv\scripts\python.exe -m pip install --upgrade pip

REM 根据 requirements.txt , 从国内镜像网站安装依赖模块。（分开写，是由于涉及模块的编译依赖）
.venv\scripts\pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

.venv\scripts\pip install maturin==0.12.20 -i https://pypi.tuna.tsinghua.edu.cn/simple

.venv\scripts\pip install notebook==6.4.10 -i https://pypi.tuna.tsinghua.edu.cn/simple

.venv\scripts\python.exe -m ipykernel install --user --name .venv --display-name "env_python367"

REM 创建激活虚拟环境的批处理文件 activate.bat
echo chcp 65001 > activate.bat
echo %~dp0.venv\scripts\activate >> activate.bat