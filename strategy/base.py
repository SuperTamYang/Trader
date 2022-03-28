# encoding: utf-8
'''
@author: Tam
@file: strategy.py
@time: 2022/3/23 11:32 PM
@desc: 用来创建交易策略、生成交易信号
'''


import data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def compose_signal(data):
    """
    整合信号
    :param data:
    :return:
    """
    # 整合信号 以下为视频课的整合（Tam： 仅考虑连续卖出的异常，未考虑周全）
    # 模拟重复卖出： 周二再次卖出
    # data['sell_signal'] = np.where((data['weekday'] == 0) | (data['weekday'] == 1), -1, 0)
    # data['sell_signal'] = np.where((data['sell_signal'] == -1)
    #                                & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    # data['signal'] = data['buy_signal'] + data['sell_signal']
    data['buy_signal'] = np.where((data['buy_signal'] == 1)
                                  & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1)
                                   & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

def calculate_prof_pct(data):
    """
    计算单次收益率：开仓、平仓（平仓的全部股数）
    :param data:
    :return:
    """
    data = data[data['signal'] != 0]
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data

def calculate_max_drawdown(data):
    """
    计算最大回撤比
    :param data:
    :return:
    """
    # 选取时间周期（时间窗口）
    window = 252
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 = （谷值 - 峰值）/ 峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min() # 最小值，可能有负值，最小的回撤就是最大回撤
    return data

def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data:
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data

def calculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: dataframe，stock
    :return: float
    """
    # 公式 sharpe ratio = （回报率的均值 - 无风险利率）/ 回报率的标准差
    # 因子项
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()  # 回报率的均值 = 日涨跌幅.mean()
    sd_return = daily_return.std()  # 回报率的标准差 = 日涨跌幅.std()
    # 计算夏普 每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year
