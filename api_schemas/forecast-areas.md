# GET /api/forecast/areas

Fetches all current forecast areas as a GeoJSON Feature Collection. Proxy to AVCAN `GET /forecasts/:lang/areas`.

**Query:** `lang` (optional) — `"en"` \| `"fr"`, default `"en"`.

## Return schema

**Content-Type:** `application/json`  
**Root:** GeoJSON **FeatureCollection**.

| Field       | Type    | Description |
|-------------|---------|-------------|
| `type`      | string  | `"FeatureCollection"`. |
| `features`  | array   | Array of GeoJSON **Feature** objects. |

### Feature (GeoJSON Feature)

| Field        | Type   | Description |
|--------------|--------|-------------|
| `id`         | string | Feature/area id (hash). |
| `type`       | string | `"Feature"`. |
| `bbox`       | array  | `[minLon, minLat, maxLon, maxLat]`. |
| `geometry`   | object | GeoJSON **Geometry** (e.g. `MultiPolygon`). |
| `properties` | object | **Properties** (centroid, id). |

### Geometry

| Field         | Type   | Description |
|---------------|--------|-------------|
| `type`        | string | e.g. `"MultiPolygon"`. |
| `coordinates` | array  | MultiPolygon: array of rings; each ring is array of `[lon, lat]`. |

### Properties (nested)

| Field       | Type   | Description |
|-------------|--------|-------------|
| `centroid`  | array  | `[longitude, latitude]`. |
| `id`        | string | Same as feature `id`. |

## Example (truncated)

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "id": "ff27f89a78600ce8622e02e807bc89b31d7f1876832b9dc0ceab5b43cab072e5",
      "type": "Feature",
      "bbox": [ -137.1192801, 59.448169, -136.23459, 60.1426753 ],
      "geometry": {
        "type": "MultiPolygon",
        "coordinates": [ [ [ [ -137.1193, 60.0403 ], [ -137.1031, 60.0017 ], ... ] ] ]
      },
      "properties": {
        "centroid": [ -136.63255032559098, 59.79371165198136 ],
        "id": "ff27f89a78600ce8622e02e807bc89b31d7f1876832b9dc0ceab5b43cab072e5"
      }
    }
  ]
}
```

## DB use

- **Tables:** e.g. `areas` with columns: `id` (PK), `geometry` (PostGIS geometry or GeoJSON text), `bbox`, `centroid` (point or lon/lat), `properties` (JSONB if needed).
- **Spatial:** Store `geometry` for containment queries (point-in-polygon for “forecast at point”). Use `centroid` or `bbox` for map bounds and quick lookups.
- **Joins:** Area `id` matches `area.id` in products and metadata.
