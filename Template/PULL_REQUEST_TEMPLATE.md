---

# 日本語版

---

## Pull Request 概要

### 概要

- QR-0093: Family へのプロジェクト追加時に Body Type を正しく照合し、SE/R パラメータのない project/phase の保存成功を防止する。
- 比較対象: `natv/sq8/feature/QR-0093` → `main`（ローカル ref、source: `3b26a19a`）。

### 変更タイプ

- [x] バグ修正
- [ ] 機能追加
- [ ] インフラ
- [ ] リファクタリング
- [x] ドキュメント

---

### 動機と背景

Family 作成処理は Destination・Powertrain・Drivetrain のみで setup を検索し、作成時には `body_type_id=1` を固定使用していた。同じ条件で Body Type が異なる場合、誤った setup/project を選択・作成する可能性があった。

SE/R がない scope でも成功を返すため、追加画面には行があるのに、パラメータの存在を条件とする Project List や再表示した追加画面では見えなくなる問題があった。

---

### 変更内容

- `utils/project_module.py`: 独立した `add_project_metadata_v1` に `body_type` を渡し、setup の検索・作成に反映。通常の `add_project_metadata` は変更しない。
- `project/views.py`: `POST /project/v1/create-new-project/` で空白除去後の `body_type` を必須化。保存後に同じ project/phase の SE または R の存在を確認し、なければ HTTP 400 と transaction rollback。
- `se/r=null` または空 object/list の組合せは挿入処理を省略し、最終的な scope の存在で判定する。既存パラメータの再送は不要。
- Family 関係は `(project_id, phase_id)` で更新。既存 SE/R は新規パラメータを送らない限り維持する。
- `project/swagger_docs.py` と2つの test file を更新。`all-projects/` の抽出条件、通常 API、schema/migration は変更しない。

---

### テスト

- [x] ユニットテスト
- [ ] 結合テスト
- [ ] 手動テスト
- [ ] 未テスト（理由を記載）

実行コマンド: `env/bin/python manage.py test project.tests.test_create_new_project project.tests.test_family_assignment --settings=backend.test_settings`

**13件成功**。Mock と隔離した in-memory SQLite を使用し、MySQL の upsert 構文をテスト内で変換している。実際の Django/MySQL 結合テスト、UI 操作、実データ更新は未実施。

| # | 確認項目 | 対象メソッド | 画面での操作 | 期待結果 | 結果 |
| - | -------- | ------------ | ------------ | -------- | ---- |
| 1 | Body Type と既存値の維持 | V1 / metadata | N/A | 同名・別 Body Type を選ばず、SE-only/R-only の値を維持 | OK |
| 2 | 空 scope・別 phase・null/空 SE/R | V1 POST | N/A | 空 scope は400、metadata/family を rollback | OK |
| 3 | 新規作成・入力必須・関数独立性 | V1 / 通常 helper | N/A | 指定 Body Type、必須検証、V1 から通常 helper を呼ばない | OK |
| 4 | Family 再表示 | V1 / all-projects | Create→Family View→追加画面 | 追加した正しい scope が再表示される | 未実施 |

---

### 影響度・リスク評価

- [ ] 低リスク（破壊的変更なし）
- [ ] 中リスク（後方互換性あり）
- [x] 高リスク（破壊的変更またはデータへの影響あり）

V1 の入力契約を変更する。`body_type` 未送信/空の client、および SE/R のない scope は400となる。確認した FE は既に `body_type` を送信する。既存の誤登録データは自動修復しない。既存の Family upsert は同じ project/phase の所属先を変更できる。

残存制限: 既存 scope に対する list/string 型の `se/r` は現在も無視され、200になる場合がある。この型検証の修正は本PRに含まれない。実MySQLの挙動はリリース前に要確認。

---

### チェックリスト

- [ ] コードがプロジェクトのコーディング規約に従っている
- [x] テストが追加または更新されている
- [x] 必要に応じてドキュメントが更新されている
- [x] 秘密情報や機密データがコミットされていない
- [ ] Terraform plan 確認（対象外）

### 関連チケット

- QR-0093

---

# English Version

---

## Pull Request Overview

### Summary

