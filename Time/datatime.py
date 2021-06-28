import numpy as np
import pandas as pd
from datetime import datetime
import json
from datetime import timedelta

# 获取日期在一年中的第几周
def get_week(date):
    if pd.to_datetime(str(date.year)+"-01-01").weekday() == 0:
        return int(datetime.strftime(date, "%W"))
    else:
        return int(datetime.strftime(date, "%W")) + 1


# 获取日期当月1号的日期
def get_firstday_month(date):
    year = str(date.year)
    month = str(date.month)
    firstday = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')

    return firstday


# 获取日期在当季度第一天的日期
def get_firstday_quarter(date):
    year = str(date.year)
    month = str(((date.month - 1) // 3 * 3 + 1))
    firstday = datetime.strptime(year+"-"+month+"-01", '%Y-%m-%d')

    return firstday


# 获取日期在当年第一天的日期
def get_firstday_year(date):
    year = str(date.year)
    firstday = datetime.strptime(year+"-01-01", '%Y-%m-%d')

    return firstday
