---
name: spdm-http
description: Tạo, sửa, rà soát hoặc kiểm chứng file .http của JetBrains HTTP Client cho SPDM, gồm luồng API nhiều bước, biến môi trường, assertion và fixture. Dùng khi người dùng yêu cầu test API SPDM bằng .http hoặc gỡ lỗi file .http trong PyCharm hay IntelliJ. Dùng skill Postman tương ứng nếu đầu ra là Postman Collection.
---

# SPDM-HTTP

Viết file có thể chạy từng request trong JetBrains HTTP Client và đối chiếu kết quả nghiệp vụ SPDM.

## Lấy đúng hợp đồng API

- Đọc các file `.http` gần thư mục đích để theo convention của project. Khi workspace có `SpDM_Documents`, dùng `SE_Confirm_REQ-0003` làm mẫu cho login và assertion, `RFL_EDIT` cho luồng nhiều bước có rollback.
- Đối chiếu route và prefix thực tế với `backend/urls.py`, route của app và handler. Dùng frontend để xác nhận payload, điều kiện gọi API, thứ tự request và cách màn hình đọc dữ liệu sau khi lưu.
- Phân biệt request quan sát với request ghi theo hành vi thực tế. Ví dụ, TLM dùng POST để đọc. Đọc dữ liệu trước, xác định fixture theo khóa nghiệp vụ và kiểm tra có đúng một target trước khi dựng payload ghi.

## Dựng file chạy được

- Đặt file tại thư mục người dùng yêu cầu. Mở đầu bằng mục đích, cách chọn environment, điều kiện fixture, thứ tự chạy và bước nào ghi dữ liệu. Đặt `### @name` cho các request cần gọi riêng. Dùng assertion cho status và dữ liệu nghiệp vụ. Dùng `# @no-log` cho request có thông tin nhạy cảm.
- Với convention hiện tại, đặt URL trực tiếp như `POST {{devApiBase}}/rfl/meta`. Lấy token từ login và dùng trực tiếp `Authorization: Bearer {{access_token}}` hoặc biến token riêng của luồng. Tránh tạo biến trong file như `@apiBase = {{rfl_base}}` khi `rfl_base` chỉ được tạo trong response handler. JetBrains từng bỏ mất phần host khi phân giải URL qua alias đó.
- Tách đúng nguồn biến trong script. Dùng `request.environment.get(...)` cho environment, `client.variables.file.get(...)` cho biến khai báo bằng `@` khi IDE hỗ trợ API này và `client.global.get(...)` cho dữ liệu giữa các request. Đưa payload động vào body bằng một biến JSON đã `JSON.stringify`, để biến đứng ngoài dấu ngoặc kép. Xóa biến payload cũ khi bắt đầu lại luồng. Chỉ tạo payload ghi sau khi preflight đạt.
- Đặt URL và cấu hình không nhạy cảm trong `http-client.env.json` khi cần. Giữ username, password và token ngoài file được commit. Dùng `http-client.private.env.json` được Git bỏ qua cho thông tin đăng nhập cục bộ. Sau khi copy file sang project khác, kiểm tra lại environment JetBrains nhìn thấy, base URL, phiên token và fixture ở DB đích.

## Fixture, lỗi và xác minh

- Ưu tiên DB cô lập hoặc scope test chuyên dụng đã kiểm chứng. Localhost có thể nối đến DB dùng chung. Với thao tác thêm, sửa, xóa hoặc thay thế, kiểm tra đúng môi trường và scope trước khi gửi request ghi. Nếu cần giữ lại hoặc dọn fixture, giới hạn theo ID thuộc lần test. Nêu rõ trạng thái còn lại sau khi chạy.
- Kiểm tra nghiệp vụ bằng một lần đọc sau khi lưu. Với rollback, lưu snapshot có ID, giá trị và thứ tự trước request, rồi so lại sau lỗi. Gắn nhãn rõ nếu một assertion **dự kiến fail trên bản hiện tại** vì đang tái hiện bug. Tách bước khôi phục để người chạy vẫn có thể chạy khi assertion fail.
- Khi gỡ lỗi, tìm request đầu tiên fail. Phân biệt lỗi phân giải URL, HTTP 401/404, scope không có fixture và assertion nghiệp vụ. `UnknownHostException: rfl` sau khi login pass thường là URL thiếu base, không phải API RFL báo lỗi. Nếu endpoint metadata trả HTTP 200 nhưng dữ liệu trống, xác minh lại tên project/phase và environment trước khi sửa backend.
- Kiểm tra cú pháp JSON/script, tên biến, URL sau thay thế và phụ thuộc giữa các request. Nếu chạy được trên fixture cô lập, thực thi chuỗi API và kiểm tra cả ca thành công lẫn ca lỗi. Nếu chỉ chạy qua trình thử mô phỏng JetBrains, hoặc chỉ chạy preflight đọc, ghi rõ mức kiểm chứng. Báo request fail, status, assertion và điều kiện còn thiếu.

Khi làm RFL edit hoặc import Excel, đọc [references/rfl.md](references/rfl.md) để chọn ca kiểm thử và kiểm tra phạm vi rollback.
