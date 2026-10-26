# SPDM Postman integration workflow reference

Đọc tài liệu này khi cần thiết kế deliverable mới, lập ma trận test hoặc rà coverage trước bàn giao.

## Fixture checklist

Fixture nên nhóm theo ý nghĩa thay vì theo table:

- `safety`: required DB suffix, namespace prefix;
- `ids`: reserved IDs có lý do rõ ràng;
- `master`: tên/ID master data cần seed hoặc bắt buộc tồn tại;
- actor/user: admin, editable user, user không quyền;
- source entity: project/variation/parameter dùng làm sentinel;
- created/updated entity: giá trị request và expected sau ghi;
- status/scenario: state transition cần kiểm tra.

Validate kiểu, positive IDs, độ dài cột legacy, uniqueness và prefix. Chỉ yêu cầu prefix ở các chuỗi mà cleanup thực sự dùng để nhận diện. Không ép các enum/nhãn hệ thống như `Active`, `suspended` hay nhãn tiếng Nhật mang prefix test.

Canonical checksum gợi ý:

```python
raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
checksum = hashlib.sha256(raw.encode("utf-8")).hexdigest()
```

## Collection normalization checklist

- URL có đúng method, route, trailing slash và `{{SUB_PATH}}`.
- Không còn password/token thật hoặc comment JavaScript trong raw JSON body.
- Collection auth dùng `Bearer {{token}}` khi phù hợp; login/public endpoint dùng `noauth` nếu header bearer chưa hợp lệ có thể làm DRF reject.
- Login script chỉ lưu token vào đúng scope đã được người dùng chọn.
- Payload được sinh từ fixture; placeholder runtime chỉ dành cho password/token sinh trong lần chạy.
- Tên folder/request ổn định vì runner dùng chúng làm case identity.
- Không giữ request giả dữ liệu trỏ nhầm vào login hoặc endpoint khác.

## Preflight sequence

Thứ tự an toàn:

1. Parse và validate fixture.
2. Parse collection; xác minh checksum và exact case set.
3. Parse config; xác minh DB suffix.
4. Khởi tạo MySQL client bằng option file tạm mode `0600`; không đưa password lên command line/log.
5. Kiểm tra/nạp schema và views.
6. Gọi readiness; so sánh database identity.
7. Chụp master state cần khôi phục.
8. Pre-clean rồi seed.
9. Lấy JWT và kiểm tra sentinel qua API.
10. Chạy cases.
11. Cleanup trong `finally`, đóng client và xóa option file.

## Assertion matrix template

| # | Method + endpoint | FE usage | Fixture keys | Expected HTTP/JSON | DB/file assertion | Write/cleanup |
|---:|---|---|---|---|---|---|
| 1 | `GET ...` | Có/không | `source.*` | 200 + sentinel | query/view/file | read-only hoặc mô tả cleanup |

Với endpoint trả binary, kiểm tra HTTP status, `Content-Type`, content disposition khi cần và payload không rỗng. Với password reset, so sánh hash trước/sau thay vì log hoặc giải mã password. Với logout, xác minh blacklist/outstanding-token state.

## Coverage gap checklist

Ghi rõ phần chưa có, ưu tiên theo rủi ro:

1. Auth và authorization: missing/invalid/expired token, inactive user, non-admin.
2. Validation: missing/null/blank/wrong type, invalid enum, ID không tồn tại.
3. Integrity: duplicate, foreign key, multi-row partial failure, transaction rollback.
4. State/idempotency: gọi lặp, transition không hợp lệ, not-found.
5. Concurrency: hai user ghi/lock/reset cùng lúc, race condition.
6. Files: positive/negative upload, extension spoofing, workbook lớn/hỏng, temp cleanup.
7. External services: email, Cognito/AWS, backup/dump; yêu cầu sandbox riêng.
8. Reliability/performance: DB disconnect, timeout, large dataset, load limits.
9. Migration compatibility: schema/view khác phiên bản MySQL.

## Bàn giao tối thiểu

- Link tuyệt đối tới collection, fixture, runner và hai file tài liệu.
- Một lệnh chạy chính.
- Kết quả unit/lint/live integration đã thực sự chạy.
- Kết quả query hậu cleanup.
- Danh sách endpoint bị loại và lý do.
- Nhận định thẳng thắn “đủ cho mục đích nào, chưa đủ cho mục đích nào”.
