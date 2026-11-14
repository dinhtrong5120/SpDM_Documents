# Kết quả điều tra RFL edit và import

Kiểm tra ngày 2026-11-14 với backend sau commit `15c1f46c` và bản sửa giữ metadata/liên kết RFL.

## Quy tắc liên kết SE khi chỉnh sửa

Logic được tạo mới do chỉnh sửa phải có `related_se_parameter_id = NULL`, chủ động không sao chép từ bản ghi nguồn. Bản ghi nguồn giữ nguyên liên kết SE; nếu tái sử dụng một Logic đã tồn tại, liên kết của bản ghi đó không bị xóa. Các thuộc tính Requirement và cạnh cây RFL vẫn được bảo toàn.

File 01 bổ sung bước 10–11 để đổi tên Logic, đọc lại và kiểm tra liên kết SE rỗng cùng hai dòng không được sửa. Fixture HTTP ban đầu chưa gắn SE; test Django dùng bản ghi nguồn có SE ID để kiểm tra thực sự không sao chép liên kết.

## Nguyên nhân các assertion fail

1. `01_rfl_edit.http`, bước 6, và `02_rfl_import_rollback.http`, bước 2: lỗi ID ngoài scope là `ValueError`, hiện trả **HTTP 400**, không phải 500. Đã sửa status trong assertion.
2. `02_rfl_import_rollback.http`, bước 5: parser tách Requirement bằng xuống dòng, không tách bằng `/`. Payload cũ nối thêm `/InvalidFourthPart` vẫn là tên một dòng hợp lệ. Đã dựng rõ bốn dòng và kiểm tra thông báo `最大3行`.
3. `02_rfl_import_rollback.http`, bước 6: đây là lỗi nghiệp vụ còn tồn tại. PATCH xóa ba dòng đã commit trước khi POST tạo mới trả 400. Transaction của POST không thể hoàn tác PATCH trước đó, nên scope còn **0 dòng**. Giữ assertion fail để tiếp tục phát hiện lỗi; bước 7–8 khôi phục fixture.

File 01 bắt đầu từ scope trống. Nếu chạy lại trên scope còn fixture, bước 3 sẽ chủ động dừng. Không bỏ assertion để ghi đè dữ liệu sẵn có.

## Mức kiểm chứng

- 16 test Django liên quan đến edit, metadata, cây RFL, thứ tự, rollback và validation đã pass trên MySQL 8.0 cô lập.
- Đã thực thi script của hai file qua trình mô phỏng JetBrains, gọi handler Django thật và đọc/ghi MySQL cô lập. Thay các biến scope bằng fixture riêng, giả lập đăng nhập bằng `force_authenticate`; không dùng thông tin đăng nhập hay scope TEST_01 đang có.
- File 01: **11/11 assertion pass**, gồm hai assertion mới cho quy tắc không kế thừa SE.
- File 02: **7/8 assertion pass**. Bước 6 fail đúng lỗi mất ba dòng qua hai request; bước khôi phục và kiểm tra thứ tự đều pass.
- Chưa chạy trực tiếp trong PyCharm, chưa kiểm tra login qua HTTP hay parser Excel của frontend. File 02 mô phỏng JSON sau khi đọc Excel.

DB view local hiện ghép tên Requirement nhiều dòng bằng `/`, trong khi SQL của `rfl_view_tlm` trong repo dùng xuống dòng. Fixture một dòng trong file 01 tránh phụ thuộc khác biệt này. Chưa thay schema/view của DB local.

## Phần còn lại

Muốn ca thay dữ liệu ở bước 6 pass, cần gom xóa và tạo dữ liệu vào cùng một transaction phía backend, rồi để frontend gửi một request. Bản sửa giữ metadata khi edit chưa thay đổi luồng import gồm hai request.

Chỉ chạy file 02 trên fixture riêng có thể xóa và khôi phục; không chạy trên dữ liệu dự án thật.
