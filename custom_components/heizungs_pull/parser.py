"""Parser for Heizungs data.php format."""

import re
from typing import Dict, Any
from .const import ACTOR_ON_VALUE, ACTOR_OFF_VALUE, TEMP_PREFIX

def parse_heizung_data(raw_text: str) -> Dict[str, Any]:
    """Parse raw text from data.php into structured data.
    
    Args:
        raw_text: Raw text response from data.php
        
    Returns:
        Dictionary with parsed data:
        {
            "actors": {
                "Heizung Parterre": "on",
                "Heizung Keller": "off",
                ...
            },
            "temperatures": {
                "kessel": 45.2,
                "vorlauf": 38.5,
                ...
            },
            "timestamp": "14:30:45"
        }
    """
    data = {
        "actors": {},
        "temperatures": {},
        "timestamp": None
    }
    
    # Extract timestamp (first line usually contains time)
    timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2})', raw_text)
    if timestamp_match:
        data["timestamp"] = timestamp_match.group(1)
    
    # Parse temperatures: Temp_Name Value
    temp_pattern = r'Temp_(\S+)\s+([-\d,]+)'
    temp_matches = re.findall(temp_pattern, raw_text)
    
    for name, value in temp_matches:
        # Convert comma to dot for float conversion
        value_clean = value.replace(',', '.')
        try:
            data["temperatures"][name.lower()] = float(value_clean)
        except ValueError:
            data["temperatures"][name.lower()] = value_clean
    
    # Parse actors: Name @Value@
    actor_pattern = r'([^#]+)@(-?\d+)@'
    actor_matches = re.findall(actor_pattern, raw_text)
    
    for name, value in actor_matches:
        name = name.strip()
        if value == ACTOR_ON_VALUE:
            data["actors"][name] = "on"
        elif value == ACTOR_OFF_VALUE:
            data["actors"][name] = "off"
        else:
            data["actors"][name] = "unknown"
    
    return data


def filter_known_actors(parsed_data: Dict[str, Any], known_actors: list) -> Dict[str, Any]:
    """Filter actors to only include known ones.
    
    Args:
        parsed_data: Parsed data from parse_heizung_data
        known_actors: List of known actor names (unused in dynamic mode)
        
    Returns:
        Filtered data with all actors (no filtering in dynamic mode)
    """
    # In dynamic mode, we return all actors
    # known_actors parameter is kept for backward compatibility
    return {
        "actors": parsed_data.get("actors", {}),
        "temperatures": parsed_data.get("temperatures", {}),
        "timestamp": parsed_data.get("timestamp")  # Can be None if not in data
    }