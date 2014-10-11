from lettuce import *
import pqaut.client as pqaut
    

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
