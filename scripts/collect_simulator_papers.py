#!/usr/bin/env python3
"""Archive the four papers cited in the simulator implementation section."""
import concurrent.futures as cf
import hashlib
import json
import re
import subprocess

from collect_papers import EVIDENCE, ROOT, collect, get

ACCESSED = '2026-11-12'


def archive_published(record):
    record.update(accessed=ACCESSED, arxiv_id='', family='sim2wm',
                  version='institutional-copy', submitted_date='')
    stem = f"{record['id']}_{record['slug']}"
    pdf = ROOT / 'papers' / f'{stem}.pdf'
    if not pdf.exists():
        data = get(record['pdf_url'], binary=True).content
        if not data.startswith(b'%PDF-'):
            raise ValueError(f'{stem}: expected PDF')
        pdf.write_bytes(data)
    data = pdf.read_bytes()
    extracted = EVIDENCE / f'{stem}.txt'
    subprocess.run(['pdftotext', '-layout', str(pdf), str(extracted)], check=True)
    info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
    record.update(local_pdf=str(pdf.relative_to(ROOT)), bytes=len(data),
                  sha256=hashlib.sha256(data).hexdigest(),
                  text_file=str(extracted.relative_to(ROOT)),
                  pages=int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1]),
                  status='downloaded_and_text_extracted')
    (EVIDENCE / f"{record['id']}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
    return record


if __name__ == '__main__':
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [
            pool.submit(archive_published, dict(
                id='P96', slug='MuJoCo_Physics_Engine',
                title='MuJoCo: A physics engine for model-based control',
                authors=['Emanuel Todorov', 'Tom Erez', 'Yuval Tassa'],
                publication_date='2012', doi='10.1109/IROS.2012.6386109',
                booktitle='2012 IEEE/RSJ International Conference on Intelligent Robots and Systems',
                source_url='https://doi.org/10.1109/IROS.2012.6386109',
                pdf_url='https://roboti.us/lab/papers/TodorovIROS12.pdf')),
            pool.submit(collect, ('P97', 'IndustReal', '2305.17110', 'sim2wm'), accessed=ACCESSED),
            pool.submit(collect, ('P98', 'Co_Simulation_Survey', '1702.00686', 'sim2wm'), accessed=ACCESSED),
            pool.submit(archive_published, dict(
                id='P99', slug='NIST_CMSD',
                title='A Core Manufacturing Simulation Data Information Model for Manufacturing Applications',
                authors=['Swee K. Leong', 'Yung-Tsun T. Lee', 'Frank H. Riddick'],
                publication_date='2006',
                booktitle='Proceedings of the Systems Interoperability Standards Organization 2006 Fall Simulation Interoperability Workshop',
                source_url='https://www.nist.gov/publications/core-manufacturing-simulation-data-information-model-manufacturing-applications',
                pdf_url='https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=822625')),
        ]
        for job in jobs:
            result = job.result()
            if not result['status'].startswith('downloaded'):
                raise RuntimeError(result)
            print(result['id'], result['title'], result['pages'], flush=True)
