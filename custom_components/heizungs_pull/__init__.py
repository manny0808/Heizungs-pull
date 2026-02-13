"""The Heizungs Pull integration."""

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_URL, CONF_SCAN_INTERVAL
import aiohttp

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .client import HeizungsClient
from .coordinator import HeizungsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Heizungs Pull from a config entry."""
    
    url = config_entry.data[CONF_URL]
    scan_interval = config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    
    # Create aiohttp session
    session = aiohttp.ClientSession()
    
    # Create client
    client = HeizungsClient(url, session)
    
    # Create coordinator
    coordinator = HeizungsDataUpdateCoordinator(hass, client, scan_interval)
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    
    # Listen for config entry updates
    config_entry.async_on_unload(
        config_entry.add_update_listener(async_update_options)
    )
    
    return True


async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
    
    if unload_ok:
        # Clean up coordinator and session
        coordinator: HeizungsDataUpdateCoordinator = hass.data[DOMAIN].pop(config_entry.entry_id)
        await coordinator.client._session.close()
    
    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)
    
    if config_entry.version == 1:
        # Future migration logic here
        pass
    
    return True