- QR-0093: Match Body Type when adding projects to a family and prevent successful saves of project/phase scopes without SE/R parameters.
- Comparison: `natv/sq8/feature/QR-0093` → `main` (local refs, source: `3b26a19a`).

### Type of Change

- [x] Bugfix
- [ ] Feature
- [ ] Infrastructure
- [ ] Refactor
- [x] Documentation

---

### Motivation and Context

Family creation previously matched setups by Destination, Powertrain and Drivetrain only, and hardcoded `body_type_id=1` when creating a setup. Projects with the same filters but different Body Types could use the wrong setup/project.

The API also reported success for scopes without SE/R parameters. A row could therefore appear during creation but disappear from Project List or the reopened creation screen, whose queries require parameter data.

---

### Changes Made

- `utils/project_module.py`: Pass `body_type` to the independent `add_project_metadata_v1` and use it in setup lookup/insertion. Leave the normal `add_project_metadata` unchanged.
- `project/views.py`: Require a nonblank, trimmed `body_type` for `POST /project/v1/create-new-project/`. After processing, require an SE or R record for that exact project/phase; otherwise return HTTP 400 and roll back the transaction.
- Skip parameter insertion for combinations of null or empty `se/r` objects/lists, then validate the resulting scope. Existing parameters need not be resent.
- Update family membership by `(project_id, phase_id)`; preserve existing SE/R when no new parameters are submitted.
- Update `project/swagger_docs.py` and two test files. No changes to `all-projects/` filtering, the normal API, or schema/migrations.

---

### Testing

- [x] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Not tested (please explain)

Executed: `env/bin/python manage.py test project.tests.test_create_new_project project.tests.test_family_assignment --settings=backend.test_settings`

**13 tests passed**, using mocks and isolated in-memory SQLite with MySQL upsert syntax translated in tests. Real Django/MySQL integration, UI testing and real-data updates were not performed.

| # | Check Item | Target Method | Screen Operation | Expected Result | Result |
| - | ---------- | ------------- | ---------------- | --------------- | ------ |
| 1 | Body Type and existing values | V1 / metadata | N/A | Match the correct Body Type; retain SE-only/R-only values | Passed |
| 2 | Empty scope, other phase, null/empty SE/R | V1 POST | N/A | Return 400 for empty scopes; roll back metadata/family writes | Passed |
| 3 | Creation, required input, helper independence | V1 / normal helper | N/A | Keep requested Body Type; validate input; V1 does not call normal helper | Passed |
| 4 | Reopen family | V1 / all-projects | Create→Family View→creation screen | The correct added scope remains visible | Not executed |

---

### Impact & Risk Assessment

- [ ] Low risk (no breaking changes)
- [ ] Medium risk (backward compatible)
- [x] High risk (breaking change or data-impacting)

This changes the V1 input contract: clients omitting/blanking `body_type`, and scopes without SE/R, now receive 400. The inspected FE already sends `body_type`. Previously incorrect records are not repaired automatically. The existing family upsert can reassign membership for the same project/phase.

Remaining limitation: list/string `se/r` values on existing scopes are still ignored and may return 200; strict type validation is outside this PR. Real MySQL behavior still needs verification before release.

---

### Checklist

- [ ] Code follows the project coding standards
- [x] Tests have been added or updated
- [x] Documentation has been updated if needed
- [x] No secrets or sensitive data are committed
- [ ] Terraform plan reviewed (not applicable)

### Related Issues / Tickets

- QR-0093

---

# Bản tiếng Việt

---

## Tổng quan Pull Request

### Tóm tắt

- QR-0093: Xác định đúng Body Type khi thêm project vào family và ngăn báo lưu thành công cho scope project/phase không có parameter SE/R.
- Đối chiếu: `natv/sq8/feature/QR-0093` → `main` (ref local, source: `3b26a19a`).

### Loại thay đổi

- [x] Sửa lỗi
- [ ] Tính năng
- [ ] Hạ tầng
- [ ] Tái cấu trúc
- [x] Tài liệu

---

### Động cơ và bối cảnh

Luồng family trước đây chỉ tìm setup theo Destination, Powertrain và Drivetrain, đồng thời gán cứng `body_type_id=1` khi tạo setup. Vì vậy, cùng các thông số này nhưng khác Body Type có thể bị chọn/tạo nhầm setup hoặc project.

