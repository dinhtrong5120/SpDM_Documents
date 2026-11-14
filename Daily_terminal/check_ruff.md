# Kiểm tra lỗi ruff trong vùng vừa sửa xong
```bash
python3 - <<'PY'
import json
import re
import subprocess
from pathlib import Path

files = subprocess.check_output([
    "git", "diff", "--name-only", "-z",
    "--diff-filter=ACMR", "HEAD", "--", "*.py",
]).decode().strip("\0").split("\0")
files = [f for f in files if f]

print("\n" + "=" * 60)
print("KẾT QUẢ KIỂM TRA RUFF TRONG VÙNG THAY ĐỔI")
print("=" * 60)

if not files:
    print("Không có file Python thay đổi.")
    print("=" * 60)
    raise SystemExit(0)

print("Các file được kiểm tra:")
for file in files:
    print(f"  - {file}")
print("-" * 60)

ranges = {}
for file in files:
    diff = subprocess.check_output([
        "git", "diff", "--no-ext-diff", "--no-renames",
        "--unified=0", "HEAD", "--", file,
    ], text=True)
    ranges[str(Path(file).resolve())] = [
        (int(start), int(start) + int(count or 1) - 1)
        for start, count in re.findall(
            r"^@@ .*? \+(\d+)(?:,(\d+))? @@", diff, re.M
        )
        if int(count or 1) > 0
    ]

result = subprocess.run([
    "ruff", "check", "--force-exclude",
    "--output-format=json", *files,
], capture_output=True, text=True)

if result.returncode not in (0, 1):
    print("Không chạy được Ruff:")
    print(result.stderr or result.stdout)
    print("=" * 60)
    raise SystemExit(result.returncode)

found = 0
for error in json.loads(result.stdout):
    first = error["location"]["row"]
    last = (error.get("end_location") or error["location"])["row"]

    if any(
        first <= end and last >= start
        for start, end in ranges.get(error["filename"], [])
    ):
        found += 1
        file = Path(error["filename"]).relative_to(Path.cwd())
        column = error["location"]["column"]
        print(f"{file}:{first}:{column}: {error['code']} {error['message']}")

if found == 0:
    print("Không có lỗi Ruff trong vùng thay đổi.")

print("-" * 60)
print(f"Tổng: {found} lỗi Ruff trong vùng thay đổi.")
print("=" * 60)

raise SystemExit(1 if found else 0)
PY
```

# Kiểm tra format code
```bash
python3 - <<'PY'
import re
import subprocess

files = subprocess.check_output([
    "git", "diff", "--name-only", "-z",
    "--diff-filter=ACMR", "HEAD", "--", "*.py",
]).decode().strip("\0").split("\0")
files = [file for file in files if file]

print("\n" + "=" * 60)
print("KIỂM TRA FORMAT TRONG VÙNG THAY ĐỔI")
print("=" * 60)

if not files:
    print("Không có file Python thay đổi.")
    print("=" * 60)
    raise SystemExit(0)

failed_files = set()
failed_ranges = 0
checked_ranges = 0

for file in files:
    diff = subprocess.check_output([
        "git", "diff", "--no-ext-diff", "--no-renames",
        "--unified=0", "HEAD", "--", file,
    ], text=True)

    ranges = re.findall(
        r"^@@ .*? \+(\d+)(?:,(\d+))? @@", diff, re.M
    )

    for start, count in ranges:
        start = int(start)
        count = int(count or 1)
        if count == 0:
            continue

        end = start + count
        checked_ranges += 1

        result = subprocess.run([
            "ruff", "format", "--check", "--force-exclude",
            "--range", f"{start}-{end}", file,
        ], capture_output=True, text=True)

        if result.returncode not in (0, 1):
            print(f"Không kiểm tra được: {file}")
            print(result.stderr or result.stdout)
            print("=" * 60)
            raise SystemExit(result.returncode)

        if result.returncode == 1:
            failed_ranges += 1
            failed_files.add(file)
            print(f"{file}:{start}-{end - 1}: Cần định dạng lại.")

if failed_ranges == 0:
    print("Không có vùng thay đổi cần định dạng lại.")

print("-" * 60)
print(f"Đã kiểm tra: {checked_ranges} vùng trong {len(files)} file.")
print(f"Cần định dạng: {failed_ranges} vùng trong {len(failed_files)} file.")
print("=" * 60)

raise SystemExit(1 if failed_ranges else 0)
PY
```

