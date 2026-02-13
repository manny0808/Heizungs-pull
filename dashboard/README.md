# Dashboard Cards & Lovelace Examples

This directory contains Lovelace dashboard examples and custom cards for the Heizungs Pull integration.

## Quick Start

Copy the YAML examples from below into your Lovelace dashboard.

## Card Examples

### 1. Basic Heating Overview Card
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
      - entity: binary_sensor.pumpe_heizung
        name: Heizung
      - entity: binary_sensor.pumpe_holzkessel
        name: Holzkessel
  - type: entities
    title: Temperaturen
    entities:
      - entity: sensor.temperature_ausen
        name: Außen
      - entity: sensor.temperature_holzkessel
        name: Holzkessel
      - entity: sensor.temperature_vorlauf
        name: Vorlauf
      - entity: sensor.temperature_boiler_mitte
        name: Boiler Mitte
      - entity: sensor.temperature_boiler_unten
        name: Boiler Unten
```

### 2. Heating Control Panel
```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # 🔥 Heizungs-Steuerung
      **Letztes Update:** {{ states('sensor.heizungs_pull_last_update') }}
  - type: horizontal-stack
    cards:
      - type: button
        entity: binary_sensor.heizung_parterre
        icon: mdi:radiator
        show_name: true
        show_state: true
        tap_action:
          action: more-info
      - type: button
        entity: binary_sensor.heizung_keller
        icon: mdi:home-floor-basement
        show_name: true
        show_state: true
        tap_action:
          action: more-info
      - type: button
        entity: binary_sensor.heizung_dachwohnung
        icon: mdi:home-roof
        show_name: true
        show_state: true
        tap_action:
          action: more-info
  - type: gauge
    entity: sensor.temp_kessel
    name: Kessel Temperatur
    min: 0
    max: 100
    severity:
      green: 0
      yellow: 60
      red: 80
```

### 3. Temperature History Card
```yaml
type: vertical-stack
cards:
  - type: history-graph
    title: Temperaturen Verlauf (24h)
    hours_to_show: 24
    entities:
      - entity: sensor.temp_aussen
        name: Außen
      - entity: sensor.temp_kessel
        name: Kessel
      - entity: sensor.temp_vorlauf
        name: Vorlauf
      - entity: sensor.temp_ruecklauf
        name: Rücklauf
  - type: statistics-graph
    entities:
      - sensor.temp_aussen
      - sensor.temp_kessel
    period:
      calendar:
        period: day
        offset: -7
    stat_types:
      - mean
      - min
      - max
```

## Complete Dashboard Example

Create a new dashboard tab with this YAML:

```yaml
views:
  - title: Heizung
    icon: mdi:radiator
    cards:
      - type: custom:mushroom-title-card
        title: Heizungs Monitoring
        subtitle: Heizungs Pull Integration
      - type: custom:mushroom-entity-card
        entity: binary_sensor.heizung_parterre
        name: Parterre Heizung
        icon: mdi:radiator
        layout: horizontal
        fill_container: true
        primary_info: name
        secondary_info: state
      - type: custom:mushroom-entity-card
        entity: binary_sensor.heizung_keller
        name: Keller Heizung
        icon: mdi:home-floor-basement
        layout: horizontal
        fill_container: true
        primary_info: name
        secondary_info: state
      - type: custom:apexcharts-card
        header:
          title: Temperaturen
        graph_span: 24h
        series:
          - entity: sensor.temp_kessel
            name: Kessel
            color: '#ff6b00'
          - entity: sensor.temp_vorlauf
            name: Vorlauf
            color: '#2196f3'
          - entity: sensor.temp_ruecklauf
            name: Rücklauf
            color: '#4caf50'
```

## Custom Card (Optional)

If you want a dedicated custom card, see `custom_card/` directory.

## Installation

1. Copy the YAML code into your Lovelace dashboard
2. Adjust entity names if needed
3. Save and refresh

## Tips

- Use **Mushroom Cards** for modern UI
- Use **ApexCharts Card** for beautiful graphs
- Create **separate tabs** for overview, history, and control
- Add **automations** based on temperature thresholds