# GET /

Health/root endpoint.

## Return schema

**Content-Type:** `application/json`

| Field    | Type   | Description        |
|----------|--------|--------------------|
| `message` | string | Static message, e.g. `"Hello World"` |

## Example

```json
{
  "message": "Hello World"
}
```

## DB use

Single key-value; typically not stored in DB. Use for health checks only.
