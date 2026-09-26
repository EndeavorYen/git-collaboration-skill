# pstack companion

Read this file only when detection says pstack is present and not off. It names pstack skills and playbooks. It does not copy their text. A missing install does not change mode behavior, apart from the Proof record.

## Detection

Once per invocation. Detection makes no forge call.

1. `pstack:off` in the invocation turns pstack off. Do not read the rest of this file.
2. `pstack:required` means detection must succeed. If pstack is absent, stop before the first write and name the missing skills.
3. If the runtime skill list includes `poteto-mode` or the hook's skill, pstack is present. That signal is authoritative.
4. Otherwise run one filesystem probe. Look for a `.cursor-plugin/plugin.json` whose `name` is `pstack` in the runtime plugin cache, or a `poteto-mode/SKILL.md` under a known skills directory (`~/.cursor/skills`, `${CLAUDE_HOME:-~/.claude}/skills`, `${CODEX_HOME:-~/.codex}/skills`, or the repo `.cursor/skills`). Read the version from `plugin.json` when it has one.
5. Otherwise pstack is absent.

A missing leaf skill disables only that hook. Many pstack skills set `disable-model-invocation: true`, so the hook says to read that skill's `SKILL.md` in full.

## Precedence

git-collaboration wins on conflict.

1. Autonomy does not waive human-only waivers, the grill, reviewer selection, or dissent-then-wait.
2. pstack forge commands do not run. Forge calls come only from `references/github.md` or `references/gitlab.md`. **Forge budget** still applies.
3. `why` and `blast-radius` use local `git log` / `git blame` and the existing snapshot only. They do not query the forge or a forge MCP.
4. A brief with an Execution plan is the work order.
5. A pstack subagent never writes to the forge and never receives the forge snapshot or credentials.
6. Marker lines and fixed field labels are exempt from `unslop` and `technical-writing` rewrites.

## Subagents and models

Use `poteto-agent` only when the runtime lists it. Otherwise use `generalPurpose`, or run inline when the runtime has no subagents. `interrogate` or `arena` with one available model records `single-model` and claims no model diversity. Models come from the `/setup-pstack` rule. This skill does not pick models.

## Hook table

| Mode / step | pstack skill | Runs when | Evidence | Fallback |
| --- | --- | --- | --- | --- | --- |
| Pre-submit on implement, revise, and conflict | **principle-prove-it-works** | Before the pre-submit gate, when the skill is present | `Proof:` from a real run of the changed behavior | `verification-before-completion` fills `Proof:`, and the record says `pstack: absent` |
| Pre-submit surface | `verify-<app>` | The repo has that skill and the diff touches a feature in its map | `Surface:` names the skill and the feature driven | `Surface: none: <reason>` |
| Pre-submit verify skill | `create-verification-skill` | The issue asks for that skill | The new verify skill is separate work | Do not create it in this PR/MR. The chat report recommends `/create-verification-skill` |
| Plan step 3 inspect | `how` | The change spans more than one subsystem | Root cause cites `file:line` | current step 3 |
| Plan step 3 inspect | `why`, local `git log` / `git blame` and the snapshot only, no forge or MCP query | The issue is a regression | Root cause names the introducing commit | current step 3 |
| Plan step 5 Recommended change | `architect`; `arena` when two or more valid shapes exist | The change crosses a function boundary | The rejected-alternative line names a real candidate | current step 5 |
| Plan step 5 Stop and dissent | `blast-radius` load-bearing fact | Shared contract, wire format, schema, or config default | That fact is a checkable Stop and dissent line | current step 5 |
| Plan step 5 Execution plan | **principle-sequence-verifiable-units** | Always when present | Each step ends in Verify | current step 5 |
| Plan step 6 before the grill | Prototype playbook | A fork whose answer can be observed by running code | The run is cited in Root cause or Recommended change | current step 6 |

## Record line

`pstack: present <version> [hooks run] | absent | off`
