# encoding: utf-8
'''
@author: Tam
@file: comp_sharpe_ratio.py
@time: 2022/3/28 22:49
@desc:
'''
import data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt
# 容器：存放夏普
sharpes = []
# 获取3只股票的数据: 比亚迪、宁德时代、隆基股份
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
for code in codes:
    data = st.get_singel_price(code, 'daily', '2019-01-01', '2022-01-01')
    # 计算每只股票的夏普比率
    sharpe = stb.calculate_sharpe(data)
    sharpes.append([code, sharpe])  # 存放[[c1,s1], [c2,s2]..]
    # 可视化3只股票并比较
    sharpes = pd.DataFrame(sharpes, columns=['code', ['sharpe']], index=code)
    print(sharpes)