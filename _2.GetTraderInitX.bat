echo off
chcp 65001

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
python get_trader_initx.py -i ".\Config\QMReportDBInfo.csv" -o ".\_Output_2_TraderInitX"

