# pstack companion

## Detection

Detection makes no forge call.

1. `pstack:off` turns pstack off.
2. `pstack:required`. If pstack is absent, stop before the first write and name the missing skills.
3. If the runtime skill list includes `poteto-mode` or the hook's skill, pstack is present.
4. Otherwise run one filesystem probe. A `.cursor-plugin/plugin.json` with `name` `pstack`, or `poteto-mode/SKILL.md` under `~/.cursor/skills`, `${CLAUDE_HOME:-~/.claude}/skills`, `${CODEX_HOME:-~/.codex}/skills`, or repo `.cursor/skills`. Use the `plugin.json` version.
5. Otherwise pstack is absent.

A missing leaf skill disables only that hook. Read its `SKILL.md` in full (`disable-model-invocation: true`).

## Precedence

git-collaboration wins on conflict.

1. Autonomy does not waive human-only waivers, the grill, reviewer selection, or dissent-then-wait.
2. pstack forge commands do not run. Forge calls come only from `references/github.md` or `references/gitlab.md`. **Forge budget** applies.
3. `why` and `blast-radius` use local `git log` / `git blame` and the existing snapshot only. No forge or MCP query.
4. A brief with an Execution plan is the work order.
5. A pstack subagent never writes to the forge and never receives the forge snapshot.
6. Marker lines and fixed labels stay verbatim under `unslop` and `technical-writing`.

## Subagents and models

Use `poteto-agent` only when listed, else `generalPurpose` or inline. One model records `single-model`. Models come from `/setup-pstack`.

## Hook table

Mode / step | pstack skill | Runs when | Evidence | Fallback

- Pre-submit. **principle-prove-it-works**. Implement, revise, conflict, before the gate. `Proof:` from a real run. `pstack: absent` via `verification-before-completion`.
- Pre-submit. `verify-<app>`. Mapped feature in the diff. `Surface:` names skill and feature. `Surface: none: <reason>`.
- Pre-submit. `create-verification-skill`. Issue asks. Separate work. Recommend `/create-verification-skill`.
- Plan step 3. `how`. More than one subsystem. `file:line` in Root cause. current step 3.
- Plan step 3. `why`. Local git and the existing snapshot only, no forge or MCP query. Introducing commit. current step 3.
- Plan step 5. `architect`. `arena` for two or more shapes. Function boundary. Real rejected candidate. current step 5.
- Plan step 5. `blast-radius`. Shared contract, wire format, schema, or config default. Stop and dissent line. current step 5.
- Plan step 5. **principle-sequence-verifiable-units**. Always when present. Verify on each step. current step 5.
- Plan step 6. Prototype playbook. Observable by running code. Cited run. current step 6.

## Record line

`pstack: present <version> [hooks run] | absent | off`

## Implement rows

- **Playbook by kind.** Bug fix steps 1, 2, 4, and 5, plus `tdd` when cheap. Feature steps 4 to 6. Refactoring step 1 and step 6.
- **Brief overrides redesign.** With an Execution plan, record `how`, `architect`, and `arena` as `skip: brief is the work order`.
- **Todo order.** `references/implement.md` steps are the outer list. Nest playbook steps under steps 10 and 11. Steps 12 to 16 replace "Run Opening a PR".
- **Delegation.** The delegate gets file pointers and the brief, never the forge snapshot, and makes no forge call. The parent reviews the diff before commit.
- **Prose.** When installed, run `technical-writing` and `unslop` on the PR/MR and commit bodies, plus `/deslop` and `/no-comments` on the diff, before the pre-submit gate.
- **PR/MR body.** `## Why`, `## Scope`, `## Tradeoffs`, `## Blast Radius`, and `## Verification` may be the layout. Include the summary, the issue link, each brief Test case id and result, the Proof record under `## Verification`, known limitations, reviewer and assignee metadata, and pre-submit waivers.
- **No pstack forge path.** No `gh` or `origin` from Opening a PR, no Babysit after opening, and no merge.
