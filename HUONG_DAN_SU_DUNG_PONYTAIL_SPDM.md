# Hướng Dẫn Tích Hợp Và Sử Dụng Ponytail Trong Dự Án SPDM_Backend

> **Repo nguồn:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail.git)  
> **Triết lý cốt lõi:** *"The best code is the code never written"* (Code tốt nhất là dòng code không bao giờ phải viết).

---

## 1. Ponytail Là Gì & Tại Sao Dự Án SPDM Cần?

### 1.1. Ponytail là gì?
**Ponytail** không phải là một thư viện Python thông thường (`pip install`), mà là một **AI Agent Skill & Ruleset Framework** chuyên biệt dành cho các AI Coding Agent (Antigravity, Codex, Cursor, PyCharm / Junie, Claude Code, GitHub Copilot, Windsurf...).

Mục tiêu chính của Ponytail là biến AI thành một **"Lazy Senior Developer"**:
- **"Lazy" ở đây là lười thông minh**: Giải quyết trọn vẹn bài toán bằng lượng code mới ít nhất có thể.
- **Ngăn chặn Over-Engineering**: Loại bỏ thói quen tự ý thêm abstractions, wrapper, design pattern phức tạp không cần thiết, hoặc cài thêm thư viện bên ngoài bừa bãi.
- **Quy tắc trách nhiệm (Accountability)**: Cuối mỗi câu trả lời, AI bắt buộc phải báo cáo rõ ràng:
  1. Những gì đã chủ động bỏ qua hoặc chưa kiểm tra.
  2. Các rủi ro tiềm ẩn mà lập trình viên cần lưu ý.

---

### 1.2. Tại sao Ponytail cực kỳ phù hợp với SPDM_Backend?
Dự án **SPDM Backend** là một hệ thống Django + Django REST Framework (DRF) + MySQL quy mô lớn, nhiều module phức tạp (`scenario`, `rfl_list`, `rfl_tree`, `parameter`, `utils`, `scripts`, `models_auto_app`...).

Khi không có Ponytail, AI thường mắc các lỗi điển hình:
1. **Tạo thêm helper trùng lặp**: Tự viết các hàm tiện ích mới trong khi thư mục `utils/` của SPDM đã có sẵn hàng loạt helper xử lý database, upload file, format, auth...
2. **Over-engineering kiến trúc Django**: Tự vẽ thêm Service Layer, Repository Pattern, Factory class... trong khi Django ORM, Serializer và ViewSet chuẩn đã giải quyết tốt.
3. **Cài thư viện bên ngoài không cần thiết**: Đòi cài thêm `requests`, `pandas`, `dateutil`... trong khi standard library hoặc `requirements.txt` hiện tại đã có.
4. **Không để ý caller cũ**: Sửa signature một hàm dùng chung khiến các module khác bị lỗi.
5. **Bỏ quên Transaction & DB Safety**: Quên bọc `transaction.atomic()` khi thực hiện ghi/xóa dữ liệu quan trọng trên MySQL.

Ponytail giải quyết triệt để vấn đề này bằng cách ép AI tuân thủ **6 bậc lọc quyết định (The Smallest Complete Change)**:
1. **Có cần tồn tại không? (YAGNI)**: Bỏ qua tính năng thừa không ai yêu cầu.
2. **Codebase đã có chưa?**: Tìm và tái sử dụng helper/pattern trong SPDM (`utils/`, shared services).
3. **Standard library / Django framework có sẵn không?**: Ưu tiên tính năng gốc của Python và Django.
4. **Dependency đã cài có giải quyết được không?**: Dùng các package đã có trong `requirements.txt`.
5. **Có thể viết thành 1 dòng rõ nghĩa không?**: Ưu tiên 1 dòng dễ hiểu.
6. **Nếu phải viết mới**: Viết lượng code tối thiểu, giữ đúng conventions của SPDM.

---

## 2. Chi Tiết Cách Cài Đặt Cho Từng Môi Trường Làm Việc

Tùy vào công cụ/editor bạn sử dụng để code SPDM_Backend, hãy chọn cách cài đặt tương ứng:

```
SPDM_Backend (Django)
├── Cách 1: Antigravity IDE & CLI (Khuyên dùng hiện tại)
├── Cách 2: OpenAI Codex CLI / Desktop
├── Cách 3: PyCharm / JetBrains IDE (Qua AGENTS.md hoặc Copilot)
├── Cách 4: Cursor IDE
└── Cách 5: Claude Code
```

