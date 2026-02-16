"""Sensor platform for Heizungs Pull integration."""

import logging
from typing import Optional
from datetime import datetime

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, ACTOR_NAMES
from .coordinator import HeizungsDataUpdateCoordinator
from .entity import HeizungsEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Heizungs sensors from a config entry."""
    coordinator: HeizungsDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # Create binary sensors for actors dynamically
    # First update to get available actors
    await coordinator.async_config_entry_first_refresh()
    
    if coordinator.data and "actors" in coordinator.data:
        for actor_name in coordinator.data["actors"].keys():
            entities.append(HeizungsBinarySensor(coordinator, actor_name))
    
    # Create temperature sensors dynamically
    if coordinator.data and "temperatures" in coordinator.data:
        for temp_name in coordinator.data["temperatures"].keys():
            entities.append(HeizungsTemperatureSensor(coordinator, temp_name))
    
    # Create timestamp sensor (only if we have data)
    if coordinator.data:
        entities.append(HeizungsTimestampSensor(coordinator))
    else:
        _LOGGER.warning("Cannot create timestamp sensor: no coordinator data after first refresh")
    
    async_add_entities(entities)


class HeizungsBinarySensor(HeizungsEntity, BinarySensorEntity):
    """Binary sensor representing a Heizungs actor."""
    
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    
    def __init__(self, coordinator: HeizungsDataUpdateCoordinator, actor_name: str):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._actor_name = actor_name
        self._attr_name = actor_name
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{actor_name.lower().replace(' ', '_')}"
    
    @property
    def is_on(self) -> Optional[bool]:
        """Return true if the actor is on."""
        if not self.coordinator.data or "actors" not in self.coordinator.data:
            return None
        
        actor_state = self.coordinator.data["actors"].get(self._actor_name)
        return actor_state == "on" if actor_state else None
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data
            and "actors" in self.coordinator.data
            and self._actor_name in self.coordinator.data["actors"]
        )


class HeizungsTemperatureSensor(HeizungsEntity, SensorEntity):
    """Temperature sensor for Heizungs readings."""
    
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    
    def __init__(self, coordinator: HeizungsDataUpdateCoordinator, temp_name: str):
        """Initialize the temperature sensor."""
        super().__init__(coordinator)
        self._temp_name = temp_name
        self._attr_name = f"Temperature {temp_name.title()}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_temp_{temp_name}"
    
    @property
    def native_value(self) -> Optional[StateType]:
        """Return the temperature value."""
        if not self.coordinator.data or "temperatures" not in self.coordinator.data:
            return None
        
        return self.coordinator.data["temperatures"].get(self._temp_name)
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data
            and "temperatures" in self.coordinator.data
            and self._temp_name in self.coordinator.data["temperatures"]
        )


class HeizungsTimestampSensor(HeizungsEntity, SensorEntity):
    """Timestamp sensor for Heizungs data synchronization."""
    
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_name = "Heizungs Data Timestamp"
    
    def __init__(self, coordinator: HeizungsDataUpdateCoordinator):
        """Initialize the timestamp sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_timestamp"
    
    @property
    def native_value(self) -> Optional[datetime]:
        """Return the timestamp value as datetime object."""
        _LOGGER.debug("Timestamp sensor native_value called")
        
        if not self.coordinator.data:
            _LOGGER.warning("No coordinator data available")
            return None
        
        _LOGGER.debug("Coordinator data keys: %s", list(self.coordinator.data.keys()))
        
        timestamp = self.coordinator.data.get("timestamp")
        if timestamp is None:
            _LOGGER.warning("Timestamp is None in coordinator data")
            return None
        if not timestamp:
            _LOGGER.warning("Timestamp is empty in coordinator data: %s", timestamp)
            return None
        
        _LOGGER.debug("Raw timestamp: %s", timestamp)
        
        # Convert HH:MM:SS to datetime object for Home Assistant
        # We'll use today's date with the time from data.php
        from datetime import datetime, date, timezone
        try:
            # Parse time string
            time_parts = timestamp.split(':')
            if len(time_parts) == 3:
                hours, minutes, seconds = map(int, time_parts)
                # Create datetime with today's date
                today = date.today()
                # Create naive datetime (no timezone)
                dt = datetime(today.year, today.month, today.day, hours, minutes, seconds)
                # Make it timezone-aware (UTC)
                dt_utc = dt.replace(tzinfo=timezone.utc)
                _LOGGER.debug("Converted to datetime: %s", dt_utc)
                return dt_utc
        except (ValueError, AttributeError) as e:
            _LOGGER.warning("Failed to parse timestamp %s: %s", timestamp, e)
        
        _LOGGER.debug("Failed to convert timestamp, returning None")
        return None
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.coordinator.data
        )