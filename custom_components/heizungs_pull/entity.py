"""Base entity for Heizungs Pull integration."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, DEFAULT_NAME
from .coordinator import HeizungsDataUpdateCoordinator


class HeizungsEntity(CoordinatorEntity):
    """Base entity for Heizungs sensors."""
    
    def __init__(self, coordinator: HeizungsDataUpdateCoordinator):
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer="Custom",
            model="Heizungs System",
        )
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
        
        attrs = {}
        
        # Add timestamp if available
        if "timestamp" in self.coordinator.data and self.coordinator.data["timestamp"]:
            attrs["last_update"] = self.coordinator.data["timestamp"]
        
        return attrs