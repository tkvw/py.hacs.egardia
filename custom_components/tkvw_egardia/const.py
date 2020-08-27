"""Constants for woonveilig."""
# Base component constants
NAME = "Egardia"
DOMAIN = "tkvw_egardia"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ISSUE_URL = "https://github.com/tkvw/py.hacs.tkvw_egardia/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
ALARM_CONTROL_PANEL = "alarm_control_panel"
BINARY_SENSOR = "binary_sensor"
PLATFORMS = [ALARM_CONTROL_PANEL, BINARY_SENSOR]


# Data
DATA_COORDINATOR = "coordinator"

# Configuration and options
CONF_ENABLED = "enabled"
CONF_INTERVAL_DISARMED = "interval_disarmed"
CONF_INTERVAL_ARMED = "interval_armed"
CONF_HOSTNAME = "hostname"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_NAME = "name"
CONF_DEVICE = "device"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_INTERVAL_DISARMED = 20
DEFAULT_INTERVAL_ARMED = 2
DEFAULT_DEVICE = "GATE-03"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