API còn báo thành công khi scope không có SE/R. Dòng xuất hiện lúc Create nhưng có thể biến mất tại Project List hoặc khi mở lại màn Create vì API đọc yêu cầu có parameter.

---

### Nội dung thay đổi

- `utils/project_module.py`: Bổ sung `body_type` vào hàm độc lập `add_project_metadata_v1`, dùng trong tìm/tạo setup. Giữ nguyên `add_project_metadata` của luồng thường.
- `project/views.py`: `POST /project/v1/create-new-project/` bắt buộc `body_type` là chuỗi không rỗng sau trim. Sau xử lý phải có ít nhất một dòng SE hoặc R đúng project/phase; nếu không, trả HTTP 400 và rollback transaction.
- Bỏ qua bước insert parameter với các tổ hợp `se/r` null hoặc object/list rỗng, sau đó kiểm tra scope cuối cùng. Không yêu cầu gửi lại parameter đã có.
- Cập nhật family theo `(project_id, phase_id)`; giữ dữ liệu SE/R hiện có khi không gửi parameter mới.
- Cập nhật `project/swagger_docs.py` và hai file test. Không đổi điều kiện `all-projects/`, API thường hoặc schema/migration.

---

### Kiểm thử

- [x] Unit test
- [ ] Integration test
- [ ] Kiểm thử thủ công
- [ ] Chưa kiểm thử (vui lòng nêu lý do)

Đã chạy: `env/bin/python manage.py test project.tests.test_create_new_project project.tests.test_family_assignment --settings=backend.test_settings`

**13 test đạt**, dùng mock và SQLite in-memory cô lập, chuyển cú pháp upsert MySQL trong test. Chưa chạy tích hợp Django/MySQL thật, kiểm thử UI hoặc cập nhật dữ liệu thật.

| # | Hạng mục kiểm tra | Phương thức mục tiêu | Thao tác trên màn hình | Kết quả mong đợi | Kết quả |
| - | ----------------- | -------------------- | ---------------------- | ---------------- | ------- |
| 1 | Body Type và giá trị hiện có | V1 / metadata | N/A | Chọn đúng Body Type; giữ dữ liệu SE-only/R-only | Đạt |
| 2 | Scope rỗng, khác phase, SE/R null/rỗng | V1 POST | N/A | Scope rỗng trả 400; rollback metadata/family | Đạt |
| 3 | Tạo mới, trường bắt buộc, hàm độc lập | V1 / helper thường | N/A | Đúng Body Type; kiểm tra đầu vào; V1 không gọi helper thường | Đạt |
| 4 | Mở lại family | V1 / all-projects | Create→Family View→màn Create | Scope được thêm vẫn hiển thị đúng | Chưa thực hiện |

---

### Đánh giá tác động và rủi ro

- [ ] Rủi ro thấp (không có thay đổi phá vỡ tương thích)
- [ ] Rủi ro trung bình (tương thích ngược)
- [x] Rủi ro cao (thay đổi phá vỡ tương thích hoặc ảnh hưởng dữ liệu)

Thay đổi hợp đồng đầu vào V1: client thiếu/để trống `body_type`, hoặc scope không có SE/R sẽ nhận 400. FE đã đối chiếu có gửi `body_type`. Không tự sửa các bản ghi đã tạo nhầm. Upsert family hiện có vẫn có thể chuyển family của cùng project/phase.

Hạn chế còn lại: `se/r` kiểu list/string trên scope đã có dữ liệu vẫn bị bỏ qua và có thể trả 200; kiểm tra chặt kiểu dữ liệu chưa nằm trong PR. Cần xác minh trên MySQL thật trước phát hành.

---

### Danh sách kiểm tra

- [ ] Code tuân thủ quy chuẩn của dự án
- [x] Test đã được thêm mới hoặc cập nhật
- [x] Tài liệu đã được cập nhật nếu cần
- [x] Không commit thông tin bí mật hoặc dữ liệu nhạy cảm
- [ ] Terraform plan đã được kiểm tra (không áp dụng)

### Ticket liên quan

- QR-0093
