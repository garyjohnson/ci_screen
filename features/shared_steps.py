from lettuce import step, world
import pqaut.client as pqaut

import features.support.helpers as helpers
import features.support.fake_ci_server as ci
import features.support.config_helper as config_helper


@step(u'I have a CI server with projects:$')
def the_ci_server_has_projects(step):
    port = world.get_port()
    ci_server = ci.FakeCIServer(port=port)
    ci_server.start()
    for project in step.hashes:
        ci_server.projects.append(project)
    world.fake_ci_servers.append(ci_server)

    config = {'general':{'poll_rate_seconds':'10'}, 'ci_servers':{'sections':''}}
    for index in range(len(world.fake_ci_servers)):
        world_ci_server = world.fake_ci_servers[index]
        config['ci_servers']['sections'] += '{},'.format(index)
        config[str(index)] = {'url':'http://localhost:{}'.format(world_ci_server.port)}

    config_helper.build_config(config)

@step(u'the app is running$')
def the_app_is_running(step):
    world.launch_ci_screen()

@step(u'the app is running at "([^"]*)"$')
def the_app_is_running_at(step, time):
    local_time_string = helpers.get_local_time_string(time)
    world.launch_ci_screen(local_time_string)

@step(u'I see "([^"]*)"$')
def i_see(step, text):
    pqaut.assert_is_visible(text)
