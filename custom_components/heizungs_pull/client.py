"""HTTP client for Heizungs Pull integration."""

import aiohttp
import asyncio
from typing import Optional
import logging

_LOGGER = logging.getLogger(__name__)

class HeizungsClient:
    """Client to fetch data from Heizungs data.php endpoint."""
    
    def __init__(self, url: str, session: aiohttp.ClientSession):
        """Initialize the client.
        
        Args:
            url: URL to data.php endpoint
            session: aiohttp ClientSession
        """
        self._url = url
        self._session = session
    
    async def async_get_data(self) -> Optional[str]:
        """Fetch raw data from the endpoint.
        
        Returns:
            Raw text data or None if failed
        """
        try:
            async with self._session.get(self._url, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from %s: %s", self._url, err)
            return None
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching data from %s", self._url)
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error fetching data: %s", err)
            return None