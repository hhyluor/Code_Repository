import numpy as np
import pandas as pd
from datetime import datetime
import json
from datetime import timedelta

# R：年度无风险利率
# T：一年的周期个数，以月为周期T=12,以周为周期T=52


# 年化夏普比率(R为一年期的无风险利率；T为一年的周期个数，以月为周期T=12,以周为周期T=52)
from Time.datatime import get_firstday_year


def get_sharpe_ratio(yield_list, R, T):
    '''

    :param yield_list:
    :param R:
    :param T:
    :return:
    '''
    yield_list = yield_list.dropna()
    if len(yield_list) > 1:
        return ((np.average(yield_list)+1)**T-1-R)/(np.std(yield_list) * np.sqrt(T))
    else:
        return np.nan


# 标准差
def get_year_std(yield_list):
    yield_list = yield_list.dropna()
    if len(yield_list) > 1:
        return yield_list.std()
    else:
        return np.nan


# 年化下行标准差(R_T为对应周期的无风险利率)
def get_DownStd(yield_list, R, T):
    yield_list = yield_list.dropna()
    R_T = (R + 1) ** (1 / T) - 1
    newlist = []
    for i in yield_list:
        if i<R_T:
            newlist.append((i-R_T)**2)
        else:
            continue
    return np.sqrt(np.average(newlist) * T)


# 最大回撤，s是以日期为索引的Series
def get_max_retracement(s):
    s_retracement = 1 - s / s.expanding(min_periods=1).max()

    edate = s_retracement.idxmax()

    max_retracement = s_retracement[edate]

    bdate = s[:edate].idxmax()

    rdate = s[s > s[bdate]][edate:].index.min()

    rdays = (rdate - edate).days

    return [max_retracement, bdate, edate, rdate, rdays]


# 最大回撤，s_source是以日期为索引的Series
def get_max_retracement(s_source, current_T, section='total'):
    if section == 'total':
        s = s_source[:current_T]
    elif section == 'year':
        if get_firstday_year(current_T) < s_source.index[0]:
            return [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            s = s_source[get_firstday_year(current_T):current_T]
    elif section == 'm3':
        if (current_T - pd.DateOffset(months=3)) < s_source.index[0]:
            return [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            s = s_source[current_T - pd.DateOffset(months=3):current_T]
    elif section == 'm6':
        if (current_T - pd.DateOffset(months=6)) < s_source.index[0]:
            return [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            s = s_source[current_T - pd.DateOffset(months=6):current_T]
    elif section == 'y1':
        if (current_T - pd.DateOffset(years=1)) < s_source.index[0]:
            return [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            s = s_source[current_T - pd.DateOffset(years=1):current_T]
    elif section == 'y3':
        if (current_T - pd.DateOffset(years=3)) < s_source.index[0]:
            return [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            s = s_source[current_T - pd.DateOffset(years=3):current_T]
    elif section == 'y5':
        if (current_T - pd.DateOffset(years=5)) < s_source.index[0]:
            return [np.nan, np.nan, np.nan, np.nan, np.nan]
        else:
            s = s_source[current_T - pd.DateOffset(years=5):current_T]
    else:
        return [np.nan, np.nan, np.nan, np.nan, np.nan]

    s_retracement = 1 - s / s.expanding(min_periods=1).max()

    edate = s_retracement.idxmax()

    max_retracement = s_retracement[edate]

    bdate = s[:edate].idxmax()

    rdate = s[s > s[bdate]][edate:].index.min()

    rdays = (rdate - edate).days

    return [max_retracement, bdate, edate, rdate, rdays]

    # return 1

# 年化索提诺比率(R为一年期的无风险利率；T为一年的周期个数，以月为周期T=12,以周为周期T=52；R_T为对应周期的无风险利率)
def get_sortino_ratio(yield_list,R,T):
    yield_list = yield_list.dropna()
    if len(yield_list) > 1:
        return ((np.average(yield_list)+1)**T-1-R) / (get_DownStd(yield_list, R, T) * np.sqrt(T))
    else:
        return np.nan


# beta
def get_beta(s1,s2):
    if s1.cov(s2) != 0 and np.var(s2, ddof=1) != 0:
        beta = s1.cov(s2) / np.var(s2, ddof=1)
        return beta
    else:
        return np.nan


# pearson
def get_pearson(s1,s2):
    if (np.std(s1) > 0 and np.std(s2) > 0):
        return s1.corr(s2)
    else:
        return np.nan


# 特雷诺指数
def get_treynor_ratio(s1, s2, R, T):
    if (pd.isnull(get_beta(s1, s2)) or get_beta(s1, s2) == 0):
        return np.nan
    else:
        treynor = ((np.average(s1.dropna())+1)**T-1-R) / get_beta(s1, s2)
        return treynor


# 平均损益比 mean(大于0的模拟组合周收益率)/mean(小于等于0的模拟组合周收益率)
def get_loss_to_profit(yield_list):
    if yield_list.empty:
        return np.nan
    else:
        avg_loss = np.average([i for i in yield_list if i <= 0])
        avg_profit = np.average([i for i in yield_list if i > 0])
        return abs(avg_profit / avg_loss)


# 波动率（年化）  波动率（年化）=模拟组合周收益率标准差*√52
def year_wave_ratio(yield_list,T):
    yield_list = yield_list.dropna()
    if len(yield_list) > 1:
        np.std(yield_list) * np.sqrt(T)
    else:
        return np.nan


# 投资胜率
def get_win_rate(yield_list):
    if yield_list.empty:
        return np.nan
    else:
        return len([i for i in yield_list if i > 0]) / len(yield_list)


# 年化收益率
def year_profit_ratio(yield_list):
    if yield_list.empty:
        return np.nan
    else:
        return np.power(1 + np.average(yield_list),52) - 1


# 最大回撤 净值
def MaxDrawdown(yield_list):
    i = np.argmax((np.maximum.accumulate(yield_list) - yield_list) / np.maximum.accumulate(yield_list)) # 结束位置
    if i == 0:
        return 0
    j = np.argmax(yield_list[:i])  # 开始位置
    return (yield_list[j] - yield_list[i]) / (yield_list[j])


# 用等差的原则填充缺少的净值数据
def NV_fillna(NV_list):
    for i in range(len(NV_list)):
        if pd.isnull(NV_list[i]):
            j = 1
            while pd.isnull(NV_list[i+j]):
                j += 1
            diff_NV = (NV_list[i+j] - NV_list[i-1])/(j+1)
            for k in range(0, j):
                NV_list[i+k] = NV_list[i-1] + (k+1) * diff_NV
        else:
            continue


# 用等差的原则填充缺少的净值数据
def NV_fillna2(NV_list):
    tmp_i1 = 0

    for mm in range(len(NV_list)):
        if pd.isna(NV_list[mm]):
            continue
        tmp_i1 = mm
        break
    NV_list[0:tmp_i1] = NV_list[tmp_i1]

    tmp_i2 = 0

    for mmm in range(len(NV_list)):
        if pd.isna(NV_list[len(NV_list)-mmm-1]):
            continue
        tmp_i2 = len(NV_list)-mmm-1

        break
    NV_list[tmp_i2:] = NV_list[tmp_i2]

    for i in range(len(NV_list)):
        if pd.isnull(NV_list[i]):
            j = 1
            while pd.isnull(NV_list[i+j]):
                j += 1
            diff_NV = (NV_list[i+j] - NV_list[i-1])/(j+1)
            for k in range(0, j):
                NV_list[i+k] = NV_list[i-1] + (k+1) * diff_NV
        else:
            continue
    # else:
    #     return NV_list