# Check ruff cho 1 commit 
```bash
python3 - <<'PY'
import json
import re
import subprocess

COMMIT = "b621005ee5d367a48a07455157383fd7e25623e4"

parent = subprocess.check_output([
    "git", "rev-parse", f"{COMMIT}^",
], text=True).strip()

files = subprocess.check_output([
    "git", "diff", "--no-renames", "--name-only", "-z",
    "--diff-filter=ACMR", parent, COMMIT, "--", "*.py",
]).decode().split("\0")
files = [file for file in files if file]

print("\n" + "=" * 60)
print(f"KIỂM TRA RUFF — COMMIT {COMMIT[:8]}")
print("=" * 60)

found = 0

for file in files:
    source = subprocess.check_output([
        "git", "show", f"{COMMIT}:{file}",
    ], text=True)

    diff = subprocess.check_output([
        "git", "diff", "--no-ext-diff", "--no-renames",
        "--unified=0", parent, COMMIT, "--", file,
    ], text=True)

    ranges = [
        (int(start), int(start) + int(count or 1) - 1)
        for start, count in re.findall(
            r"^@@ .*? \+(\d+)(?:,(\d+))? @@", diff, re.M
        )
        if int(count or 1) > 0
    ]

    if not ranges:
        continue

    result = subprocess.run([
        "ruff", "check", "--force-exclude",
        "--output-format=json", "--stdin-filename", file, "-",
    ], input=source, capture_output=True, text=True)

    if result.returncode not in (0, 1):
        print(f"Không kiểm tra được: {file}")
        print(result.stderr or result.stdout)
        print("=" * 60)
        raise SystemExit(result.returncode)

    for error in json.loads(result.stdout):
        first = error["location"]["row"]
        last = (error.get("end_location") or error["location"])["row"]

        if any(
            first <= end and last >= start
            for start, end in ranges
        ):
            found += 1
            column = error["location"]["column"]
            print(
                f"{file}:{first}:{column}: "
                f"{error['code']} {error['message']}"
            )

if not files:
    print("Commit không có file Python được thêm hoặc sửa.")
elif found == 0:
    print("Không có lỗi Ruff trong vùng thay đổi.")

print("-" * 60)
print(f"Tổng: {found} lỗi Ruff trong vùng thay đổi.")
print("=" * 60)

raise SystemExit(1 if found else 0)
PY
```

# Check Format cho 1 commit
```bash
python3 - <<'PY'
import re
import subprocess

COMMIT = "b621005ee5d367a48a07455157383fd7e25623e4"

parent = subprocess.check_output([
    "git", "rev-parse", f"{COMMIT}^",
], text=True).strip()

files = subprocess.check_output([
    "git", "diff", "--no-renames", "--name-only", "-z",
    "--diff-filter=ACMR", parent, COMMIT, "--", "*.py",
]).decode().split("\0")
files = [file for file in files if file]

print("\n" + "=" * 60)
print(f"KIỂM TRA FORMAT — COMMIT {COMMIT[:8]}")
print("=" * 60)

checked_ranges = 0
failed_ranges = 0
failed_files = set()

for file in files:
    source = subprocess.check_output([
        "git", "show", f"{COMMIT}:{file}",
    ], text=True)

    diff = subprocess.check_output([
        "git", "diff", "--no-ext-diff", "--no-renames",
        "--unified=0", parent, COMMIT, "--", file,
    ], text=True)

    for start, count in re.findall(
        r"^@@ .*? \+(\d+)(?:,(\d+))? @@", diff, re.M
    ):
        start = int(start)
        count = int(count or 1)
        if count == 0:
            continue

        end = start + count
        checked_ranges += 1

        result = subprocess.run([
            "ruff", "format", "--check", "--force-exclude",
            "--range", f"{start}-{end}",
            "--stdin-filename", file, "-",
        ], input=source, capture_output=True, text=True)

        if result.returncode not in (0, 1):
            print(f"Không kiểm tra được: {file}")
            print(result.stderr or result.stdout)
            print("=" * 60)
            raise SystemExit(result.returncode)

        if result.returncode == 1:
            failed_ranges += 1
            failed_files.add(file)
            print(f"{file}:{start}-{end - 1}: Cần định dạng lại.")

if failed_ranges == 0:
    print("Không có vùng thay đổi cần định dạng lại.")

print("-" * 60)
print(f"Đã kiểm tra: {checked_ranges} vùng trong {len(files)} file.")
print(f"Cần định dạng: {failed_ranges} vùng trong {len(failed_files)} file.")
print("=" * 60)

raise SystemExit(1 if failed_ranges else 0)
PY
```