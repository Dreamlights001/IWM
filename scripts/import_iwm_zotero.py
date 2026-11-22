#!/usr/bin/env python3
"""Import the report bibliography and PDF files using Zotero's RDF importer.

Uses the supported Connector import route; never edits Zotero's database.
The existing IWM collection must be selected. A receipt prevents blind reimport.
"""
import argparse
import html
import json
from pathlib import Path
import sys
import uuid
import xml.etree.ElementTree as ET
import requests

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:23119'
NS={'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#','z':'http://www.zotero.org/namespaces/export#','dc':'http://purl.org/dc/elements/1.1/','dcterms':'http://purl.org/dc/terms/','bib':'http://purl.org/net/biblio#','foaf':'http://xmlns.com/foaf/0.1/','link':'http://purl.org/rss/1.0/modules/link/'}
for prefix,uri in NS.items():ET.register_namespace(prefix,uri)
def q(s):
    a,b=s.split(':',1);return '{'+NS[a]+'}'+b
def text(parent,name,value):
    if value is not None and str(value):ET.SubElement(parent,q(name)).text=str(value)
def ref(parent,name,target):return ET.SubElement(parent,q(name),{q('rdf:resource'):target})
def desc(root,uri,typ):
    x=ET.SubElement(root,q('rdf:Description'),{q('rdf:about'):uri});ref(x,'rdf:type',NS[typ.split(':')[0]]+typ.split(':')[1]);return x
def note(root,parent,uri,body):
    n=desc(root,uri,'bib:Memo');text(n,'rdf:value',body);ref(parent,'dcterms:isReferencedBy',uri)

COLLECTIONS={
 'latent':'01 潜变量与模型式控制',
 'jepa':'02 JEPA与特征预测',
 'asset':'03 可交互资产与仿真环境',
 'factory':'04 工业过程、生产与多机协同',
 'gaussian':'05 高斯表示与动态重建',
 'physics':'06 高斯与物理数字孪生',
 'video':'07 生成式视频与交互模型',
 'structured':'08 三维动力学与场景图',
 'reconstruction':'09 几何重建',
 'evaluation':'10 世界模型与物理评测',
 'cutting':'11 形变、切削与材料去除',
 'standards':'12 标准与官方技术文档'
}
CROSS_CUTTING={'P19','P20','P21','P31','P32','P44','P49'}

