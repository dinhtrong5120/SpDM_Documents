# RFL edit, thứ tự và import

Xem ví dụ đang dùng tại `SpDM_Documents/RFL_EDIT/01_rfl_edit.http` và `02_rfl_import_rollback.http` nếu thư mục đó có trong workspace. Xác minh scope đích trước khi dùng lại. `test_pjcode_9800101` là fixture của DB cô lập, không có sẵn trong DB local thông thường. Các ví dụ ở Documents có thể trỏ vào một scope test cục bộ đã được chọn riêng.

## Đọc và tạo fixture

- `POST /rfl/meta` xác định đúng project, lot, phase và hierarchy. `POST /rfl/v2/tlm` lấy dữ liệu đã sắp xếp, `units_dict` và `wp_dict`. Kiểm tra scope gồm project, phase, WP và hierarchy. Đọc lại TLM sau mỗi lần lưu để xác minh thứ tự người dùng nhìn thấy.
- Dùng scope trống để tạo ba dòng đánh dấu riêng cho lần test. Hai dòng có cùng tên R/F/L nhưng khác Logic Use case. Dòng thứ ba dùng Function khác làm giá trị thay thế đã tồn tại trong DB. `POST /rfl/rfl-add-new` nhận nhóm dòng theo hierarchy và `list_order` với `rfl_id: null` cho dòng mới. Kiểm tra ID riêng biệt và thứ tự chính xác.

## Sửa làm đổi ID và rollback

- Qua `PATCH /rfl/update`, đổi Function của một dòng sang Function đã tồn tại với cùng đơn vị. Chọn tổ hợp R/F/L và use case khiến liên kết của dòng phải đổi ID. Gửi `list_order` chứa ID cũ và chủ động đặt dòng vào vị trí khác. Kỳ vọng HTTP 200, ID mới đúng vị trí và các dòng còn lại giữ ID.
- Trước ca thành công, gửi cùng payload với thêm một ID biết chắc ngoài scope. Xác nhận lỗi chỉ nêu ID ngoài scope, rồi đọc lại ID, Function và thứ tự. Cả ba phải giống snapshot. Đối chiếu status theo phiên bản đang test. Backend tại thời điểm tạo ví dụ trả HTTP 500 cho lỗi này.

## Import Excel

- File `.http` kiểm tra JSON **sau khi frontend đọc Excel**. Muốn kiểm thử parser hoặc thao tác import thật, dùng file `.xlsx` theo template xuất từ ứng dụng và chạy qua parser/frontend. Ghi rõ lớp nào đã được chạy.
- Import vào scope trống là ca tạo mới. Nếu cố tình thêm ID ngoài scope vào `list_order` của request tạo mới, kiểm tra các dòng vừa chèn được rollback và dữ liệu đã có còn nguyên.
- Với luồng thay dữ liệu gồm PATCH xóa rồi POST tạo, test hai request độc lập. Ví dụ để POST fail, dùng Requirement mới có bốn phần phân tách bằng `/` nếu backend hiện tại hỗ trợ tối đa ba phần. Đọc lại và assert các dòng cũ vẫn còn. Ở phiên bản từng tái hiện, PATCH trả 200, POST trả 400, DB còn 0 dòng. Đây là lỗi giữa hai request, khác rollback trong một request. Chỉ chạy ca này với fixture riêng và chuẩn bị bước khôi phục.
