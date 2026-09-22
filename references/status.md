# Status

Read this file for `/git-pr-status`.

Remain read-only and report the state and next command. The recommended next command must pass the actor gate. Never recommend `/git-fix-conflict`, `/git-revise-pr`, `/git-request-review`, or `/git-merge-approved` for a foreign PR/MR, and never recommend `/git-review-pr` for an owned or `self_authored_head` PR/MR. Print Solo override when the PR/MR is `owned` or `self_authored_head`.

## Focused PR/MR Status Workflow

Use this when the user asks about one PR/MR, supplies a URL or iid without a valid action, or invokes `/git-pr-status`.

Keep the command read-only. Run the PR/MR command preflight, classify the primary state, and report `Current state`, `Head and gates`, `Evidence`, and `Recommended next command`. Do not post a status comment to the forge. Recommended next commands must pass the actor gate. Print Solo override when the PR/MR is `owned` or `self_authored_head`.
