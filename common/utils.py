from base64 import b64encode
from datetime import datetime, date

from dateutil.relativedelta import relativedelta


def covert_time(manufacturing_time, expiry_time):
    # manufacturing time = 2020/03/12 and expiry_time = 12
    # Then it convert manufacturing time in DateTime obj and expiry_date into Datetime obj
    for fmt in ["%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"]:
        try:
            manufacturing_date = datetime.strptime(manufacturing_time, fmt).date()
            expiry_date = manufacturing_date + relativedelta(months=+int(expiry_time))
            return manufacturing_date, expiry_date
        except Exception as e:
            continue


def is_expired_func(expiry_time):
    time_diff_delta = expiry_time - date.today()
    if time_diff_delta.days <= 0:
        return True
    return False


def conversion_image_into_bs64(file_location):
    with open(f"{file_location}", "rb") as img_file:
        img_file = b64encode(img_file.read())
    return img_file
