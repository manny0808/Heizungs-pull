"""Constants for Heizungs Pull integration."""

DOMAIN = "heizungs_pull"
DEFAULT_NAME = "Heizungs Pull"
DEFAULT_SCAN_INTERVAL = 120  # seconds

CONF_URL = "url"
CONF_SCAN_INTERVAL = "scan_interval"

# Actor names (as they appear in data.php)
ACTOR_NAMES = [
    "Heizung Parterre",
    "Heizung Keller",
    "Heizung Dachwohnung",
    "Pumpe Holzkessel"
]

# Temperature prefixes
TEMP_PREFIX = "Temp_"

# Data parsing constants
ACTOR_ON_VALUE = "-1"
ACTOR_OFF_VALUE = "0"