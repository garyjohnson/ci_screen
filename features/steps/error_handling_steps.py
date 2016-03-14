import time

from behave import *

import features.support.helpers as helpers


@step(u'CI server (?P<server>\d+) is failing')
def ci_server_is_failing(context, server):
    context.fake_ci_servers[int(server) - 1].failing = True

@given(u'my poll rate is (?P<seconds>\d+) seconds')
def my_poll_rate_is_seconds(context, seconds):
    context.poll_rate = int(seconds)
    helpers.rebuild_config_file(context)

@when(u'I wait (?P<seconds>\d+) seconds')
def i_wait_seconds(context, seconds):
    time.sleep(int(seconds))
