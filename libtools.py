# libtools.py
import os

def get_config_path(SCRIPT_FOLDER):
    xdg_config_home_dir = os.environ.get('XDG_CONFIG_HOME', '')
    home_dir = os.environ.get('HOME', '')
    path = ""
    if xdg_config_home_dir:
        path = os.path.join(xdg_config_home_dir, SCRIPT_FOLDER)
    elif home_dir:
        path = os.path.join(home_dir, '.config', SCRIPT_FOLDER)
    return path


def get_config_file_full_path(SCRIPT_FOLDER, CONFIG_FILENAME):
    return os.path.join(get_config_path(SCRIPT_FOLDER), CONFIG_FILENAME)
