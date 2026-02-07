# GET /api/forecast/metadata

Metadata about current forecast products (high-level, useful for map display). Proxy to AVCAN `GET /forecasts/:lang/metadata`.

**Query:** `lang` (optional) — `"en"` \| `"fr"`, default `"en"`.

## Return schema

**Content-Type:** `application/json`  
**Root:** array of **MetadataItem** objects.

### MetadataItem

| Field            | Type   | Nullable | Description |
|------------------|--------|----------|-------------|
| `product`        | object | no       | **ProductRef** (slug, type, title, id, reportId). |
| `area`           | object | no       | **Area** with id, name, bbox. |
| `icons`          | array  | no       | **Icon** objects (rating graphics over time). |
| `centroid`       | object | yes      | `longitude`, `latitude` (number). |
| `url`            | string | yes      | Human-readable forecast URL. |
| `owner`          | object | yes      | `value`, `display`, `isExternal`, `url`. |
| `highestDanger`  | object | yes      | `value`, `display`, `colour` (e.g. "yellow"). |

### ProductRef (nested)

| Field       | Type   | Description |
|-------------|--------|-------------|
| `slug`      | string | Product slug. |
| `type`      | string | e.g. `"avalancheforecast"`. |
| `title`     | string | Area/forecast title. |
| `id`        | string | Product id. |
| `reportId`  | string | Report id. |

### Icon (nested)

| Field      | Type   | Description |
|------------|--------|-------------|
| `type`     | string | e.g. `"ratings"`. |
| `from`     | string | ISO datetime. |
| `to`       | string | ISO datetime. |
| `ratings`  | object | `alp`, `tln`, `btl` — string values (e.g. "moderate"). |
| `graphic`  | object | `id`, `url`, `alt`. |

## Example (truncated)

```json
[
  {
    "product": {
      "slug": "4d81ab95-0a72-4647-946c-78de31cdfba8_03eb3e06...",
      "type": "avalancheforecast",
      "title": "Chic-Chocs",
      "id": "4d81ab95-0a72-4647-946c-78de31cdfba8_03eb3e06...",
      "reportId": "4d81ab95-0a72-4647-946c-78de31cdfba8_03eb3e06..."
    },
    "area": {
      "id": "03eb3e06c31ffda095ce133e8c6974197efdccd29c7723d078ef27742ff6a762",
      "name": "Chic-Chocs",
      "bbox": [ -66.2457, 48.7669, -65.9819, 49.051 ]
    },
    "icons": [
      {
        "type": "ratings",
        "from": "0001-01-01T00:00:00Z",
        "to": "2026-02-07T22:30:00Z",
        "ratings": { "alp": "moderate", "tln": "low", "btl": "low" },
        "graphic": { "id": "moderate-low-low", "url": "https://assets.avalanche.ca/...", "alt": "" }
      }
    ],
    "centroid": { "longitude": -66.08685907369768, "latitude": 48.90968671256848 },
    "url": "https://avalanche.ca/en/forecasts/...",
    "owner": { "value": "avalanche-quebec", "display": "Avalanche Québec", "isExternal": false, "url": "..." },
    "highestDanger": { "value": "moderate", "display": "2 - Moderate", "colour": "yellow" }
  }
]
```

## DB use

- **Tables:** e.g. `metadata` or `forecast_metadata` with product id, area id, title, bbox, centroid, highest_danger, owner, url.
- **Keys:** `product.id` as primary key; link to full products/areas if stored.
- **Map display:** Use `centroid`, `bbox`, `area.name`, `highestDanger`, `icons` for list/map views without loading full reports.
