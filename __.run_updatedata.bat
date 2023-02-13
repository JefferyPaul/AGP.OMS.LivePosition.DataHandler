echo off
chcp 65001

title Position_AIO

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
python run_bat_scheduler.py --interval 60

