"""
Simple file-based geocoding cache to avoid redundant Nominatim API calls.
Stores results as JSON keyed by "lat,lng" or address string.
"""

import json
import os
import time
from typing import Any

_CACHE_FILE = 'location_cache.json'
_CACHE_TTL = 86400 * 30


def _load_cache() -> dict[str, Any]:
    if not os.path.exists(_CACHE_FILE):
        return {}
    try:
        with open(_CACHE_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache: dict[str, Any]) -> None:
    try:
        with open(_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except OSError:
        pass


def get(key: str) -> dict[str, Any] | None:
    cache = _load_cache()
    entry = cache.get(key)
    if entry is None:
        return None
    if time.time() - entry.get('ts', 0) > _CACHE_TTL:
        return None
    return entry.get('data')


def set(key: str, data: dict[str, Any]) -> None:
    cache = _load_cache()
    cache[key] = {'data': data, 'ts': time.time()}
    _save_cache(cache)


def clear() -> None:
    if os.path.exists(_CACHE_FILE):
        os.remove(_CACHE_FILE)
