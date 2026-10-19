# Finite conceptual examples

These checks are deterministic and run offline with Python 3.9 or newer. They
make no model calls and do not create or modify benchmark cases.

`check_governance_foundation_examples_v1.py` and
`recorded-foundation-examples.json` preserve the original portable runner and
scientific fixture. The recorded receipt names the original research runner's
hash; the portable runner has a different hash because its output path differs.
The v2 replay compares every scientific result after removing only that field.

`check_governance_foundation_examples_v2.py` adds separately recorded checks for
the manuscript's affirmative-eligibility four-cell construction, correct
undetermined answers under insufficient evidence, the deny-to-undetermined
transition after adding a disjoint-origin report, both attainable observation
branches, negative literals and rejection of an empty admissible-world set.
It pins both preserved v1 input hashes and never rewrites either input.

Run the complete replay from the package root:

```sh
python3 -B examples/check_governance_foundation_examples_v2.py
```

The v2 checker uses a temporary directory for the v1 replay. Its default command
verifies `recorded-foundation-examples-v2.json` without replacing it. The
development-only `--record` option creates that supplemental receipt exclusively
and refuses to replace an existing receipt. Exhaustion of these small finite
domains establishes the stated illustrative consequences under the supplied
contracts; it does not validate the governance policies in a deployment.
