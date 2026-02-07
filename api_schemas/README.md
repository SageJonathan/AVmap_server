# API return schemas

These documents describe the JSON return shape of each API endpoint for use when loading data into the database.

**Giving an agent access to this data?** See [AGENT_ACCESS.md](AGENT_ACCESS.md) for options (API-only vs your own DB vs hybrid) and a recommended approach.

| Endpoint | Schema doc |
|----------|------------|
| Base url/api.avalanche.ca/
| `GET /` | [root.md](root.md) |
| `GET /api/forecast/products` | [forecast-products.md](forecast-products.md) |
| `GET /api/forecast/metadata` | [forecast-metadata.md](forecast-metadata.md) |
| `GET /api/forecast/areas` | [forecast-areas.md](forecast-areas.md) |
| `GET /api/forecast/id` | [forecast-by-id.md](forecast-by-id.md) |
| `GET /api/forecast/point` | [forecast-point.md](forecast-point.md) |
| `GET /api/forecast/point/summary` | [forecast-point-summary.md](forecast-point-summary.md) |
| `GET /api/forecast/archive/{datetime_str}` | [forecast-archive.md](forecast-archive.md) |
