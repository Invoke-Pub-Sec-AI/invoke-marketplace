# Locate and inspect the worker

Resolve the user's selected AA repository or current workspace containing
`src/pseudonyms.py`, `src/agent_team.py` and `docs/CONTEXT.md`. If none is selected,
locate the maintained AA research-team repository; this is a discovery fallback,
not a license to apply an unrelated checkout's rules. Confirm the repository
before using it. Installed skill paths are independent of checkout layout.

Read its `AGENTS.md` and current `docs/CONTEXT.md`. Inspect only implementation
needed for the task; current code wins over this navigation guide. Before changing
worker phases, consult `docs/OPENAI_MATH_RESEARCH_METHOD.md` as repository guidance
requires. Source-bearing artifacts stay in the approved target.

| Operation | Source of truth |
| --- | --- |
| Validate aliases, allocate/reuse local keys, substitute prose | `src/pseudonyms.py`: `Registry`, `register`, `replace`, `validate_tokens`, `validate_preserved` |
| Host masking, declared/observed changes, claim preservation and specialist audit | `src/agent_team.py`: `local_scrub`, `changed_paths`, `preserve_claims`, `AgentTeam.sanitize` |
| Runtime role instructions | `src/prompts.py` |
| Document-scoped catalog allocation and continuation binding | `src/catalog.py`: `_Aggregate` and its pseudonym reservation/merge checks |
| Summary eligibility and exact review boundary | `src/research_release.py` |

The legacy `aa-private-pseudonyms/1` lookup contains
`entries:[{key,category,values}]`. Values are original exact aliases. Registering
an alias proves its occurrence in the supplied private source; it does not prove
that variants refer to one person. Registry mutation is atomic and rejects invalid
identity sequences and conflicting aliases. Read current validation for bounds.

The `aa-private-catalog-pseudonyms/1` lookup retains global `key`, `local_key`,
category, values and document identity. Preserve validated child receipts and
`pseudonym_order`; reconstruct keys through the existing continuation path rather
than trusting an unbound root lookup or merging names globally.

The private lookup artifact, source-bearing research dumps and review details remain
target-only, including partial, failed or stopped work. Retained-key guards do
not establish semantic fidelity; deleted or structurally changed fields still
need evidence-aware review. Input review remains bound to its exact snapshot and
the existing no-PII/PHI handling declaration.