def build():
    records=json.loads((ROOT/'papers/manifest.json').read_text())
    notes=json.loads((ROOT/'research/paper_notes.json').read_text())
    docs=json.loads((ROOT/'research/supplementary_sources.json').read_text())
    before=json.loads((ROOT/'research/zotero_existing_matches.json').read_text())
    tree=ET.Element(q('rdf:RDF'))
    membership={k:[] for k in COLLECTIONS}
    plan=[]
    for r in records:
        pid=r['id'];uri='urn:iwm:survey:2026-11-09:'+pid
        item=desc(tree,uri,'bib:Document')
        typ='preprint' if r['arxiv_id'] else ('journalArticle' if r.get('doi') else 'report')
        text(item,'z:itemType',typ);text(item,'dc:title',r['title'])
        text(item,'z:abstractNote',r.get('abstract',''));text(item,'z:url',r['source_url'])
        text(item,'dc:date',r.get('submitted_date') or r['publication_date'])
        text(item,'z:accessDate','2026-11-09');text(item,'z:language','en')
        text(item,'z:libraryCatalog','IWM survey primary-source archive')
        text(item,'z:citationKey',pid+'_'+r['slug'])
        if r['arxiv_id']:
            text(item,'z:repository','arXiv');text(item,'z:archiveID',r['arxiv_id']+r['version'])
            text(item,'z:DOI','10.48550/arXiv.'+r['arxiv_id'])
        else:
            for k,f in [('doi','DOI'),('publication_title','publicationTitle'),('volume','volume'),('page_range','pages'),('report_number','reportNumber'),('institution','institution')]:
                if k in r and not (typ=='report' and k=='publication_title'):text(item,'z:'+f,r[k])
            if typ=='report':text(item,'z:seriesTitle',r.get('publication_title',''));text(item,'z:reportType','Technical report')
        seq=ET.SubElement(ET.SubElement(item,q('bib:authors')),q('rdf:Seq'))
        for author in r.get('authors',[]):
            li=ET.SubElement(seq,q('rdf:li'));person=ET.SubElement(li,q('foaf:Person'))
            parts=author.rsplit(' ',1)
            text(person,'foaf:surname',parts[-1])
            if len(parts)>1:text(person,'foaf:givenName',parts[0])
        for tag in ['IWM','IWM/'+pid,'路线/'+COLLECTIONS[r['family']][3:]]:text(item,'dc:subject',tag)
        if r['family']=='cutting' or pid in CROSS_CUTTING:text(item,'dc:subject','现象/形变-切削-材料去除')
        original=before.get(pid,[])
        extra=f"IWM ID: {pid}\nArchived version: {r['version']}\nSurvey date: 2026-11-09\nPDF SHA-256: {r['sha256']}"
        if original:extra+='\nExisting library records preserved: '+', '.join(original)
        text(item,'z:extra',extra)
        n=notes[pid]
        body='<h2>'+html.escape(pid+' · '+r['title'])+'</h2>'+''.join('<p><strong>'+label+'</strong> '+html.escape(value)+'</p>' for label,value in zip(['贡献：','论文证据范围：','工厂迁移边界（本报告分析）：','阅读定位：'],n))
        body+='<p>调研日：2026-11-09；报告未复现论文实验。归档版本：'+html.escape(r['version'])+'。来源：'+html.escape(r['source_url'])+'</p>'
        body+='<p>固定版本 PDF：'+html.escape(r['pdf_url'])+'；SHA-256：'+r['sha256']+'</p>'
        if original:body+='<p>为本次 IWM 报告保存带固定版本全文的独立归档；原库已有记录 '+', '.join(original)+' 保留，未合并或修改。</p>'
        note(tree,item,uri+':note',body)
        attachment_uri=uri+':pdf';ref(item,'link:link',attachment_uri)
        a=desc(tree,attachment_uri,'z:Attachment');text(a,'z:itemType','attachment')
        text(a,'dc:title',f"{pid} · Full text ({r['version']})")
        text(a,'link:type','application/pdf');ref(a,'z:path',(ROOT/r['local_pdf']).as_uri())
        membership[r['family']].append(uri)
        if pid in CROSS_CUTTING:membership['cutting'].append(uri)
        plan.append({'id':pid,'title':r['title'],'primary_category':r['family'],'existing_records_preserved':original,'source_pdf':r['local_pdf'],'sha256':r['sha256']})
    for d in docs:
        uri='urn:iwm:survey:2026-11-09:'+d['id'];item=desc(tree,uri,'bib:Document')
        text(item,'z:itemType','webpage');text(item,'dc:title',d['title'])
        text(item,'z:url',d['url']);text(item,'z:accessDate',d['accessed'])
        text(item,'z:websiteType','Official technical documentation / standard')
        text(item,'z:abstractNote',d['use']);text(item,'z:extra','IWM source ID: '+d['id'])
        for tag in ['IWM','IWM/'+d['id'],'技术文档与标准']:text(item,'dc:subject',tag)
        note(tree,item,uri+':note','<p><strong>报告用途：</strong>'+html.escape(d['use'])+'</p><p>官方网页／标准索引；未伪装为研究论文。检索日：2026-11-09。</p>')
        membership['standards'].append(uri)
        plan.append({'id':d['id'],'title':d['title'],'primary_category':'standards','source_url':d['url']})
    for family,uris in membership.items():
        c=desc(tree,'urn:iwm:category:'+family,'z:Collection');text(c,'dc:title',COLLECTIONS[family])
        for uri in uris:ref(c,'dcterms:hasPart',uri)
    ET.indent(tree)
    payload=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
    p=ROOT/'papers/IWM_zotero_import.rdf';p.write_bytes(payload)
    details={'destination':{'library':'My Library','libraryID':1,'collection':'IWM','collectionID':1,'collectionKey':'CBS6V74B'},'paper_count':len(records),'document_count':len(docs),'category_counts':{COLLECTIONS[k]:len(v) for k,v in membership.items()},'items':plan,'rdf_file':str(p)}
    (ROOT/'research/zotero_import_plan.json').write_text(json.dumps(details,ensure_ascii=False,indent=2))
    return payload,details

def main():
    args=argparse.ArgumentParser();args.add_argument('--execute',action='store_true');a=args.parse_args()
    payload,plan=build()
    print(json.dumps({k:v for k,v in plan.items() if k!='items'},ensure_ascii=False,indent=2),flush=True)
    if not a.execute:return
    receipt=ROOT/'research/zotero_import_receipt.json'
    assert not receipt.exists(),'Receipt exists: verify the previous import; do not blindly reimport.'
    headers={'X-Zotero-Connector-API-Version':'3','Content-Type':'application/json'}
    selected=requests.post(BASE+'/connector/getSelectedCollection',json={},headers=headers,timeout=20);selected.raise_for_status();target=selected.json()
    assert (target.get('libraryID'),target.get('id'),target.get('name'))==(1,1,'IWM'),target
    session='iwm-survey-'+uuid.uuid4().hex
    (ROOT/'research/zotero_import_attempt.json').write_text(json.dumps({'session':session,'target':{k:target[k] for k in ['libraryID','libraryName','id','name']},'payload_bytes':len(payload)},indent=2))
    response=requests.post(BASE+'/connector/import',params={'session':session},data=payload,headers={'X-Zotero-Connector-API-Version':'3','Content-Type':'application/rdf+xml'},timeout=300)
    response.raise_for_status()
    result={'status':response.status_code,'session':session,'expected_papers':plan['paper_count'],'expected_documents':plan['document_count'],'response':response.json()}
    receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('IMPORT COMPLETE',response.status_code,'response_items',len(result['response']),flush=True)

if __name__=='__main__':main()
