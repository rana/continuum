# Builder expected-layout corpus closeout

This Research Delta fully reads `research/owned-stack/2026-10-16/native-builder-slice/preparation-01/fixtures/expected/01.layout.json` at Base12 commit `88382e793b65c84fd8e223840c27f6bb8682864a`, tree `5cf96129bdcb0dde075f6f5800ae0c68a95c4b82`. The 45,963-byte file has Git blob identity `46ea90748643ed2a51d364bbb1dd8c69de1be51a` and SHA-256 `5e434b2498e1225d398929f01b8cabb51a9da70f40915d04dd2cb948c6e11a77`. This chat owns the read-only contribution based on Continuum main `89e790e880240f2a97f1f7217e4ccd703fdbe417`. The [ledger](base12-coverage-builder-layout-corpus-closeout.json) and [validation record](../../research/runs/base12-builder-layout-corpus-closeout/validation.json) retain the exact source and executed checks.

## Complete runner metadata

All thirteen top-level fields were read. A lossless compact projection includes every label, every relocation record, all 518 map rows and the complete embedded code field; no record is represented by an omitted middle. Original source-position reconstruction reproduces all fields and the complete JSON bytes, including key order and formatting.

The fixture input is byte-identical to the previously held runner source, so that held source supplies the join without claiming fresh acquisition of the fixture path. Its 471 instructions, 47 labels and 109 relocations agree with the frozen manifest. Source-derived instruction widths determine every map offset and encoded span.

All 518 source rows agree with the held migration table, including label names, source lines, kinds, file offsets and lengths. All 47 named labels agree after explicitly converting the migration table's virtual addresses to layout file offsets by subtracting the fixed image base. All 109 patches agree on target name, field offset and signed displacement. Treating file offsets and virtual addresses as interchangeable would break this relation.

## Supplied bytes checked against source fields

The complete embedded code field contains 2,834 bytes. Original finite checks cover all 471 instruction snippets across the runner's 33 retained contract forms. For 362 nonrelocating instructions, checks read the saved REX/opcode, register or memory fields, minimal displacement width and literal immediate fields as applicable. For 109 branches/calls, opcode, instruction boundary, named target and signed four-byte displacement agree with the source. There are 91 positive and 18 negative displacements.

These are checks of supplied data against retained source semantics, reusing the finite field method applied earlier to the witness set. They neither invoke an upstream encoder nor produce a native file. They are scoped to these contract families and correlated authored data, rather than a general compiler proof or an independent runtime oracle.

The literal source-position map reconstructs 16,608 bytes with the expected digest, completing the earlier migration review's predicted-map relation. The declared 6,930-byte ELF length agrees with its fixed prefix plus code length. Its ELF digest remains copied from the frozen case manifest; unacquired headers and padding were not reconstructed or authenticated. Saved successful status, publication flag and output metadata agree with that manifest, with no new candidate invocation.

## Closed layout scope, open artifact scope

All **32 expected-layout paths / 213,453 path bytes** in this fixture directory now have full semantic reading or identical-blob credit. They contain **17 distinct blobs**. Repeated layouts retain their separate source conditions and fault-case contexts; their byte equality does not imply identical expected publication outcomes or observed parser progress.

This closes a useful static evidence chain: complete source text, source-position records, label/patch metadata and supplied literal encoding fields agree within the retained corpus. The result makes later artifact checks more precise without converting a hypothetical expected layout into an observed native output. The transferable lesson is to close each representation layer explicitly, preserving address conversions and data provenance across joins.

No raw map or ELF was acquired, upstream module imported, materializer/candidate executed, native artifact emitted, model consulted, live process scanned, workstation activated or upstream recipient acceptance obtained.

Cumulative semantic reading reaches **595 distinct blobs / 5,239,835 bytes**, plus **94 identical alias paths**. **4,904 paths / 3,834 distinct blobs** still lack full semantic-reading credit. Historical global acquisition overlap and whole-repository reading remain incomplete.

Next: read only the binary map metadata for expected02/03/04, totaling 7,808 bytes. Decode every header/record field and compare it with the fully read layouts. This bounded metadata acquisition leaves native ELF/code artifacts and execution outside the unit. Reconcile fresh main and ownership first; owned-storage, dispatch and public checkpoint lanes remain separate. No recipient has accepted that next unit.
