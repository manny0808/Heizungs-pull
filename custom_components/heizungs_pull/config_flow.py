"""Config flow for Heizungs Pull integration."""

from typing import Any, Dict, Optional
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL, CONF_URL, CONF_SCAN_INTERVAL

class HeizungsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Heizungs Pull."""
    
    VERSION = 1
    
    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Validate URL
            url = user_input[CONF_URL]
            if not url.startswith(("http://", "https://")):
                errors[CONF_URL] = "invalid_url"
            else:
                # Create entry
                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data=user_input
                )
        
        # Show form
        data_schema = vol.Schema({
            vol.Required(CONF_URL, default="http://heizung.lan.brunner-it.com/data.php"): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_int,
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return HeizungsOptionsFlow(config_entry)

class HeizungsOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Heizungs Pull."""
    
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Manage the options."""
        errors = {}
        
        if user_input is not None:
            # Validate scan interval
            if user_input[CONF_SCAN_INTERVAL] < 30:
                errors[CONF_SCAN_INTERVAL] = "interval_too_short"
            else:
                # Update options
                return self.async_create_entry(title="", data=user_input)
        
        # Show form with current values
        data_schema = vol.Schema({
            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            ): cv.positive_int,
        })
        
        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
        )