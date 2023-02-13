echo off
chcp 65001

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
python get_trader_position.py -i ".\Config\OmsDBInfo.csv" -o ".\_Output_1_TraderPosition"

