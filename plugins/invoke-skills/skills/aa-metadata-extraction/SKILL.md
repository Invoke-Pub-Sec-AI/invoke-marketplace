---
name: aa-metadata-extraction
description: Extract evidence-grounded PBC requirements and KSD schema metadata for the legacy AA graph worker, including field meanings and system roles.
---

# AA metadata extraction

Produce a useful document/field catalog while distinguishing inspected facts, inference and missing definitions. Follow the user's selected sources, output format and existing authorization; this skill does not authorize model submissions, external writes or export.

These are Codex instructions, separate from the worker's model roles. Use fictional or explicitly releasable material for local Codex analysis. Actual source-bound inputs, maps and private critiques remain in the approved target; worker model phases use the configured service transport there. A checkout or available tool does not grant corpus access. Continue authorized code, fictional and releasable work within its existing scope.

## Check the worker version

Use the parser, settings, and artifact contracts from the exact legacy revision selected for the task. Read `main.py` and `src/cli.py` as source before running commands. The newer PDF launcher starts processing when invoked, even for interface discovery. See [AA project](../aa-project/SKILL.md) for that worker.

## Ground the catalog

Establish the selected population, extraction question and destination. Inspect one document or bounded window at a time. Keep a private evidence ledger tying observations to the exact inspected source/window; filenames, lexical matches and file listings are navigation rather than evidence. Preserve unread, skipped and ambiguous material in the limitations. Full text coverage alone does not establish metadata completeness.

Capture supported detail:

- **PBC:** requested evidence, required fields, format, frequency/period and system requirements. Use only approved business context; retain personal or unknown tracker columns privately under the applicable handling rules.
- **KSD:** document type/schema, record grain and period coverage; field definitions, declared or inferred types, units, key roles/uniqueness, formula definitions and missing semantics. Describe schema rather than copying business record values.
- **Systems:** distinguish producer, storer and recorder. A location or filename alone does not establish provenance. Preserve the distinction in `generated_in`, `stored_in` and `recorded_in` relationships when the current contract uses them.

For each retained definition, mark the basis **observed**, **inferred** or **unknown**, with concise support and uncertainty. A sampled type is inferred unless declared; a formula definition is not a verified calculation; a plausible key is not proven unique. Record absent meanings/units as explicit gaps rather than filling them with guesses.

When using the AA graph contract, retain `{field,value,basis}` entries. Current guidance favors eligible `document.*`, `field.<generic_label>.*` and `system.*` labels with `observed:`, `inferred:` or `unknown:` basis prefixes. These are conventions, not a schema enum or a requirement to populate unsupported slots. Keep labels consistent and generic, and basis explanations free of source quotations. Preserve meaningful metadata in the structured records instead of reducing each document to a broad narrative.

## Preserve the boundary

Keep exact quotes, source IDs/hashes/paths, source-bound findings, raw tracker context and identity/lookup maps in the approved target. Separately prepare eligible generalized metadata, limitations and export-only relationships. A stable opaque key may preserve identity across a reviewed summary; its original values and lookup remain private. Pseudonymization does not establish release eligibility.

Treat supplied PBC-to-returned-KSD associations as provided history, not inferred matching or evidence fulfillment. In the worker, those joins are host operations after independent reviews; document models do not receive the private association manifest. Support downstream analysis without extending the assignment into consumer interfaces, learning/grouping workflows or retrieval products.

Use existing authorization for ordinary inspection and reversible preparation. Worker inference still requires its exact-input handling declaration; never manufacture it. Export separately requires authorized review of the exact summary bytes and applicable no-PII/no-CUI declarations. Model cleanup and this skill cannot supply that approval.

## Completion and worker integration

Finish with structured metadata, explicit support/unknowns and scope limitations. Connect retained definitions to private inspected support and distinguish observation, inference and unknowns; every omitted/uninspected portion must remain visible. Manual annotations remain proposals until the host validates machine receipts and assigns authoritative identities. Report actual artifacts and checks performed, without claiming target accuracy or corpus completeness from synthetic tests.

For worker execution, schema changes or persisted artifacts, locate the user's supplied AA repository/worktree first. If no checkout is selected, locate the maintained AA research-team repository; verify it exists rather than assuming that checkout is current. Read its `AGENTS.md` and `docs/CONTEXT.md`. Consult `src/prompts.py`, `src/sources.py` and `src/research_release.py` for current handling, metadata and release contracts; read `docs/OPENAI_MATH_RESEARCH_METHOD.md` before changing phases or making methodological claims. Reuse these maintained contracts rather than copying a schema manual into this skill.
