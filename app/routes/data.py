"""
Routes that fetch AVCAN data (forecast for point, archive).
"""

from fastapi import APIRouter, HTTPException

from app.services.avcan import (
    fetch_archive,
    fetch_areas,
    fetch_forecast_for_id,
    fetch_forecast_for_point,
    fetch_metadata,
    fetch_products,
)

router = APIRouter(prefix="/api", tags=["data"])


@router.get("/forecast/products")
def get_forecast_products(lang: str = "en"):
    """
    Proxy: GET api.avalanche.ca/forecasts/:lang/products
    Fetches all current forecasts. Returns an array of forecasts. lang: en | fr.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        return fetch_products(lang=lang)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e


@router.get("/forecast/metadata")
def get_forecast_metadata(lang: str = "en"):
    """
    Proxy: GET api.avalanche.ca/forecasts/:lang/metadata
    Metadata about current products; high-level data useful for map display. lang: en | fr.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        return fetch_metadata(lang=lang)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e


@router.get("/forecast/areas")
def get_forecast_areas(lang: str = "en"):
    """
    Proxy: GET api.avalanche.ca/forecasts/:lang/areas
    Fetches all current areas as a GeoJSON feature collection. lang: en | fr.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        return fetch_areas(lang=lang)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e


@router.get("/forecast/id")
def get_forecast_for_id(id: str, lang: str = "en"):
    """
    Proxy: GET api.avalanche.ca/forecasts/:lang/products/:id
    Fetches the AVCAN forecast for the given product ID. lang: en | fr.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        return fetch_forecast_for_id(product_id=id, lang=lang)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e


@router.get("/forecast/point")
def get_forecast_for_point(lat: float, long: float, lang: str = "en"):
    """
    Fetch the AVCAN forecast that contains the given point (lat/long).
    Returns raw AVCAN JSON. Use /forecast/point/summary for a typed summary model.
    lang: 'en' or 'fr'.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        return fetch_forecast_for_point(lat=lat, long=long, lang=lang)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e


@router.get("/forecast/point/summary")
def get_forecast_for_point_summary(lat: float, long: float, lang: str = "en"):
    """
    Same as /forecast/point but returns a typed summary model: danger days (numeric levels),
    area, dates, problem count, and max danger level. Good for analysis and display.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        raw = fetch_forecast_for_point(lat=lat, long=long, lang=lang)
        product = parse_forecast_product(raw)
        summary = forecast_to_summary(product)
        return summary.model_dump()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e


@router.get("/forecast/archive/{datetime_str}")
def get_forecast_archive(datetime_str: str, lang: str = "en"):
    """
    Fetch all AVCAN forecasts that were available at the provided datetime.
    datetime_str: e.g. ISO datetime or date (YYYY-MM-DD).
    lang: 'en' or 'fr'.
    """
    if lang not in ("en", "fr"):
        raise HTTPException(status_code=400, detail="lang must be 'en' or 'fr'")
    try:
        return fetch_archive(lang=lang, datetime_str=datetime_str)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AVCAN fetch failed: {e!s}") from e