---

### Cách 1: Cài đặt cho Antigravity (IDE & CLI)

Antigravity hỗ trợ nạp quy tắc tự động qua file `AGENTS.md` tại thư mục gốc của dự án, đồng thời hỗ trợ cài các Skills thông qua `agy plugin`.

#### Bước 1.1: Tạo file `AGENTS.md` tại root của SPDM_Backend
Tạo file `/Users/TrongKieu/untitled/XX0_SPDM-Backend-/AGENTS.md` với nội dung rút gọn chuẩn của Ponytail (kết hợp các lưu ý cho SPDM). Khi mở workspace SPDM Backend, Antigravity sẽ tự động đọc file này làm **Always-On Rules**.

*(Nội dung file `AGENTS.md` mẫu được cung cấp ở Mục 5 của tài liệu này).*

#### Bước 1.2: Cài đặt bộ 6 Skills Ponytail qua CLI (Tùy chọn)
Nếu bạn sử dụng Antigravity CLI, chạy lệnh sau trong Terminal:
```bash
agy plugin install https://github.com/DietrichGebert/ponytail
```
Lệnh này sẽ nạp 6 kỹ năng (`ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`) và cho phép bạn gọi trực tiếp bằng các slash commands như `/ponytail-review`.

---

### Cách 2: Cài đặt cho OpenAI Codex CLI & Codex Desktop

Nếu bạn phát triển bằng Codex CLI hoặc Codex Desktop:

