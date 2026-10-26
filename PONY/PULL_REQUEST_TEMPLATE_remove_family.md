---

# 日本語版

---

## Pull Request 概要

### 概要

- プロジェクトをファミリから解除（`project.family_id = NULL`）するための新規 API エンドポイント `POST /api/project/remove-project-family/` を追加しました。
- 楽観的ロック（楽観排他制御）の考え方を適用し、対象プロジェクトが指定された `family_code` に所属している場合のみ解除を実行します。
- 既に別のファミリに変更されているか解除済みの場合は `409 Conflict`、対象プロジェクトが存在しない場合は `404 Not Found` を返却します。

### 変更タイプ

該当するものを選択してください：

- [ ] バグ修正
- [x] 機能追加
- [ ] インフラ
- [ ] リファクタリング
- [ ] ドキュメント

---

### 動機と背景

- **以前の状態**: プロジェクトとファミリの紐付けを解除するための独立した専用 API がなく、UI や外部連携から安全にファミリ所属をリセットする手段がありませんでした。
- **問題とリスク**: 複数ユーザーによる同時編集時に、古い画面状態のまま解除リクエストが送信された場合、意図しないファミリ状態を上書きしてしまうリスクがありました。
- **目的**: 管理者（`USER_GR_ADMIN`）権限のもと、最新のファミリ状態と一致することを確認した上で安全に `family_id` をクリア（`NULL` 設定）できるように改善しました。

---

### 変更内容

- `project/urls.py`:
  - 新規ルート `path('remove-project-family/', views.remove_project_family)` を登録。
- `project/seirializers.py`:
  - 入力バリデーション用 `RemoveProjectFamilySerializer` を追加（`project_id`: 1 以上の整数、`family`: 空文字不可の文字列）。
- `project/views.py`:
  - ビュー関数 `remove_project_family` を実装。
  - `IsAuthenticated` および `USER_GR_ADMIN` グループ所属チェックを適用（非管理者は `403 Forbidden`）。
  - `transaction.atomic()` 内で `UPDATE project_info AS project JOIN family AS fam ON project.family_id = fam.id SET project.family_id = NULL WHERE project.id = %s AND fam.family_code = %s` を実行。
  - `cursor.rowcount == 0` の場合、`SELECT id FROM project_info WHERE id = %s` でプロジェクト存在確認を行い、プロジェクトが存在すれば `409 Conflict`（"Project is no longer in this family."）、非存在なら `404 Not Found`（"Project not found."）を返却。
  - 正常時は `200 OK`（`status: "success"`）を返却。
- `project/swagger_docs.py`:
  - `remove_project_family_docs` デコレータを定義し、リクエスト body およびステータスコード（200, 400, 401, 403, 404, 409, 500）のスキーマを定義。
- `project/tests/test_remove_project_family.py`:
  - 単体テストクラス `RemoveProjectFamilyTests` を追加（正常系解除、stale 状態での 409、権限不足 403、不正な project_id による 400）。

---

### テスト

- [ ] ユニットテスト
- [ ] 結合テスト
- [ ] 手動テスト
- [x] 未テスト（理由を記載）

> ※ 単体テストコード（`test_remove_project_family.py`）はフィーチャーブランチ上で作成されていますが、PR 作成時点のローカル作業ブランチ（`release`）ではブランチ切替を行わない安全基準に従い、実際の Django/MySQL テスト実行は未実施です。Git 上のコンフリクト確認（`git merge-tree`）のみ実施済みです。

