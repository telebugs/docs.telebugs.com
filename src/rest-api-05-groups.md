# Groups

Groups represent aggregated errors. You can list, filter, resolve, and mute them
via the API.

## List Groups for a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Filtering

You can filter groups using the following parameters:

| Parameter | Description                       | Example              |
| --------- | --------------------------------- | -------------------- |
| `status`  | `unresolved`, `resolved`, `muted` | `?status=unresolved` |
| `search`  | Search in error type/message      | `?search=Payment`    |
| `since`   | Groups that occurred after date   | `?since=2026-05-01`  |
| `until`   | Groups that occurred before date  | `?until=2026-05-20`  |

Example with filters:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups?status=unresolved&search=TypeError" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Resolve a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/resolve \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Unresolve a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/resolve \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Mute a Group

```
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Unmute a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/mute \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Bulk Resolve

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/bulk_resolve \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [123, 456, 789]}'
```

## Bulk Mute

```
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/bulk_mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [123, 456, 789]}'
```
