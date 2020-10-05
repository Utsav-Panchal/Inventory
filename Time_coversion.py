import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def covert_time(manufacturing_time, expiry_time):
    # manufacturing time = 2020/03/12 and expiry_time = 12
    # Then it convert manufacturing time in DateTime obj and expiry_date into Datetime obj
    manufacturing_date = datetime.strptime(manufacturing_time, "%Y/%m/%d").date()
    expiry_date = manufacturing_date + relativedelta(months=+int(expiry_time))
    return manufacturing_date, expiry_date


def is_expired_func(expiry_time):
    print("Came to check expired ???????????????????????")
    time_diff_delta = expiry_time - date.today()
    if time_diff_delta.days <= 0:
        return True
    return False