| # | 確認項目 | 対象メソッド | 画面での操作 | 期待結果 | 結果 |
| - | -------- | ------------ | ------------ | -------- | ---- |
| 1 | マージコンフリクト確認 | `git merge-tree` | N/A | `release` との差分でコンフリクトが発生しないこと | OK |
| 2 | ファミリ解除の正常系 | `POST /api/project/remove-project-family/` | N/A | `project_info.family_id` が `NULL` に更新され 200 OK が返る | 未実施 |
| 3 | Stale 状態（ファミリ不一致）の検出 | `POST /api/project/remove-project-family/` | N/A | 更新されず 409 Conflict が返る | 未実施 |
| 4 | 存在しないプロジェクト ID の指定 | `POST /api/project/remove-project-family/` | N/A | 404 Not Found が返る | 未実施 |
| 5 | 管理者権限（`USER_GR_ADMIN`）なし | `POST /api/project/remove-project-family/` | N/A | 403 Forbidden が返る | 未実施 |
| 6 | 不正なパラメータ（`project_id: 0`） | `POST /api/project/remove-project-family/` | N/A | 400 Bad Request が返る | 未実施 |

---

### 影響度・リスク評価

- [x] 低リスク（破壊的変更なし）
- [ ] 中リスク（後方互換性あり）
- [ ] 高リスク（破壊的変更またはデータへの影響あり）

- **評価根拠**: 既存の API やモデル構造の変更はなく、独立した新規エンドポイントの追加であるため、既存機能への破壊的影響はありません。
- **残存リスク**: 実 DB（MySQL）でのインテグレーションテストおよび UI 結合テストは未実施のため、マージ後のステージング環境での疎通確認が必要です。

---

### チェックリスト

- [x] コードがプロジェクトのコーディング規約に従っている
- [x] テストが追加または更新されている
- [x] 必要に応じてドキュメントが更新されている
- [x] 秘密情報や機密データがコミットされていない

---

### 関連チケット

- SQ8 (`natv/sq8/feature/remove_family`)

---

# English Version

---

## Pull Request Overview

### Summary

- Added a new API endpoint `POST /api/project/remove-project-family/` to disassociate a project from its family by updating `project.family_id = NULL`.
- Utilizes optimistic locking / concurrency checking: the update only executes if the project currently belongs to the requested `family_code`.
- Returns `409 Conflict` if the family relation is already stale/changed, and `404 Not Found` if the project does not exist.

### Type of Change

Please select the appropriate type:

- [ ] Bugfix
- [x] Feature
- [ ] Infrastructure
- [ ] Refactor
- [ ] Documentation

---

### Motivation and Context

- **Previous Behavior**: There was no standalone endpoint to safely remove a project's family assignment, making it difficult to unbind families independently via the management interface.
- **Problem & Risk**: In concurrent operations, if a user submitted an unbind request based on an outdated view, there was a risk of overwriting or unbinding an already reassigned project.
- **Purpose**: Allow authorized administrators (`USER_GR_ADMIN`) to safely clear `project.family_id` to `NULL` while verifying that the current database state matches the expected family code.

---

### Changes Made

- `project/urls.py`:
  - Added URL route `path('remove-project-family/', views.remove_project_family)`.
- `project/seirializers.py`:
  - Added `RemoveProjectFamilySerializer` validating `project_id` (integer >= 1) and `family` (non-blank string).
- `project/views.py`:
  - Implemented `remove_project_family(request)` view.
  - Applied authentication and `USER_GR_ADMIN` group permission check (unauthorized requests return `403 Forbidden`).
  - Executed transactional raw SQL inside `transaction.atomic()`: `UPDATE project_info AS project JOIN family AS fam ON project.family_id = fam.id SET project.family_id = NULL WHERE project.id = %s AND fam.family_code = %s`.
  - When `cursor.rowcount == 0`, checks project existence: returns `409 Conflict` ("Project is no longer in this family.") if project exists, or `404 Not Found` ("Project not found.") if not.
  - Returns `200 OK` (`status: "success"`) upon successful disassociation.
- `project/swagger_docs.py`:
  - Created `remove_project_family_docs` decorator defining request body schema and response specifications (200, 400, 401, 403, 404, 409, 500).
- `project/tests/test_remove_project_family.py`:
  - Created test suite `RemoveProjectFamilyTests` covering successful removal, stale state 409 response, 403 permission rejection, and 400 invalid project ID.

---

### Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [x] Not tested (please explain)

> *Note: Unit test cases (`test_remove_project_family.py`) were committed on the feature branch. However, to preserve the current workspace branch state (`release`), live Django/MySQL tests were not executed in this environment. Clean mergeability was verified via `git merge-tree`.*

