# Japanese-English-Vietnamese PR Format

Use this structure unless the repository's existing template requires additional sections. Replace all placeholders with evidence from the source-to-target branch diff.

```markdown
---

# 日本語版

---

## Pull Request 概要

### 概要

- <変更の要約>

### 変更タイプ

該当するものを選択してください：

- [ ] バグ修正
- [ ] 機能追加
- [ ] インフラ
- [ ] リファクタリング
- [ ] ドキュメント

---

### 動機と背景

<変更前の状態、問題の原因、ユーザーまたはシステムへの影響、変更の目的>

---

### 変更内容

- <具体的なファイル、関数、API、SQL、またはデータ処理の変更>

---

### テスト

- [ ] ユニットテスト
- [ ] 結合テスト
- [ ] 手動テスト
- [ ] 未テスト（理由を記載）

<実際に実施した確認と未実施の確認を明記>

| # | 確認項目 | 対象メソッド | 画面での操作 | 期待結果 | 結果 |
| - | -------- | ------------ | ------------ | -------- | ---- |
| 1 | <確認項目> | <対象> | <操作または N/A> | <期待結果> | <OK または未実施> |

---

### 影響度・リスク評価

- [ ] 低リスク（破壊的変更なし）
- [ ] 中リスク（後方互換性あり）
- [ ] 高リスク（破壊的変更またはデータへの影響あり）

<リスク判断の根拠と残存リスク>

---

### チェックリスト

- [ ] コードがプロジェクトのコーディング規約に従っている
- [ ] テストが追加または更新されている
- [ ] 必要に応じてドキュメントが更新されている
- [ ] 秘密情報や機密データがコミットされていない

---

### 関連チケット

- <チケット ID。存在しない場合は空欄>

---

# English Version

---

## Pull Request Overview

### Summary

- <Concise change summary>

### Type of Change

Please select the appropriate type:

- [ ] Bugfix
- [ ] Feature
- [ ] Infrastructure
- [ ] Refactor
- [ ] Documentation

---

### Motivation and Context

<Previous behavior, root cause, user or system impact, and purpose of the change>

---

### Changes Made

- <Concrete file, function, API, SQL, or data-processing changes>

---

### Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Not tested (please explain)

<State what was actually verified and what remains untested>

| # | Check Item | Target Method | Screen Operation | Expected Result | Result |
| - | ---------- | ------------- | ---------------- | --------------- | ------ |
| 1 | <Check item> | <Target> | <Operation or N/A> | <Expected result> | <Passed or Not executed> |

---

### Impact & Risk Assessment

- [ ] Low risk (no breaking changes)
- [ ] Medium risk (backward compatible)
- [ ] High risk (breaking change or data-impacting)

<Reason for the risk rating and any residual risk>

---

### Checklist

- [ ] Code follows the project coding standards
- [ ] Tests have been added or updated
- [ ] Documentation has been updated if needed
- [ ] No secrets or sensitive data are committed

---

### Related Issues / Tickets

- <Ticket ID; leave blank if none is known>

---

# Bản tiếng Việt

---

## Tổng quan Pull Request

### Tóm tắt

- <Tóm tắt ngắn gọn thay đổi>

### Loại thay đổi

Vui lòng chọn loại phù hợp:

- [ ] Sửa lỗi
- [ ] Tính năng
- [ ] Hạ tầng
- [ ] Tái cấu trúc
- [ ] Tài liệu

---

### Động cơ và bối cảnh

<Hành vi trước đây, nguyên nhân gốc, ảnh hưởng tới người dùng hoặc hệ thống và mục đích của thay đổi>

---

### Nội dung thay đổi

- <Các thay đổi cụ thể về file, hàm, API, SQL hoặc xử lý dữ liệu>

---

### Kiểm thử

- [ ] Unit test
- [ ] Integration test
- [ ] Kiểm thử thủ công
- [ ] Chưa kiểm thử (vui lòng nêu lý do)

<Nêu rõ những gì đã được kiểm tra thực tế và những gì chưa được kiểm tra>

| # | Hạng mục kiểm tra | Phương thức mục tiêu | Thao tác trên màn hình | Kết quả mong đợi | Kết quả |
| - | ----------------- | -------------------- | ---------------------- | ---------------- | ------- |
| 1 | <Hạng mục kiểm tra> | <Mục tiêu> | <Thao tác hoặc N/A> | <Kết quả mong đợi> | <Đạt hoặc Chưa thực hiện> |

---

### Đánh giá tác động và rủi ro

- [ ] Rủi ro thấp (không có thay đổi phá vỡ tương thích)
- [ ] Rủi ro trung bình (tương thích ngược)
- [ ] Rủi ro cao (thay đổi phá vỡ tương thích hoặc ảnh hưởng dữ liệu)

<Lý do đánh giá mức rủi ro và các rủi ro còn lại>

---

### Danh sách kiểm tra

- [ ] Code tuân thủ quy chuẩn của dự án
- [ ] Test đã được thêm mới hoặc cập nhật
- [ ] Tài liệu đã được cập nhật nếu cần
- [ ] Không commit thông tin bí mật hoặc dữ liệu nhạy cảm

---

### Ticket liên quan

- <ID ticket; để trống nếu chưa xác định>
```

## Translation Consistency

Before delivery, verify that all three versions agree on:

- change type and risk level;
- files, functions, endpoints, fields, and tables;
- tests passed, tests not executed, and remaining validation;
- ticket identifiers and scope boundaries.
