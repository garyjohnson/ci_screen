import os
import shutil
from ConfigParser import SafeConfigParser


config_path = None
config_file = "ci_screen.cfg"
config_file_backup = config_file + ".backup"
bin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def _path_to(file):
    return os.path.join(bin_path, file)

def _set_config_settings(config_settings):
    config = SafeConfigParser()
    if os.path.isfile(_path_to(config_file)):
        config.read(_path_to(config_file))

    for group_name, group_settings in config_settings.items():
        if not config.has_section(group_name):
            config.add_section(group_name)

        for setting_name, setting_value in group_settings.items():
            if setting_value is None:
                config.remove_option(group_name, setting_name)
            else:
                config.set(group_name, setting_name, setting_value)

    with open(_path_to(config_file), 'w') as file:
        config.write(file)

def build_config(config_settings = {}):
    if os.path.isfile(_path_to(config_file)) and not os.path.isfile(_path_to(config_file_backup)):
        shutil.move(_path_to(config_file), _path_to(config_file_backup))

    _set_config_settings(config_settings)

def restore_config_file():
    if os.path.isfile(_path_to(config_file_backup)):
        shutil.move(_path_to(config_file_backup), _path_to(config_file))
