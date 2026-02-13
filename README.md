# Heizungs Pull - Home Assistant Integration

**Home Assistant integration for Siemens Logo SPS with Logo monitoring Software with data.php as source.**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

![Logo](https://raw.githubusercontent.com/manny0808/Heizungs-pull/main/logo.png)

*Dark Mode Logo - Optimized for modern interfaces*

A dynamic Home Assistant integration that automatically discovers all sensors and actors from a Siemens Logo PLC with Logo monitoring software's `data.php` interface. No configuration needed - just point it to your `data.php` URL!

## ✨ Features

- **Dynamic Discovery**: Automatically detects all temperature sensors and actors from `data.php`
- **No Configuration**: Zero configuration needed after initial setup
- **Real-time Updates**: Polls the PLC every 30 seconds (configurable)
- **HACS Compatible**: Easy installation via HACS
- **Complete Dashboard**: Ready-to-use Lovelace dashboard templates
- **Automation Ready**: Pre-built automations for heating control

## 📋 Requirements

- Home Assistant 2023.8 or newer
- Siemens Logo PLC with Logo monitoring software
- `data.php` endpoint accessible from Home Assistant
- HACS (recommended for easy installation)

## 🔧 Installation

### Via HACS (Recommended)

1. Open HACS → Integrations
2. Click "⋮" (three dots) → "Custom repositories"
3. Add repository: `https://github.com/manny0808/Heizungs-pull`
4. Select category: "Integration"
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/heizungs_pull` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## ⚙️ Configuration

1. Go to **Settings → Devices & Services**
2. Click **"Add Integration"**
3. Search for **"Heizungs Pull"**
4. Enter your `data.php` URL (e.g., `http://heizung.lan.brunner-it.com/data.php`)
5. Click **"Submit"**

The integration will automatically discover all available sensors and actors.

## 📊 Dashboard Templates

Complete dashboard examples are available in the `dashboard/` folder:

- **`heizung_dashboard.yaml`** - Complete Lovelace dashboard with all sensors
- **`mushroom_cards.yaml`** - Modern UI using Mushroom Cards (requires HACS)

### Quick Dashboard Example
```yaml
type: vertical-stack
cards:
  - type: glance
    title: Heizungs Status
    entities:
      - entity: sensor.heizung_parterre
        name: Parterre
      - entity: sensor.heizung_keller
        name: Keller
      - entity: sensor.heizung_dachwohnung
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

## 🤖 Automation Examples

Ready-to-use automations are available in the `automation/` folder:

- **`temperature_alarms.yaml`** - Temperature monitoring and alerts
- **`heating_logic.yaml`** - Heating control logic  
- **`energy_optimization.yaml`** - Energy saving automations

Copy these files to your Home Assistant `automations/` folder or include them in your `automation.yaml`.

### Quick Examples

**Temperature Alert:**
```yaml
automation:
  - alias: "Holzkessel zu heiß"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature_holzkessel
      above: 85
    action:
      service: notify.mobile_app
      data:
        message: "⚠️ Holzkessel zu heiß: {{ states('sensor.temperature_holzkessel') }}°C"
```

**Heating Control:**
```yaml
automation:
  - alias: "Heizung bei Kessel-Temperatur"
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
      entity_id: sensor.heizung_parterre
```

## 🏗️ Architecture

### Entity naming
- Temperatures: `sensor.temperature_{name_lowercase}` (e.g., `sensor.temperature_kessel`)
- Actor status: `sensor.{name_lowercase_with_underscores}` (e.g., `sensor.heizung_parterre`)

### Data Flow
```
Siemens Logo PLC → data.php → Heizungs Pull → Home Assistant
                    (JSON)        (Integration)    (Entities)
```

## 🔍 Troubleshooting

### Common Issues

1. **"Unable to connect"**: Check network connectivity to your PLC
2. **"No entities discovered"**: Verify `data.php` returns valid data
3. **Entities not updating**: Check polling interval in integration settings

### Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.heizungs_pull: debug
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This integration is not affiliated with or endorsed by Siemens. Use at your own risk.