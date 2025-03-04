"""
相同trader名字的，直接合并
    position 相加
    initX 平均
"""

import os
import shutil
import argparse
import sys
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

PATH_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PATH_ROOT)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-p', '--position',)
arg_parser.add_argument('-i', '--initX',)
arg_parser.add_argument('-t', '--ticker_info', default='')
arg_parser.add_argument('-w', '--white_list', default='')
arg_parser.add_argument('-o', '--output',)
arg_parser.add_argument('--group', default='')
arg_parser.add_argument('--grouptrader', default='')

args = arg_parser.parse_args()
PATH_POSITION_ROOT = os.path.abspath(args.position)
PATH_GTI_File = os.path.abspath(args.ticker_info)
PATH_WHILT_LIST_File = os.path.abspath(args.white_list)
PATH_INITX_ROOT = os.path.abspath(args.initX)
PATH_OUTPUT_ROOT = os.path.abspath(args.output)
PATH_GROUP_FOLDER = os.path.abspath(args.group)
GROUP_TRADER = args.grouptrader

if not os.path.isdir(PATH_OUTPUT_ROOT):
    os.makedirs(PATH_OUTPUT_ROOT)
assert os.path.isdir(PATH_POSITION_ROOT)
assert os.path.isdir(PATH_INITX_ROOT)
assert os.path.isfile(PATH_GTI_File)


from pyptools.common.general_ticker_info import GeneralTickerInfoFile, TickerInfoData
from pyptools.common.object import Product, Ticker


D_TRADER_NAME_MAP = {
    # "gz030": "GuoZe",
    # "JC": "JunCheng",
    # "JHWG10": "TangYin",
    # "ZouQian": "ZouWei",
    "AIO@Test@AIO": "Paper.AIO",
    "AIO@Test@FastTrend": "Paper.FT",
    "AIO@Test@AnthonyPA": "Paper.PA",
    "AIO@Test@LongShort": "Paper.LS",
    "AIO@Test@SPA": "Paper.S8PA",
    "AIO@Test@Call220K": "Paper.Call220K",
    "AIO@Test@PA2": "Paper.PA2",
}


def handle_trader_name(name: str):
    if name in D_TRADER_NAME_MAP.keys():
        name = D_TRADER_NAME_MAP[name]
        return name
    else:
        if "@" in name:
            name = name.split("@")[1]        
        if name in D_TRADER_NAME_MAP.keys():
            name = D_TRADER_NAME_MAP[name]
        return name
    
    
def handle_group(trader_volume: dict) -> Dict[str, float]:
    # 讀取分組
    d_product_with_group = dict()
    for _group_name in os.listdir(PATH_GROUP_FOLDER):
        _path_group = os.path.join(PATH_GROUP_FOLDER, _group_name)
        if not os.path.isdir(_path_group):
            continue
        for _product_name in os.listdir(_path_group):
            _path_product = os.path.join(_path_group, _product_name)
            if not os.path.isdir(_path_product):
                continue
            d_product_with_group[_product_name] = _group_name
    
    # 
    d_value_in_product = defaultdict(float)
    for _ticker, _volume in trader_volume.items():
        _product_obj: Product = Ticker.from_name(_ticker).product
        _product_internal_name = _product_obj.InternalProduct
        if _product_internal_name in d_product_with_group:
            
            # TODO    忽略 CFFEX 
            _group_name = d_product_with_group[_product_internal_name]
            if _group_name == '_Cffex':
                continue
            d_value_in_product[_group_name] += float(_volume)
        else:
            d_value_in_product['Unknown'] += float(_volume)
    
    return d_value_in_product
            

