## Login
```
aws sso login --profile uu3-spdm-dev
```
### Đối với FE thì thêm điều kiện dưới đây
```
export PATH="$HOME/Library/Python/3.13/bin:$PATH"
```

# Cập nhật code tất cả các nhánh
```
current=$(git branch --show-current)

echo "==================== Fetching AWS ===================="
git fetch aws --prune

for branch in $(git branch --format='%(refname:short)'); do
    remote="aws/$branch"

    if git show-ref --verify --quiet "refs/remotes/$remote"; then
        echo ""
        echo "==================== Updating $branch ===================="
        git switch "$branch"
        git merge --ff-only "$remote" || echo "⚠️ Cannot fast-forward $branch"
    else
        echo "⚠️ No remote branch for $branch"
    fi
done

git switch "$current"
```