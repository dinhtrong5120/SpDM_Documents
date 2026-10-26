---
name: spdm-flowchart
description: Phân tích code API trong SPDM và tạo flowchart thuật toán dạng draw.io có swimlane, đầy đủ decision và nhánh xử lý. Dùng khi cần chuyển endpoint, view hoặc chuỗi helper của SPDM thành sơ đồ để BA, developer hoặc reviewer đọc hiểu; không dùng cho sơ đồ kiến trúc tổng quát không dựa trên code.
---

# SPDM Flowchart

Tạo file `.drawio` mô tả đúng thuật toán đang chạy trong source SPDM. Mục tiêu là giúp người đọc hiểu luồng xử lý, không phải chép từng dòng code vào sơ đồ.

## Phân tích source

1. Xác định route đang active trong `urls.py`. Nếu có route cũ bị comment hoặc nhiều phiên bản, chỉ mô tả route thật sự được gọi, trừ khi user yêu cầu so sánh.
2. Đọc toàn bộ chuỗi xử lý có thể đi tới từ endpoint: view, serializer/validator, helper/module, query, model lookup, state dùng chung, permission và error handler.
3. Ghi nhận chính xác:
   - input bắt buộc, tùy chọn, default và chuẩn hóa;
   - filter, join, existence check, grouping, ordering và chọn record;
   - mọi decision, loop, early return và exception path;
   - cấu trúc response và điều kiện trả 2xx/4xx/5xx;
   - side effect như cập nhật global state, lock hoặc cache.
4. Không sửa application code khi user chỉ yêu cầu sơ đồ.

## Chuyển thành thuật toán

- Ưu tiên logic có ý nghĩa: validate → scope → business filtering → transform → build tree → permission → response.
- Không bỏ logic chỉ vì nhánh khó đạt hoặc có vẻ thừa. Ghi rõ nếu code làm một nhánh trở thành unreachable.
- Có thể gộp các câu lệnh liên tiếp nếu việc gộp không làm mất điều kiện, dữ liệu vào/ra hoặc side effect.
- Tách function phức tạp thành trang riêng và thể hiện decision tree chi tiết. Trang tổng quan phải dẫn tới trang con bằng tên rõ ràng.
- Dùng Terminator cho Start/End, Process cho bước xử lý, Decision hình thoi cho điều kiện. Mỗi Decision phải có đúng hai nhánh `YES` và `NO`.

## Ngôn ngữ và thuật ngữ

- Diễn giải bằng tiếng Việt.
- Giữ nguyên từ chuyên ngành và identifier trong code, ví dụ `list`, `dict`, `DataFrame`, `project_id`, `drivetrain`, `wp`, `variation`, `setup_id`, `r_parameter_id`, tên model/table/function và key response.
- Không dịch identifier thành cụm tiếng Việt nếu việc dịch làm người đọc khó đối chiếu code.
- Dùng tên biến trung gian trong code khi nó giúp theo dõi data flow, ví dụ `scopes`, `single`, `master`, `available_wp`, `editable_wp`.

## Thiết kế draw.io

- Xuất XML draw.io đầy đủ, không nén, import trực tiếp vào diagrams.net.
- Layout top-down. Mỗi trang dùng ba swimlane: `Data input`, `Data processing`, `Business logic`.
- Trang đầu là thuật toán tổng quát; các trang sau chỉ tách khi cần đọc rõ hơn.
- Node ngắn gọn nhưng phải nêu field/biến quan trọng. Tránh mô tả chung như “xử lý dữ liệu”.
- Hạn chế đường nối cắt qua node. Loop phải quay lại đúng decision điều khiển vòng lặp.
- Đọc [references/drawio-conventions.md](references/drawio-conventions.md) trước khi tạo XML.

## Kiểm tra và bàn giao

Chạy validator sau khi tạo file:

```bash
python3 scripts/validate_drawio.py /absolute/path/to/file.drawio
```

Sửa mọi lỗi trước khi bàn giao. Mở hoặc parse lại file để bảo đảm XML hợp lệ. Nếu user yêu cầu “không giải thích”, final chỉ chứa link tải file `.drawio`.
