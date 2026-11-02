# Điều kiện: 
1. Tạo 1 thư mục code dưới local
2. code luôn
3. tạo repo trên github

# Đẩy code lên github
```angular2html
git init

printf '%s\n' \
  '.venv/' '.idea/' '.env' '.env.*' '!.env.example' \
  '*.sqlite3' '__pycache__/' '*.pyc' '.DS_Store' \
  > .gitignore

git add .
git status
git commit -m "first commit"
git branch -M main
```

```angular2html
git remote add origin https://github.com/dinhtrong5120/my_exam_web_BackEnd.git
git push -u origin main
```