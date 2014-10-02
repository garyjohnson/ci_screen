import time

from lettuce import *
import pqaut.client as pqaut

import features.support.config_helper as config_helper
import features.support.fake_ci_server as ci
    

@step(u'the CI server has projects:$')
def the_ci_server_has_projects(step):
    for project in step.hashes:
        world.fake_ci_server.projects.append(project)

    config_helper.build_config({'ci_servers':{'sections':'test'}, 'test':{'url':'http://localhost:1234'}})

@step(u'the app is running$')
def the_app_is_running(step):
    world.launch_ci_screen()

@step(u'I see projects "([^"]*)"$')
def i_see_projects(step, projects):
    for project in projects.split(", "):
        pqaut.assert_is_visible(project)

@step(u'I see successful projects "([^"]*)"')
def i_see_successful_projects(step, projects):
    for project in projects.split(", "):
        pqaut.assert_is_visible(project, 'successful_project')

@step(u'I see failed projects "([^"]*)"')
def i_see_failed_projects(step, projects):
    for project in projects.split(", "):
        pqaut.assert_is_visible(project, 'failed_project')
