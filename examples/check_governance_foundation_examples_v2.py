#!/usr/bin/env python3
"""Replay preserved examples and check the supplemental conceptual constructions.

Offline and deterministic. No model calls or benchmark modifications. The v1
runner and scientific receipt are read-only inputs. --record creates a new
receipt exclusively; the default checks that receipt without replacing it.
"""
import argparse
from contextlib import redirect_stdout
import hashlib
import importlib.util
from io import StringIO
from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / 'examples/check_governance_foundation_examples_v1.py'
ORIGINAL = ROOT / 'examples/recorded-foundation-examples.json'
RECEIPT = ROOT / 'examples/recorded-foundation-examples-v2.json'
V1_SHA = '92b1f51ede221ba5c76a8d37ccabad27af272640d9f298e46fc926f77bd77f49'
ORIGINAL_SHA = '5de090ea9d5d19d5c91268b87aa0b7f507d11f2fcecaa99e8672858b0655695c'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_checks():
    assert sha(V1) == V1_SHA, 'Preserved v1 runner changed'
    assert sha(ORIGINAL) == ORIGINAL_SHA, 'Preserved original receipt changed'
    spec = importlib.util.spec_from_file_location('preserved_examples', V1)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    with TemporaryDirectory(prefix='foundation-examples-v2-') as temporary:
        original.OUTPUT = Path(temporary) / 'v1-replay.json'
        with redirect_stdout(StringIO()):
            original.main()
        replay = json.loads(original.OUTPUT.read_text())
    recorded = json.loads(ORIGINAL.read_text())
    replay.pop('script_sha256')
    recorded.pop('script_sha256')
    assert replay == recorded, 'Original scientific results changed'

    def worlds_for(supported, atoms, integrity):
        worlds = [dict(zip(atoms, bits)) for bits in product([False, True], repeat=len(atoms))]
        worlds = [world for world in worlds if integrity(world)]
        satisfies = lambda world, literals: all(world[atom] == value for atom, value in literals)
        repairs = original.maximal_repairs(supported, lambda literals: any(satisfies(w, literals) for w in worlds))
        return [w for w in worlds if any(satisfies(w, repair) for repair in repairs)], repairs

    def decision(worlds, predicate):
        if not worlds:
            raise ValueError('An empty admissible-world set requires a failure policy')
        values = [bool(predicate(world)) for world in worlds]
        return 'allow' if all(values) else 'deny' if not any(values) else 'undetermined'

    integrity = lambda w: not (w['p'] and w['c'])
    release = lambda w: w['p'] and not w['c']
    with_r3, repairs = worlds_for([('p', True), ('c', True)], ['p', 'c'], integrity)
    without_r3, reduced_repairs = worlds_for([('c', True)], ['p', 'c'], integrity)
    assert without_r3 == [{'p': False, 'c': True}]
    assert decision(without_r3, release) == 'deny'
    assert decision(with_r3, release) == 'undetermined'
    assert original.packing([frozenset(['o1', 'o2']), frozenset(['o2', 'o3'])])[0] == 1
    assert original.packing([frozenset(['o1', 'o2']), frozenset(['o2', 'o3']), frozenset(['o4'])])[0] == 2
    observations = {}
    for atom in ['p', 'c']:
        observations[atom] = {}
        for value in [False, True]:
            branch = [w for w in with_r3 if w[atom] == value]
            assert branch, 'Observation branches must be attainable'
            observations[atom][str(value)] = decision(branch, release)
        assert set(observations[atom].values()) == {'allow', 'deny'}

    profiles = original.subsets(['a', 'b'])
    base = [(('a',), 'm'), (('b',), 't'), (('m', 't'), 'release')]
    joint = [(('a',), 'u'), (('u',), 't')]
    semantic_validity = {}
    for name, edit in [('empty', []), ('joint', joint)]:
        gains = [sorted(p) for p in profiles
                 if 'release' in original.closure(p, base + edit)
                 and 'release' not in original.closure(p, base)]
        goal_met = 'm' in original.closure({'a'}, base + edit)
        semantic_validity[name] = {'gains': gains, 'goal_met': goal_met,
                                   'valid': goal_met and not gains}
    assert semantic_validity['empty']['valid']
    assert not semantic_validity['joint']['valid']

    # All reports below are stipulated current, authorized and in scope. Each
    # answer affirmatively asserts eligibility; an undetermined answer would
    # instead be correct on the one-report packet.
    packets = {'pair': [frozenset(['e1']), frozenset(['e2'])],
               'single': [frozenset(['e1'])]}
    eligibility = {}
    for name, reports in packets.items():
        quorum = original.packing(reports)[0] >= 2
        worlds, _ = worlds_for([('eligible', True)] if quorum else [],
                               ['eligible'], lambda w: True)
        warranted = decision(worlds, lambda w: w['eligible'])
        eligibility[name] = {'quorum': quorum, 'decision': warranted,
                             'affirmative_assertion_warranted': warranted == 'allow'}
    assert eligibility['pair']['decision'] == 'allow'
    assert eligibility['single']['decision'] == 'undetermined'
    four_cells = [dict(change=change, packet=packet,
                       proposed_change_valid=semantic_validity[change]['valid'],
                       response_eligibility_assertion='allow',
                       asserted_eligibility_warranted=eligibility[packet]['affirmative_assertion_warranted'])
                  for change in ['empty', 'joint'] for packet in ['pair', 'single']]
    assert {(r['proposed_change_valid'], r['asserted_eligibility_warranted'])
            for r in four_cells} == set(product([False, True], repeat=2))
    assert eligibility['single']['decision'] == 'undetermined'  # Correct abstention, not an error.

    empty_worlds, _ = worlds_for([], ['p'], lambda w: False)
    try:
        decision(empty_worlds, lambda w: w['p'])
    except ValueError:
        empty_world_rejected = True
    else:
        raise AssertionError('Vacuous permission must not be granted')
    negative_worlds, _ = worlds_for([('p', False)], ['p'], lambda w: True)
    assert decision(negative_worlds, lambda w: w['p']) == 'deny'
    assert sha(V1) == V1_SHA and sha(ORIGINAL) == ORIGINAL_SHA
    return {
        'status': 'PASS', 'new_model_calls': 0, 'benchmark_inputs_changed': False,
        'scope': 'Supplemental finite conceptual checks, not new model measurements.',
        'preserved_v1_runner_sha256': V1_SHA, 'preserved_original_receipt_sha256': ORIGINAL_SHA,
        'v1_scientific_replay_exact_except_documented_runner_hash': True,
        'checker_sha256': sha(Path(__file__)),
        'removed_r3': {'worlds': without_r3, 'release': 'deny',
                       'after_r3_added_release': 'undetermined'},
        'observation_branches': observations,
        'semantic_construction': semantic_validity,
        'eligibility_packets': eligibility, 'four_cell_affirmative_answers': four_cells,
        'one_report_undetermined_answer_is_correct': True,
        'empty_world_set_rejected': empty_world_rejected,
        'supported_negative_literal_is_respected': True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true', help='Create the supplemental receipt once')
    args = parser.parse_args()
    actual = run_checks()
    if args.record:
        with RECEIPT.open('x') as stream:
            json.dump(actual, stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        assert actual == json.loads(RECEIPT.read_text()), 'Supplemental receipt replay differs'
    print('PASS: preserved v1 replay; four-cell assertions; deny-to-undetermined transition; observation branches; empty-world guard')


if __name__ == '__main__':
    main()
