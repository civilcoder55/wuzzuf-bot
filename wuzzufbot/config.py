from wuzzufbot.utils import get_app_config_data

app_config_data = get_app_config_data()

WUZZUF_JOBS_URL = app_config_data.get('WUZZUF_JOBS_URL')

PUSHOVER_TOKEN = app_config_data.get('PUSHOVER_TOKEN')
PUSHOVER_USER = app_config_data.get('PUSHOVER_USER')
CONFIG_PATH = app_config_data.get('CONFIG_PATH')