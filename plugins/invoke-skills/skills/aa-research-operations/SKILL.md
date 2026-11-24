---
name: aa-research-operations
description: Set up, run, stop, resume, or diagnose the legacy AA PBC/KSD graph worker in an approved target environment.
---

# AA research operations

Operate the Python worker while preserving its reviewed input snapshot, durable task state and private output boundary. A completed research run prepares proposals; it does not establish metadata accuracy or authorize export.

## Check the worker version

Use the parser, settings, and artifact contracts from the exact legacy revision selected for the task. Read `main.py` and `src/cli.py` as source before running commands. The newer PDF launcher starts processing when invoked, even for interface discovery. See [AA project](../aa-project/SKILL.md) for that worker.

## Establish the actual runtime

Use the runtime or checkout selected by the user. Locate `main.py`, `src/` and `requirements.txt` in that workspace before running commands. For maintained documentation, locate the corresponding checkout containing `docs/CONTEXT.md`; if no checkout is selected, locate the maintained AA research-team repository. A packaged runtime may contain no documentation. Check its `VERSION` and source manifest against the documentation/code being consulted instead of assuming the local checkout matches the deployed release.

Read `docs/CONTEXT.md` and the operational sections of `README.md` from the resolved checkout. For setup, stopping or continuation, read the matching section of the worker operations documentation. Resolve current command arguments from safe source inspection of the legacy command parser when present; do not invoke the auto-running launcher for help. This skill deliberately does not duplicate the command inventory.

Determine where execution is authorized and accessible. A local Codex checkout or successful mock test does not establish target filesystem access, approved model access or permission to transfer private data. Use existing authorization for requested operations and reversible inspection; prepare concrete diagnostics before asking for information or an attestation that is actually missing.

## Prepare and start

1. Verify Python compatibility and the complete `requirements.txt` in the selected runtime. Required imports are direct; a missing library must be corrected through the target's approved package process. Use its supplied package inventory and approved wheel source when applicable. Do not substitute a newly discovered library or treat a package catalog as proof of active-compute installation.
2. Read the settings initialization in the selected revision’s `main.py`. For example, one graph revision reads `genai_model_name`, while a later revision reads `OPENAI_MODEL`. Match input paths, output directory, provider, and secret names to that same file. Supply the secret through the target’s configured mechanism.
3. Inspect and preflight the exact selected inputs before inference; both checks may run offline with handling review still pending and make zero model calls. Require applicable exact-input declarations only before inference. Use `$aa-evidence-intake` for source selection, extraction gaps, supplied associations and exact-input review. Recording the no-PII/PHI and approved service-handling declarations requires the authorized reviewer's actual assertions for that snapshot; a request to run is not itself those assertions.
4. Invoke the `run` command identified in that revision’s parser with a fresh output directory. Inspect its JSON receipt and private artifacts to establish the outcome. Missing configuration and unapproved inputs can initialize artifacts with zero model calls; distinguish that state from completed research.

Setup is complete when the intended runtime imports its approved dependencies, the target configuration is resolved without exposing credentials, and preflight identifies the intended population with its review state explicit. Pending declarations do not block offline setup or preflight; they block inference. A run is complete only to the extent recorded by its authoritative receipts; disclose partial, withheld and skipped work.

## Follow the work

Use `RUN.json`, `CATALOG_PROGRESS.json`, and validated task state for counts and blockers. Human-readable plans and progress files are projections; editing them cannot alter approvals, evidence credit, task counters or continuation eligibility.

The main orchestrator and nested team containers have no aggregate turn ceiling. An exact leaf assignment has a default 15-turn allowance; `aa_subagent_turn_limit` controls that allowance and `aa_document_concurrency` controls document-team concurrency. Check root configuration for current defaults and legacy-setting precedence. Revisions and continuation preserve consumed leaf turns. Reassigning identical work is not a counter reset. No worker elapsed-time deadline applies; provider context/output constraints and failures still apply.

Keep root coordination source-free: counts and opaque handles support plan review. Evidence critique occurs within document teams using inspected source windows. Neither planning-adversary acceptance nor model cleanup establishes release eligibility.

## Stop, recover or diagnose

For a requested stop, use the stop signal defined by that revision (the `STOP` file in the reviewed graph worker) in the active run directory and inspect the resulting receipt. The host cancels and reaps its owned request process and preserves validated state. Cancellation or interruption can leave model delivery uncertain.

For continuation, first inspect the `CONTINUATION_STATUS.json` receipt and matching contract. Use the explicit `run --resume-from ... --output ...` interface only when the host's exact input, runtime, policy and task-state checks permit it. Keep the original run intact. Accepted work is reused, pending required review resumes as review, and exhausted or withheld assignments stay terminal. Active, consumed and uncertain-delivery parents block continuation. The current CLI has no receipt-reset or delivery-reconciliation command. Preserve the original pending/failed receipts and seek actual delivery evidence and an owner decision; inventing a recovery command, manually resetting markers or automatically replaying a request does not resolve uncertainty. Continue independent fictional or code work within existing authorization.

Diagnose from the earliest failed phase and its safe receipt:

- Configuration or import failure: verify required settings, installed approved dependencies and the selected runtime.
- Input-review failure: compare the inspected snapshot and review receipt; changed source/study/association bytes require renewed review.
- Provider failure: inspect the fixed error code, configured endpoint/model and target access. Preserve ambiguous delivery; rely on the transport's explicit retry semantics rather than adding a resend loop.
- Partial or withheld research: inspect task exhaustion, coverage gaps and unresolved critique obligations; preserve the distinction between failed extraction, incomplete research and content withholding.

Report the output location, actual status/counts, concrete blocker and safe next action. Keep source-bearing diagnostics and notes inside the target. Successful research may produce `summary-draft/`; input-handling approval is separate from authorized exact-byte export review. Packaging or transmitting a return archive requires the separately requested and satisfied release workflow.
