"""
Geocoding service using OpenStreetMap's Nominatim.
Provides reverse geocoding (coordinates -> address) with fallback and caching.
"""

import time
from typing import Any

import requests

import location_cache

_USER_AGENT = 'WaterTracker/1.0 (civic app)'
_NOMINATIM_URL = 'https://nominatim.openstreetmap.org/reverse'
_TIMEOUT = 10
_LAST_REQUEST = 0


def _rate_limit() -> None:
    global _LAST_REQUEST
    now = time.time()
    elapsed = now - _LAST_REQUEST
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _LAST_REQUEST = time.time()


def reverse_geocode(lat: float, lng: float) -> dict[str, Any]:
    cache_key = f'{lat:.6f},{lng:.6f}'
    cached = location_cache.get(cache_key)
    if cached is not None:
        return cached

    result = _nominatim_reverse(lat, lng)
    location_cache.set(cache_key, result)
    return result


def _nominatim_reverse(lat: float, lng: float) -> dict[str, Any]:
    try:
        _rate_limit()
        resp = requests.get(
            _NOMINATIM_URL,
            params={
                'lat': str(lat),
                'lon': str(lng),
                'format': 'json',
                'addressdetails': '1',
                'zoom': '18',
            },
            headers={'User-Agent': _USER_AGENT},
            timeout=_TIMEOUT,
        )
        if resp.status_code != 200:
            return _fallback_result(lat, lng)

        data = resp.json()
        if 'error' in data or 'address' not in data:
            return _fallback_result(lat, lng)

        addr = data.get('address', {})
        return {
            'address': data.get('display_name', ''),
            'road': addr.get('road', ''),
            'ward': addr.get('ward', addr.get('suburb', '')),
            'city': addr.get('city', addr.get('town', addr.get('village', ''))),
            'district': addr.get('county', addr.get('state_district', '')),
            'state': addr.get('state', ''),
            'country': addr.get('country', ''),
            'postcode': addr.get('postcode', ''),
            'lat': lat,
            'lng': lng,
        }
    except (requests.RequestException, ValueError, KeyError):
        return _fallback_result(lat, lng)


def _fallback_result(lat: float, lng: float) -> dict[str, Any]:
    return {
        'address': f'{lat:.6f}, {lng:.6f}',
        'road': '',
        'ward': '',
        'city': '',
        'district': '',
        'state': '',
        'country': '',
        'postcode': '',
        'lat': lat,
        'lng': lng,
    }
