import behave
import logging

import features.support.helpers as helpers
import features.support.config_helper as config_helper
import features.support.mqtt_service as mqtt_service


behave.use_step_matcher("re")
logging.getLogger("requests").setLevel(logging.ERROR)

def before_all(context):
    context.config.setup_logging()
    context.mqtt_service = mqtt_service.MqttService()
    context.mqtt_service.start()

def before_scenario(context, scenario):
    context.app_path = "./main.py"
    context.app_process = None
    context.poll_rate = 10
    context.dev_null = None
    context.fake_ci_servers = []
    context.holiday = False
    context.mqtt_enabled = False
    context.mqtt_now_playing_topic = ''
    helpers.rebuild_config_file(context)

def after_scenario(context, scenario):
    helpers.kill_ci_screen(context)
    config_helper.restore_config_file()
    for ci_server in context.fake_ci_servers:
        ci_server.stop()

def after_all(context):
    context.mqtt_service.stop()
