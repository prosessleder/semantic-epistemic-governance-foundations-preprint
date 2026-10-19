#!/usr/bin/env python3
"""Build the editable source and HTML; optionally export a PDF with Tectonic."""
import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--pdf', action='store_true')
args = parser.parse_args()
out = ROOT / 'output/pdf'
out.mkdir(parents=True, exist_ok=True)
tex = out / 'semantic-epistemic-governance-foundations.tex'
shutil.copyfile(ROOT / 'paper.tex', tex)
subprocess.run(['pandoc', str(ROOT / 'paper.md'), '--standalone', '--mathml',
                '--metadata=pagetitle:Semantic and Epistemic Governance',
                '--output=' + str(ROOT / 'output/paper.html')], check=True)
if args.pdf:
    subprocess.run(['tectonic', '--only-cached', '--keep-logs',
                    '--outdir', str(out), str(tex)], check=True)
print('Generated standalone source:', tex)
