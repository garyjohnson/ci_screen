import time

from lettuce import *
import pqaut.client as pqaut

import features.support.config_helper as config_helper
import features.support.fake_ci_server as ci
    

@step(u'the CI server has projects:$')
def the_ci_server_has_projects(step):
    world.fake_ci_server = ci.FakeCIServer(port=1234)
    for project in step.hashes:
        world.fake_ci_server.add_project(project)

    world.fake_ci_server.start()

    config_helper.build_config({'ci_servers':{'sections':'test'}, 'test':{'url':'http://localhost:1234'}})

@step(u'the app is running$')
def the_app_is_running(step):
    world.launch_ci_screen()

@step(u'I see projects "([^"]*)"$')
def i_see_projects(step, projects):
    for project in projects.split(", "):
        pqaut.assert_is_visible(project)
