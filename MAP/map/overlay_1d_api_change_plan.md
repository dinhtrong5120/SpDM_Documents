# Kế hoạch API cho MAP `OVERLAY_1D`

## 1. Phạm vi và quyết định dữ liệu

- Không thay đổi schema MySQL.
- Không tạo bảng series/point.
- Tái sử dụng `map_variable`, `map_structure` và `detail_data_map_name`.
- Mode API mới: `OVERLAY_1D`.
- Biến X tiếp tục dùng `map_variable.axis = 'X'`.
- Biến T dùng `map_variable.axis = 'OVERLAY_1D'` để phân biệt với TABLE hiện tại.
- Một MAP `OVERLAY_1D` có đúng hai dòng trong `map_structure`: một dòng X và một dòng T.

Định dạng `map_structure.value` của mỗi trục:

```text
series_key:value1,value2,...;series_key:value1,value2,...
```

Ví dụ:

```text
X = UP_1-2:12.648,12.648,14.5,23,30,48,48;DOWN_2-1:0.25,0.25,16.497,16.497
T = UP_1-2:0,18,20,30,40,70,80;DOWN_2-1:0,70,70.001,80
```

## 2. Contract dùng chung cho create/edit/read

Không ép loại mới vào `df_edited`, vì cấu trúc đó là bảng chữ nhật và TABLE hiện tại chỉ có một X dùng chung. Thêm payload riêng:

```json
{
  "mode": "OVERLAY_1D",
  "xname": "101_Vsp_km/h",
  "tname": "102_vAPO_deg",
  "overlay_series": [
    {
      "series_key": "UP_1-2",
      "x_values": [12.648, 12.648, 14.5, 23, 30, 48, 48],
      "t_values": [0, 18, 20, 30, 40, 70, 80]
    },
    {
      "series_key": "DOWN_2-1",
      "x_values": [0.25, 0.25, 16.497, 16.497],
      "t_values": [0, 70, 70.001, 80]
    }
  ],
  "df_edited": null,
  "df_editeds": null,
  "df_edited_z": null
}
```

Response đọc MAP bổ sung cùng cấu trúc `overlay_series`. Với series chuyển số, backend có thể trả metadata dẫn xuất để UI không phải parse hai lần:

```json
{
  "series_key": "UP_1-2",
  "direction": "UP",
  "from_no": 1,
  "to_no": 2,
  "x_values": [12.648, 12.648, 14.5, 23, 30, 48, 48],
  "t_values": [0, 18, 20, 30, 40, 70, 80]
}
```

`direction`, `from_no`, `to_no` chỉ là dữ liệu dẫn xuất từ `series_key` có dạng `UP_n-m` hoặc `DOWN_n-m`; không lưu riêng trong database. Series tự do trả các trường này bằng `null`.

## 3. API bắt buộc phải chỉnh

### 3.1 `POST /api/se-list/se-map/get-infomation/`

View: `se_list.views.se_map_get_infomation`.

Mục đích thay đổi:

- Thêm `OVERLAY_1D` vào danh sách `マップ種類`.
- Trả danh sách biến X hiện có.
- Trả danh sách biến có `axis = 'OVERLAY_1D'` cho T.
- Cho phép frontend tạo biến T mới thông qua key `add_new.tname`.

Response bổ sung dự kiến:

```json
{
  "マップ種類": ["TABLE", "MAP", "CUBE", "OVERLAY_1D"],
  "OVERLAY_1D": {
    "X軸名": ["101_Vsp_km/h"],
    "X軸名_new": [{"id": 101, "variable_name": "Vsp", "unit": "km/h"}],
    "T軸名": ["102_vAPO_deg"],
    "T軸名_new": [{"id": 102, "variable_name": "vAPO", "unit": "deg"}],
    "max_points_per_series": 20
  }
}
```

Code tác động:

- `utils.map_module.create_df_display_for_new_map()`.
- `utils.map_module.get_map_variables_all()` không cần thay đổi query.
- Swagger `se_map_get_infomation_docs`.

### 3.2 `POST /api/se-list/se-map/map-button/`

View: `se_list.views.map_button`.

Mục đích thay đổi: đọc MAP đã lưu và trả dữ liệu cho màn hình overlay.

Luồng xử lý:

1. `get_map_variables_by_name(map_name)` vẫn dùng nguyên query hiện tại.
2. `judge_map_mode()` nhận diện một dòng `X` và một dòng `OVERLAY_1D`.
3. Không gọi `get_df_display()` cho mode mới.
4. Parse hai chuỗi X/T.
5. Kiểm tra thứ tự `series_key` và độ dài cặp X/T.
6. Trả `overlay_series`; các field dataframe cũ trả `null` hoặc danh sách rỗng.

Response `data` bổ sung:

