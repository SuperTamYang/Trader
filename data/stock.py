import pandas as pd
from jqdatasdk import *
import datetime

auth('18898740516', 'Yxl940516')

# 设置行列不忽略
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)

# 全局变量
data_root = '/Users/yangxianliang/Downloads/TamTrader/data/'

def get_stock_list():
    """
    获取所有A股股票列表
    上海证券交易所.XSHG
    深圳证券交易所.XSHE
    :return: stock_list
    """
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list

def get_singel_price(code, time_freq, start_date, end_date):
    """
    获取单个股票行情数据
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    """
    # 如果start_date=None，默认为股票上市日
    if start_date is None:
        start_date = get_security_info(code).start_date
    # 获取行情数据
    data = get_price(code, start_date=start_date, end_date=end_date,
                     frequency=time_freq, panel=False)
    return data

def calculate_change_pct(data):
    """
    涨跌幅 = （当期收盘价 - 前期收盘价） / 前期收盘价
    :param data: dataframe 带有收盘价
    :return: dataframe 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) \
                        / data['close'].shift(1)
    return data

def export_data(data, filename, type):
    """
    导出股票行情数据
    :param data:
    :param filename:
    :param type 股票数据类型，可以是： price，finance
    :return:
    """
    file_root = data_root + type + '/' + filename + '.csv'
    data.index.names = ['date']
    data.to_csv(file_root)
    print('已成功存储至', file_root)

def get_csv_data(code, type):
    file_root = data_root + type + '/' + code + '.csv'
    return pd.read_csv(file_root)

def transfer_price_freq(data, time_freq):
    """
    转化股票行情数据：开盘价、收盘价、最高价，最低价
    :param data:
    :param time_freq:
    :return:
    """
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans

def get_single_finance(code, date, statDate):
    """
    获取单个股票财务指标
    :param code:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statDate)
    return data

def get_single_valuation(code, date, statDate):
    """
    获取单个股票估值指标
    :param code:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)
    return data


