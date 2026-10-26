---
name: spdm-swagger
description: Create, update, review, or brainstorm drf_yasg Swagger documentation for APIs in the SPDM Django backend while following the repository's established swagger_docs.py form. Use for SPDM Swagger/OpenAPI endpoint requests; do not use for unrelated Django projects.
---

# SPDM Swagger

Follow the target app's existing `swagger_docs.py` conventions. Preserve the user's changes and avoid unrelated cleanup.

## Select the mode

- If the user asks to brainstorm, analyze, propose, or output Markdown, inspect the code and create or update a reviewable `.md` file only. Do not edit Python unless explicitly requested.
- If the user asks to create, add, implement, fix, or update Swagger, edit the relevant `swagger_docs.py`, import the decorator in the view when needed, attach it to the correct method, and verify the result.
- A short request such as `tạo swagger cho POST abc/` is sufficient. Resolve the endpoint and contract from the repository without asking for details that the source can answer.

## Inspect before writing

1. Resolve the URL through the root URL configuration and app `urls.py`.
2. Read the complete target view method, including every success and error return.
3. Trace serializers, helpers, tests, fixtures, and in-repository callers when they define request or response shape.
4. Inspect nearby Swagger definitions for the same view style and request type.
5. Derive method, authentication, parameters, request body, response status codes, data types, nullable behavior, and examples from evidence. Do not invent fields.

If a nested payload remains materially ambiguous after inspection, state the uncertainty in a brainstorm document. During implementation, ask one focused question only when choosing a shape would risk documenting the wrong contract.

## Required source form

Start each API block with the exact separator used by the repository:

```python
# =============================================================================================
# API <short endpoint name>

# 1. Định nghĩa request
...

# 2. Định nghĩa response
...

# 3. Tạo Decorator
...
```

Use the separator for every new API block. Keep request, response, and decorator in that order even when one part is empty; add a short comment such as `# Không có params` instead of silently removing the section.

Read [references/form.md](references/form.md) when writing or reviewing concrete Swagger code.

## Contract rules

- Give schemas endpoint-specific names. Never reuse misleading names copied from another API.
- Match `TYPE_OBJECT`, `TYPE_ARRAY`, item schemas, nested properties, and HTTP status codes to actual code paths.
- Put JSON bodies in `request_body`; put query/path/header inputs in `manual_parameters` as appropriate.
- Do not add a request body to GET unless the implementation genuinely consumes one.
- Define reusable item schemas separately when a response or request contains arrays of objects.
- Include realistic `example` values supported by source or existing fixtures.
- Document authentication responses consistent with the view permission classes and repository conventions.
- Separate decorators for different HTTP methods sharing one URL.
- For an `APIView`, attach a method-specific decorator directly to `get`, `post`, `put`, and so on; do not add `method=` to that decorator.
- For function-based views that handle multiple methods through DRF decorators, follow nearby code and set `method=` when required by `swagger_auto_schema`.

## Verification

- Confirm the decorator is imported and attached to the intended method.
- Re-read every documented field against the implementation.
- Run the narrowest available syntax/import, Django check, or Swagger schema generation check.
- If dependencies or database access prevent runtime validation, run static checks that are available and report the exact limitation.
- In brainstorm mode, validate the Markdown diff and leave Python files untouched.
