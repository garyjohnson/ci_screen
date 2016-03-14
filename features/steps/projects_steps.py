from behave import *
import pqaut.client
import features.support.helpers as helpers
    

@step(u'I see projects "(?P<projects>[^"]*)"')
def i_see_projects(context, projects):
    for project in projects.split(", "):
        pqaut.client.assert_is_visible(project, timeout=10)

@step(u'I do not see projects "(?P<projects>[^"]*)"')
def i_do_not_see_projects(context, projects):
    for project in projects.split(", "):
        pqaut.client.assert_is_not_visible(project, timeout=10)

@step(u'I see successful projects "(?P<projects>[^"]*)"')
def i_see_successful_projects(context, projects):
    for project in projects.split(", "):
        pqaut.client.assert_is_visible(project, 'successful_project', timeout=10)

@step(u'I see failed projects "(?P<projects>[^"]*)"')
def i_see_failed_projects(context, projects):
    for project in projects.split(", "):
        pqaut.client.assert_is_visible(project, 'failed_project', timeout=10)

@step(u'I do not see failed projects "(?P<projects>[^"]*)"')
def i_do_not_see_failed_projects(context, projects):
    for project in projects.split(", "):
        pqaut.client.assert_is_not_visible(project, 'failed_project', timeout=10)

@step(u'I do not see successful projects "(?P<projects>[^"]*)"')
def i_do_not_see_successful_projects(context, projects):
    for project in projects.split(", "):
        pqaut.client.assert_is_not_visible(project, 'successful_project', timeout=10)

@step(u'"(?P<above>[^"]*)" is above "(?P<below>[^"]*)"')
def is_above(context, above, below):
    helpers.assert_is_above(above, below)
