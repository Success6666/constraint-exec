import sys
import hashlib
import json
import random
import shutil
from pathlib import Path

repo=Path(__file__).resolve().parents[2]
exp=repo/'evals/experiments'/(sys.argv[1] if len(sys.argv)>1 else 'research-transfer-2026-11-09')
data=json.loads((exp/'results.json').read_text())
assert len(data['results'])==data['expected_rows']==120
assert all(r['success'] for r in data['results'])
cases=json.loads((repo/'evals/research_combined_cases.json').read_text())
rows={(r['case_id'],r['variant']):r for r in data['results']}
rng=random.Random(971239 if "grounded" in exp.name else 826913 if "refined" in exp.name else 791113)
rng.shuffle(cases)
packets=[];key={}
for i,c in enumerate(cases,1):
    arms=['compact-v3','upgraded'];rng.shuffle(arms)
    packet={'id':f'research-{i:02d}','case_id':c['id'],'repeat':1,'category':c['category'],'cohort':c.get('cohort'),'count_unnecessary_defense':c['count_unnecessary_defense'],'messages':c['messages'],'criteria':c['review_criteria'],'answers':{}}
    for side,arm in zip(('P','Q'),arms):
        path=exp/'raw/r1'/arm/c['id']/'answer.md'
        t=path.read_text()
        packet['answers'][side]={'text':t,'sha256':hashlib.sha256(t.encode()).hexdigest()}
        key[packet['id']+side]=arm
    packets.append(packet)
(exp/'review-packets.json').write_text(json.dumps(packets,ensure_ascii=False,indent=2)+'\n')
(exp/'review-key.json').write_text(json.dumps(key,indent=2)+'\n')
shutil.copyfile(repo/'evals/experiments/compact-entry-refined-2026-11-09/capability-contracts.py',exp/'capability-contracts.py')
print('Prepared 60 arm-masked packets; author review, not independent.')
