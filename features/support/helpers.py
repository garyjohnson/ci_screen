import datetime
import time

import pytz
import tzlocal
import dateutil.parser
import pqaut.client
from nose.tools import assert_true 


def get_local_time_string(utc_time_string):
    date_time = dateutil.parser.parse(utc_time_string).replace(tzinfo=pytz.utc)
    local_date_time = date_time.astimezone(tzlocal.get_localzone())
    return datetime.datetime.strftime(local_date_time, "%Y-%m-%d %H:%M:%S")

def assert_is_above(above, below):
    pqaut.client.assert_is_visible(above)
    pqaut.client.assert_is_visible(below)

    above_y = 0
    below_y = 0
    for retry in range(5):
        above_element = pqaut.client.find_element(above, None)
        below_element = pqaut.client.find_element(below, None)

        above_y = above_element.get('global_position', {}).get('y', 0)
        below_y = below_element.get('global_position', {}).get('y', 0)
        if above_y < below_y:
            break

        time.sleep(0.5)

    assert_true(above_y < below_y, u'Expected "{above}" (y:{above_y}) to be above "{below}" (y:{below_y})'.format(above=above, below=below, above_y=above_y, below_y=below_y))
