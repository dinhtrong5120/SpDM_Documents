# SPDM Swagger form

Use the nearest existing API as the style baseline. The forms below capture the repository-level invariants.

## GET with query parameters

```python
# =============================================================================================
# API get abc

# 1. Định nghĩa params
abc_project_id_param = openapi.Parameter(
    "project_id",
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    required=True,
    description="Project id.",
)


# 2. Định nghĩa response
abc_success_response = openapi.Response(
    description="Thành công.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
            "data": openapi.Schema(type=openapi.TYPE_OBJECT, properties={...}),
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)


# 3. Tạo Decorator
get_abc_docs = swagger_auto_schema(
    manual_parameters=[abc_project_id_param],
    responses={
        200: abc_success_response,
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Not authenticated"),
        500: openapi.Response(description="Unexpected error"),
    },
    operation_summary="Get abc",
    operation_description="API lấy thông tin abc.",
)
```

## POST with JSON body

```python
# =============================================================================================
# API create abc

# 1. Định nghĩa request
create_abc_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["name"],
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Tên abc.",
            example="Example",
        ),
    },
)


# 2. Định nghĩa response
create_abc_success_response = openapi.Response(
    description="Tạo abc thành công.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
            "data": openapi.Schema(type=openapi.TYPE_OBJECT, properties={...}),
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)

create_abc_error_response = openapi.Response(
    description="Lỗi không mong đợi.",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_STRING, example="failed"),
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)


# 3. Tạo Decorator
create_abc_docs = swagger_auto_schema(
    request_body=create_abc_request,
    responses={
        200: create_abc_success_response,
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Not authenticated"),
        500: create_abc_error_response,
    },
    operation_summary="Create abc",
    operation_description="API tạo abc.",
)
```

## Attach decorators

For `APIView` methods:

```python
class AbcView(APIView):
    @get_abc_docs
    def get(self, request):
        ...

    @create_abc_docs
    def post(self, request):
        ...
```

For function-based views, preserve the decorator order already used by the target app and supply `method=` when the function serves multiple methods:

```python
@swagger_auto_schema(method="post", request_body=create_abc_request, responses={...})
@api_view(["POST"])
def create_abc(request):
    ...
```

## Review checklist

- Exact separator is present.
- Sections are request, response, decorator, in that order.
- URL and HTTP method resolve to the correct view.
- Request fields match `request.data`, query params, or serializer fields.
- Required fields match actual validation or direct dictionary indexing.
- Response object/array nesting matches the returned payload.
- Every explicit response status is documented.
- Decorator is attached to the correct method.
- GET and POST sharing a URL do not share a misleading decorator.
- Examples are realistic and contain no secrets.
