# encoding: utf-8
'''
@author: Tam
@file: stock.py
@time: 2022/3/23 11:12 PM
@desc:获取价格，并且计算涨跌幅
'''

import data.stock as st

# 获取股票行情数据（日k）
# 初始化变量
code = '002594.XSHE'
data = st.get_singel_price(code=code,
                           time_freq='daily',
                           start_date='2022-01-01',
                           end_date='2022-03-23')
# print(data)
# 计算涨跌幅，验证准确性

data = st.calculate_change_pct(data)
# print(data)


# 获取周k

data_w = st.transfer_price_freq(data, 'w')
print(data_w)


# 计算涨跌幅，验证准确性

data_w = st.calculate_change_pct(data_w)
print(data_w)