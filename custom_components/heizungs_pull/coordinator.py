"""Data update coordinator for Heizungs Pull integration."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import HeizungsClient
from .parser import parse_heizung_data, filter_known_actors
from .const import DOMAIN, ACTOR_NAMES

_LOGGER = logging.getLogger(__name__)

class HeizungsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Heizungs data."""
    
    def __init__(self, hass: HomeAssistant, client: HeizungsClient, scan_interval: int):
        """Initialize the coordinator.
        
        Args:
            hass: Home Assistant instance
            client: HeizungsClient instance
            scan_interval: Update interval in seconds
        """
        self.client = client
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
    
    async def _async_update_data(self):
        """Fetch data from the endpoint and parse it.
        
        Returns:
            Parsed data dictionary
        """
        _LOGGER.debug("Fetching data from endpoint")
        raw_data = await self.client.async_get_data()
        
        if raw_data is None:
            _LOGGER.error("Failed to fetch data from Heizungs endpoint")
            raise UpdateFailed("Failed to fetch data from Heizungs endpoint")
        
        _LOGGER.debug("Raw data received (first 100 chars): %s", raw_data[:100])
        
        try:
            parsed_data = parse_heizung_data(raw_data)
            _LOGGER.debug("Parsed data keys: %s", list(parsed_data.keys()))
            _LOGGER.debug("Parsed timestamp: %s", parsed_data.get('timestamp'))
            
            # Filter to only known actors
            filtered_data = filter_known_actors(parsed_data, ACTOR_NAMES)
            
            _LOGGER.debug(
                "Fetched data: %d actors, %d temperatures",
                len(filtered_data["actors"]),
                len(filtered_data["temperatures"])
            )
            
            return filtered_data
            
        except Exception as err:
            raise UpdateFailed(f"Error parsing data: {err}") from err