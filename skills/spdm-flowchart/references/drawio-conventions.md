# Quy ước flowchart SPDM

## Cấu trúc trang khuyến nghị

Chỉ tạo các trang thực sự cần cho endpoint. Một flow thường dùng:

1. Thuật toán tổng quát.
2. Validate input.
3. Resolve scope hoặc entity chính.
4. Query và business filtering.
5. Transform/build tree của từng helper phức tạp.
6. Permission, response và exception handling.

## Swimlane

- `Data input`: request, query params, authenticated user và dữ liệu đầu vào của subroutine.
- `Data processing`: query, mapping, grouping, sorting, transform, state update.
- `Business logic`: rule loại/giữ, permission, response, validation failure và exception result.

## Shape

- Terminator: `rounded=1;arcSize=50`.
- Process: rectangle với `rounded=0`.
- Decision: `rhombus`.
- Swimlane: `swimlane;horizontal=1`.
- Connector: orthogonal, có mũi tên kết thúc.

Mỗi diagram cần có Start và End phù hợp. Toàn bộ document phải có đủ Terminator, Process và Decision. Mỗi Decision phải có hai outgoing edge được label chính xác `YES` và `NO`.

## Nội dung node

- Viết hành động trước, sau đó nêu field hoặc biến: “Filter `scopes` theo `variation`”.
- Với query, mô tả filter/join/existence/group/order ảnh hưởng kết quả; không cần chép nguyên SQL.
- Với response, dùng đúng key như `setup_id`, `variation_id`, `parameter_single_project`.
- Với tree, thể hiện từng level, cách tạo `key`, `category`, `children`, record và default field.
- Với list rỗng, null/default hoặc early return, luôn tạo decision riêng nếu kết quả flow thay đổi.
- Với exception, phân biệt validation error được re-raise với unexpected exception được log và trả 500.

## XML

- Root là `mxfile`; mỗi trang là một `diagram` chứa `mxGraphModel`.
- Mỗi `mxCell` trong cùng một diagram phải có `id` duy nhất.
- `source` và `target` của edge phải trỏ tới cell tồn tại.
- Escape ký tự XML trong label. Dùng `&#xa;` cho xuống dòng trong `value`.
- Ưu tiên XML không nén để review diff, sửa và validate dễ dàng.
