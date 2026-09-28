# Work-order brief

Read this file when `/git-plan-issue` writes a handoff brief (another session, model, or agent will execute, or the user asks for a full work-order), or when `/git-issue-pr` implements a brief that has an `### Execution plan`. The decision card and the dissent recipe stay in `references/plan-issue.md`.

This recipe adds `### Execution plan`, `### Interfaces`, and `### Test cases` to the decision card:

````markdown
<!-- git-plan-issue -->
## Implementation brief

**Goal:** <one observable completion state>
**Root cause:** <file and behavior evidence>
**Recommended change:** <what to change, where, and why this shape; one line naming the rejected alternative>
**Out of scope:** <work this issue will not do>
**Acceptance criteria:** <summary of acceptance changes or deliverables; full checkable list lives in the issue description, do not duplicate the full checklist>
**Tests:** <test files to add or change, and the exact commands to run>
**Proof:** <verify skill and feature to drive, or command> | tests only: <reason>
**Constraints:** <repo-local instructions or existing contracts>
**Planned at:** `<branch>@<short SHA>`

### Execution plan
1. **<imperative step title>**
   - Files: `<path>` (edit | create)
   - Change: <symbol and the exact behavior it gains or loses>
   - Verify: `<command>` → <expected result>
2. ...

### Interfaces
```<language>
<new or changed signatures, types, config keys, or payload shapes only; no bodies>
```

### Test cases
| # | Test | Given | When | Then | Covers |
| --- | --- | --- | --- | --- | --- |
| T1 | `<file>::<test name>` | <concrete input or state> | <call or action> | <exact expected output, error, or state> | <description checklist line number, e.g. `#2`> |

### Stop and dissent when
- <an assumption this plan relies on, stated so the executor can check it>

**Next:** `/git-issue-pr <exact issue URL>`
````

## Executor-ready brief

The work-order / handoff profile is a work order. The executor reads it, opens the files named in step 1, and writes the first failing test. It should not need a second design pass. Check the draft against every rule below before plan-issue step 7. Do not apply the Execution plan, Interfaces, or Test cases requirements to a decision card:

- **Paths and symbols exist.** Every `edit` path and symbol exists at the planned-at SHA. Every `create` path names the directory it goes in, following an existing neighbor.
- **Steps are ordered and small.** The first step writes or changes the failing tests from Test cases. Each later step touches one concern and ends with a Verify command and its expected result. The last step runs the repo's full relevant check.
- **Interfaces fix the contract, not the body.** Give new or changed signatures, types, return values, error behavior, config keys, and payload shapes. Show only the new form of a changed signature; omit the old form and unchanged neighbors. Do not write function bodies and do not paste existing source. A body goes stale when the code moves, and a weaker executor copies it anyway.
- **Test cases are concrete.** Given, When, and Then use literal values, not "valid input" or "works correctly". Every acceptance line is covered by at least one test case or an exact command. `Covers` holds the description checklist line number, never the line's text, so the brief does not duplicate the checklist. Include the regression case that reproduces the root cause, and each edge case the change introduces.
- **No vague verbs.** Replace "handle", "improve", "clean up", "as needed", "appropriate", "etc.", and "similar" with the exact behavior. If you cannot state the exact behavior, the evidence is too thin or a product decision is unsettled.
- **Stop and dissent when** lists the assumptions the plan relies on that the executor can check: a symbol's current behavior, a caller count, a config default, a test that currently passes. If one fails, the executor dissents instead of improvising.
- **Proof.** `tests only: <reason>` is allowed only when the change has no user-visible surface. Do not paste pstack artifacts into the brief.
- **Size.** When the Execution plan needs more than 8 steps or touches unrelated areas, how to split the work is a scope choice: treat it as an unsettled product decision about Out of scope.
