#!/usr/bin/env python3
"""Archive the two non-arXiv primary-source machining papers."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import requests

ROOT=Path(__file__).resolve().parents[1]
PAPERS=[
 dict(id='P48',slug='Tri_Dexel_Robotic_Machining',family='cutting',arxiv_id='',version='author-manuscript',
      title='Coupled Dynamic Simulator With Tri-Dexel Milling Module For Robotic Machining Operations',
      authors=['Valentin Dambly','Édouard Rivière-Lorphèvre','Olivier Verlinden'],
      publication_date='2023',submitted_date='2023',doi='10.1016/j.procir.2023.03.031',publication_title='Procedia CIRP',volume='117',page_range='175-180',
      source_url='https://doi.org/10.1016/j.procir.2023.03.031',
      pdf_url='https://orbi.umons.ac.be/bitstream/20.500.12907/47947/1/PROCIR_CMMO_2023_Dambly.pdf',
      abstract='A coupled robotic machining simulator links machine dynamics with dexel-based material removal, cutting-force computation and updated workpiece geometry. Experimental milling tests verify forces, deviations and geometry.'),
 dict(id='P50',slug='Thermomechanical_Machining_FEM',family='cutting',arxiv_id='',version='Report-14-01',
      title='Finite Element Simulation of macroscopic Machining Processes - Implementation of time dependent Domain and Boundary Conditions',
      authors=['Carsten Niebuhr','Daniel Niederwestberg','Alfred Schmidt'],
      publication_date='2014-01',submitted_date='2014-01',publication_title='Berichte aus der Technomathematik',report_number='14-01',institution='Universität Bremen',
      source_url='https://www.math.uni-bremen.de/zetem/cms/detail.php?person=CarstenNiebuhr&template=publikationen_person',
      pdf_url='https://www.math.uni-bremen.de/zetem/cms/media.php/262/Zetem%20Report%2014-01.pdf',
      abstract='A dexel-based material-removal simulation is coupled to thermomechanical finite elements and process models for cutting forces and heat flux, to predict macroscopic shape errors on a time-dependent domain. Microscopic chip formation is represented through process models rather than explicitly resolved.')
]
for r in PAPERS:
    r['accessed']='2026-11-09'
    r['local_pdf']=f"papers/{r['id']}_{r['slug']}_{r['version']}.pdf"
    p=ROOT/r['local_pdf']
    if not p.exists():
        response=requests.get(r['pdf_url'],timeout=90);response.raise_for_status()
        assert response.content.startswith(b'%PDF-'),r['id']
        p.write_bytes(response.content)
    data=p.read_bytes();r['bytes']=len(data);r['sha256']=hashlib.sha256(data).hexdigest()
    textpath=ROOT/'research'/f"{r['id']}_{r['slug']}.txt"
    subprocess.run(['pdftotext','-layout',str(p),str(textpath)],check=True)
    r['text_file']=str(textpath.relative_to(ROOT))
    info=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True)
    r['pages']=int(re.search(r'Pages:\s+(\d+)',info.stdout).group(1))
    r['submission_history']='Institutional author manuscript; bibliographic source and PDF source recorded separately.'
    r['status']='downloaded_and_text_extracted'
    (ROOT/'research'/f"{r['id']}.json").write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(r['id'],r['title'],r['pages'],flush=True)
