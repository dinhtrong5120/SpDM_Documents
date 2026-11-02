---
name: spdm-frontend-pr
description: Chuẩn bị mô tả Pull Request 3 ngôn ngữ (Nhật - Anh - Việt) cho repository SPDM Frontend từ git diff giữa source và target branch, kèm bằng chứng kiểm chứng UI và tích hợp API. Prepare SPDM Frontend pull request descriptions from a source-to-target Git diff, with complete Japanese, English, and Vietnamese versions and UI-focused verification evidence. Use for Frontend PR preparation or filling .github/PULL_REQUEST_TEMPLATE.md; not for implementing UI changes or Backend-only PRs.
---

# SPDM Frontend Trilingual Pull Request

Produce an evidence-based PR description: a full Japanese version, then English, then Vietnamese. Each version must stand alone and describe the same scope, behavior, verification results, and residual risks.

## Inspect the Change

1. Read applicable repository instructions and inspect `git status`. Preserve unrelated working-tree changes.
2. Resolve the requested source and target branches and verify both refs exist. Ask for missing refs rather than silently substituting a similarly named branch.
3. Inspect the PR delta with:
   - `git log --oneline --no-merges <target>..<source>`
   - `git diff --stat <target>...<source>`
   - `git diff --name-status <target>...<source>`
   - `git diff --function-context <target>...<source>`
4. Read affected routes, components, shared callers, API clients, state logic, and tests as needed to explain the resulting behavior. Identify the actual framework and available commands from repository configuration; do not assume React, Vue, TypeScript, or a package manager.
5. Use local refs as the evidence available. Fetch only if requested or required by repository instructions. A read-only `git merge-tree` check may help; do not merge or check out a branch solely to prepare the description.

For mixed Frontend/Backend changes, describe the Frontend scope and relevant API dependencies, and make the coverage boundary explicit. Do not claim a complete Backend review from Frontend evidence.

## Assess and Verify

Read [references/frontend-guidelines.md](references/frontend-guidelines.md) for UI-specific evidence, proportional checks, and risk assessment. Apply only scenarios relevant to the diff.

- Classify by behavior: correcting existing behavior is normally a bugfix; adding a user-facing capability is a feature.
- Run safe, proportional checks using the repository's existing commands when feasible. Do not add tests, install dependencies, update snapshots, or modify application code solely to prepare a PR description unless separately requested.
- Record the command, outcome, and material limitations. A successful build does not prove the interface works in a browser; mocked API checks do not prove real Backend integration.
- Mark `OK` / `Passed` / `Đạt` only for executed checks that passed. Distinguish failed, blocked, and not-executed checks. Never present an expected result as an observed result.
- State browser/manual and real Backend integration coverage explicitly in all three versions when relevant, including when they were not performed.
- Derive ticket IDs only from provided information or branch names; do not invent tickets, links, browser/device coverage, or screenshots.

## Write and Deliver

Read [references/pr-format.md](references/pr-format.md) and follow its headings and ordering, preserving additional requirements from the repository's existing template.

- Lead with affected screens and concrete before/after behavior. Include routes, components, API endpoints, or payload fields when they help explain the change and are supported by the diff.
- Include screenshots or responsive, accessibility, localization, and permission scenarios only when relevant; use actual evidence and leave unperformed checks clearly labeled.
- Keep the three language versions equivalent, with natural engineering terminology. Verify matching change type, risk, identifiers, results, and scope boundaries before delivery.
- If asked to fill `.github/PULL_REQUEST_TEMPLATE.md`, modify that file only, then run `git diff --check`. Report pre-existing unrelated failures separately.
- If asked only for text, return the description without modifying the repository.
- PR preparation does not authorize merging, committing, pushing, creating a PR, or changing application code. Perform those only when separately requested.
- In the final response, link any resulting file and summarize material verification gaps.
