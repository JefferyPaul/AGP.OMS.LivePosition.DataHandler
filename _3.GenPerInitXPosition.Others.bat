echo off
chcp 65001

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\Others\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.Others.txt"


cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\LongShort\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.LongShort.txt"

