# GET /api/forecast/products

Fetches all current avalanche forecasts. Proxy to AVCAN `GET /forecasts/:lang/products`.

**Query:** `lang` (optional) — `"en"` \| `"fr"`, default `"en"`.

## Return schema

**Content-Type:** `application/json`  
**Root:** array of **Product** objects.

### Product

| Field   | Type   | Nullable | Description |
|---------|--------|----------|-------------|
| `id`    | string | no       | Unique product id (UUID-style composite). |
| `slug`  | string | no       | Same as `id` for URLs. |
| `url`   | string | no       | Human-readable forecast URL. |
| `type`  | string | no       | e.g. `"avalancheforecast"`. |
| `area`  | object | no       | **Area** (id, name, bbox). |
| `report`| object | no       | **Report** (forecast content). |

### Area (nested)

| Field   | Type    | Nullable | Description |
|---------|---------|----------|-------------|
| `id`    | string  | no       | Area identifier (hash). |
| `name`  | string  | yes      | Area name (can be hash if not resolved). |
| `bbox`  | [number] \| null | yes | `[minLon, minLat, maxLon, maxLat]` or null. |

### Report (nested)

| Field            | Type    | Nullable | Description |
|------------------|---------|----------|-------------|
| `id`             | string  | no       | Report id. |
| `forecaster`     | string  | yes      | e.g. "Parks Canada". |
| `dateIssued`     | string  | yes      | ISO 8601 datetime. |
| `validUntil`     | string  | yes      | ISO 8601 datetime. |
| `timezone`       | string  | yes      | IANA timezone. |
| `title`          | string  | yes      | Forecast title. |
| `highlights`     | string  | yes      | HTML snippet. |
| `confidence`     | object  | yes      | `rating.value`, `rating.display`. |
| `summaries`      | array   | yes      | Array of `{ type: { value, display }, content }`. |
| `dangerRatings`  | array   | yes      | **DangerRating** per day. |
| `problems`       | array   | yes      | **Problem** objects. |

### DangerRating (per day)

| Field     | Type   | Description |
|-----------|--------|-------------|
| `date`    | object | `value` (ISO date), `display` (e.g. "Saturday"). |
| `ratings` | object | `alp`, `tln`, `btl` — each `{ display, rating: { value, display } }`. |
|           |        | `value`: `"low"` \| `"moderate"` \| `"considerable"` \| `"high"` \| `"extreme"` \| `"norating"`. |

### Problem

| Field      | Type   | Description |
|------------|--------|-------------|
| `type`     | object | `value`, `display` (e.g. "Wet Loose"). |
| `comment`  | string | HTML. |
| `factors`  | array  | Optional factor objects. |

## Example (truncated)

```json
[
  {
    "id": "fa96012c-18ee-444f-8265-8efc97b7f4e9_426b4bc4f761f2890921214b32ed3bf9f5de086f39b6f755296daf3a3048587e",
    "slug": "fa96012c-18ee-444f-8265-8efc97b7f4e9_...",
    "url": "https://avalanche.ca/forecasts/...",
    "type": "avalancheforecast",
    "area": { "id": "426b4bc4...", "name": "...", "bbox": null },
    "report": {
      "id": "...",
      "forecaster": "Parks Canada",
      "dateIssued": "2026-02-07T00:00:00.000Z",
      "validUntil": "2026-02-10T00:00:00.000Z",
      "dangerRatings": [
        { "date": { "value": "2026-02-08T00:00:00Z", "display": "Saturday" },
          "ratings": { "alp": { "rating": { "value": "moderate", "display": "2 - Moderate" } }, ... }
        }
      ],
      "problems": [ ... ]
    }
  }
]
```

## DB use

- **Tables:** e.g. `products`, `areas`, `reports`, `danger_ratings`, `problems`, `summaries`.
- **Keys:** Use `id` (product) and `area.id` as primary/foreign keys. `report.dateIssued` / `validUntil` for validity range.
- **Danger scale:** Map `rating.value` to numeric 1–5 (low=1, moderate=2, considerable=3, high=4, extreme=5; norating=null).
