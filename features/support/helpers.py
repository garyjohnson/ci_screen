import datetime

import pytz
import tzlocal
import dateutil.parser


def get_local_time_string(utc_time_string):
    date_time = dateutil.parser.parse(utc_time_string).replace(tzinfo=pytz.utc)
    local_date_time = date_time.astimezone(tzlocal.get_localzone())
    return datetime.datetime.strftime(local_date_time, "%Y-%m-%d %H:%M:%S")

