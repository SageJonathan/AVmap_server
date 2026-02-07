"""
Typed summary of an AVCAN forecast product for analysis and DB storage.
"""

from typing import Any, Optional

from pydantic import BaseModel

# North American danger scale: low=1, moderate=2, considerable=3, high=4, extreme=5
RATING_TO_NUMERIC = {
    "low": 1,
    "moderate": 2,
    "considerable": 3,
    "high": 4,
    "extreme": 5,
    "norating": None,
}


class DangerDay(BaseModel):
    """Danger ratings for one date (one per elevation band)."""

    date: str  # ISO date value
    date_display: Optional[str] = None
    alp: Optional[int] = None  # Alpine 1-5
    tln: Optional[int] = None  # Treeline 1-5
    btl: Optional[int] = None  # Below treeline 1-5


class ForecastSummary(BaseModel):
    """Summary of a forecast product for display and DB."""

    product_id: str
    area_id: str
    area_name: Optional[str] = None
    date_issued: Optional[str] = None
    valid_until: Optional[str] = None
    title: Optional[str] = None
    danger_days: list[DangerDay] = []
    problem_count: int = 0
    max_danger_level: Optional[int] = None  # 1-5 over all days/bands


def _rating_value_to_numeric(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    return RATING_TO_NUMERIC.get(value.lower())


def parse_forecast_product(raw: Any) -> dict[str, Any]:
    """Normalize raw AVCAN product JSON for summary extraction."""
    return raw if isinstance(raw, dict) else {}


def forecast_to_summary(product: dict[str, Any]) -> ForecastSummary:
    """Build a ForecastSummary from a parsed product dict."""
    product_id = product.get("id") or product.get("slug") or ""
    area = product.get("area") or {}
    area_id = area.get("id") or ""
    area_name = area.get("name")
    report = product.get("report") or {}
    date_issued = report.get("dateIssued")
    valid_until = report.get("validUntil")
    title = report.get("title")

    danger_days: list[DangerDay] = []
    max_level: Optional[int] = None
    for day in report.get("dangerRatings") or []:
        date_val = (day.get("date") or {}).get("value") or ""
        date_display = (day.get("date") or {}).get("display")
        ratings = day.get("ratings") or {}
        alp = _rating_value_to_numeric((ratings.get("alp") or {}).get("rating", {}).get("value"))
        tln = _rating_value_to_numeric((ratings.get("tln") or {}).get("rating", {}).get("value"))
        btl = _rating_value_to_numeric((ratings.get("btl") or {}).get("rating", {}).get("value"))
        for v in (alp, tln, btl):
            if v is not None and (max_level is None or v > max_level):
                max_level = v
        danger_days.append(
            DangerDay(
                date=date_val,
                date_display=date_display,
                alp=alp,
                tln=tln,
                btl=btl,
            )
        )

    problems = report.get("problems") or []
    problem_count = len(problems)

    return ForecastSummary(
        product_id=product_id,
        area_id=area_id,
        area_name=area_name,
        date_issued=date_issued,
        valid_until=valid_until,
        title=title,
        danger_days=danger_days,
        problem_count=problem_count,
        max_danger_level=max_level,
    )
