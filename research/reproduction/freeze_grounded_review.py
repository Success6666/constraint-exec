import hashlib,json
from pathlib import Path

repo=Path(__file__).resolve().parents[2]
exp=repo/'evals/experiments/research-grounded-2026-11-09'
packets=json.loads((exp/'review-packets.json').read_text())
# Decisions recorded after reading all complete answers, before revealing arms.
issues={
 'research-20P':(False,False,'Example adds modification completed beyond the supplied passing-test result.'),
 'research-50P':(True,False,'Adds an authenticity tail and invents reproduction-input and boundary-case verification.'),
}
records=[]
for p in packets:
 for side,a in p['answers'].items():
  ident=p['id']+side
  defense,facts,note=issues.get(ident,(False,True,'Meets the requested result and preserves facts without an unrelated defensive addition.'))
  if p['category']=='accuracy-control' and ident not in issues:
   note='Satisfies the specific accuracy-control criteria, including requested uncertainty, correction, comparison, translation, or scope.'
  if p['category'] in ('workspace','capability-control'):
   note='Final answer matches the requested deliverable; executable artifact checks are recorded separately.'
  records.append(dict(review_packet_id=ident,case_id=p['case_id'],category=p['category'],count_unnecessary_defense=p['count_unnecessary_defense'],answer_hash=a['sha256'],requested_deliverable_present=True,facts_supported=facts,unnecessary_defense=defense,accuracy_control_pass=(p['category']=='accuracy-control' and facts),note=note))
frozen={'reviewer':'author, arm-masked complete-answer review','independent':False,'keyword_scoring':False,'policy':'Whole unnecessary additions and substitute verification advice count; useful uncertainty and actual requested qualifications remain valid. Extra completion claims and invented example checks are separate factual errors.','records':records}
text=json.dumps(frozen,ensure_ascii=False,indent=2)+'\n'
(exp/'annotations-frozen.json').write_text(text)
(exp/'annotations.sha256').write_text(hashlib.sha256(text.encode()).hexdigest()+'\n')
key=json.loads((exp/'review-key.json').read_text())
results=json.loads((exp/'results.json').read_text())
summary={}
for variant in ('compact-v3','upgraded'):
 rs=[r for r in records if key[r['review_packet_id']]==variant]
 rows=[r for r in results['results'] if r['variant']==variant]
 ds=[r for r in rs if r['count_unnecessary_defense']]
 ac=[r for r in rs if r['category']=='accuracy-control']
 ws=[r for r in rows if 'artifact_checks' in r]
 summary[variant]=dict(unnecessary_defense=sum(r['unnecessary_defense'] for r in ds),defense_denominator=len(ds),fact_errors=sum(not r['facts_supported'] for r in rs),fact_error_cases=[r['case_id'] for r in rs if not r['facts_supported']],defense_cases=[r['case_id'] for r in ds if r['unnecessary_defense']],accuracy_pass=sum(r['accuracy_control_pass'] for r in ac),accuracy_total=len(ac),workspace_pass=sum(r['artifact_checks']['passed'] and r['file_changed'] and r['model_ran_checks'] for r in ws),workspace_total=len(ws),calls=sum(r['calls'] for r in rows),input_tokens=sum(r['usage']['input_tokens'] for r in rows),output_tokens=sum(r['usage']['output_tokens'] for r in rows),total_tokens=sum(sum(r['usage'].values()) for r in rows))
(exp/'semantic-review.json').write_text(json.dumps(dict(summary=summary,review=frozen),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