| # | Check Item | Target Method | Screen Operation | Expected Result | Result |
| - | ---------- | ------------- | ---------------- | --------------- | ------ |
| 1 | Merge conflict check | `git merge-tree` | N/A | Merges cleanly with `release` without conflicts | Passed |
| 2 | Successful family removal | `POST /api/project/remove-project-family/` | N/A | `project_info.family_id` is set to `NULL` and returns 200 OK | Not executed |
| 3 | Stale family state detection | `POST /api/project/remove-project-family/` | N/A | No rows updated; returns 409 Conflict | Not executed |
| 4 | Non-existent project ID | `POST /api/project/remove-project-family/` | N/A | Returns 404 Not Found | Not executed |
| 5 | Unauthorized non-admin user | `POST /api/project/remove-project-family/` | N/A | Returns 403 Forbidden | Not executed |
| 6 | Invalid parameter (`project_id: 0`) | `POST /api/project/remove-project-family/` | N/A | Returns 400 Bad Request | Not executed |

---

### Impact & Risk Assessment

- [x] Low risk (no breaking changes)
- [ ] Medium risk (backward compatible)
- [ ] High risk (breaking change or data-impacting)

- **Justification**: This is an additive change introducing a standalone endpoint without modifying existing routes, database schemas, or contracts.
- **Residual Risk**: Live database and integration tests against real MySQL instances have not been executed locally; verification should be conducted in staging prior to release.

---

### Checklist

- [x] Code follows the project coding standards
- [x] Tests have been added or updated
- [x] Documentation has been updated if needed
- [x] No secrets or sensitive data are committed

---

### Related Issues / Tickets

- SQ8 (`natv/sq8/feature/remove_family`)

---

# Bản tiếng Việt

---

## Tổng quan Pull Request

### Tóm tắt

- Bổ sung API endpoint mới `POST /api/project/remove-project-family/` để gỡ một project ra khỏi family (cập nhật `project.family_id = NULL`).
- Áp dụng cơ chế kiểm tra trạng thái tương tranh (optimistic lock): chỉ gỡ khi project thực sự đang thuộc về `family_code` được gửi lên.
- Trả về mã lỗi `409 Conflict` nếu dữ liệu đã bị thay đổi trước đó (stale state) và `404 Not Found` nếu project không tồn tại trong hệ thống.

### Loại thay đổi

Vui lòng chọn loại phù hợp:

- [ ] Sửa lỗi
- [x] Tính năng
- [ ] Hạ tầng
- [ ] Tái cấu trúc
- [ ] Tài liệu

---

### Động cơ và bối cảnh

- **Hành vi trước đây**: Chưa có API chuyên biệt để gỡ bỏ độc lập mối quan hệ giữa project và family, khiến việc quản lý hoặc huỷ liên kết family từ giao diện quản trị gặp hạn chế.
- **Vấn đề & rủi ro**: Trong trường hợp nhiều người dùng thao tác đồng thời, nếu một người gửi yêu cầu gỡ family dựa trên dữ liệu màn hình cũ thì có nguy cơ ghi đè hoặc gỡ nhầm dữ liệu mới.
- **Mục đích**: Cung cấp API cho nhóm quản trị viên (`USER_GR_ADMIN`) cho phép gỡ liên kết family (`family_id = NULL`) một cách an toàn, chỉ thực thi khi dữ liệu trên DB khớp với `family_code` được yêu cầu.

---

### Nội dung thay đổi

- `project/urls.py`:
  - Khai báo routing mới `path('remove-project-family/', views.remove_project_family)`.
- `project/seirializers.py`:
  - Định nghĩa serializer `RemoveProjectFamilySerializer` validate `project_id` (số nguyên >= 1) và `family` (chuỗi ký tự không để trống).
