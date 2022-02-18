import os
import shelve

import questionary


def _get_user_config_directory():
    """Returns a platform-specific root directory for user config settings."""
    if os.name == "nt":
        appdata = os.getenv("LOCALAPPDATA")
        if appdata:
            return appdata
        appdata = os.getenv("APPDATA")
        if appdata:
            return appdata
        return None
    # On non-windows, use XDG_CONFIG_HOME if set, else default to ~/.config.
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        return xdg_config_home
    return os.path.join(os.path.expanduser("~"), ".config")


def _get_app_config_path():
    """Returns exists app config settings directory."""
    user_config_directory = _get_user_config_directory()
    app_config_directory = os.path.join(user_config_directory, '.wuzzufparser')
    is_exist = os.path.exists(app_config_directory)

    if not is_exist:
        os.makedirs(app_config_directory)

    return os.path.join(user_config_directory, '.wuzzufparser', '.db')


def get_app_config_data():
    app_config_path = _get_app_config_path()
    with shelve.open(app_config_path) as db:
        try:
            WUZZUF_JOBS_URL = db['WUZZUF_JOBS_URL']
            PUSHOVER_TOKEN = db['PUSHOVER_TOKEN']
            PUSHOVER_USER = db['PUSHOVER_USER']
        except:
            WUZZUF_JOBS_URL = questionary.text("wuzzuf jobs url?").ask()
            db['WUZZUF_JOBS_URL'] = WUZZUF_JOBS_URL

            PUSHOVER_TOKEN = questionary.text("pushover token?").ask()
            db['PUSHOVER_TOKEN'] = PUSHOVER_TOKEN

            PUSHOVER_USER = questionary.text("pushover user?").ask()
            db['PUSHOVER_USER'] = PUSHOVER_USER

    return {
        'CONFIG_PATH': app_config_path,
        'WUZZUF_JOBS_URL': WUZZUF_JOBS_URL,
        'PUSHOVER_TOKEN': PUSHOVER_TOKEN,
        'PUSHOVER_USER': PUSHOVER_USER
    }
