# Legacy summary release

Match the packaged runtime to its source revision. Read `src/cli.py` for commands, `src/agent_exchange.py` for the graph, and `src/research_release.py` for the archive contract. The PDF worker has a different launcher and output format.

## Check the draft and archive

In the reviewed graph implementation, `aa-research-return/5` is the archive schema and `aa-research-summary/2` is the embedded release schema. Read the selected revision's schema constants when checking another package.

- `export_artifacts` derives the root JSON reports and individual PBC and KSD projections. `load_draft` checks their membership and content against the reviewed graph. Recreate a stale draft before seeking review.
- `validate_review` checks the human declarations and their binding to the exact payload. A changed payload needs a new review. The canonical payload hash and the ZIP file hash identify different objects.
- `create_archive` checks the review and its output. `read_archive` verifies member names, manifest membership, hashes, export identity, and projection consistency. Use `expected_payload_sha256` when the reviewed payload hash is available.

## Package the reviewed return

Find the matching draft, review, pack, or unpack command in the selected parser's source. Record review declarations only for the bytes the authorized reviewer approved. Preserve the existing review receipt and write the archive or unpacked files to a fresh destination.

After packing, use the maintained reader or unpack path to verify the return. Keep source files, private lookup data, and the target-only human-readable report in the approved workspace.
