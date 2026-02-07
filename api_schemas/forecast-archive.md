# GET /api/forecast/archive/{datetime_str}

Fetches all AVCAN forecasts that were available at the given datetime. Proxy to AVCAN `GET /forecasts/:lang/archive/:datetime`.

**Path:** `datetime_str` — e.g. ISO datetime or date `YYYY-MM-DD`.  
**Query:** `lang` (optional) — `"en"` \| `"fr"`, default `"en"`.

## Return schema

**Content-Type:** `application/json`  
**Root:** array of **Product** objects.

Same structure as [forecast-products.md](forecast-products.md): each element is a full **Product** (id, slug, url, type, area, report with dangerRatings, summaries, problems). The only difference is that the set of products reflects the archive at the requested point in time.

**Note:** The upstream AVCAN archive endpoint may return 400 or empty for invalid or future dates; handle non-200 or empty array in your client.

## Example

```json
[
  {
    "id": "...",
    "slug": "...",
    "url": "https://avalanche.ca/forecasts/...",
    "type": "avalancheforecast",
    "area": { "id": "...", "name": "...", "bbox": [...] },
    "report": {
      "dateIssued": "2026-02-01T00:00:00.000Z",
      "validUntil": "...",
      "dangerRatings": [ ... ],
      "problems": [ ... ]
    }
  }
]
```

## DB use

- Same as forecast-products: store each product by `id`; use `report.dateIssued` / `validUntil` for validity.
- **Time dimension:** Use `datetime_str` as the “as-of” time when inserting: e.g. column `archive_at` or `as_of_date` so you can query “forecasts as they were on date X”.
- Consider unique constraint on (product_id, archive_at) for historical snapshots.
