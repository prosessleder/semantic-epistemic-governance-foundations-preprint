#!/usr/bin/env python3
"""Offline example replay and package consistency checks; no model calls."""
import json
from pathlib import Path
import subprocess
import sys
import hashlib
from zipfile import ZipFile
from package_release import FILES

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, '-B', str(ROOT / 'examples/check_governance_foundation_examples_v2.py')], check=True)
tex = (ROOT / 'paper.tex').read_text()
assert tex == (ROOT / 'output/pdf/semantic-epistemic-governance-foundations.tex').read_text()
assert tex.count('\\begin{tabularx}') == tex.count('\\end{tabularx}') == 5
assert '\\resizebox' not in tex
assert 'Semantic and Epistemic Governance in Language-Model Reasoning' in (ROOT / 'paper.md').read_text()
assert '10.5281/zenodo.23401477' not in (ROOT / 'CITATION.cff').read_text()
assert tex.count('\\bibitem{') == 9
assert 'In every cell, consider an answer' in tex
assert 'insufficient evidence alone is not an evidence-use error' in tex
assert 'preliminary results are not yet available' not in tex
declarations = (
    'The author declares no competing interests.',
    'This research received no external funding.',
    'conducted this work independently, without institutional affiliation.',
)
markdown = (ROOT / 'paper.md').read_text()
for declaration in declarations:
    assert declaration in tex and declaration in markdown, 'Declaration differs: ' + declaration
assert 'confirmed no external\nfunding and no competing interests.' in (ROOT / 'README.md').read_text()
for current_text in (tex, markdown, (ROOT / 'README.md').read_text()):
    assert 'semantic-epistemic-governance-' + 'level1' not in current_text
    assert 'transport-' + 'unknown slots' not in current_text
if '--package' in sys.argv:
    package = ROOT / 'release/semantic-epistemic-governance-foundations-0.2.0-preprint.zip'
    with ZipFile(package) as archive:
        manifest = json.loads(archive.read('SHA256SUMS.json'))
        assert sorted(manifest) == sorted(FILES), 'Publication allowlist differs'
        assert sorted(archive.namelist()) == sorted([*manifest, 'SHA256SUMS.json'])
        for name, expected in manifest.items():
            assert not name.startswith('/') and '..' not in Path(name).parts
            assert not name.startswith('validation/') and name != 'AGENTS.md'
            assert Path(name).suffix not in {'.aux', '.log', '.out', '.xdv', '.pyc'}
            data = archive.read(name)
            assert hashlib.sha256(data).hexdigest() == expected
            assert data == (ROOT / name).read_bytes(), 'Packaged file differs: ' + name
            assert (b'/' + b'Users/') not in data and (b'/' + b'private/tmp/') not in data
print('PASS: preserved and supplemental finite examples, editable source, citations and publication-package boundaries')
