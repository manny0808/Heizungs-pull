# Heizungs Pull - Home Assistant Integration

**Generic Home Assistant integration for Siemens heating controllers with data.php interface.**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

## Features
- **Dynamic detection** of all actors and temperatures from data.php
- **No static configuration** - automatically adapts to your data.php
- **Complete dashboard templates** included (Standard + Mushroom Cards)
- **Automatic updates** every 2 minutes
- **Professional Material Design icons**
- **HACS ready** with version support

## Installation

### Via HACS (recommended)
1. Open **HACS → Integrations**
2. Click the three dots (⋮) → **Custom repositories**
3. Add repository URL: `https://github.com/manny0808/Heizungs-pull`
4. Category: **Integration**
5. Click **"Install"**
6. Restart Home Assistant

### Manual Installation
1. Copy the `custom_components/heizungs_pull` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration
1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **Heizungs Pull**
4. Enter the URL of your data.php (e.g., `http://heizung.lan.brunner-it.com/data.php`)
5. Click **Submit**

**That's it!** The integration will automatically detect all actors and temperatures from your data.php.

## Dynamic Detection

### How it works
The integration **dynamically detects** all sensors from your data.php:
- **All `Temp_*` values** become temperature sensors
- **All `*@-1@` or `*@0@` patterns** become binary sensors (actors)
- **No static lists** - works with any Siemens controller using this format

### Example data.php format
```
14:30:45
Temp_Kessel 45,2
Temp_Vorlauf 38,5
Temp_Ausen -2,25
Heizung Parterre@-1@
Heizung Keller@0@
Pumpe Holzkessel@-1@
```

### Entity naming
- Temperatures: `sensor.temperature_{name_lowercase}` (e.g., `sensor.temperature_kessel`)
- Binary sensors: `binary_sensor.{name_lowercase_with_underscores}` (e.g., `binary_sensor.heizung_parterre`)

## Dashboard Templates

### Standard Dashboard
`dashboard/heizung_dashboard.yaml` - Complete heating dashboard with:
- Status overview (binary sensors)
- Temperature gauges
- History graphs (24h)
- Weekly statistics
- Automation examples

### Modern UI with Mushroom Cards
`dashboard/mushroom_cards.yaml` - Modern dashboard using Mushroom Cards:
- Clean, card-based layout
- Color-coded temperature cards
- ApexCharts graphs
- Responsive design

### Quick Dashboard Example
```yaml
type: vertical-stack
cards:
  - type: glance
    title: Heizungs Status
    entities:
      - entity: binary_sensor.heizung_parterre
        name: Parterre
      - entity: binary_sensor.heizung_keller
        name: Keller
      - entity: binary_sensor.heizung_dachwohnung
        name: Dachwohnung
  - type: entities
    title: Temperaturen
    entities:
      - entity: sensor.temperature_ausen
        name: Außen
      - entity: sensor.temperature_holzkessel
        name: Holzkessel
      - entity: sensor.temperature_vorlauf
        name: Vorlauf
```

## Automation Examples

### Temperature Alerts
```yaml
automation:
  - alias: "Boiler too hot"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature_holzkessel
      above: 85
    action:
      service: notify.mobile_app
      data:
        message: "⚠️ Boiler too hot: {{ states('sensor.temperature_holzkessel') }}°C"
```

### Heating Logic
```yaml
automation:
  - alias: "Turn on heating when boiler is hot and outside is cold"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature_holzkessel
      above: 60
    condition:
      condition: numeric_state
      entity_id: sensor.temperature_ausen
      below: 15
    action:
      service: homeassistant.turn_on
      entity_id: binary_sensor.heizung_parterre
```

## For Developers

### Project Structure
```
custom_components/heizungs_pull/
├── __init__.py          # Main integration
├── config_flow.py       # Configuration UI
├── const.py             # Constants
├── coordinator.py       # Data update coordinator
├── manifest.json        # Integration metadata (v1.0.0)
├── parser.py            # Generic parser for data.php format
├── sensor.py            # Dynamic sensor creation
└── entity.py            # Base entity class
```

### Testing the Parser
```python
from custom_components.heizungs_pull.parser import parse_heizung_data

raw_data = """14:30:45
Temp_Kessel 45,2
Temp_Vorlauf 38,5
Heizung Parterre@-1@
Heizung Keller@0@"""

parsed = parse_heizung_data(raw_data)
print(parsed)
# Output: {'actors': {'Heizung Parterre': 'on', 'Heizung Keller': 'off'},
#          'temperatures': {'kessel': 45.2, 'vorlauf': 38.5},
#          'timestamp': '14:30:45'}
```

## Changelog

### v1.0.0
- First stable release
- Dynamic detection of all actors and temperatures
- Complete dashboard templates
- Professional Material Design icons
- HACS support with versioning

## Support
- **GitHub Issues:** [Report bugs or request features](https://github.com/manny0808/Heizungs-pull/issues)
- **Compatible with:** Any Siemens controller using the data.php format

## License
MIT License - see LICENSE file for details.