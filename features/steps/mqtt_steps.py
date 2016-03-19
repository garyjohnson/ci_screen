import json

from behave import *
import pqaut.client as pqaut

from features.support.wait_helpers import *
import features.support.helpers as helpers


@given(u'I have MQTT enabled')
def i_have_mqtt_enabled(context):
    context.mqtt_enabled = True
    helpers.rebuild_config_file(context)

@given(u'I do not have MQTT enabled')
def i_do_not_have_mqtt_enabled(context):
    context.mqtt_enabled = False
    helpers.rebuild_config_file(context)

@then(u'the app connects to MQTT')
def the_app_connects_to_mqtt(context):

    def app_connected_to_mqtt():
        test_clients = 1
        expected_app_clients = 1
        expected_clients = test_clients + expected_app_clients
        return context.mqtt_service.client_connected_count == expected_clients

    if not eventually(app_connected_to_mqtt, retries=24):
        raise Exception('Expected an MQTT test connection and an app connection, found {}'.format(context.mqtt_service.client_connected_count))

@then(u'the app does not connect to MQTT')
def the_app_does_not_connect_to_mqtt(context):

    def no_mqtt_clients():
        test_clients = 1
        expected_app_clients = 0
        expected_clients = test_clients + expected_app_clients
        return context.mqtt_service.client_connected_count == expected_clients

    if not consistently(no_mqtt_clients):
        raise Exception('Expected an MQTT test connection and no app connections, found {}'.format(context.mqtt_service.client_connected_count))

@given(u'now playing topic is set to "(?P<topic>[^"]*)"')
def now_playing_topic_is_set_to(context, topic):
    context.mqtt_now_playing_topic = topic
    helpers.rebuild_config_file(context)

@when(u'I publish now playing info to "(?P<topic>[^"]*)"')
def publish_now_playing_info_to(context, topic):
    for row in context.table:
        now_playing = {'song':row['song'], 'artist':row['artist'], 'album':row['album'], 'albumArt':row['album art']}
        context.mqtt_service.publish(topic, json.dumps(now_playing), retain=True)

@then(u'I see now playing info')
def see_now_playing_info(context):
    for row in context.table:
        pqaut.assert_is_visible(row['song'], 'song')
        pqaut.assert_is_visible(row['artist'], 'artist')
        pqaut.assert_is_visible(row['album art'], 'albumArt')
