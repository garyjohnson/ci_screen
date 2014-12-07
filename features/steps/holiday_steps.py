from behave import *
import pqaut.client
import features.support.helpers as helpers

@given(u'I have holiday effects enabled')
def i_have_holiday_effects_enabled(context):
    context.holiday = True
    helpers.rebuild_config_file(context)

@then(u'I see snow')
def i_see_snow(context):
    pqaut.client.assert_is_visible('snow')

@then(u'I do not see snow')
def i_do_not_see_snow(context):
    pqaut.client.assert_is_not_visible('snow')
