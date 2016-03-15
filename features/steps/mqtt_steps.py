from behave import *
import pqaut.client

from features.support.wait_helpers import *
import features.support.helpers as helpers


@given(u'I do not have MQTT enabled')
def i_do_not_have_mqtt_enabled(context):
    context.mqtt_enabled = False
    helpers.rebuild_config_file(context)

@then(u'the app does not connect to MQTT')
def the_app_does_not_connect_to_mqtt(context):

    def no_mqtt_clients():
        test_clients = 1
        expected_app_clients = 0
        expected_clients = test_clients + expected_app_clients
        return context.mqtt_service.client_connected_count == expected_clients

    if not consistently(no_mqtt_clients):
        raise Exception('Expected an MQTT test connection and no app connections, found {}'.format(context.mqtt_service.client_connected_count))
