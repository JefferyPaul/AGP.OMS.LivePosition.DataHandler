echo off
chcp 65001

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
python cleaning_data_for_perInitX.py -p ".\_Output_1_TraderPosition" -i ".\_Output_2_TraderInitX" -o ".\_Output_3_PositionPInitX\AIO\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.AIO.txt"