#### Bước 2.1: Thêm Marketplace và Cài đặt Plugin
Mở Terminal và chạy 2 lệnh riêng biệt:
```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

#### Bước 2.2: Kích hoạt Hooks và Skills
1. Chạy lệnh `codex`.
2. Gõ `/hooks`, kiểm tra và tin tưởng (trust) hai lifecycle hooks của Ponytail (`sessionStart` và `beforeSubmitPrompt`).
3. Mở thread mới. Bạn có thể gọi các skill bằng tiền tố `$`:
   - `$ponytail:ponytail` (Bật chế độ lazy senior dev)
   - `$ponytail:ponytail-review` (Review code)
   - `$ponytail:ponytail-help` (Xem trợ giúp)

---

### Cách 3: Cài đặt cho PyCharm / JetBrains IDE

Vì SPDM Backend được cấu hình dự án với PyCharm (`.idea/`):

#### Cách 3.1: Sử dụng qua file `AGENTS.md` (Cho JetBrains Junie / Codex extension)
1. Đảm bảo file `AGENTS.md` đã có mặt tại thư mục gốc của SPDM Backend.
2. Trong PyCharm: Vào **Settings** → **Tools** → **Junie** (hoặc plugin AI tương ứng) → **Project Settings** → Trỏ **Guidelines Path** tới file `AGENTS.md`.

#### Cách 3.2: Sử dụng với GitHub Copilot trong PyCharm
Tạo file `.github/copilot-instructions.md` trong SPDM Backend và sao chép toàn bộ nội dung từ `AGENTS.md` vào. Copilot trong PyCharm sẽ tự động áp dụng quy tắc này trong mọi gợi ý chat và inline completion.

---

### Cách 4: Cài đặt cho Cursor

Nếu bạn hoặc đồng nghiệp mở SPDM Backend bằng Cursor:

#### Lựa chọn A (Đơn giản nhất - Rule File):
Tạo file `.cursor/rules/ponytail.mdc` trong thư mục gốc của dự án SPDM Backend:
```bash
mkdir -p .cursor/rules
curl -sSL https://raw.githubusercontent.com/DietrichGebert/ponytail/main/.cursor/rules/ponytail.mdc -o .cursor/rules/ponytail.mdc
```

#### Lựa chọn B (Dùng Lifecycle Hooks - Quản lý level linh hoạt):
Clone repo và cài đặt native hooks vào cấu hình dự án:
```bash
git clone https://github.com/DietrichGebert/ponytail /tmp/ponytail
node /tmp/ponytail/scripts/cursor-hooks.js install --project
```
Khi dùng hooks, bạn có thể gõ trực tiếp trong chat Cursor: `/ponytail lite`, `/ponytail full`, `/ponytail ultra` hoặc `/ponytail off`.

---

### Cách 5: Cài đặt cho Claude Code

Trong cửa sổ lệnh Claude Code, nhập lần lượt 2 lệnh (gửi thành 2 prompt riêng biệt):
```
/plugin marketplace add DietrichGebert/ponytail
```
```
/plugin install ponytail@ponytail
```

---

## 3. Hệ Thống Các Lệnh & Kỹ Năng Của Ponytail

Ponytail cung cấp **3 cấp độ hoạt động (Levels)** và **6 kỹ năng chuyên sâu (Skills)**:

### 3.1. Ba cấp độ hoạt động (Intensity Levels)

| Mức độ | Lệnh kích hoạt | Hành vi đối với SPDM Backend |
| :--- | :--- | :--- |
| **Lite** | `/ponytail lite` | Thực hiện đúng yêu cầu, nhưng nếu có cách ngắn hơn (1 dòng hoặc dùng helper có sẵn) thì AI sẽ nêu ra phương án đó để bạn duyệt trước. |
| **Full** *(Mặc định)* | `/ponytail` hoặc `/ponytail full` | Áp dụng triệt để 6 bậc lọc. Không sinh boilerplate, tận dụng triệt để `utils/`, không cài package mới, diff ngắn nhất có thể. |
| **Ultra** | `/ponytail ultra` | **Phản biện mạnh mẽ**: Trước khi bắt tay vào code, AI sẽ chất vấn xem tính năng này có thực sự cần thiết không, có nguy cơ làm phình codebase không. |

*Để tắt chế độ Ponytail, chỉ cần nói: "stop ponytail" hoặc gõ `/ponytail off`.*

---

### 3.2. Bộ 6 Kỹ Năng Đắc Lực Cho SPDM Backend

#### 1. `ponytail` (Chế độ cốt lõi)
Tự động kích hoạt tư duy lập trình tinh gọn. Kết thúc mỗi câu trả lời luôn có 2 dòng trách nhiệm:
```text
[Skipped / Not checked]: Không kiểm tra module X, không tạo wrapper serializer.
[Risk]: Cần chạy migration trên MySQL trước khi gọi endpoint này.
```

#### 2. `ponytail-review` (Review code cực chuẩn)
Review git diff, commit gần nhất hoặc PR theo tư duy của Tech Lead trực ca:
- **Thứ tự ưu tiên**: Đúng logic > An toàn bảo mật > Chịu tải thực tế > Có test > Tốc độ > Tinh gọn.
- **Rà soát đặc thù SPDM**:
  - Có bị lỗi N+1 Query trên MySQL không (`select_related`, `prefetch_related`)?
  - Các thao tác sửa đổi nhiều bảng có bọc `transaction.atomic()` không?
  - Sửa hàm này có làm hỏng các nơi khác đang gọi (grep callers) không?
- **Cách gọi**:
  ```text
  /ponytail-review
  hoặc
  Review giúp tôi các thay đổi chưa commit theo ponytail-review
  ```

#### 3. `ponytail-audit` (Rà soát toàn bộ module hoặc repo)
Rà soát tìm dead code, code dư thừa hoặc các helper bị viết lặp:
- **Ứng dụng trong SPDM**:
  ```text
  /ponytail-audit folder utils/
  hoặc
  /ponytail-audit module scenario/
  ```
  AI sẽ chỉ ra những hàm nào trong `scenario/` đang làm lại việc mà `utils/` đã có, hoặc những class nào không còn ai gọi.

#### 4. `ponytail-debt` (Sổ nợ kỹ thuật - Technical Debt Ledger)
Ponytail quy định khi bạn muốn viết một giải pháp tạm thời (shortcut) để kịp deadline, bạn phải đặt comment theo chuẩn:
```python
# shortcut: chỉ hỗ trợ phân trang tối đa 100 record, nâng cấp khi FE hỗ trợ cursor pagination
```
Khi gọi `/ponytail-debt`, AI sẽ quét toàn bộ dự án và lập bảng thống kê tất cả các shortcut nợ kỹ thuật cùng điều kiện kích hoạt nâng cấp.

#### 5. `ponytail-gain` (Xem bảng thành tích tiết kiệm)
Hiển thị thống kê giảm thiểu code của Ponytail trên benchmark chuẩn (giảm ~53% LOC thừa, tiết kiệm chi phí và token).

#### 6. `ponytail-help` (Tra cứu nhanh)
Hiển thị thẻ tóm tắt cú pháp và các lệnh.

---

## 4. Hướng Dẫn Thực Chiến Trong Dự Án SPDM_Backend

### Tình huống 1: Yêu cầu AI viết một API Endpoint mới
*Thay vì để AI tự tạo Service/Repository rườm rà:*

> **Prompt mẫu:**
> ```text
> /ponytail
> Tạo API xuất danh sách parameter theo định dạng JSON tại module parameter/views.py.
> Yêu cầu: Tuân thủ quy chuẩn SPDM, dùng trực tiếp DRF ModelViewSet/Serializer sẵn có, không tạo service layer thừa thãi.
> ```

### Tình huống 2: Xử lý logic dùng chung (Helper/Util)
*Tránh việc AI tự viết lại hàm mới:*

> **Prompt mẫu:**
> ```text
> /ponytail full
> Tôi cần hàm validate định dạng ngày tháng và xuất file Excel cho kết quả rfl_list.
> Hãy kiểm tra trong thư mục utils/ trước xem đã có helper tương tự chưa. Nếu đã có thì tái sử dụng, không viết hàm mới.
> ```

### Tình huống 3: Review trước khi tạo PR
*Đảm bảo an toàn cơ sở dữ liệu MySQL và tương thích ngược:*

> **Prompt mẫu:**
> ```text
> /ponytail-review
> Review nhánh hiện tại trước khi tạo PR vào master.
> Chú ý đặc biệt: MySQL transaction, query optimization, rủi ro làm gãy các caller cũ trong scenario và rlist.
> ```

---

## 5. File `AGENTS.md` Mẫu Dành Riêng Cho SPDM_Backend

Dưới đây là nội dung đề xuất cho file `AGENTS.md` đặt tại thư mục gốc `/Users/TrongKieu/untitled/XX0_SPDM-Backend-/AGENTS.md`. File này đã được tinh chỉnh để kết hợp hoàn hảo giữa **Ponytail Core** và **Kiến trúc SPDM Backend**:

```markdown
# Ponytail: SPDM Backend Lazy Senior Dev Mode

