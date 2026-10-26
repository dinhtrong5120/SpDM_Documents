---
name: spdm-db
description: Create, review, and harden database maintenance utilities for the SPDM Django backend, especially scripts that inspect or mutate MySQL data. Use for tools under utils/Tools, project-data cleanup, raw SQL, transactions, FK-aware deletion, dry runs, or PyCharm-run database scripts in the SPDM repository. Do not use for ordinary application queries that do not involve maintenance tooling or database safety.
---

# SPDM_DB

Build SPDM database tools that match the repository's conventions and make destructive behavior difficult to trigger accidentally.

## Inspect the Repository First

- Read the target utility and relevant schema, models, migrations, or SQL dumps before changing logic.
- Inspect `utils/update_member_list.py` and nearby utilities when choosing the integration style.
- Prefer `django.db.connection` for raw SQL and `transaction.atomic()` for mutations. Do not introduce SQLAlchemy solely for a standalone SPDM maintenance script when Django already owns the database configuration.
- When a file is intended to run directly, initialize Django before importing models or using the connection:

```python
if __name__ == "__main__":
    import os
    import sys
    from pathlib import Path

    import django

    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()
```

Keep the direct-run bootstrap compatible with importing the module from an already initialized Django process.

## Preserve Database Safety

- Never embed database usernames, passwords, hosts, or full connection URLs in source. Reuse `backend.settings` and `configs.ini` through Django.
- Treat delete, truncate, bulk update, schema changes, and production-like connections as destructive operations.
- Default maintenance tools to preview/dry-run. Require a separate execution flag for mutation.
- For scripts run with the PyCharm Run button, expose clearly named constants near the top, such as `RUN_PROJECT_IDS`, `RUN_EXECUTE = False`, and `RUN_ASSUME_YES = False`.
- Before mutation, display the database name, host, selected records, affected tables, and estimated row counts without displaying credentials.
- Require an exact interactive confirmation containing the database name and target IDs unless the user explicitly needs an audited non-interactive mode.
- Keep non-interactive confirmation bypasses disabled by default.
- Put the full mutation in one `transaction.atomic()` block. Raise on unexpected row counts or remaining references so Django rolls back the entire operation.
- Do not connect to a live database or execute a mutation merely to test generated code. Static checks, pure-function tests, mocks, and `--help` are safe defaults; request appropriate authorization before live execution.

## Write Correct Raw SQL

- Pass values through Django cursor parameters using `%s`; never interpolate user-provided values into SQL.
- Make insert/import utilities idempotent by default when re-running the same input is a normal workflow. Unless the user explicitly requests fail-on-duplicate or update/upsert behavior, report rows whose unique key already exists, skip them, and continue inserting the missing rows. Treat an all-existing input as a successful no-op without a traceback. Do not suppress unrelated validation, connection, constraint, or database errors.
- Dynamic table and column names cannot be parameterized. Derive them from trusted metadata or an explicit allowlist, validate them against a strict identifier pattern, then quote them.
- Generate the exact number of placeholders for lists and reject empty lists before constructing `IN (...)` clauses.
- Normalize IDs to positive integers, remove duplicates while retaining order, and verify every requested record exists before mutation.
- If a table has multiple project-reference columns, preserve all of them and combine their predicates rather than arbitrarily selecting one.

## Handle Relationships Deliberately

- Discover real direct relationships through `information_schema.KEY_COLUMN_USAGE`, restricted to `DATABASE()` and base tables.
- Keep legacy columns without declared FKs in a reviewed allowlist. Do not treat every column named `project_id` as safe to delete automatically.
- Determine child-before-parent order from FK dependencies; alphabetical table order is not a dependency order.
- Respect `CASCADE`, `RESTRICT`, `NO ACTION`, and `SET NULL` behavior. Let the transaction fail and roll back rather than disabling foreign-key checks.
- Inspect indirect relationships that do not contain the target key. Only add custom cleanup when the join uniquely identifies rows belonging to the target; otherwise report the schema ambiguity and recommend a proper FK or migration.
- Treat external resources such as S3 objects separately from database rows. Delete or queue them only after a successful database commit, using a recoverable workflow where possible.

## Verify Changes

- Run syntax parsing or compilation and the repository's available linter.
- Test pure helpers such as ID normalization, placeholder construction, identifier validation, and dependency ordering without opening a database connection.
- Confirm direct execution can locate `backend.settings` from the script path, because IDE working directories vary.
- State clearly whether a real database connection or deletion was performed.
- When reviewing rather than changing code, lead with concrete findings ordered by severity and cite exact files and lines.
