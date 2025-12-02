import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class GeocodingService:
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> bool:
        return -180 <= longitude <= 180 and -90 <= latitude <= 90

    @staticmethod
    def reverse_geocode(latitude: float, longitude: float) -> dict:
        # Get configuration from environment
        api_url = os.getenv("GEOCODING_API_URL", "https://nominatim.openstreetmap.org/reverse")
        api_key = os.getenv("GEOCODING_API_KEY")
        timeout = int(os.getenv("GEOCODING_TIMEOUT", "5"))
        
        # Build request parameters
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json"
        }
        
        # Build headers
        headers = {
            "User-Agent": "TrafficMonitoringService/1.0"
        }
        
        # Include API key if configured
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        try:
            # Make API request with timeout
            response = requests.get(
                api_url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Extract structured address components
            address = data.get("address", {})
            
            # Try to get city from various possible fields
            city = (
                address.get("city") or 
                address.get("town") or 
                address.get("village") or 
                address.get("municipality") or
                address.get("county") or
                None
            )
            
            # Try to get province/state
            province = (
                address.get("state") or 
                address.get("province") or 
                address.get("region") or
                None
            )
            
            return {
                "city": city,
                "province": province,
                "fulladdress": data.get("display_name")
            }
                
        except requests.exceptions.Timeout:
            logger.error(f"Geocoding API timeout for coordinates ({latitude}, {longitude})")
            return {"city": None, "province": None, "fulladdress": None}
        except requests.exceptions.HTTPError as e:
            logger.error(f"Geocoding API HTTP error for coordinates ({latitude}, {longitude}): {e}")
            return {"city": None, "province": None, "fulladdress": None}
        except requests.exceptions.RequestException as e:
            logger.error(f"Geocoding API request failed for coordinates ({latitude}, {longitude}): {e}")
            return {"city": None, "province": None, "fulladdress": None}
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse geocoding API response for coordinates ({latitude}, {longitude}): {e}")
            return {"city": None, "province": None, "fulladdress": None}
