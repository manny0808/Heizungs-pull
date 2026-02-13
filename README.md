# Heizungs Pull Integration for Home Assistant

Native Home Assistant integration for monitoring heating system status via web scraping.

## Features

- **Binary Sensors**: Monitor heating actuators (on/off status)
- **Temperature Sensors**: Track various temperature readings
- **Automatic Discovery**: Automatically detects available sensors from data source
- **Configurable Polling**: Adjustable update interval
- **HACS Compatible**: Easy installation via HACS

## Installation

### Via HACS (Recommended)
1. Add this repository as a custom repository in HACS
2. Search for "Heizungs Pull" and install
3. Restart Home Assistant
4. Add integration via Configuration → Integrations

### Manual Installation
1. Copy the `custom_components/heizungs_pull` folder to your `custom_components` directory
2. Restart Home Assistant
3. Add integration via Configuration → Integrations

## Configuration

The integration requires:
- **URL**: The endpoint providing heating data (e.g., `http://heizung.lan.brunner-it.com/data.php`)
- **Update Interval**: How often to poll for updates (default: 120 seconds)

## Data Format

The integration expects data in the following format:
```
Temp_Name Value
Actor_Name @-1@  # -1 = ON, 0 = OFF
```

Example:
```
Temp_Kessel 45,2
Temp_Vorlauf 38,5
Heizung_Parterre @-1@
Pumpe_Holzkessel @0@
```

## Supported Sensors

### Binary Sensors (Actors)
- Heizung Parterre
- Heizung Keller  
- Heizung Dachwohnung
- Pumpe Holzkessel

### Temperature Sensors
All temperature readings starting with "Temp_" are automatically detected.

## Development

This integration uses:
- `aiohttp` for asynchronous HTTP requests
- Regular expressions for parsing the legacy data format
- Home Assistant's DataUpdateCoordinator for efficient polling

## License

MIT License