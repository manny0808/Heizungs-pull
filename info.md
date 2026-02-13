# Heizungs Pull

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Integration für Heizungs-Steuerung über data.php Schnittstelle.

## Features
- Liest Temperaturen von data.php
- Erkennt Aktoren-Status (Heizungen, Pumpen, Mischer)
- Automatische Aktualisierung alle 2 Minuten
- Komplette Dashboard-Vorlagen inklusive

## Installation
1. Über HACS → Custom repositories
2. URL: `https://github.com/manny0808/Heizungs-pull`
3. Kategorie: Integration
4. Installieren und Home Assistant neu starten

## Konfiguration
1. Gehe zu **Einstellungen → Geräte & Dienste**
2. Klicke **+ Integration hinzufügen**
3. Suche nach **Heizungs Pull**
4. Gib die URL deiner data.php ein (z.B. `http://heizung.lan.brunner-it.com/data.php`)

## Dashboard
Das Repository enthält komplette Dashboard-Vorlagen:
- `dashboard/heizung_dashboard.yaml` - Standard Dashboard
- `dashboard/mushroom_cards.yaml` - Modernes UI mit Mushroom Cards

## Unterstützte Sensoren
### Temperaturen
- Holzkessel
- Vorlauf
- Boiler Mitte
- Boiler Unten
- Außen

### Aktoren (Binary Sensors)
- Heizung Parterre
- Heizung Keller
- Heizung Dachwohnung
- Pumpe Heizung
- Pumpe Holzkessel
- Pumpe Solarkolektor
- Mischer offen/zu/AUF/ZU
- Pumpe Zirkulation
- Elektro HZ Mitte/Unten

## Changelog
### v1.0.0
- Erste stabile Version
- Komplette Integration mit Parser und Coordinator
- Professionelle Icons (Material Design)
- Dashboard-Vorlagen

## Support
Bei Problemen: [GitHub Issues](https://github.com/manny0808/Heizungs-pull/issues)