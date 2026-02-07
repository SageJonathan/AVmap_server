# GET /api/forecast/point/summary

Same as `/api/forecast/point` but returns a typed summary (danger days as numeric levels, area, dates, problem count, max danger level). Good for analysis and DB storage.

**Query:** `lat` (float), `long` (float), `lang` (optional, `"en"` \| `"fr"`).

## Return schema

**Content-Type:** `application/json`  
**Root:** **ForecastSummary** object.

### ForecastSummary

| Field               | Type            | Nullable | Description |
|---------------------|-----------------|----------|-------------|
| `product_id`        | string          | no       | Product id. |
| `area_id`           | string          | no       | Area id. |
| `area_name`         | string          | yes      | Area name. |
| `date_issued`       | string          | yes      | ISO 8601 (report issue time). |
| `valid_until`       | string          | yes      | ISO 8601 (validity end). |
| `title`             | string          | yes      | Forecast title. |
| `danger_days`       | array           | no       | Array of **DangerDay**. |
| `problem_count`     | integer         | no       | Number of avalanche problems. |
| `max_danger_level`   | integer \| null | yes      | Max danger 1–5 over all days/bands. |

### DangerDay (element of danger_days)

| Field          | Type            | Nullable | Description |
|----------------|-----------------|----------|-------------|
| `date`         | string          | no       | ISO date value. |
| `date_display`  | string          | yes      | e.g. "Saturday". |
| `alp`           | integer \| null | yes      | Alpine rating 1–5 (null = norating). |
| `tln`           | integer \| null | yes      | Treeline rating 1–5. |
| `btl`           | integer \| null | yes      | Below treeline rating 1–5. |

**Danger scale:** 1 = Low, 2 = Moderate, 3 = Considerable, 4 = High, 5 = Extreme.

## Example

```json
{
  "product_id": "fa96012c-18ee-444f-8265-8efc97b7f4e9_426b4bc4f761f2890921214b32ed3bf9f5de086f39b6f755296daf3a3048587e",
  "area_id": "426b4bc4f761f2890921214b32ed3bf9f5de086f39b6f755296daf3a3048587e",
  "area_name": "426b4bc4f761f2890921214b32ed3bf9f5de086f39b6f755296daf3a3048587e",
  "date_issued": "2026-02-07T00:00:00.000Z",
  "valid_until": "2026-02-10T00:00:00.000Z",
  "title": "Brazeau-Churchill-Cirrus-Wilson-Fryatt-Icefields-Maligne-Marmot-Miette Lake-Pyramid",
  "danger_days": [
    { "date": "2026-02-08T00:00:00Z", "date_display": "Saturday", "alp": 2, "tln": 2, "btl": 2 },
    { "date": "2026-02-09T00:00:00Z", "date_display": "Sunday",   "alp": 2, "tln": 2, "btl": 2 },
    { "date": "2026-02-10T00:00:00Z", "date_display": "Monday",   "alp": 1, "tln": 1, "btl": 1 }
  ],
  "problem_count": 1,
  "max_danger_level": 2
}
```

## DB use

- **Tables:** e.g. `forecast_summaries` (product_id PK, area_id, area_name, date_issued, valid_until, title, problem_count, max_danger_level); `forecast_danger_days` (product_id, date, date_display, alp, tln, btl) with composite key (product_id, date).
- **Indexes:** By area_id, date_issued/valid_until for time range queries; max_danger_level for filtering.
- **Joins:** product_id and area_id link to products and areas if stored separately.
