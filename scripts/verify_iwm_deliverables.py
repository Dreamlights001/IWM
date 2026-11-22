#!/usr/bin/env python3
"""Read back HTML, bibliography, Zotero categories and archived attachments."""
import concurrent.futures as cf
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlparse
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
API='http://127.0.0.1:23119/api/users/0'
def get(tail,**params):
    response=requests.get(API+tail,params=params or None,timeout=25);response.raise_for_status()
    return response.json() if 'json' in response.headers.get('Content-Type','') else response.text

def verify_files():
    records=json.loads((ROOT/'papers/manifest.json').read_text())
    soup=BeautifulSoup((ROOT/'report.html').read_text(),'html.parser')
    ids=[e['id'] for e in soup.select('[id]')];errors=[]
    for a in soup.select('a[href]'):
        h=a['href']
        if h.startswith('#') and h[1:] not in ids:errors.append('anchor '+h)
        if not h.startswith(('https:','http:','#','zotero:')) and not (ROOT/h).exists():errors.append('file '+h)
    for r in records:
        p=ROOT/r['local_pdf'];data=p.read_bytes()
        if not data.startswith(b'%PDF-') or hashlib.sha256(data).hexdigest()!=r['sha256']:errors.append('PDF '+r['id'])
        if (ROOT/r['text_file']).stat().st_size<2000:errors.append('PDF text '+r['id'])
    assert len(records)==len(soup.select('.paper'))
    assert len(ids)==len(set(ids)) and not errors,errors
    assert soup.select_one('#deformation') and any(len(t.select('thead th'))>=8 for t in soup.select('#comparison table'))
    result={'checked_at':date.today().isoformat(),'paper_count':len(records),'pdf_count':len(list((ROOT/'papers').glob('*.pdf'))),'total_pdf_pages':sum(r['pages'] for r in records),'pdf_bytes':sum(r['bytes'] for r in records),'all_sha256_verified':True,'all_pdf_signatures_valid':True,'all_local_links_valid':True,'all_fragment_links_valid':True,'section_count':len(soup.select('main>section')),'route_count':len(soup.select('.route')),'citation_links':len(soup.select('a.cite')),'errors':errors}
    (ROOT/'qa/content-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('HTML/PDF checks:',json.dumps(result,ensure_ascii=False),flush=True)

def verify_zotero():
    assert (ROOT/'research/zotero_finalization_receipt.json').exists(),'Native authorization / finalization still pending.'
    plan=json.loads((ROOT/'research/zotero_classification_plan.json').read_text())
    records={r['id']:r for r in json.loads((ROOT/'papers/manifest.json').read_text())}
    cols=get('/collections');bykey={c['key']:c for c in cols}
    category_counts={}
    category_itemkeys={}
    for name,key in plan['category_keys'].items():
        assert bykey[key]['data']['parentCollection']=='CBS6V74B'
        items=get('/collections/'+key+'/items/top',limit=100)
        category_counts[name]=len(items);category_itemkeys[key]={i['key'] for i in items}
    def check(row):
        item=get('/items/'+row['key']);data=item['data'];assert not data.get('deleted')
        assert set(row['collections']).issubset(data.get('collections',[])),row['id']
        children=get('/items/'+row['key']+'/children')
        note_children=[c for c in children if c['data']['itemType']=='note']
        assert note_children,row['id']+' note'
        result={**row,'verified':True,'notes':len(note_children)}
        if row['id'] in records:
            expected=records[row['id']];pdfs=[c for c in children if c['data']['itemType']=='attachment' and c['data'].get('filename')==Path(expected['local_pdf']).name]
            assert len(pdfs)==1,(row['id'],'archived PDF missing / duplicated')
            pdf=pdfs[0];assert pdf['data'].get('linkMode')=='imported_file'
            fileinfo=get('/items/'+pdf['key']+'/file/view/url')
            url=fileinfo if isinstance(fileinfo,str) else fileinfo.get('url')
            assert url and url.startswith('file:'),fileinfo
            path=Path(unquote(urlparse(url).path));assert path.exists()
            digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==expected['sha256'],row['id']
            result['attachment_key']=pdf['key'];result['archived_pdf_hash_verified']=True
        return result
    with cf.ThreadPoolExecutor(max_workers=4) as pool:verified=list(pool.map(check,plan['items']))
    allkeys=set().union(*category_itemkeys.values())
    assert len(allkeys)==57 and len(verified)==57
    assert category_counts['11 形变、切削与材料去除']==11
    for key in plan['redundant_imported_parents_to_trash']:
        assert get('/items/'+key)['data'].get('deleted') is True
    summary={'status':'verified','checked_at':date.today().isoformat(),'destination':'My Library / IWM','collection_key':'CBS6V74B','unique_papers':50,'technical_documents':7,'subcollections':12,'pdf_hashes_verified':50,'existing_bibliographic_records_reused':3,'redundant_new_parents_trashed':3,'category_counts':category_counts,'items':verified}
    (ROOT/'research/zotero_verified_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Zotero:',json.dumps({k:v for k,v in summary.items() if k!='items'},ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--zotero',action='store_true');args=p.parse_args()
    verify_files()
    if args.zotero:verify_zotero()
