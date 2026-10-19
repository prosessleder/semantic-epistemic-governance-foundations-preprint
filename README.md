# Semantic and Epistemic Governance

**Semantic and Epistemic Governance in Language-Model Reasoning**

Timothy O'Brien · Preprint 0.2.0, released 19 October 2026 · Not peer reviewed

ORCID: [0009-0001-2589-347X](https://orcid.org/0009-0001-2589-347X).

This conceptual methods paper distinguishes judging what an ontology change
permits from judging what supplied evidence warrants. It specifies task-relative
contracts for protected consequences, source authority, provenance, conflicting
interpretations and warranted action. Its contribution is an evaluation-oriented
synthesis of established foundations, illustrated by exhaustive finite examples.
It introduces no new model measurements.

## Manuscript and scientific supplement

| File | Purpose |
|---|---|
| [paper.tex](paper.tex) | Canonical editable manuscript |
| [paper.md](paper.md) | Readable manuscript companion |
| [output/pdf/semantic-epistemic-governance-foundations.pdf](output/pdf/semantic-epistemic-governance-foundations.pdf) | Typeset manuscript |
| [output/pdf/semantic-epistemic-governance-foundations.tex](output/pdf/semantic-epistemic-governance-foundations.tex) | Exact standalone source copy |
| [references.md](references.md) | Nine references and primary-source links |
| [examples/README.md](examples/README.md) | Scope and replay instructions for the preserved and supplemental examples |
| [examples/check_governance_foundation_examples_v2.py](examples/check_governance_foundation_examples_v2.py) | Offline original and supplemental finite-example replay |
| [release/semantic-epistemic-governance-foundations-0.2.0-preprint.zip](release/semantic-epistemic-governance-foundations-0.2.0-preprint.zip) | Scientific supplement with an explicit SHA-256 manifest |

The supplement includes both preserved v1 scientific files byte-for-byte and a
separately versioned v2 checker and receipt. The v2 checks make explicit that an
unsupported affirmative assertion differs from a correct undetermined answer,
and that adding a conflicting supported report can turn denial into indeterminacy.
Neither checker calls models or modifies a benchmark.

## Verify and build

Requires Python 3.9 or newer and Pandoc. The manuscript uses `elsarticle`, 12-point,
single-column A4, wrapped tables, author ORCID and a CC BY notice. Tectonic is
needed for local PDF export; the built-in LaTeX editor can compile the standalone
source independently. The Tectonic command uses cached dependencies only.

```sh
python3 -B scripts/build_paper.py --pdf
python3 -B scripts/check_project.py
python3 -B scripts/package_release.py
python3 -B scripts/check_project.py --package
```

The check command replays the original scientific receipt in a temporary
directory, checks the supplemental receipt and verifies source-copy consistency.
Its `--package` check also verifies every ZIP member against the manifest and
current scientific files. The ZIP contains a strict scientific allowlist: no
agent instructions, private review notes, local-path provenance, logs or compiler
intermediates. All replay code runs offline. Edit `paper.tex` and synchronize
`paper.md`, then rebuild both generated formats and the supplement.

## Status and rights

This is the public preprint and scientific supplement, version `0.2.0-preprint`.
[Download the release](https://github.com/prosessleder/semantic-epistemic-governance-foundations-preprint/releases/tag/v0.2.0-preprint).
It has no assigned DOI and makes no journal submission, acceptance or external
peer-review claim. The author conducted the
work independently, without institutional affiliation, and confirmed no external
funding and no competing interests. Venue-specific submission requirements must
be applied before submission.

The manuscript and original supporting materials are licensed under
[CC BY 4.0](LICENSE.md). Linked third-party sources retain their own rights.
