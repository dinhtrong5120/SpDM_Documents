---
name: spdm-bilingual-pr
description: Prepare SPDM pull request descriptions by comparing a source Git branch with a target branch and writing a Japanese-first, English-second, Vietnamese-third `.github/PULL_REQUEST_TEMPLATE.md`. Use for SPDM branch merge or PR preparation; do not perform the merge, commit, push, or PR creation unless separately requested.
---

# SPDM Trilingual Pull Request

Create an evidence-based PR description from the actual Git diff. The Japanese, English, and Vietnamese sections must be complete standalone versions, not interleaved line-by-line translations.

## Inspect the Change

1. Read repository instructions and check `git status` before making changes. Preserve unrelated working-tree changes.
2. Resolve the source and target branch names from the request. Verify both refs exist; do not silently substitute a similarly named branch.
3. Review the PR delta with the three-dot comparison:
   - `git log --oneline --no-merges <target>..<source>`
   - `git diff --stat <target>...<source>`
   - `git diff --name-status <target>...<source>`
   - `git diff --function-context <target>...<source>`
4. Read enough surrounding code, tests, schemas, and documentation to explain the behavior rather than merely restating changed lines.
5. When useful, use `git merge-tree` as a read-only conflict check. Do not merge or check out the source branch just to prepare the description.
6. Treat local refs as the evidence available. Fetch only when the user explicitly asks for current remote state or when normal repository instructions require it.

## Classify and Validate

- Choose the change type from behavior: a missing or incorrect existing behavior is usually a bugfix; a new user-facing capability is a feature.
- Assess risk from data writes, schema/API compatibility, affected callers, and deployment concerns. A response-only additive field is normally low risk.
- Run safe, proportional checks when possible, such as syntax validation, targeted tests, or a small transformation simulation.
- Never claim unit, integration, manual, database, or UI testing that was not actually performed.
- In the testing table, record `OK` / `Passed` / `Đạt` only for executed checks. Record `未実施` / `Not executed` / `Chưa thực hiện` for planned checks that were not run.
- If a real Django/MySQL test was not run, state that explicitly in all three language versions.
- Derive related ticket IDs from the request or branch name, but do not invent issue links or numbers.

## Write the PR Description

Read [references/pr-format.md](references/pr-format.md) and follow its ordering and headings.

- Put the full Japanese version first, the full English version second, and the full Vietnamese version third.
- Keep all three versions semantically equivalent and technically precise.
- Use natural Japanese and Vietnamese engineering terminology rather than word-for-word translation.
- Mention concrete files, functions, endpoints, fields, migrations, or tables when supported by the diff.
- Explain the prior behavior, its user/system impact, the implementation, testing evidence, and residual risk.
- Include a test table in all three versions when there are meaningful verification scenarios.
- Keep unchecked checklist items unchecked when tests or documentation were not added.

## Apply and Deliver

- If the user asks to fill `.github/PULL_REQUEST_TEMPLATE.md`, update that file only and run `git diff --check` afterward.
- If the user asks only for output text, do not modify the repository.
- Do not merge, commit, push, create a PR, or modify application code unless the user explicitly asks for that separate action.
- In the final response, link the resulting file, summarize what was produced, and clearly state any verification not performed.
