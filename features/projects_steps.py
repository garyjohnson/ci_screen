import time
import random

from lettuce import *
import pqaut.client as pqaut

import features.support.config_helper as config_helper
import features.support.fake_ci_server as ci
    

@step(u'I have a CI server with projects:$')
def the_ci_server_has_projects(step):
    port = world.get_port()
    ci_server = ci.FakeCIServer(port=port)
    ci_server.start()
    for project in step.hashes:
        ci_server.projects.append(project)
    world.fake_ci_servers.append(ci_server)

    config = {'ci_servers':{'sections':''}}
    for index in range(len(world.fake_ci_servers)):
        world_ci_server = world.fake_ci_servers[index]
        config['ci_servers']['sections'] += '{},'.format(index)
        config[str(index)] = {'url':'http://localhost:{}'.format(world_ci_server.port)}

    config_helper.build_config(config)

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

@step(u'I do not see failed projects "([^"]*)"$')
def i_do_not_see_failed_projects(step, projects):
    for project in projects.split(", "):
        pqaut.assert_is_not_visible(project, 'failed_project')

@step(u'I do not see successful projects "([^"]*)"$')
def i_do_not_see_successful_projects(step, projects):
    for project in projects.split(", "):
        pqaut.assert_is_not_visible(project, 'successful_project')
