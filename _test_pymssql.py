import pyodbc

serverName = '127.0.0.1'
userName = 'sa'
passWord = 'Elvis2024'
port = '2166'
db = ''
# 建立连接并获取cursor
# conn = pyodbc.connect(server=serverName, user=userName, password=passWord, database=db, port=port)
import pyodbc

coon = pyodbc.connect('DRIVER={SQL Server};' + f'SERVER={serverName};DATABASE={db};UID={userName};PWD={passWord},PORT={port}')
coon.close()
