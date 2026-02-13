"""Constants for Heizungs Pull integration."""

DOMAIN = "heizungs_pull"
DEFAULT_NAME = "Heizungs Pull"
DEFAULT_SCAN_INTERVAL = 120  # seconds

CONF_URL = "url"
CONF_SCAN_INTERVAL = "scan_interval"

# Actor names (as they appear in data.php) - kept for backward compatibility
# In dynamic mode, all actors from data.php are automatically detected
ACTOR_NAMES = [
    "Mischer offen",
    "Mischer zu",
    "Mischer AUF",
    "Mischer ZU",
    "Pumpe Zirkulation",
    "Heizung Parterre",
    "Heizung Keller",
    "Heizung Dachwohnung",
    "Pumpe Heizung",
    "Pumpe Solarkolektor",
    "Pumpe Holzkessel",
    "Elektro HZ Mitte",
    "Elekltro HZ Unten"
]

# Temperature prefixes
TEMP_PREFIX = "Temp_"

# Data parsing constants
ACTOR_ON_VALUE = "-1"
ACTOR_OFF_VALUE = "0"