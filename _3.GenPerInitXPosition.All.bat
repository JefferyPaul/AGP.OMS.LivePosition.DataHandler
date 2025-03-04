echo off
chcp 65001

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\AIO\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.AIO.txt"

cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\PA\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.PA.txt"


cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\S8\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.S8.txt"


cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\LongShort\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.LongShort.txt"


cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\FastTrend\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.FastTrend.txt"


cd %~dp0
python cleaning_data_for_perInitX.py -p "..\Data\OmsLivePosition\_Output_1_TraderPosition" -i "..\Data\OmsLivePosition\_Output_2_TraderInitX" -o "..\Data\OmsLivePosition\_Output_3_PositionPInitX\Call220K\data.csv" -t ".\Config\GeneralTickerInfo.csv" -w ".\Config\WhiteListTrader.Call220K.txt"

