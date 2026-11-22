#!/usr/bin/env python3
"""核对 works/ 引用的来源，并把结果缓存到 research/：

- arXiv：缺元数据的 ID 抓取 arxiv.org/abs 页面（标题、日期、作者、摘要）→ works_arxiv_meta.json
- GitHub：`gh api repos/<name>` → works_repos_verified.json（规范名、是否归档、描述、最近推送）
- 其他链接：HTTP 状态；DOI 用 Crossref 取标题 → works_urls_verified.json

用法：python3 scripts/verify_works_sources.py [--refresh]
"""
import json, re, subprocess, sys, time, html
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from works_src import load_works, common  # noqa: E402

RES = ROOT / 'research'
UA = {'User-Agent': 'IndustrialWorldModelSurvey/1.0 (academic literature review)'}
TOKEN = re.compile(r'\[\[([A-Z]):([^\]]+)\]\]')


def collect():
    arx, repos = set(), set()
    blobs = []
    for w in load_works():
        blobs.append(json.dumps(w, ensure_ascii=False))
        for _, items in w['refs']:
            for key, _ in items:
                if key.startswith('A:'):
                    arx.add(key[2:])
        repos.update(name for name, _ in w['repos'])
    blobs.append(json.dumps(common.LOOPS, ensure_ascii=False))
    for b in blobs:
        for kind, val in TOKEN.findall(b):
            if kind == 'A':
                arx.add(val)
            elif kind == 'R':
                repos.add(val)
    return sorted(arx), sorted(repos)


def fetch_arxiv(aid):
    for attempt in range(5):
        r = requests.get(f'https://arxiv.org/abs/{aid}', headers=UA, timeout=60)
        if r.status_code == 200:
            t = r.text
            meta = lambda n: [html.unescape(x) for x in re.findall(rf'<meta name="{n}" content="([^"]*)"', t)]
            ab = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', t, re.S)
            abstract = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', ab.group(1))).replace('Abstract:', '').strip() if ab else ''
            title = meta('citation_title')
            if title:
                return dict(title=title[0], date=(meta('citation_date') or [''])[0], authors=meta('citation_author'),
                            abstract=html.unescape(abstract), verified=True)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f'arXiv {aid}: 无法取得元数据')


def gh_repo(name):
    p = subprocess.run(['gh', 'api', f'repos/{name}'], capture_output=True, text=True)
    if p.returncode != 0:
        return dict(ok=False, error=p.stderr.strip()[:200])
    d = json.loads(p.stdout)
    return dict(ok=True, full_name=d['full_name'], archived=d['archived'], description=d.get('description') or '',
                pushed_at=d.get('pushed_at'), stars=d.get('stargazers_count'), url=d['html_url'])


def check_url(url):
    try:
        r = requests.get(url, headers=UA, timeout=60, allow_redirects=True, stream=True)
        return dict(status=r.status_code, final=r.url)
    except requests.RequestException as e:
        return dict(status=None, error=str(e)[:200])


def crossref(doi):
    r = requests.get(f'https://api.crossref.org/works/{doi}', headers=UA, timeout=60)
    if r.status_code != 200:
        return None
    return (r.json()['message'].get('title') or [''])[0]


def main():
    refresh = '--refresh' in sys.argv
    arx, repos = collect()
    mp = RES / 'works_arxiv_meta.json'
    meta = json.loads(mp.read_text()) if mp.exists() else {}
    missing = [a for a in arx if a not in meta]
    for a in missing:
        meta[a] = fetch_arxiv(a)
        print('arXiv 新增', a, meta[a]['title'][:70])
        time.sleep(1.5)
    mp.write_text(json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True))

    rp = RES / 'works_repos_verified.json'
    rv = json.loads(rp.read_text()) if rp.exists() and not refresh else {}
    for name in repos:
        if name not in rv:
            rv[name] = gh_repo(name)
            rv[name]['checked'] = time.strftime('%Y-%m-%d')
    rp.write_text(json.dumps(rv, ensure_ascii=False, indent=1, sort_keys=True))

    up = RES / 'works_urls_verified.json'
    uv = {}
    for key, d in common.DOCS.items():
        uv[key] = dict(check_url(d['url']), checked=time.strftime('%Y-%m-%d'))
        if d.get('doi'):
            uv[key]['crossref_title'] = crossref(d['doi'])
    up.write_text(json.dumps(uv, ensure_ascii=False, indent=1, sort_keys=True))

    bad = [n for n, v in rv.items() if not v.get('ok') or v.get('archived') or v['full_name'].lower() != n.lower()]
    print(f'arXiv {len(arx)} 个（新增 {len(missing)}）；GitHub {len(repos)} 个；问题仓库：')
    for n in bad:
        print('  ', n, rv[n])
    for k, v in uv.items():
        print('  链接', k, v.get('status'), v.get('crossref_title', ''))


if __name__ == '__main__':
    main()