- `project/views.py`:
  - Hiện thực hàm view `remove_project_family(request)`.
  - Kiểm tra xác thực và quyền nhóm admin `USER_GR_ADMIN` (trả về `403 Forbidden` nếu không đủ quyền).
  - Thực thi raw SQL trong `transaction.atomic()`: `UPDATE project_info AS project JOIN family AS fam ON project.family_id = fam.id SET project.family_id = NULL WHERE project.id = %s AND fam.family_code = %s`.
  - Xử lý khi không có dòng nào được cập nhật (`cursor.rowcount == 0`): truy vấn kiểm tra project có tồn tại không để trả về `409 Conflict` ("Project is no longer in this family.") hoặc `404 Not Found` ("Project not found.").
  - Trả về `200 OK` (`status: "success"`) khi gỡ thành công.
- `project/swagger_docs.py`:
  - Khai báo decorator Swagger `remove_project_family_docs` mô tả chi tiết request body và các mã response (200, 400, 401, 403, 404, 409, 500).
- `project/tests/test_remove_project_family.py`:
  - Tạo mới bộ test `RemoveProjectFamilyTests` kiểm tra các kịch bản: gỡ thành công (200), dữ liệu stale (409), thiếu quyền admin (403), và project_id không hợp lệ (400).

---

### Kiểm thử

- [ ] Unit test
- [ ] Integration test
- [ ] Kiểm thử thủ công
- [x] Chưa kiểm thử (vui lòng nêu lý do)

> *Lưu ý: Bộ test unit (`test_remove_project_family.py`) đã được viết sẵn trong nhánh feature. Tuy nhiên, nhằm tuân thủ quy tắc giữ an toàn cho nhánh làm việc hiện tại (`release`), kiểm thử thực tế trên Django/MySQL chưa được chạy trực tiếp ở môi trường này. Đã kiểm tra tính tương thích khi merge qua `git merge-tree`.*

| # | Hạng mục kiểm tra | Phương thức mục tiêu | Thao tác trên màn hình | Kết quả mong đợi | Kết quả |
| - | ----------------- | -------------------- | ---------------------- | ---------------- | ------- |
| 1 | Kiểm tra xung đột merge | `git merge-tree` | N/A | Tự động merge sạch sẽ với `release`, không bị conflict | Đạt |
| 2 | Gỡ project khỏi family thành công | `POST /api/project/remove-project-family/` | N/A | `project_info.family_id` chuyển thành `NULL`, trả về 200 OK | Chưa thực hiện |
| 3 | Phát hiện trạng thái cũ (stale family) | `POST /api/project/remove-project-family/` | N/A | Không update dữ liệu, trả về 409 Conflict | Chưa thực hiện |
| 4 | Truyền ID project không tồn tại | `POST /api/project/remove-project-family/` | N/A | Trả về 404 Not Found | Chưa thực hiện |
| 5 | Người dùng không có quyền admin | `POST /api/project/remove-project-family/` | N/A | Trả về 403 Forbidden | Chưa thực hiện |
| 6 | Tham số không hợp lệ (`project_id: 0`) | `POST /api/project/remove-project-family/` | N/A | Trả về 400 Bad Request | Chưa thực hiện |

---

### Đánh giá tác động và rủi ro

- [x] Rủi ro thấp (không có thay đổi phá vỡ tương thích)
- [ ] Rủi ro trung bình (tương thích ngược)
- [ ] Rủi ro cao (thay đổi phá vỡ tương thích hoặc ảnh hưởng dữ liệu)

- **Lý do đánh giá**: Thay đổi chỉ bổ sung một API endpoint độc lập mới, không sửa đổi các route hoặc logic nghiệp vụ hiện hữu, không sửa schema database.
- **Rủi ro còn lại**: Cần kiểm thử tích hợp thực tế với cơ sở dữ liệu MySQL và giao diện FE trên môi trường staging trước khi release.

---

### Danh sách kiểm tra

- [x] Code tuân thủ quy chuẩn của dự án
- [x] Test đã được thêm mới hoặc cập nhật
- [x] Tài liệu đã được cập nhật nếu cần
- [x] Không commit thông tin bí mật hoặc dữ liệu nhạy cảm

---

### Ticket liên quan

- SQ8 (`natv/sq8/feature/remove_family`)
