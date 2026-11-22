#!/usr/bin/env python3
"""Finish classification and reuse three existing records through Zotero 10's
authenticated local API. Uses Zotero's native user-authorization dialog.
No keys are printed or stored. Newly imported redundant parents go to Trash.
"""
import argparse
import concurrent.futures as cf
import json
from pathlib import Path
import re
import uuid
import requests

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:23119'
API=BASE+'/api/users/0'
from import_iwm_zotero import COLLECTIONS,CROSS_CUTTING

def get(tail,**params):
    r=requests.get(API+tail,params=params or None,timeout=25);r.raise_for_status();return r.json()

def prepare():
    papers=json.loads((ROOT/'papers/manifest.json').read_text())
    docs=json.loads((ROOT/'research/supplementary_sources.json').read_text())
    existing=json.loads((ROOT/'research/zotero_existing_matches.json').read_text())
    receipt=json.loads((ROOT/'research/zotero_import_receipt.json').read_text())
    imported=receipt['response'];byid={}
    for i in imported:
        m=re.search(r'IWM (?:ID|source ID): (P\d+|S\d+)',i.get('extra',''))
        assert m,('missing ID',i['key']);byid[m[1]]=i['key']
    cols=get('/collections')
    children={c['data']['name']:c['key'] for c in cols if c['data'].get('parentCollection')=='CBS6V74B'}
    assert set(COLLECTIONS.values()).issubset(children)
    desired=[];child_updates=[];redundant=[];mapping=[]
    source_byid={r['id']:r for r in papers+docs}
    for pid,imported_key in byid.items():
        source=source_byid[pid];family=source.get('family','standards')
        wanted=['CBS6V74B',children[COLLECTIONS[family]]]
        if pid in CROSS_CUTTING and family!='cutting':wanted.append(children[COLLECTIONS['cutting']])
        keys=existing.get(pid,[]);assert len(keys)<=1
        final_key=keys[0] if keys else imported_key
        current=get('/items/'+final_key);data=current['data']
        merged=list(dict.fromkeys(data.get('collections',[])+wanted))
        tags=list(data.get('tags',[]))
        for tag in ['IWM','IWM/'+pid]:
            if not any(t['tag']==tag for t in tags):tags.append({'tag':tag,'type':1})
        desired.append({'key':final_key,'version':current['version'],'collections':merged,'tags':tags})
        if keys:
            children_items=get('/items/'+imported_key+'/children')
            for child in children_items:
                patch={'key':child['key'],'version':child['version'],'parentItem':final_key}
                if child['data']['itemType']=='note':
                    content=child['data']['note']
                    content=re.sub(r'<p>为本次 IWM 报告保存.*?</p>','<p>复用原库已有书目条目，新增本报告固定版本全文与调研注释；保留原书目元数据、既有附件及集合归属。</p>',content,flags=re.S)
                    patch['note']=content
                child_updates.append(patch)
            parent=get('/items/'+imported_key)
            redundant.append({'key':imported_key,'version':parent['version'],'deleted':True})
        mapping.append({'id':pid,'title':source['title'],'key':final_key,'reused_existing':bool(keys),'collections':merged,'archived_pdf_sha256':source.get('sha256')})
    patches=desired+child_updates+redundant
    plan={'destination':'My Library / IWM','paper_count':len(papers),'document_count':len(docs),'category_keys':children,'reused_existing':len(redundant),'redundant_imported_parents_to_trash':[r['key'] for r in redundant],'child_attachments_and_notes_to_reparent':len(child_updates),'update_count':len(patches),'batches':[patches[i:i+50] for i in range(0,len(patches),50)],'items':mapping}
    (ROOT/'research/zotero_classification_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
    return plan

def execute(plan):
    receipt=ROOT/'research/zotero_finalization_receipt.json'
    assert not receipt.exists(),'Finalization receipt already exists; verify before retrying.'
    root=requests.get(BASE+'/api/',timeout=15);root.raise_for_status()
    server_id=root.headers['Zotero-Server-ID']
    key=None;remember=False;results=[]
    for i,batch in enumerate(plan['batches']):
        if key is None:
            print(f'Waiting for Zotero native local API authorization (batch {i+1}/{len(plan["batches"])}).',flush=True)
            auth=requests.post(BASE+'/api/local/authorize',json={'appName':'Codex · IWM 文献分类与去重'},headers={'Zotero-API-Version':'3','Zotero-Server-ID':server_id},timeout=(10,600))
            if auth.status_code==403:
                print('Zotero authorization denied; no further changes made.',flush=True)
                (ROOT/'research/zotero_finalization_denied.json').write_text(json.dumps({'completed_batches':len(results),'status':403}))
                return False
            auth.raise_for_status();credentials=auth.json();key=credentials['key'];remember=credentials['remember']
        headers={'Zotero-API-Version':'3','Zotero-Server-ID':server_id,'Zotero-API-Key':key,'Zotero-Write-Token':uuid.uuid4().hex[:24]}
        response=requests.post(API+'/items',json=batch,headers=headers,timeout=120)
        response.raise_for_status();result=response.json();results.append({'batch':i+1,'count':len(batch),'response':result})
        (ROOT/'research/zotero_finalization_progress.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
        assert not result.get('failed'),result.get('failed')
        print(f'Applied batch {i+1}: {len(batch)} item updates.',flush=True)
        if not remember:key=None
    receipt.write_text(json.dumps({'status':'completed','update_count':plan['update_count'],'reused_existing':plan['reused_existing'],'batches':results},ensure_ascii=False,indent=2))
    print('Classification and reuse completed.',flush=True)
    return True

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    plan=prepare()
    print(json.dumps({k:plan[k] for k in ['destination','paper_count','document_count','reused_existing','child_attachments_and_notes_to_reparent','update_count']},ensure_ascii=False,indent=2),flush=True)
    if args.execute:execute(plan)
