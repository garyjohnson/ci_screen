import copy
import os
import subprocess
import sys

from lettuce import *
import pqaut.client as pqaut

import features.support.fake_ci_server as ci
import features.support.config_helper as config_helper


world.app_path = "./main.py"
world.app_process = None

@world.absorb
def kill_ci_screen():
    if world.app_process:
        subprocess.Popen.kill(world.app_process)

def get_linux_faketime_path():
    paths = ['/usr/lib', '/usr/lib/arm-linux-gnueabihf', '/usr/lib/arm-linux-gnueabi']
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

@world.absorb
def launch_ci_screen(fake_time = None):
    if fake_time is not None:
        os.environ['FAKETIME'] = "@{}".format(fake_time)

    env_vars = copy.deepcopy(os.environ)
    if fake_time is not None:
        env_vars = add_faketime_to_env_vars(env_vars, fake_time)

    launch_kwargs = {   'env':env_vars, 
                        'stdout':subprocess.PIPE, 
                        'stderr':subprocess.PIPE, }
    if os.getenv("DEBUG"):
        del launch_kwargs['stdout']
        del launch_kwargs['stderr']

    world.app_process = subprocess.Popen([world.app_path, "--automation_server"], **launch_kwargs)

    pqaut.wait_for_automation_server()

@before.all
def before_all():
    world.port = 6500

@after.all
def after_all(obj):
    for ci_server in world.fake_ci_servers:
        ci_server.stop()

@before.each_scenario
def before_each(obj):
    kill_ci_screen()
    world.fake_ci_servers = []

@after.each_scenario
def after_each(obj):
    kill_ci_screen()
    config_helper.restore_config_file()

@world.absorb
def get_port():
    world.port += 1
    return world.port