```json
{
  "mode": "OVERLAY_1D",
  "xname": "101_Vsp_km/h",
  "tname": "102_vAPO_deg",
  "overlay_series": [],
  "df_display": null,
  "df_display_z": null,
  "list_df_displays_new": []
}
```

Code tác động:

- `utils.map_module.judge_map_mode()`.
- `utils.map_module.mapgrid_by_name()`.
- Helper parse/merge mới trong `utils/map_overlay_1d.py`.
- Swagger `se_map_button_docs`.

### 3.3 `POST /api/se-list/se-map/map-create/`

View: `se_list.views.map_create`.

Mục đích thay đổi: tạo MAP overlay và ghi hai dòng `map_structure` cùng lịch sử.

Luồng xử lý:

1. Nếu `mode != 'OVERLAY_1D'`, giữ nguyên toàn bộ luồng MAP/TABLE/CUBE.
2. Đọc `xname`, `tname`, `overlay_series`.
3. Nếu có `add_new.tname`, tạo `map_variable` với `axis = 'OVERLAY_1D'`.
4. Validate payload.
5. Serialize thành `x_value` và `t_value`.
6. Trong một `transaction.atomic()`:
   - insert hai dòng `map_structure`;
   - insert hai dòng `detail_data_map_name`;
   - cập nhật `project_parameter` hoặc `test_project_senario_parameter` theo `chosen_id`.
7. Không gọi nhánh dataframe legacy cho mode mới.

Code tác động:

- `se_list.views.map_create()` thêm nhánh mode mới và mapping `tname -> OVERLAY_1D`.
- `utils.map_module.update_mapgrid_by_name()` dispatch sang service overlay trước luồng legacy.
- Helper ghi mới, ví dụ `create_overlay_1d_map()`.
- Swagger `se_map_create_docs`.

### 3.4 `POST /api/se-list/se-map/map-edit/`

View: `se_list.views.map_edit`.

Mục đích thay đổi: cập nhật hai chuỗi X/T và ghi lịch sử.

Luồng xử lý:

1. Giữ nguyên logic map name/version hiện tại.
2. Khi `mode = 'OVERLAY_1D'`, dùng `overlay_series`, không chuyển thành DataFrame.
3. Lấy ID X/T bằng `get_map_variable_id()` mở rộng cho mode mới.
4. Validate và serialize.
5. Trong một transaction:
   - update đúng hai dòng `map_structure`;
   - insert đúng hai dòng `detail_data_map_name`;
   - thực hiện cập nhật tên/version hiện có nếu request yêu cầu.

Code tác động:

- `se_list.views.map_edit()`.
- `utils.map_module.get_map_variable_id()`.
- `utils.map_module.update_mapgrid_by_name()`.
- Helper ghi sửa, ví dụ `update_overlay_1d_map()`.
- Swagger `se_map_edit_docs`.

## 4. API dùng helper chung hoặc cần kiểm thử tương thích

### 4.1 `POST /api/scenario/scenario-map/`

View này gọi `mapgrid_by_name(result, 3)`. Không cần nhánh SQL riêng, nhưng response sẽ tự có `overlay_series` sau khi helper chung được cập nhật. Cần cập nhật Swagger Scenario và frontend Scenario MapModal nếu loại mới được phép dùng ở Scenario.

### 4.2 `POST /api/se-list/se-map/rfl-map-button/`

View này cũng gọi `mapgrid_by_name()`. Không cần sửa thuật toán riêng. Chỉ cập nhật frontend/Swagger nếu RFL phải hiển thị loại mới; nếu feature chỉ dành cho SE/Scenario thì giữ RFL ngoài phạm vi và thêm test không regression.

### 4.3 `GET/POST /api/se-list/se-map/import/`

SQL hiện tại đã làm việc theo `map_structure` và `map_variable.axis`, nên về nguyên tắc:

- GET dùng `mode_map=OVERLAY_1D` sẽ lấy cả hai dòng X/T của MAP phù hợp.
- POST đã insert generic `map_name`, `map_variable_id`, `map_value` vào `map_structure` và history.

Không cần viết storage riêng. Cần:

- cho phép frontend chọn mode `OVERLAY_1D`;
- cập nhật Swagger GET/POST;
- kiểm thử import hai dòng cùng map name trong một transaction.

## 5. API không cần thay đổi

Các API sau làm việc theo `map_name` hoặc dữ liệu generic, nên không cần biết format bên trong `value`:

- `POST /api/se-list/se-map/map-last-editor/`;
- `POST /api/se-list/se-map/map-delete/`;
- `POST /api/se-list/se-map/map-change-ver/`.

Chỉ cần regression test với MAP `OVERLAY_1D`.

## 6. Helper code đề xuất

Tạo `utils/map_overlay_1d.py` để không tiếp tục làm `utils/map_module.py` phình to.

