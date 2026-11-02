# Frontend Japanese-English-Vietnamese PR Format

Use this structure unless the repository's existing template requires additional sections. Replace all placeholders with evidence from the source-to-target branch diff. Omit conditional UI-evidence sections when irrelevant. Preserve additional repository requirements.

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

- <対象画面・ルート・コンポーネント、変更前後の動作、関連する API・状態管理の変更>

---

### テスト

- [ ] ユニットテスト
- [ ] 結合テスト
- [ ] 手動テスト
- [ ] 未テスト（理由を記載）

<実行したコマンドと結果、関連するブラウザー・画面操作確認、実 Backend との連携確認の実施状況と制約を明記。ビルド成功と UI 動作確認を区別する>

| # | 確認項目 | 対象画面 / コンポーネント | 画面での操作 | 期待結果 | 結果 |
| - | -------- | ------------ | ------------ | -------- | ---- |
| 1 | <確認項目> | <対象> | <操作または N/A> | <期待結果> | <OK / 失敗 / 実行不可（理由） / 未実施> |

---

### UI の確認資料（該当する場合のみ）

<実際の画像・成果物へのリンク、対象画面と状態。変更前後の画像は両方存在する場合のみ記載。関連する表示幅・言語・権限の確認結果または未実施を明記>

---

### 影響度・リスク評価

- [ ] 低リスク
- [ ] 中リスク
- [ ] 高リスク

<対象フロー、共通コンポーネントの利用箇所、権限・データ送信への影響に基づく根拠、残存リスク、該当する API 依存関係>

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

- <Affected screens/routes/components, before-and-after behavior, and relevant API/state changes>

---

### Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Not tested (please explain)

<State executed commands and outcomes, relevant browser/manual coverage, real Backend integration coverage, and limitations. Distinguish build success from UI verification>

| # | Check Item | Screen / Component | Screen Operation | Expected Result | Result |
| - | ---------- | ------------- | ---------------- | --------------- | ------ |
| 1 | <Check item> | <Target> | <Operation or N/A> | <Expected result> | <Passed / Failed / Blocked (reason) / Not executed> |

---

### UI Evidence (only when relevant)

<Links to actual screenshots/artifacts and the screen/state shown. Include before/after images only when both exist. State results or gaps for relevant viewport, locale, and role checks>

---

### Impact & Risk Assessment

- [ ] Low risk
- [ ] Medium risk
- [ ] High risk

<Reason based on affected flows, shared callers, permissions/data submission; residual risks and applicable API dependencies>

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

- <Màn hình/route/component bị ảnh hưởng, hành vi trước/sau và thay đổi API/state liên quan>

---

### Kiểm thử

- [ ] Unit test
- [ ] Integration test
- [ ] Kiểm thử thủ công
- [ ] Chưa kiểm thử (vui lòng nêu lý do)

<Ghi lệnh đã chạy và kết quả, phạm vi kiểm tra trình duyệt/thủ công, tích hợp Backend thật và giới hạn. Phân biệt build thành công với xác minh hành vi UI>

| # | Hạng mục kiểm tra | Màn hình / Component | Thao tác trên màn hình | Kết quả mong đợi | Kết quả |
| - | ----------------- | -------------------- | ---------------------- | ---------------- | ------- |
| 1 | <Hạng mục kiểm tra> | <Mục tiêu> | <Thao tác hoặc N/A> | <Kết quả mong đợi> | <Đạt / Không đạt / Không thể thực hiện (lý do) / Chưa thực hiện> |

---

### Bằng chứng giao diện (chỉ khi liên quan)

<Link ảnh/artifact thực tế và màn hình/trạng thái tương ứng. Chỉ thêm ảnh trước/sau khi có đủ cả hai. Ghi kết quả hoặc phần chưa kiểm tra về viewport, ngôn ngữ và quyền liên quan>

---

### Đánh giá tác động và rủi ro

- [ ] Rủi ro thấp
- [ ] Rủi ro trung bình
- [ ] Rủi ro cao

<Căn cứ từ luồng bị ảnh hưởng, nơi dùng component chung, quyền/gửi dữ liệu; rủi ro còn lại và phụ thuộc API nếu có>

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
- affected screens, routes, components, endpoints, payload fields, and state behavior;
- tests passed, tests not executed, and remaining validation;
- ticket identifiers and scope boundaries.
