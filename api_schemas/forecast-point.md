# GET /api/forecast/point

Returns the AVCAN forecast that contains the given point (lat/long). Proxy to AVCAN `GET /forecasts/:lang/products/point?lat=&long=`.

**Query:**

| Param  | Type   | Required | Description |
|--------|--------|----------|-------------|
| `lat`  | float  | yes      | Latitude. |
| `long` | float  | yes      | Longitude. |
| `lang` | string | no       | `"en"` \| `"fr"`, default `"en"`. |

## Return schema

**Content-Type:** `application/json`  
**Root:** single **Product** object (same as [forecast-by-id.md](forecast-by-id.md) and one element of [forecast-products.md](forecast-products.md)).

If the point is not inside any forecast area, the API may return 404 or an error; document actual behavior when integrating.

## Example

Same structure as in [forecast-products.md](forecast-products.md): one product with `id`, `slug`, `url`, `type`, `area`, `report` (dangerRatings, summaries, problems).

## DB use

- Same as products: store by `id`; use for “forecast at this location” and then persist to products/areas/reports/danger_ratings/problems.
- For typed/summary-only storage, use [forecast-point-summary.md](forecast-point-summary.md) instead.
