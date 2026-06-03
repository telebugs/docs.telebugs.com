# Users

You can list, inspect, and manage team members via the REST API. You can also
control which users have access to which projects.

> **Note:** Listing users, updating roles, deactivating users, and managing
> project memberships all require admin access. Non-admin requests receive
> `403 Forbidden`.

## The User Object

```json
{
  "id": 42,
  "name": "Kyrylo",
  "email_address": "kyrylo@telebugs.com",
  "role": "admin",
  "active": true,
  "project_ids": [1, 2, 3],
  "created_at": "2025-02-07T12:00:00.000Z",
  "updated_at": "2025-02-07T12:00:00.000Z"
}
```

| Field          | Type    | Description                                      |
| -------------- | ------- | ------------------------------------------------ |
| `id`           | integer | Unique user ID                                   |
| `name`         | string  | Display name                                     |
| `email_address`| string  | Email address                                    |
| `role`         | string  | `admin` or `member`                              |
| `active`       | boolean | `true` for active accounts                       |
| `project_ids`  | array   | IDs of projects this user can access             |
| `created_at`   | string  | Creation timestamp (ISO 8601)                    |
| `updated_at`   | string  | Last update timestamp (ISO 8601)                 |

## List Users

Returns all active users (team members). Supports cursor-based pagination.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Pagination Parameters

| Parameter | Description                     | Default | Max |
| --------- | ------------------------------- | ------- | --- |
| `limit`   | Number of results to return     | 25      | 100 |
| `cursor`  | ID to start after (for next page) | —     | —   |

Example with pagination:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/users?limit=10&cursor=100" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Response shape:

```json
{
  "users": [ /* User objects */ ],
  "next_cursor": 87,
  "has_more": true
}
```

## Get a User

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/users/USER_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Response:

```json
{
  "user": { /* User object */ }
}
```

## Update a User

You can change a user's role. Only `role` is updatable.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/users/USER_ID \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{ "role": "admin" }'
```

- Setting `role` to `admin` automatically grants the user access to every project (with notifications enabled).
- Invalid roles return a validation error (422).

Response on success: the updated user object (wrapped in `user`).

## Deactivate a User

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/users/USER_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

This soft-deletes the user (sets `active` to `false`). Returns `204 No Content`.

Deactivated users cannot authenticate and are excluded from all listings.

## Project Users

Manage which users have access to a specific project.

All endpoints in this section require admin access and return `204 No Content` on success (except the list endpoint).

### List Users for a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Supports the same `limit` and `cursor` pagination parameters as the global users list.

Response:

```json
{
  "users": [ /* User objects (only those with access to the project) */ ],
  "next_cursor": 55,
  "has_more": false
}
```

### Add a User to a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/users \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "user_id": 123 }'
```

- `user_id` is required.
- The user must exist and be active.
- The operation is idempotent (adding a user who is already a member succeeds with 204).
- Returns `204 No Content` on success.
- Validation problems (missing user_id, user not found) return `422 Unprocessable Content` with Problem Details.

### Remove a User from a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/users/USER_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Removes the membership (if it exists). Idempotent. Returns `204 No Content`.

Removing a user from a project does not deactivate the user account.
