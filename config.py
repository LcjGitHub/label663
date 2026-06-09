import os
from dotenv import load_dotenv

load_dotenv()


def _get_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ('true', '1', 'yes', 'on')


def _get_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


APP_PORT = _get_int('APP_PORT', 8050)
DEBUG_MODE = _get_bool('DEBUG_MODE', True)
AUTO_REFRESH_INTERVAL = _get_int('AUTO_REFRESH_INTERVAL', 30)
REFRESH_RATE_LIMIT = _get_int('REFRESH_RATE_LIMIT', 5)
APP_HOST = os.getenv('APP_HOST', '127.0.0.1')


def get_config_summary():
    return {
        'APP_PORT': APP_PORT,
        'DEBUG_MODE': DEBUG_MODE,
        'AUTO_REFRESH_INTERVAL': AUTO_REFRESH_INTERVAL,
        'REFRESH_RATE_LIMIT': REFRESH_RATE_LIMIT,
        'APP_HOST': APP_HOST
    }
