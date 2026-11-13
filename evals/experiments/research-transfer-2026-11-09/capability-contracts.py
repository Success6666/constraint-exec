from pathlib import Path
import ast,json,re,subprocess,sys,tempfile,hashlib
repo=Path(__file__).resolve().parents[3];exp=Path(__file__).resolve().parent
sys.path.insert(0,str(repo/'evals'))
from runtime_env import clean_subprocess_environment
saved=exp/'capability-checks.json';done=json.loads(saved.read_text()) if saved.exists() else {}
for p in [exp/'review-packets.json']:
 for pair in json.loads(p.read_text()):
  if pair['category']!='capability-control':continue
  for side,ans in pair['answers'].items():
   ident=pair['id']+side
   if ident in done:continue
   cid=pair['case_id'];raw=ans['text'];row={'case_id':cid,'repeat':pair['repeat'],'review_packet_id':ident,'passed':False}
   try:
    if cid=='exact-format-en':
     val=json.loads(raw);assert val=={'before_ms':120,'after_ms':90,'reduction_pct':25};row['passed']=True;row['checks']=['exact JSON object and numeric result']
    else:
     fences=re.findall(r'```(?:python)?\s*\n(.*?)```',raw,re.S);source=next((s for s in fences if 'def ' in s),raw)
     tree=ast.parse(source);funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
     if cid=='required-enforcement-zh':
      assert raw.lstrip().startswith('def accept_upload(');assert len(tree.body)==1
      test="assert [m.accept_upload(v) for v in ['a.exe','b.sh','a.EXE','B.Sh','c.txt','shell','a.exe.txt']]==[False,False,False,False,True,True,True]"
      row['checks']=['extension rejection','case insensitivity','other names accepted','only function code']
     elif cid=='soft-dependency-en':
      assert len(funcs)==1;name=funcs[0].name
      test=f"x=m.{name}('category,amount\\n\\\"a,b\\\",2.5\\n\\\"a,b\\\",1.5\\n餐饮,-1\\n');assert float(x['a,b'])==4.0 and float(x['餐饮'])==-1.0;assert m.{name}('category,amount\\n')=={{}}"
      row['checks']=['quoted comma parsing','Unicode category','repeated category sum','negative amount','empty CSV']
     else:
      sn=next(n.name for n in funcs if 'save' in n.name);ln=next(n.name for n in funcs if 'load' in n.name)
      # Ignore top-level demonstration calls while preserving imports, constants and complete functions.
      tree.body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef)) or isinstance(n,ast.Assign) and not any(isinstance(z,ast.Call) and isinstance(z.func,ast.Name) and z.func.id in {sn,ln} for z in ast.walk(n))]
      source=ast.unparse(tree)
      sa=next(n for n in funcs if n.name==sn);la=next(n for n in funcs if n.name==ln)
      assert len(sa.args.args) in [1,2] and len(la.args.args) in [0,1]
      if len(sa.args.args)==1:
       test=f"items=[{{'title':'买牛奶','done':False}}];m.{sn}(items);assert m.{ln}()==items;m.{sn}([]);assert m.{ln}()==[]"
      else:
       first=sa.args.args[0].arg;args="'tasks.json',items" if any(x in first for x in ['path','file']) else "items,'tasks.json'"
       empty="'tasks.json',[]" if any(x in first for x in ['path','file']) else "[],'tasks.json'"
       test=f"items=[{{'title':'买牛奶','done':False}}];m.{sn}({args});assert m.{ln}('tasks.json')==items;m.{sn}({empty});assert m.{ln}('tasks.json')==[]"
      test+=";from pathlib import Path;assert any(p.suffix=='.json' for p in Path('.').iterdir())"
      row['checks']=['Unicode JSON persistence','independent reload','overwrite with empty list','durable file exists']
     with tempfile.TemporaryDirectory(prefix='compact-capability-') as temp:
      (Path(temp)/'sample.py').write_text(source)
      check='import sys;sys.path.insert(0,".");import sample as m;'+test+';print("PASS")'
      r=subprocess.run([sys.executable,'-I','-c',check],cwd=temp,env=clean_subprocess_environment(),capture_output=True,text=True,timeout=5)
      row.update({'passed':r.returncode==0,'output':r.stdout+r.stderr,'source_hash':hashlib.sha256(source.encode()).hexdigest()})
   except Exception as e:row['error']=str(e)
   done[ident]=row
saved.write_text(json.dumps(done,ensure_ascii=False,indent=2)+'\n')
print({'checked':len(done),'passed':sum(r['passed'] for r in done.values()),'failures':[r for r in done.values() if not r['passed']]})
