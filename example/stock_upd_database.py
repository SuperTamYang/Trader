# encoding: utf-8
'''
@author: Tam
@file: stock_upd_database.py
@time: 2022/3/20 1:00 AM
@desc: 用于调用股票行情数据的脚本
'''

import data.stock as st
import pandas as pd
# 初始化变量
code = '002594.XSHE'

# 调用一只股票的行情数据
data = st.get_singel_price(code=code,
                           time_freq='daily',
                           start_date='2022-01-01',
                           end_date='2022-03-18')
# 存入csv
st.export_data(data=data, filename=code, type='price')

# 从csv中获取数据

data = st.get_csv_data(code=code, type='price')
print(data)

# 作业：实时更新数据：假设每天更新日K数据 > 寸到csv文件里面 > data.to_csv(append)
# 思路：在export_data方法中，如果文件已经存在，则新增append，若不存在，则保持创建新文件夹
