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

def kill_ci_screen(context):
    if context.app_process:
        subprocess.Popen.kill(context.app_process)
    if context.dev_null:
        context.dev_null.close()

def launch_ci_screen(context, fake_time = None):
    if fake_time is not None:
        os.environ['FREEZETIME'] = fake_time

    kwargs = {'env': os.environ }
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
    config = {
                'general': {
                    'poll_rate_seconds':str(context.poll_rate), 
                    'rotation':'0', 
                    'holiday':str(context.holiday),
                    'mqtt':str(context.mqtt_enabled)
                },  

                'ci_servers': {
                    'sections':''
                },

                'mqtt': {
                    'host':'0.0.0.0',
                    'port':'52129',
                    'now_playing_topic':str(context.mqtt_now_playing_topic),
                    'online_topic':str(context.mqtt_online_topic),
                    'marquee_topic':str(context.mqtt_marquee_topic)
                }
             }

    for index in range(len(context.fake_ci_servers)):
        world_ci_server = context.fake_ci_servers[index]
        config['ci_servers']['sections'] += '{},'.format(index)
        config[str(index)] = {'url':'http://0.0.0.0:{}'.format(world_ci_server.port)}

    config_helper.build_config(config)

