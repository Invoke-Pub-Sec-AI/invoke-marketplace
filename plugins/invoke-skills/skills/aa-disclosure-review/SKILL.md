---
name: aa-disclosure-review
description: Review and pseudonymize summaries from the legacy AA graph worker while preserving stable entity keys, private lookups, and research fidelity.
---

# AA disclosure review

Produce a faithful summary candidate with stable opaque identities and a private
lookup. This Codex skill supports review work; it does not replace runtime role
instructions or establish release authority.

Keep originals, aliases, source identifiers, paths, quotes, critiques and lookup
tables inside the approved target workspace. Local analysis uses fictional or
explicitly releasable material; actual source-bound disclosure review runs in the
approved target through the configured service worker. Filesystem availability
alone does not permit reading private inputs or lookup maps into local Codex.
Ordinary code work, synthetic tests and eligible material remain in scope.
Output pseudonymization does not change source admission requirements or
authorize movement of source-bearing material.

For an existing AA run or worker implementation, first read
[the worker contract](references/worker-contract.md) to locate the current
repository and the validators relevant to the requested operation.

## Check the worker version

Use the parser, settings, and artifact contracts from the exact legacy revision selected for the task. Read `main.py` and `src/cli.py` as source before running commands. The newer PDF launcher starts processing when invoked, even for interface discovery. See [AA project](../aa-project/SKILL.md) for that worker.

## Review and preserve identity

- Reuse an established established opaque key for the same exact registered value. Group
  variants only when evidence establishes that they identify the same entity;
  retain ambiguity when that judgment is unresolved. Keys are sequential opaque
  labels, not content hashes or proof of anonymity.
- Keep `pii` and `cui` categories, explicit aliases and original values in the
  private lookup. Reject category rebinding, aliases assigned to conflicting keys
  and unknown token references. Credentials, source paths and `[WITHHELD]`
  placeholders remain withheld rather than becoming aliases.
- Preserve document scope. Equal names in separate documents can denote different
  people; local `hash-1` labels can also denote different entities. Catalog global
  keys must retain their validated document/local-key binding. Neither string
  equality nor aggregation establishes a cross-document identity match.
- Apply source-grounded substitutions consistently in retained summary prose.
  Keep each retained key stable; a generic “contact” or another person's key loses
  identity. Where fidelity and disclosure cannot both be preserved, withhold the
  affected field/node and describe the omission without exposing its contents.

## Preserve research meaning

Compare the candidate against the private original and evidence. Account for
actual changed fields, claim identities, relationships, scope disclosures and
confidence. Retain uncertainty; cleanup cannot strengthen confidence, introduce
claims, restore deleted topology or imply that a proposed result was adopted.
Use the worker's host validation and specialist/auditor workflow when operating
its artifacts. Literal replacement and pattern checks leave semantic CUI,
homonyms, combinations and reidentification risk unresolved.

Complete the requested cleanup with a reviewable candidate, preserved private
lookup, concise changes and explicit unresolved issues or withholding. Automated
checks and model critique cannot certify that actual content is free of PII/CUI.
Authorized review of the exact outgoing bytes remains separate. Honor an already
provided, applicable exact-byte authorization without requesting duplicate
approval; a changed candidate invalidates authorization tied to older bytes.
