# GET /api/forecast/id

Fetches the AVCAN forecast for a given product ID. Proxy to AVCAN `GET /forecasts/:lang/products/:id`.

**Query:**

| Param  | Type   | Required | Description |
|--------|--------|----------|-------------|
| `id`   | string | yes      | Product id (e.g. from /api/forecast/products or metadata). |
| `lang` | string | no       | `"en"` \| `"fr"`, default `"en"`. |

## Return schema

**Content-Type:** `application/json`  
**Root:** single **Product** object (same shape as one element of `/api/forecast/products`).

See [forecast-products.md](forecast-products.md) for the full **Product** schema (id, slug, url, type, area, report with dangerRatings, summaries, problems).

## Example (truncated)

```json
{
  "id": "fa96012c-18ee-444f-8265-8efc97b7f4e9_426b4bc4f761f2890921214b32ed3bf9f5de086f39b6f755296daf3a3048587e",
  "slug": "fa96012c-18ee-444f-8265-8efc97b7f4e9_...",
  "url": "https://avalanche.ca/forecasts/...",
  "type": "avalancheforecast",
  "area": { "id": "426b4bc4...", "name": "...", "bbox": null },
  "report": {
    "dateIssued": "2026-02-07T00:00:00.000Z",
    "validUntil": "2026-02-10T00:00:00.000Z",
    "dangerRatings": [ ... ],
    "problems": [ ... ]
  }
}
```

## DB use

- Same as [forecast-products.md](forecast-products.md): one product per response; upsert by `id` into products/reports/areas/danger_ratings/problems tables.
