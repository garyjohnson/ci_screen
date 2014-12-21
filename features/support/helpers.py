import copy
import os
import datetime
import sys
import subprocess
import time

import pytz
import tzlocal
import dateutil.parser
import pqaut.client
from nose.tools import assert_true 

import features.support.config_helper as config_helper


port = 6500
LOG_DEBUG = 10

def get_local_time_string(utc_time_string):
    date_time = dateutil.parser.parse(utc_time_string).replace(tzinfo=pytz.utc)
    local_date_time = date_time.astimezone(tzlocal.get_localzone())
    return datetime.datetime.strftime(local_date_time, "%Y-%m-%d %H:%M:%S")

def assert_is_above(above, below):
    pqaut.client.assert_is_visible(above)
    pqaut.client.assert_is_visible(below)

    above_y = 0
    below_y = 0
    for retry in range(10):
        above_element = pqaut.client.find_element(above, None)
        below_element = pqaut.client.find_element(below, None)

        above_y = above_element.get('global_position', {}).get('y', 0)
        below_y = below_element.get('global_position', {}).get('y', 0)
        if above_y < below_y:
            break

        time.sleep(0.5)

    assert_true(above_y < below_y, u'Expected "{above}" (y:{above_y}) to be above "{below}" (y:{below_y})'.format(above=above, below=below, above_y=above_y, below_y=below_y))

def get_linux_faketime_path():
    paths = ['/usr/local/lib', '/usr/lib', '/usr/lib/arm-linux-gnueabihf', '/usr/lib/arm-linux-gnueabi']
    for path in paths:
        faketime_path = '{}/faketime/libfaketime.so.1'.format(path)
        if os.path.exists(faketime_path):
            return faketime_path

def add_faketime_to_env_vars(env_vars, fake_time):
    faketime_vars = { 'LD_PRELOAD': get_linux_faketime_path() }
    if sys.platform == 'darwin':
        faketime_vars = {   'DYLD_INSERT_LIBRARIES': '/usr/local/lib/faketime/libfaketime.1.dylib:/System/Library/Frameworks/OpenGL.framework/Resources/GLEngine.bundle/GLEngine',
                            'DYLD_FORCE_FLAT_NAMESPACE': '1'}
    env_vars.update(faketime_vars)
    return env_vars

def kill_ci_screen(context):
    if context.app_process:
        subprocess.Popen.kill(context.app_process)
    if context.dev_null:
        context.dev_null.close()

def launch_ci_screen(context, fake_time = None):
    if fake_time is not None:
        os.environ['FAKETIME'] = "@{}".format(fake_time)

    env_vars = os.environ
    if fake_time is not None:
        env_vars = add_faketime_to_env_vars(env_vars, fake_time)

    kwargs = {'env': env_vars}
    context.dev_null = open(os.devnull, 'w')
    if context.config.logging_level > LOG_DEBUG:
        kwargs.update({'stdout':context.dev_null, 'stderr':context.dev_null})

    context.app_process = subprocess.Popen([context.app_path, "--automation_server"], **kwargs)

    pqaut.client.wait_for_automation_server()

def get_port():
    global port
    port = port + 1
    return port

def rebuild_config_file(context):
    config = {'general':{'poll_rate_seconds':str(context.poll_rate), 'rotation':'0', 'holiday':str(context.holiday)},  'ci_servers':{'sections':''}}
    for index in range(len(context.fake_ci_servers)):
        world_ci_server = context.fake_ci_servers[index]
        config['ci_servers']['sections'] += '{},'.format(index)
        config[str(index)] = {'url':'http://0.0.0.0:{}'.format(world_ci_server.port)}

    config_helper.build_config(config)

