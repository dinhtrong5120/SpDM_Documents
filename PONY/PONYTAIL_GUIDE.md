# Hướng Dẫn Tích Hợp Và Sử Dụng Ponytail Trong Dự Án SPDM_Backend

> **Repo nguồn:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail.git)  
> **Tài liệu đầy đủ:** Xem chi tiết tại [HUONG_DAN_SU_DUNG_PONYTAIL_SPDM.md](file:///Users/TrongKieu/Developer/personal/SpDM_Documents/HUONG_DAN_SU_DUNG_PONYTAIL_SPDM.md)

---

## 1. Tóm Tắt Nhanh

**Ponytail** là bộ quy tắc và kỹ năng AI ("Lazy Senior Dev Mode") giúp các trợ lý AI lập trình:
- Giải quyết trọn vẹn bài toán với **lượng code mới ít nhất**.
- **Không over-engineering**, không tự ý sinh Service/Repository wrapper thừa thãi.
- **Tái sử dụng tối đa** các tiện ích sẵn có trong `utils/` và tính năng gốc của Django / DRF.
- **Bắt buộc minh bạch**: Luôn kết thúc bằng 1-2 dòng nêu rõ những gì đã bỏ qua và rủi ro cần biết.

---

## 2. Cách Kích Hoạt Trong SPDM_Backend

Dự án đã có file cấu hình quy tắc tại root: [`AGENTS.md`](file:///Users/TrongKieu/untitled/XX0_SPDM-Backend-/AGENTS.md).

### Sử dụng với các công cụ:
- **Antigravity / Gemini**: Tự động nhận diện `AGENTS.md`. Có thể cài trọn bộ 6 skill bằng `agy plugin install https://github.com/DietrichGebert/ponytail`.
- **Codex**: Chạy `codex plugin marketplace add DietrichGebert/ponytail` và `codex plugin add ponytail@ponytail`.
- **Cursor**: Copy file quy tắc vào `.cursor/rules/ponytail.mdc` hoặc chạy `node scripts/cursor-hooks.js install --project`.
- **PyCharm**: Cấu hình file `AGENTS.md` trong Settings AI Guidelines hoặc dùng GitHub Copilot instructions.

---

## 3. Các Lệnh Thường Dùng

- `/ponytail`: Bật chế độ lập trình tối giản (mặc định - level full).
- `/ponytail lite`: Làm đúng yêu cầu, gợi ý phương án ngắn hơn nếu có.
- `/ponytail ultra`: Phản biện lại yêu cầu nếu thấy over-engineering trước khi code.
- `/ponytail-review`: Review chất lượng code diff / PR (bảo mật, MySQL transaction, N+1 query, caller impact).
- `/ponytail-audit`: Quét dead code, logic trùng lặp trong module.
- `/ponytail-debt`: Liệt kê các comment `# shortcut:` đang nợ kỹ thuật trong dự án.
- `/ponytail off` hoặc `stop ponytail`: Trở lại chế độ thông thường.
