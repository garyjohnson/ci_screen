from lettuce import step, world
import pqaut.client as pqaut

import features.support.helpers as helpers


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
