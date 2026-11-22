"""引用记号解析与校验。md 与 html 两种输出共用同一套查表，未知记号直接报错。"""
import html as H
import json
import os
import re
from pathlib import Path

from . import common

ROOT = Path(__file__).resolve().parents[2]
TOKEN = re.compile(r'\[\[(?:([A-Z]):)?([^\]]+)\]\]')


class Sources:
    def __init__(self, works):
        res = ROOT / 'research'
        self.arxiv = json.loads((res / 'works_arxiv_meta.json').read_text())
        self.repos = json.loads((res / 'works_repos_verified.json').read_text())
        self.urls = json.loads((res / 'works_urls_verified.json').read_text())
        self.papers = {p['id']: p for p in json.loads((ROOT / 'papers' / 'manifest.json').read_text())}
        self.supp = {s['id']: s for s in json.loads((res / 'supplementary_sources.json').read_text())}
        self.works = {w['id']: w for w in works}
        self.used = dict(A=set(), P=set(), S=set(), D=set(), R=set())

    # ---- 单个来源 -> (显示文字, 目标, 是否本地路径)
    def target(self, kind, val):
        if kind == 'A':
            m = self.arxiv.get(val)
            assert m and m.get('verified'), f'arXiv {val} 未核对'
            self.used['A'].add(val)
            return f'arXiv {val}', f'https://arxiv.org/abs/{val}', False
        if kind == 'P':
            p = self.papers.get(val)
            assert p and (ROOT / p['local_pdf']).exists(), f'{val} 缺本地 PDF'
            self.used['P'].add(val)
            return val, p['local_pdf'], True
        if kind == 'S':
            s = self.supp.get(val)
            assert s, f'补充来源 {val} 不存在'
            self.used['S'].add(val)
            return val, s['url'], False
        if kind == 'D':
            d = common.DOCS.get(val)
            assert d, f'文档 {val} 不存在'
            st = self.urls.get(val, {}).get('status')
            assert st == 200 or d.get('check'), f'文档 {val} 链接状态 {st}，且无人工核对记录'
            self.used['D'].add(val)
            return d['label'], d['url'], False
        if kind == 'L':
            assert val in common.L_DIRS, f'链路 {val} 不存在'
            assert (ROOT / '链路' / common.L_DIRS[val] / 'README.md').exists(), val
            return common.L_LABEL.get(val, val), f'链路/{common.L_DIRS[val]}/README.md', True
        if kind == 'W':
            w = self.works.get(val)
            assert w, f'工作 {val} 不存在'
            return f'{val}（{w["name"]}）', f'works/{w["folder"]}/README.md', True
        if kind == 'R':
            r = self.repos.get(val)
            assert r and r.get('ok') and not r.get('archived') and r['full_name'].lower() == val.lower(), f'仓库 {val} 未通过核对'
            self.used['R'].add(val)
            return val, f'https://github.com/{val}', False
        raise AssertionError(f'未知记号类型 {kind}:{val}')

    def key(self, key):
        """refs 列表里的键：'A:xxxx'、'P65'、'S2'、'D:key'。"""
        if re.fullmatch(r'P\d{2}', key):
            return 'P', key
        if re.fullmatch(r'S\d+', key):
            return 'S', key
        kind, val = key.split(':', 1)
        return kind, val

    # ---- 正文记号替换
    def md(self, text, here):
        def rep(m):
            kind, val = m.group(1), m.group(2)
            if kind is None:
                kind, val = self.key(val)
            label, tgt, local = self.target(kind, val)
            if local:
                tgt = os.path.relpath(ROOT / tgt, ROOT / here)
            return f'[{label}]({tgt})'
        return TOKEN.sub(rep, text)

    def html(self, text, here, wlink='drawer'):
        out, pos = [], 0
        for m in TOKEN.finditer(text):
            out.append(H.escape(text[pos:m.start()]))
            kind, val = m.group(1), m.group(2)
            if kind is None:
                kind, val = self.key(val)
            label, tgt, local = self.target(kind, val)
            if kind == 'W' and wlink == 'drawer':
                out.append(f'<a class="wref" href="#{val}" data-w="{val}">{H.escape(label)}</a>')
            else:
                if local:
                    tgt = os.path.relpath(ROOT / tgt, ROOT / here)
                out.append(f'<a class="cite" href="{H.escape(tgt)}">{H.escape(label)}</a>')
            pos = m.end()
        out.append(H.escape(text[pos:]))
        return ''.join(out)

    # ---- 文献条目
    def entry(self, key, note, here, fmt='md'):
        kind, val = self.key(key)
        label, tgt, local = self.target(kind, val)
        if local:
            tgt = os.path.relpath(ROOT / tgt, ROOT / here)
        if kind == 'A':
            m = self.arxiv[val]
            title, extra = m['title'], (m.get('date') or '')[:4]
        elif kind == 'P':
            p = self.papers[val]
            title, extra = p['title'], (p.get('publication_date') or '')[:4]
        elif kind == 'S':
            s = self.supp[val]
            title, extra = s['label'], s.get('kind', '')
        else:
            d = common.DOCS[val]
            title, extra = d['title'], d['who']
        link_text = f'{label} 本地 PDF' if kind == 'P' else ('链接' if kind in 'SD' else label)
        if fmt == 'md':
            return f'- **{title}**（{extra}），[{link_text}]({tgt})：{self.md(note, here)}'
        return (f'<li><a class="t" href="{H.escape(tgt)}">{H.escape(title)}</a> '
                f'<span class="yr">{H.escape(extra)}</span><span class="nt">{self.html(note, here)}</span></li>')

    def repo(self, name, note, here, fmt='md'):
        self.target('R', name)
        if fmt == 'md':
            return f'- [{name}](https://github.com/{name})：{self.md(note, here)}'
        return f'<li><a class="t" href="https://github.com/{H.escape(name)}">{H.escape(name)}</a><span class="nt">{self.html(note, here)}</span></li>'
