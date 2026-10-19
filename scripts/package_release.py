#!/usr/bin/env python3
"""Build a local scientific supplement from an explicit publication allowlist.

This creates no public release, deposit or DOI. Private review/provenance files,
agent instructions, local paths, logs and compiler intermediates are excluded.
"""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    'README.md', 'LICENSE.md', 'CITATION.cff', 'paper.tex', 'paper.md',
    'references.md', 'output/paper.html',
    'output/pdf/semantic-epistemic-governance-foundations.tex',
    'output/pdf/semantic-epistemic-governance-foundations.pdf',
    'scripts/build_paper.py', 'scripts/check_project.py', 'scripts/package_release.py',
    'examples/README.md',
    'examples/check_governance_foundation_examples_v1.py',
    'examples/recorded-foundation-examples.json',
    'examples/check_governance_foundation_examples_v2.py',
    'examples/recorded-foundation-examples-v2.json',
]
TARGET = ROOT / 'release/semantic-epistemic-governance-foundations-0.2.0-preprint.zip'


def main():
    payloads = {name: (ROOT / name).read_bytes() for name in sorted(FILES)}
    for name, data in payloads.items():
        assert (b'/' + b'Users/') not in data and (b'/' + b'private/tmp/') not in data, name
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()}
    payloads['SHA256SUMS.json'] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(TARGET, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in payloads.items():
            info = ZipInfo(name, date_time=(2026, 10, 19, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    print(TARGET)


if __name__ == '__main__':
    main()
