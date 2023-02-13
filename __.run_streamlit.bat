echo off
chcp 65001

title Position_AIO

cd %~dp0
call "venv\Scripts\activate.bat"

cd %~dp0
streamlit run "st_home.py" --server.port 8888


pause