```python
MODE_OVERLAY_1D = "OVERLAY_1D"
AXIS_OVERLAY_1D = "OVERLAY_1D"

def validate_overlay_series(series): ...
def serialize_overlay_axis(series, value_key): ...
def parse_overlay_axis(value): ...
def merge_overlay_axes(x_value, t_value): ...
def derive_shift_metadata(series_key): ...
```

Quy tắc validate:

- `overlay_series` không rỗng.
- `series_key` không rỗng và không trùng.
- `series_key` không chứa `:`, `;` hoặc `,`.
- `x_values` và `t_values` không rỗng, có cùng số phần tử.
- Không chấp nhận `null`, chuỗi rỗng, `NaN` hoặc vô cực trong một cặp.
- Cho phép số âm và số thập phân.
- Giữ nguyên thứ tự series và thứ tự điểm.
- Giới hạn 20 điểm/series nếu backend chính thức áp dụng giới hạn của UI mẫu.

Không dùng `float` để chuẩn hóa chuỗi nếu cần giữ nguyên biểu diễn thập phân. Có thể validate bằng `Decimal(str(value))`, sau đó serialize bằng biểu diễn decimal hữu hạn.

## 7. Thay đổi trong `utils/map_module.py`

Thay đổi nhỏ, theo hướng dispatch:

```python
def judge_map_mode(df_map_variables):
    if overlay_count == 1 and x_count == 1:
        return MODE_OVERLAY_1D
    # MAP/TABLE/CUBE giữ nguyên
```

```python
def update_mapgrid_by_name(..., overlay_series=None, tname=None):
    if mode == MODE_OVERLAY_1D:
        return save_overlay_1d(...)
    # Luồng cũ giữ nguyên
```

Không nên nhét mode mới vào tuple trả về của `make_sql_text()`. Tạo serializer riêng giúp không làm thay đổi contract nội bộ của MAP/TABLE/CUBE.

## 8. TD export không phải API nhưng phải xem xét

`scenario/td_export/override_build.py` hiện chỉ nhận `TABLE`, `MAP`, `CUBE`. Nếu MAP mới được export sang TD, thêm nhánh `OVERLAY_1D` và trả hai chuỗi đã serialize theo dạng tương tự `[X_value, T_value]` sau khi xác nhận consumer TD chấp nhận format này.

Nếu TD chưa hỗ trợ loại mới, cần trả lỗi rõ ràng thay vì coi MAP không tồn tại.

## 9. Swagger cần cập nhật

Trong `se_list/swagger_docs.py`:

- thêm schema dùng chung cho `overlay_series` item;
- cập nhật request create/edit với `tname` và `overlay_series`;
- cập nhật response map-button với `overlay_series`;
- cập nhật response get-information với option `OVERLAY_1D`;
- mô tả `df_edited*` là `null` khi mode mới;
- bổ sung lỗi 400/422 cho payload series sai thay vì trả mọi validation error dưới HTTP 200.

Trong `scenario/swagger_docs.py`, cập nhật response của `scenario-map` nếu feature được mở cho Scenario.

## 10. Frontend phụ thuộc API

Các điểm chính cần đổi sau khi backend contract được chốt:

- `SEListMapModal.tsx`: thêm `OVERLAY_1D` vào `MapType`, form state và payload create/edit/read.
- Tạo component overlay riêng; không tái sử dụng `Table1D.tsx` vì TABLE có một X chung.
- `Scenario/MapModal/MapModal.tsx`: cập nhật nếu Scenario hỗ trợ mode mới.
- Import modal: thêm filter `OVERLAY_1D` nếu import nằm trong phạm vi.

## 11. Kiểm thử tối thiểu

### Unit test helper

- round-trip serialize/parse MAP 2 cấp;
- round-trip đủ 16 series/120 điểm của MAP 9 cấp;
- series có số điểm khác nhau;
- số âm và số thập phân;
- trùng `series_key`;
- X/T khác độ dài;
- ký tự phân cách trong key;
- chuỗi malformed từ database.

### API integration

1. create `OVERLAY_1D` tạo đúng hai dòng `map_structure` và hai dòng history;
2. map-button đọc lại đúng dữ liệu create;
3. edit cập nhật cả X/T và thêm history;
4. create/edit lỗi phải rollback toàn bộ;
5. version/rename giữ nguyên hai dòng;
6. import/export round-trip;
7. delete/history vẫn hoạt động;
8. MAP/TABLE/CUBE hiện tại không thay đổi response.

## 12. Thứ tự triển khai

1. Chốt mode/axis `OVERLAY_1D` và request `overlay_series`.
2. Viết helper parse/validate/serialize cùng unit test.
3. Mở rộng read path: `judge_map_mode()` và `mapgrid_by_name()`.
4. Mở rộng create/edit trong transaction.
5. Cập nhật get-information.
6. Cập nhật Swagger.
7. Cập nhật frontend.
8. Kiểm thử Scenario/RFL/import/TD export theo phạm vi sản phẩm.

