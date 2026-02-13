# Heizungs Pull

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![version_badge](https://img.shields.io/github/v/release/manny0808/Heizungs-pull)
![downloads_badge](https://img.shields.io/github/downloads/manny0808/Heizungs-pull/total)
![ha_version](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue)
![license](https://img.shields.io/github/license/manny0808/Heizungs-pull)

**Home Assistant integration for Siemens Logo SPS with Logo monitoring Software with data.php as source.**

![Logo](https://raw.githubusercontent.com/manny0808/Heizungs-pull/main/logo.png)

*Dark Mode Logo - Optimized for modern interfaces*

## Features
- **Dynamic detection** of all actors and temperatures from data.php
- **No static configuration** - automatically adapts to your data.php
- **Complete dashboard templates** included (Standard + Mushroom Cards)
- **Automatic updates** every 2 minutes
- **Professional Material Design icons**
- **HACS ready** with version support

## Installation
1. In HACS: **Add custom repository**
2. URL: `https://github.com/manny0808/Heizungs-pull`
3. Category: **Integration**
4. Install and restart Home Assistant

## Configuration
1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **Heizungs Pull**
4. Enter the URL of your data.php (e.g., `http://heizung.lan.brunner-it.com/data.php`)

**That's it!** The integration will automatically detect all actors and temperatures from your data.php.

## Dynamic Detection

### How it works
The integration **dynamically detects** all sensors from your data.php:
- **All `Temp_*` values** become temperature sensors
- **All `*@-1@` or `*@0@` patterns** become binary sensors (actors)
- **No static lists** - works with any Siemens controller using this format

### Entity naming
- Temperatures: `sensor.temperature_{name_lowercase}` (e.g., `sensor.temperature_kessel`)
- Binary sensors: `binary_sensor.{name_lowercase_with_underscores}` (e.g., `binary_sensor.heizung_parterre`)

## Dashboard Templates
The repository contains complete dashboard templates:
- `dashboard/heizung_dashboard.yaml` - Standard Dashboard with gauges, graphs, statistics
- `dashboard/mushroom_cards.yaml` - Modern UI with Mushroom Cards and ApexCharts

## Automation Examples
```yaml
automation:
  - alias: "Boiler too hot alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature_holzkessel
      above: 85
    action:
      service: notify.mobile_app
      data:
        message: "⚠️ Boiler too hot: {{ states('sensor.temperature_holzkessel') }}°C"
```

## Changelog
### v1.0.0
- First stable release
- Dynamic detection of all actors and temperatures
- Complete dashboard templates
- Professional Material Design icons
- HACS support with versioning

## Support
For issues or feature requests: [GitHub Issues](https://github.com/manny0808/Heizungs-pull/issues)

**Compatible with:** Any Siemens controller using the data.php format