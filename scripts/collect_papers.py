#!/usr/bin/env python3
"""Download primary-source papers and record verifiable local provenance."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / 'papers'
EVIDENCE = ROOT / 'research'
SEEDS = [
 ('P01','World_Models','1803.10122','latent'),
 ('P02','DreamerV3','2301.04104','latent'),
 ('P03','TD_MPC2','2310.16828','latent'),
 ('P04','V_JEPA','2404.08471','jepa'),
 ('P05','V_JEPA_2','2506.09985','jepa'),
 ('P06','V_JEPA_2_1','2603.14482','jepa'),
 ('P07','DINO_WM','2411.04983','jepa'),
 ('P08','SAPIEN','2003.08515','asset'),
 ('P09','ManiSkill3','2410.00425','asset'),
 ('P10','Isaac_Lab','2511.04831','asset'),
 ('P11','RoboCasa','2406.02523','asset'),
 ('P12','RoboCasa365','2603.04356','asset'),
 ('P13','RoboFactory','2503.16408','factory'),
 ('P14','URDFormer','2405.11656','asset'),
 ('P15','Articulate_Anything','2410.13882','asset'),
 ('P16','3D_Gaussian_Splatting','2308.04079','gaussian'),
 ('P17','4D_Gaussian_Splatting','2310.08528','gaussian'),
 ('P18','Dynamic_3D_Gaussians','2308.09713','gaussian'),
 ('P19','PhysGaussian','2311.12198','physics'),
 ('P20','Spring_Gaus','2403.09434','physics'),
 ('P21','PhysTwin','2503.17973','physics'),
 ('P22','Robo_GS','2408.14873','physics'),
 ('P23','DreMa','2412.14957','physics'),
 ('P24','ManiGaussian','2403.08321','gaussian'),
 ('P25','ManiGaussian_PlusPlus','2506.19842','gaussian'),
 ('P26','ArticulatedGS','2503.08135','gaussian'),
 ('P27','ArtiTwinSplat','2606.24628','gaussian'),
 ('P28','Cosmos','2501.03575','video'),
 ('P29','Cosmos_3','2606.02800','video'),
 ('P30','Genie','2402.15391','video'),
 ('P31','Graph_Network_Simulator','2002.09405','structured'),
 ('P32','MeshGraphNets','2010.03409','structured'),
 ('P33','ConceptGraphs','2309.16650','structured'),
 ('P34','Hydra','2201.13360','structured'),
 ('P35','DUSt3R','2312.14132','reconstruction'),
 ('P36','VGGT','2503.11651','reconstruction'),
 ('P37','Industrial_Process_JEPA','2503.01411','factory'),
 ('P38','AWMP_Dynamic_Scheduling','2610.29308','factory'),
 ('P39','FMAPPO_Machine_Tending','2609.14567','factory'),
 ('P40','GRUtopia','2407.10943','asset'),
 ('P41','WorldModelBench','2502.20694','evaluation'),
 ('P42','PhysBench','2501.16411','evaluation'),
 ('P43','UniSim','2310.06114','video'),
 ('P44','PointWorld','2601.03782','structured'),
 ('P45','iVideoGPT','2405.15223','video'),
 ('P46','DiSECt','2203.10263','cutting'),
 ('P47','GaussianFluent','2601.09265','cutting'),
 ('P49','GaussianBench','2610.10554','evaluation'),
]

def get(url, binary=False):
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=(15,100), headers={'User-Agent':'IndustrialWorldModelSurvey/1.0 (academic literature review)'})
            r.raise_for_status()
            return r if binary else r.text
        except Exception:
            if attempt == 2: raise
            time.sleep(2 + attempt*3)

def collect(seed, accessed='2026-11-09'):
    pid, slug, aid, family = seed
    record = dict(id=pid,slug=slug,arxiv_id=aid,family=family,
                  source_url=f'https://arxiv.org/abs/{aid}',accessed=accessed)
    try:
        html_path = EVIDENCE / f'{pid}_{slug}.source.html'
        raw = html_path.read_text() if html_path.exists() else get(record['source_url'])
        html_path.write_text(raw)
        soup = BeautifulSoup(raw,'html.parser')
        def meta(name):
            return [t.get('content','') for t in soup.select(f'meta[name="{name}"]')]
        record['title'] = (meta('citation_title') or [soup.title.get_text()])[0]
        record['authors'] = meta('citation_author')
        record['publication_date'] = (meta('citation_date') or [''])[0]
        record['submitted_date'] = (meta('citation_online_date') or [''])[0]
        abstract = soup.select_one('blockquote.abstract')
        record['abstract'] = abstract.get_text(' ',strip=True).removeprefix('Abstract:') if abstract else ''
        history = soup.select_one('.submission-history')
        record['submission_history'] = history.get_text(' ',strip=True) if history else ''
        versions = re.findall(r'\[v(\d+)\]',record['submission_history'])
        version = f'v{max(map(int,versions))}' if versions else ''
        record['version'] = version
        record['pdf_url'] = f'https://arxiv.org/pdf/{aid}{version}'
        record['local_pdf'] = f'papers/{pid}_{slug}_{aid}{version}.pdf'
        out = ROOT / record['local_pdf']
        if not out.exists() or not out.read_bytes().startswith(b'%PDF-'):
            r = get(record['pdf_url'],True)
            if not r.content.startswith(b'%PDF-'): raise ValueError('Response is not a PDF')
            out.write_bytes(r.content)
        data = out.read_bytes()
        record['sha256'] = hashlib.sha256(data).hexdigest()
        record['bytes'] = len(data)
        text_path = EVIDENCE / f'{pid}_{slug}.txt'
        p = subprocess.run(['pdftotext','-layout',str(out),str(text_path)],capture_output=True,text=True)
        if p.returncode: raise ValueError('pdftotext failed: '+p.stderr[:150])
        info = subprocess.run(['pdfinfo',str(out)],capture_output=True,text=True)
        pages = re.search(r'Pages:\s+(\d+)',info.stdout)
        record['pages'] = int(pages.group(1)) if pages else None
        record['text_file'] = str(text_path.relative_to(ROOT))
        record['status'] = 'downloaded_and_text_extracted'
    except Exception as e:
        record['status'] = 'failed'
        record['error'] = str(e)
    (EVIDENCE/f'{pid}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
    print(f"{pid} {slug}: {record['status']} {record.get('title','')} {record.get('error','')}",flush=True)
    return record

def main():
    PAPERS.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(collect,SEEDS))
    (PAPERS/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    print(f"Completed {sum(r['status'].startswith('downloaded') for r in records)}/{len(records)}",flush=True)

if __name__ == '__main__': main()
