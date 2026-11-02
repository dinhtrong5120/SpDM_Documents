# Frontend Evidence and Verification

## Explain the User Flow

Identify affected screens/routes, user roles where relevant, the triggering action, previous behavior, and resulting behavior. Follow shared components and hooks/composables far enough to understand other affected callers. Do not treat a component name as an explanation of user impact.

For API-related changes, inspect request construction, response mapping, and error handling. Mention endpoint, method, payload, or response changes only when evidenced. Distinguish a dependency on an existing API from a Backend change included in this PR. Flag required deployment order or API availability when supported by the code or requirements.

## Select Relevant Checks

Use repository scripts and existing test infrastructure. Choose checks based on the changed behavior rather than turning this list into a mandatory suite:

| Changed behavior | Useful verification |
| --- | --- |
| Rendering or layout | Target screen, changed UI state, relevant viewport; actual before/after screenshots when available |
| Form or data mutation | Required/invalid values, valid submission, duplicate-submit prevention, success and error feedback |
| API or asynchronous data | Loading, empty, success, error, and stale/out-of-order responses where affected |
| Filtering, sorting, pagination | Query parameters, page reset, displayed results, related state synchronization |
| Routing or navigation | Destination, parameters, direct access, back/forward behavior where affected |
| Permissions | Relevant roles, disabled/hidden controls and guarded routes; UI restrictions alone do not prove server authorization |
| Shared component or state | Representative callers, state reset/persistence, cache invalidation where affected |
| Localization or formatting | Changed labels, relevant locales, date/number formats, overflow |
| Interactive controls | Relevant keyboard interaction, focus, accessible names, and validation feedback |
| Build/configuration | Relevant lint, typecheck, build, or targeted automated tests supported by the repository (e.g. `npm run lint`, `npm run format:check`, `npm run build`) |

Do not claim responsive or cross-browser coverage without testing the stated viewport/browser. For screenshots, identify the screen and relevant state and use real artifact paths or supported links. Include before/after evidence only when both exist; otherwise describe available evidence and its limits. Avoid capturing credentials or personal data.

## Record Evidence Honestly

For each meaningful scenario, record the target screen/component, action or executed command, expected result, and actual outcome. Include the environment or mocked/real API distinction when it changes what the result proves. For commands, use N/A for screen operations when appropriate.

Use these result labels consistently:

| Japanese | English | Vietnamese |
| --- | --- | --- |
| OK | Passed | Đạt |
| 失敗 | Failed | Không đạt |
| 実行不可（理由） | Blocked (reason) | Không thể thực hiện (lý do) |
| 未実施 | Not executed | Chưa thực hiện |

Keep executed checks separate from proposed manual scenarios through explicit result labels. Do not check off “tests added/updated” merely because existing tests passed. If a check is irrelevant, omit it or mark it N/A when a repository template requires it.

## Assess Frontend Risk

Judge risk from the affected flow, breadth of shared callers, and consequences of failure. Backward compatibility alone does not determine risk.

- A local label or isolated visual change can be low risk when evidence supports that scope.
- Changes to shared components, navigation, asynchronous state, or API mapping may affect multiple screens and need representative verification.
- Changes to permission flows, destructive operations, or payloads used to save data can carry high risk even without a schema change.

Explain concrete residual risks and missing verification. Mention Backend dependencies and deployment order only when applicable. Do not infer low risk merely from a small diff.