if __name__ == '__main__':
    # 读取position
    d_trader_ticker_volume_px = defaultdict(lambda: defaultdict(float))
    for _file_name in os.listdir(PATH_POSITION_ROOT):
        p_trader_position = os.path.join(PATH_POSITION_ROOT, _file_name)
        if not os.path.isfile(p_trader_position):
            continue
        # _trader = handle_trader_name(_file_name.replace('.csv', ''))
        _trader = _file_name.replace('.csv', '')
        with open(p_trader_position) as f:
            l_lines = f.readlines()
        for line in l_lines:
            line = line.strip()
            if line == '':
                continue
            _ticker = line.split(',')[0]
            _volume = float(line.split(',')[1])
            if _ticker.split('.')[-1] == 'CFFEX':
                # 国债特殊处理
                if _ticker.find('T2') == 0:
                    _volume = _volume / 5
                elif _ticker.find('TL2') == 0:
                    _volume = _volume / 2
            _price = float(line.split(',')[2])
            d_trader_ticker_volume_px[_trader][_ticker] += _volume * _price

    # 读取 general ticker info
    # 从 volume 计算 value
    if os.path.isfile(PATH_GTI_File):
        d_ticker_info: Dict[Product, TickerInfoData] = GeneralTickerInfoFile.read(PATH_GTI_File)
        for _trader, _d_trader_data in d_trader_ticker_volume_px.items():
            for _ticker, _volume_px in _d_trader_data.items():
                _product: Product = Ticker.from_name(_ticker).product
                if _product not in d_ticker_info:
                    print(f'GTI文件没有此 product: {str(_product)}')
                    raise KeyError
                _point_value = d_ticker_info[_product].point_value
                _d_trader_data[_ticker] = _volume_px * _point_value

    # 读取initx
    d_trader_initX = defaultdict(float)
    for _file_name in os.listdir(PATH_INITX_ROOT):
        p_trader_initx = os.path.join(PATH_INITX_ROOT, _file_name)
        if not os.path.isfile(p_trader_initx):
            continue
        _trader = _file_name.replace('.csv', '')
        with open(p_trader_initx) as f:
            l_lines = f.readlines()
        _initx = l_lines[0].strip()
        if _initx == '':
            print(f'{p_trader_initx} 错误')
            raise Exception
        _initx = float(_initx)
        d_trader_initX[_trader] += _initx

    # 相除
    _error = False
    # l_trader_ticker_volume_p_initx = [ [ticker, trader_name, volume_per_initX ], ]
    l_trader_ticker_volume_p_initx = []
    for _trader in d_trader_ticker_volume_px.keys():
        if _trader not in d_trader_initX:
            # print(f'{_trader} 缺少initX')
            _error = True
            continue
        _initx = d_trader_initX[_trader]
        for _ticker, _position in d_trader_ticker_volume_px[_trader].items():
            if _initx == 0:
                l_trader_ticker_volume_p_initx.append([
                    _ticker, handle_trader_name(_trader), str(0)
                ])
            else:
                l_trader_ticker_volume_p_initx.append([
                    _ticker, handle_trader_name(_trader), str(_position / _initx)
                ])
    # if _error:
    #     raise Exception

    # trader name 处理
    # for _ in l_trader_ticker_volume_p_initx:
    #     _[1] = handle_trader_name(_[1])

    # 白名单
    if os.path.isfile(PATH_WHILT_LIST_File):
        with open(PATH_WHILT_LIST_File) as f:
            l_lines = f.readlines()
        l_white_list = [_.strip() for _ in l_lines if _.strip()]
        l_trader_ticker_volume_p_initx = [_ for _ in l_trader_ticker_volume_p_initx if _[1] in l_white_list]

    # 输出
    path_output_data = os.path.join(PATH_OUTPUT_ROOT, 'data.csv')
    with open(path_output_data, 'w') as f:
        f.writelines('\n'.join([
            ','.join(_)
            for _ in l_trader_ticker_volume_p_initx
        ]))
    path_output_update_time = os.path.join(PATH_OUTPUT_ROOT, '_update.csv')
    with open(path_output_update_time, 'w') as f:
        f.writelines(datetime.now().strftime('%Y%m%d %H%M%S'))


    # 2025/3/2 新增功能，按 group 分組統計持倉市值
    if PATH_GROUP_FOLDER:
        if not GROUP_TRADER:
            raise Exception
        d_group_trader_ticker_volume = dict()
        for _ in l_trader_ticker_volume_p_initx:
            _ticker = _[0]
            _trader = _[1]
            _volume = _[2]
            if _trader != GROUP_TRADER:
                continue
            d_group_trader_ticker_volume[_ticker] = _volume
        d_group_volume: Dict[str, float] = handle_group(d_group_trader_ticker_volume)
        l_output_data = [
            f'{str(_k)},{str(_v)}'
            for _k, _v in d_group_volume.items()
        ]
        
        path_output_grouped = os.path.join(PATH_OUTPUT_ROOT, 'data_grouped.csv')
        with open(path_output_grouped, 'w') as f:
            f.writelines('\n'.join(l_output_data))
        
    