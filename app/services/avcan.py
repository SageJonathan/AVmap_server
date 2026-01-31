"""
AVCAN (Avalanche Canada) API client.
"""

import requests
from typing import Any

BASE_URL = "https://api.avalanche.ca"


def _get_url(path: str) -> str:
    return f"{BASE_URL}{path}"


def fetch_products(lang: str = "en") -> Any:
    """
    Fetch all current forecasts. Returns an array of forecasts.
    GET /forecasts/:lang/products
    """
    if lang not in ("en", "fr"):
        raise ValueError("lang must be 'en' or 'fr'")
    path = f"/forecasts/{lang}/products"
    response = requests.get(_get_url(path), timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_metadata(lang: str = "en") -> Any:
    """
    Fetch metadata about current products. High-level product data, useful for map display.
    GET /forecasts/:lang/metadata
    """
    if lang not in ("en", "fr"):
        raise ValueError("lang must be 'en' or 'fr'")
    path = f"/forecasts/{lang}/metadata"
    response = requests.get(_get_url(path), timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_areas(lang: str = "en") -> Any:
    """
    Fetch all current areas as a GeoJSON feature collection.
    GET /forecasts/:lang/areas
    """
    if lang not in ("en", "fr"):
        raise ValueError("lang must be 'en' or 'fr'")
    path = f"/forecasts/{lang}/areas"
    response = requests.get(_get_url(path), timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_forecast_for_point(lat: float, long: float, lang: str = "en") -> Any:
    """
    Fetch the forecast that contains the given point (lat/long).
    GET /forecasts/:lang/products/point?lat=&long=
    """
    if lang not in ("en", "fr"):
        raise ValueError("lang must be 'en' or 'fr'")
    path = f"/forecasts/{lang}/products/point"
    url = _get_url(path)
    response = requests.get(url, params={"lat": lat, "long": long}, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_forecast_for_id(product_id: str, lang: str = "en") -> Any:
    """
    Fetch the AVCAN forecast for the given product ID.
    GET /forecasts/:lang/products/:id
    """
    if lang not in ("en", "fr"):
        raise ValueError("lang must be 'en' or 'fr'")
    path = f"/forecasts/{lang}/products/{product_id}"
    response = requests.get(_get_url(path), timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_archive(lang: str, datetime_str: str) -> Any:
    """
    Fetch all forecasts that were available at the provided datetime.
    GET /forecasts/:lang/archive/:datetime
    """
    if lang not in ("en", "fr"):
        raise ValueError("lang must be 'en' or 'fr'")
    path = f"/forecasts/{lang}/archive/{datetime_str}"
    response = requests.get(_get_url(path), timeout=30)
    response.raise_for_status()
    return response.json()
