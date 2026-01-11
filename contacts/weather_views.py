"""
Weather API integration for contacts application.

Integrates with:
1. OpenStreetMap Nominatim API - for geocoding city names to coordinates
2. Open-Meteo API - for fetching current weather data

Implements caching to reduce API requests.
"""

import requests
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

# API endpoints
NOMINATIM_API = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"

# Cache timeout in seconds (30 minutes)
CACHE_TIMEOUT = 1800


def get_city_coordinates(city_name):
    """
    Get latitude and longitude for a city using OpenStreetMap Nominatim API.
    
    Results are cached to reduce API calls.
    
    Args:
        city_name (str): Name of the city
        
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    # Check cache first
    cache_key = f"coords_{city_name.lower()}"
    cached_coords = cache.get(cache_key)
    if cached_coords:
        return cached_coords
    
    try:
        # Request to Nominatim API
        headers = {
            'User-Agent': 'ContactsApp/1.0'  # Nominatim requires User-Agent
        }
        params = {
            'q': city_name,
            'format': 'json',
            'limit': 1
        }
        
        response = requests.get(NOMINATIM_API, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            
            # Cache the result
            cache.set(cache_key, (lat, lon), CACHE_TIMEOUT)
            return lat, lon
        
        return None, None
        
    except Exception as e:
        logger.error(f"Error fetching coordinates for {city_name}: {str(e)}")
        return None, None


def get_weather_data(latitude, longitude):
    """
    Get current weather data for given coordinates using Open-Meteo API.
    
    Results are cached to reduce API calls.
    
    Args:
        latitude (float): Latitude
        longitude (float): Longitude
        
    Returns:
        dict: Weather data with temperature, humidity, wind_speed or None
    """
    # Check cache first
    cache_key = f"weather_{latitude}_{longitude}"
    cached_weather = cache.get(cache_key)
    if cached_weather:
        return cached_weather
    
    try:
        # Request to Open-Meteo API
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true',
            'hourly': 'relativehumidity_2m',
            'forecast_days': 1
        }
        
        response = requests.get(OPEN_METEO_API, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if 'current_weather' in data:
            current = data['current_weather']
            # Get current humidity from hourly data
            humidity = None
            if 'hourly' in data and 'relativehumidity_2m' in data['hourly']:
                humidity = data['hourly']['relativehumidity_2m'][0]
            
            weather_data = {
                'temperature': current.get('temperature'),
                'wind_speed': current.get('windspeed'),
                'humidity': humidity,
                'weather_code': current.get('weathercode')
            }
            
            # Cache the result (shorter timeout for weather - 15 minutes)
            cache.set(cache_key, weather_data, 900)
            return weather_data
        
        return None
        
    except Exception as e:
        logger.error(f"Error fetching weather for {latitude}, {longitude}: {str(e)}")
        return None


@require_http_methods(["GET"])
def get_weather(request, city):
    """
    API endpoint to get weather data for a city.
    
    Returns JSON with temperature, humidity, and wind speed.
    Implements caching to minimize API requests.
    
    Args:
        request: HTTP request
        city (str): City name
        
    Returns:
        JsonResponse: Weather data or error message
    """
    if not city:
        return JsonResponse({'error': 'City parameter is required'}, status=400)
    
    # Get coordinates
    lat, lon = get_city_coordinates(city)
    if lat is None or lon is None:
        return JsonResponse({
            'error': 'City not found',
            'city': city
        }, status=404)
    
    # Get weather data
    weather_data = get_weather_data(lat, lon)
    if weather_data is None:
        return JsonResponse({
            'error': 'Weather data not available',
            'city': city
        }, status=503)
    
    # Return formatted response
    return JsonResponse({
        'city': city,
        'coordinates': {
            'latitude': lat,
            'longitude': lon
        },
        'weather': {
            'temperature': weather_data.get('temperature'),
            'temperature_unit': '°C',
            'humidity': weather_data.get('humidity'),
            'humidity_unit': '%',
            'wind_speed': weather_data.get('wind_speed'),
            'wind_speed_unit': 'km/h'
        }
    })
