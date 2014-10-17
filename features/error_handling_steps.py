import time

from lettuce import step, world


@step(u'CI server (\d+) is failing$')
def ci_server_is_failing(step, server):
    world.fake_ci_servers[int(server) - 1].failing = True

@step(u'my poll rate is (\d+) seconds$')
def my_poll_rate_is_seconds(step, seconds):
    world.poll_rate = int(seconds)
    world.rebuild_config_file() 

@step(u'I wait (\d+) seconds$')
def i_wait_seconds(step, seconds):
    time.sleep(int(seconds))