You are a lazy senior developer working on the SPDM Django Backend project.
The best code is the code never written. Solve the whole problem with the least new code.
Always end your reply with 1-2 lines stating:
1. What you skipped or did not check.
2. Any risk the user must know.

## The Smallest Complete Change (6-Step Filter)

Take the first option that fully works:
1. **Does it need to exist? (YAGNI)**: Skip features, wrappers, and options nobody asked for. Name them in one line.
2. **Already in SPDM?**:
   - Check `utils/`, existing models, and serializers before writing anything new.
   - Reuse existing patterns and helpers.
3. **Standard library or Django/DRF built-in?**: Use native Django features (ORM, generic views, validators) instead of custom abstractions.
4. **Already installed dependency?**: Use packages already in `requirements.txt`. Never add a new dependency for a few lines.
5. **Can it be a clean, readable one-liner?**: Keep it one line.
6. **Otherwise**: The absolute minimum code that works.

## SPDM Specific Rules

- **Database Safety (MySQL 8.x)**:
  - Any mutating operation touching multiple tables must use `transaction.atomic()`.
  - Check for N+1 queries. Use `select_related()` and `prefetch_related()`.
  - Never delete foreign-key constrained records blindly.
- **Do Not Break Callers**:
  - Before modifying a shared function or method signature in `utils/` or common apps, grep every caller in the codebase.
- **No Unnecessary Architecture**:
  - Do NOT create repository layers or service wrappers unless the existing module pattern explicitly demands it.
- **Shortcuts & Tech Debt**:
  - If a shortcut is taken for speed, leave a comment: `# shortcut: <the limit>, <when to upgrade>`.

## What Never to Cut
Never compromise on:
- Validation at API trust boundaries (`serializers.ValidationError`).
- Database transaction safety and data integrity.
- Authentication & permissions checks.
- Backwards compatibility with active frontend callers.
```

---

## 6. Tổng Kết & Checklist Bắt Đầu

Để bắt đầu ngay bây giờ với SPDM_Backend:

1. [ ] **Tạo file `AGENTS.md`** tại root của `XX0_SPDM-Backend-` (sao chép nội dung ở Mục 5).
2. [ ] **Trong phiên chat với AI**, gõ `/ponytail` hoặc kích hoạt skill `spdm-yagni` / `ponytail`.
3. [ ] **Khi hoàn thành một tính năng**, luôn chạy `/ponytail-review` để AI rà soát lại diff trước khi commit.
4. [ ] **Thỉnh thoảng chạy `/ponytail-debt`** để quản lý các phần code shortcut đã tạm hoãn.
