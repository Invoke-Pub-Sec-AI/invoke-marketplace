---
name: aa-evidence-intake
description: Check PBC workbooks and KSD evidence for the legacy AA graph worker. Use for input selection, extraction coverage, and review of source associations.
---

# AA evidence intake

Establish exactly which source records the metadata worker can inspect, what extraction omits and whether that exact snapshot has the required input-handling review. Inspection and local pattern checks do not certify absence of PII/PHI or authorize export.

## Check the worker version

Use the parser, settings, and artifact contracts from the exact legacy revision selected for the task. Read `main.py` and `src/cli.py` as source before running commands. The newer PDF launcher starts processing when invoked, even for interface discovery. See [AA project](../aa-project/SKILL.md) for that worker.

## Resolve the maintained intake contract

Start with the user's runtime or checkout. Confirm `main.py` and `src/sources.py` in the selected workspace. Locate its matching `docs/CONTEXT.md` and the input-selection section of the worker operations documentation; if no checkout is selected, locate the maintained AA research-team repository. For a packaged runtime without docs, reconcile `VERSION` and source manifest before treating a separate checkout's documentation as current.

Read current intake behavior in those documents. For header aliases and extraction decisions, consult `src/sources.py`; for exact-input declarations, consult the input-review implementation and command parser by reading source; do not invoke the launcher for help. Inspect the actual target only when accessible and authorized. A local path, fictional fixture or package list does not establish target availability.

## Select and inspect the population

1. Resolve `aa_pbc_path` and `aa_ksd_paths` through root `main.py`. Inputs are ordinary filesystem paths: individual files, recursive folders or JSON path lists. Storage URIs need an approved filesystem exposure first. Overlapping selections are deduplicated; source names and private IDs stay on the target.
2. Check each PBC workbook has one unambiguous worksheet with its recognized request-ID and description columns in the first row. Read the source aliases instead of inventing a header mapping. Reserves are excluded. Repeated request keys in different workbooks receive private namespaces, so preserve the resulting snapshot IDs.
3. Inspect `python3 main.py inspect-inputs` output in a fresh private directory. Read `INPUT_SNAPSHOT.json` and `FILETREE.md` for selected records, reserves, unsupported formats, extraction warnings and skips. Compare these with the requested population. Inspection and preflight make zero model calls and may run with `input_review_required=true`; declarations are required before inference, not before these offline checks.
4. Check fidelity and any supplied association history below. Finalize selection before exact-input review, since changed paths, bytes, study, extraction semantics or association input invalidate the earlier snapshot.

Additional nonempty PBC tracker cells are retained privately in `pbc_context`. Only the explicit business-header allowlist enters model source text, including supported service, focus-area, system, period and format context. Contact/personal and unrecognized columns remain off-model; preserve their withholding disclosure. This is not permission to add source PII/PHI contrary to the existing handling declaration. Business metadata remains subject to exact input and output review.

## Assess extraction fidelity

The worker supports UTF-8 TXT/MD/CSV/JSON, XLSX, DOCX main-body text and PDFs with usable text layers. Unsupported or unextractable files remain inventoried with reasons; report them as outside admitted evidence rather than silently treating them as inspected.

- PDF extraction has no OCR or rendered-layout guarantee. An image-only or unusable PDF needs a separately approved extraction path, not an automatic new dependency or a claim of coverage.
- Word extraction preserves final tracked revisions and text/table separators, with known gaps for headers, footers, comments, drawings and rendered layout.
- Excel extraction preserves sparse cell coordinates and literal formulas, recognized date serials and visible rich-text runs. It does not reproduce formatting, charts or formula evaluation; consult current warnings for omitted sheet types.

Read optional limits from the actual runtime configuration. Current production intake has no default corpus-count, source-size or extracted-text ceiling; host memory, decoders and model context/output constraints still exist. Extraction is not a fidelity certificate. A long source is inspected through bounded windows, and repeated/overlapping reads contribute only their unique spans to coverage.

Use `SOURCE_COVERAGE.json` and study acceptance receipts after research to distinguish admitted extracted-text coverage from skipped content, rendered-document fidelity and metadata completeness. These are different claims.

## Handle supplied PBC/KSD history when requested

Use `aa_pbc_ksd_associations` only for an explicitly supplied return-history relationship. Read `src/associations.py` for its current schema and validation. The manifest uses exact `pbc_record_id` and `ksd_record_id` values from the selected snapshot; obtain those IDs before constructing or repairing its rows. Infer no association from similar names, shared fields or folder proximity.

When manifest repair is authorized as part of the task, use the following recovery if unresolved configured IDs block snapshot creation. Existing repair authorization carries forward. For an inspect-only task, report the unresolved manifest and propose the repair without temporarily overwriting it. For an authorized repair, preserve the original manifest bytes outside every selected evidence root and keep the intended source selections unchanged. For discovery only, temporarily use a schema-valid empty association list at the same configured manifest path, so that file remains reserved; disabling the association setting could instead admit it as a KSD. Obtain exact private IDs, prepare a corrected copy outside evidence roots, then place the corrected bytes at the reserved configured path. Keep the original copy and restore it if repair is abandoned. Reinspect the final full selections and configured manifest before inference, and apply handling review only to that final hash. Backups and repair copies stay outside selected roots; preserve validation and snapshot IDs rather than renaming IDs to fit a failed join.

Keep the manifest private. Its exact bytes and resolved endpoints bind the input fingerprint. The configured manifest is reserved from KSD admission even inside a recursive KSD folder; other JSON documents remain eligible. Reinspect after changing the manifest. The host may retain eligible endpoints as unverified `source_association` links, with fulfillment unassessed; supplied history does not establish that a KSD satisfies a PBC.

## Record exact-input review and hand off

Prepare the concrete snapshot identity, admitted counts and disclosed gaps for the authorized reviewer. Preserve prior user authorization for inspection and requested preparation. Record `review-inputs` only after the reviewer has actually confirmed both the no-PII/PHI and approved service-handling declarations for those exact inputs. These assertions cover the reviewed snapshot, including private retained data; automated withholding does not replace them.

Run preflight before or after handling review and report its approval state without manufacturing declarations. Before inference, use the current review command's confirmation flags only for actual authorized assertions, retain the output parent's `input-reviews/` receipt and check that it matches the final input-snapshot receipt. Any later fingerprint change requires an applicable review for the new final snapshot.

Offline intake is complete when every requested selection is accounted for as admitted, reserved, skipped or intentionally unselected, fidelity gaps are explicit, supplied relationships resolve exactly, and the pending or satisfied review state is reported. Readiness for inference additionally requires an authorized handling receipt matching the final snapshot. Hand those facts and target-only artifact locations to research operations. Source identifiers, raw context, filenames, paths and manifests remain inside the target. Exact-input handling review does not authorize a summary ZIP to leave the approved target workspace; export requires a separate review of its exact bytes.
