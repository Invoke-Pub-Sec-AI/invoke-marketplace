---
name: aa-project
description: Route Agentic Auditor (AA) tasks to the PBC workbench, research worker, SME review app, or Lab. Use when reviewing a returned package, changing a project workflow, or identifying the worker version.
---

# Agentic Auditor

Match the artifact in the request to its owner. Read the instructions in the selected checkout and confirm its Git revision. A packaged worker can be older than the repository default branch.

| Task | Repository and first source |
| --- | --- |
| Prepare PBC (Provided By Client) requests, map supporting evidence, or review suggestions | `aa-pbc-workbench`. Start with `AGENTS.md` and `docs/CONTEXT.md`. Follow the architecture or operator guide linked by that checkout. |
| Issue an SME work package, preview a returned review, or apply it | `aa-pbc-workbench` owns issuance and acceptance. Read its SME handoff guide and the companion's `CONTRACT.md`. For a returned `sme-reviews_*.json` file, use Galaxy's **Returned SME reviews** preview. Match the package ID and checksum to the issued copy, inspect the import, and preserve the named reviewer's history when applying it. |
| Import an issued package, record a subject matter expert's edits, or export their review | `aa-sme-review` imports an issued `explore-sme-package_*.json` file and keeps the attributed review journal. Read `README.md` and `CONTRACT.md`. For a protocol change, test the round trip across both repositories with a synthetic package. |
| Work on a Lab question or multi-part study | Read the question folder's `QUESTION.md` and the workbench's `aa-lab` skill. For a study, also read `aa-lab-study`. Locate these under `backend/features/lab/skills/` or, in older checkouts, `review/skills/`. Follow the question's data scope and result format. |
| Process documents, diagnose a research run, or review its outputs | `aa-research-team`. Read `AGENTS.md`, the **Current root worker** section in `README.md`, and the source of the selected launcher's `main.py`. Identify the worker before choosing commands. |

## Identify the research worker

The **PDF worker** has `src/pii_worker.py` and `src/summarize.py`. Its root launcher can install dependencies and start processing as soon as it runs. Inspect its source to determine arguments and side effects, including when looking for help. PBC documents receive name-only processing. KSD summaries go through cleanup and a final review against the original source. The output ZIP contains completed PDFs. Failed candidates, the metadata catalog, and optional review JSON stay in the private review workspace.

The **legacy graph worker** has `src/cli.py`, `src/sources.py`, and `src/research_release.py`. Read the parser and configuration in the exact packaged revision. Legacy revisions share these modules but differ in their settings and flags. Choose the specialist skill for the task.

- `aa-evidence-intake` for input selection, extraction coverage, and handling review.
- `aa-research-operations` for preflight, start, stop, resume, or diagnostics.
- `aa-metadata-extraction` for field and system metadata.
- `aa-adversarial-review` for challenging a research claim or orchestration plan.
- `aa-disclosure-review` for pseudonymization and private lookup review.
- `aa-summary-release` for the reviewed JSON return and its release checks.

Use synthetic fixtures for local round trips. Keep source materials and private lookups in the workspace approved for them. Verify the selected worker's output contract before treating an artifact as eligible for transfer.
