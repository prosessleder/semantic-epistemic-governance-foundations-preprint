#!/usr/bin/env python3
"""Exhaustive checks for conceptual paper examples; no benchmark/model calls."""
from itertools import combinations, product
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'output/foundation-examples.json'


def subsets(values):
    values=tuple(values)
    return [frozenset(c) for n in range(len(values)+1) for c in combinations(values,n)]


def closure(profile,rules):
    facts=set(profile)
    while True:
        expanded=facts|{head for body,head in rules if set(body)<=facts}
        if expanded==facts:return facts
        facts=expanded


def packing(reports):
    valid=[s for s in subsets(range(len(reports))) if all(not(reports[a]&reports[b]) for a,b in combinations(s,2))]
    best=max(map(len,valid))
    return best,[sorted(s) for s in valid if len(s)==best]


def maximal_repairs(support,consistent):
    candidates=[s for s in subsets(support) if consistent(s)]
    return [s for s in candidates if not any(s<t for t in candidates)]


def main():
    profiles=subsets(['a','b'])
    old=[(('a',),'m'),(('b',),'t'),(('m','t'),'release')]
    d1=[(('a',),'u')];d2=[(('u',),'t')]
    variants={'original':old,'first_only':old+d1,'second_only':old+d2,'combined':old+d1+d2}
    values={k:[bool('release' in closure(p,v)) for p in profiles] for k,v in variants.items()}
    assert values=={'original':[False,False,False,True], 'first_only':[False,False,False,True],
                    'second_only':[False,False,False,True], 'combined':[False,True,False,True]}
    gains={k:[sorted(p) for p,v,b in zip(profiles,a,values['original']) if v and not b] for k,a in values.items()}
    assert gains['combined']==[['a']] and not gains['first_only'] and not gains['second_only']
    p_reports=[frozenset(x) for x in [('o1','o2'),('o2','o3'),('o4',)]]
    c_reports=[frozenset(['o5']),frozenset(['o6'])]
    pmax,pcert=packing(p_reports);cmax,ccert=packing(c_reports)
    assert pmax==cmax==2 and packing(p_reports[:2])[0]==1
    consistent=lambda s:not {'p','c'}<=s
    repairs=maximal_repairs(['p','c'],consistent);assert set(repairs)=={frozenset(['p']),frozenset(['c'])}
    worlds=[dict(zip(['p','c'],bits)) for bits in product([False,True],repeat=2)]
    worlds=[w for w in worlds if consistent({a for a,v in w.items() if v}) and any(all(w[a] for a in r) for r in repairs)]
    predicates={'release':lambda w:w['p'] and not w['c'],'override':lambda w:w['p'] and w['c'],'retain':lambda w:w['p'] or w['c']}
    def warrant(ws):
        assert ws
        return {a:'allow' if all(f(w) for w in ws) else 'deny' if not any(f(w) for w in ws) else 'undetermined' for a,f in predicates.items()}
    actions=warrant(worlds);assert actions=={'release':'undetermined','override':'deny','retain':'allow'}
    branches={str(result):warrant([w for w in worlds if w['p']==result]) for result in [False,True]}
    assert branches['True']['release']=='allow' and branches['False']['release']=='deny'
    assert all('undetermined' not in x.values() for x in branches.values())
    # Zero-query plans leave one action open; either p or c, cost one, resolves all.
    assert sum(v=='undetermined' for v in actions.values())==1
    for atom in ['p','c']:
        assert all('undetermined' not in warrant([w for w in worlds if w[atom]==result]).values() for result in [False,True])
    other=maximal_repairs(['p','c','d'],lambda s:not({'p','c'}<=s or {'p','d'}<=s))
    assert set(other)=={frozenset(['p']),frozenset(['c','d'])}
    result=dict(status='PASS',new_model_calls=0,benchmark_inputs_changed=False,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        semantic=dict(profiles=[sorted(p) for p in profiles],release=values,gains=gains),
        epistemic=dict(p_maximum_disjoint=pmax,p_certificates=pcert,c_maximum_disjoint=cmax,c_certificates=ccert,
            p_without_independent_report=packing(p_reports[:2])[0],repairs=[sorted(s) for s in repairs],worlds=worlds,
            actions=actions,p_observation_branches=branches,optimal_objective=[0,1],tied_optimal_observations=['p','c'],
            inclusion_maximal_not_maximum=[sorted(s) for s in other]),
        scope='Conceptual illustrations, exhaustive finite checks; not model measurements or benchmark additions.')
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with OUTPUT.open('w') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print('PASS: four profiles, joint-edit gain, provenance packings, repairs, worlds, actions and tied one-step plans')


if __name__=='__main__':main()
