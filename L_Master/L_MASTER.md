# L Item-List Master

## Deployment

Apply `migrations/2026110501_l_master.sql` once **before** deploying these backend endpoints and the RFL picker changes. The script adds `hierarchy_id INT NOT NULL DEFAULT 1`, `is_active` and the status-history table. Hierarchy ID 1 must exist. Existing L IDs and `related_se_parameter_id` remain unchanged. The migration has not been run against the configured `spdm` database as part of this code change.

Do not create a unique index on raw `unit_id` and `wp_id`: legacy master rows have different IDs with the same blank label. Existing duplicate data must be audited separately before choosing a database-wide constraint or cleanup. L Master writes are serialized by locking hierarchy ID 1 inside the save/status transaction; concurrent requests through these endpoints cannot both create the same normalized key. Legacy writers outside L Master do not acquire this lock and retain their existing behavior.

## API

All endpoints require authentication. Paths below are relative to `/api/` (and the configured sub-path).

- `GET rfl/l-parameter/?include_inactive=1`: rows plus Hierarchy/WP/Unit options and permissions. Without the flag, only active rows are returned.
- `POST rfl/l-parameter/`: atomic `{ "add": [...], "update": [...] }`. Each item has `hierarchy_id`, `wp_id`, `l_item`, `unit`; updates also require `id`. Only Hierarchy is required. Unit supports AutoComplete text and resolves to the existing normalized Unit or creates a Unit entry. Blank WP resolves to the existing NULL-labelled WP row because legacy RFL views use an inner JOIN. New items receive a stable ID from the existing ID allocator.
- `POST rfl/l-parameter/set-active/`: `{ "is_active": false, "items": [{ "id": 123, "reason": "..." }] }`. Reason is required per item, at most 100 characters. Restricted to Admin/MBSE/Project Owner, using the existing custom user-group tables.
- `GET rfl/l-parameter/123/history/`: status-only history, including operator, timestamp, reason and resulting status.

The business key is `(l_item, units.unit, wp.wp)`, with NULL/empty/whitespace normalized to `""`, trimmed and compared case-insensitively. Hierarchy is not part of the key. Duplicate conflicts return HTTP 409 with `{ "code": "duplicate", "conflict": { ...existing row... } }`. This applies to add/edit, inactive peers, in-request batch collisions and reactivation. Untouched legacy duplicate groups do not block unrelated changes.

The list returns both `related_se_parameter_id` and `has_related_se_parameter`. Only existing SE references set the boolean true. Phase 1 cannot change this relation. Updates touch only the four editable fields, and status actions only touch `is_active` plus status history.

RFL/TLM and RFL-TO picker queries exclude inactive L items. Existing project-view joins remain unchanged, so inactive items remain readable by old references. Scenario L options also exclude inactive items for new selections, while explicit existing IDs remain resolvable.

## Verification

Backend: `env/bin/python manage.py test rfl_list.test_l_master` uses isolated in-memory relational fixtures and does not access the configured MySQL databases. It covers normalized duplicates, inactive conflicts, batch conflicts, identity/SE preservation, required Hierarchy, read-only relation, permission checks and status history.

Frontend: `npm run test:l-master`, `npx tsc --noEmit --project tsconfig.app.json`, and `npm run build`.

Live MySQL migration/concurrency and full existing-project RFL/RFL-TO regression remain deployment checks; the isolated fixtures do not prove those checks.
