# Reports

Reports are individual error occurrences. You can list and retrieve reports
under a specific group.

## List Reports under a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Filtering

You can filter reports using these parameters:

| Parameter | Description                  | Example             |
| --------- | ---------------------------- | ------------------- |
| `since`   | Reports that occurred after  | `?since=2026-05-01` |
| `until`   | Reports that occurred before | `?until=2026-05-20` |

Example:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports?since=2026-05-01&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Reports support cursor-based pagination using `cursor` and return `next_cursor` + `has_more`.

## Get a Single Report

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports/REPORT_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```
