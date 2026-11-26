#!/usr/bin/env python3
"""生成 works/：研究步骤总看板 research_board.html、索引 README.md 和 17 个工作文件夹。

数据在 scripts/works_src/（每项工作一个文件，公共数据在 common.py）。
先运行 scripts/verify_works_sources.py 核对来源，再运行本脚本。所有引用都要通过核对，否则报错。
"""
import json
import re
import sys
from html import escape as E
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from works_src import load_works, common  # noqa: E402
from works_src.refs import Sources  # noqa: E402
from works_src.diagram import GEOM, main_svg  # noqa: E402
from works_src.mdgen import work_md, index_md, ref_count  # noqa: E402
from works_src import htmlgen as hg  # noqa: E402

OUT = ROOT / 'works'
DATE = '2026-11-27'


def check(works):
    ids = [w['id'] for w in works]
    assert set(GEOM) == set(ids), '总图布局与工作列表不一致'
    stages = {s['id'] for s in common.STAGES}
    for w in works:
        assert w['stage'] in stages, w['id']
        for k in ('folder', 'name', 'card', 'oneline', 'why', 'inputs', 'outputs', 'tasks', 'papers', 'links', 'refs', 'repos'):
            assert k in w, (w['id'], k)
        assert w['papers'] and w['refs'], w['id']
        assert all(c in common.L_DIRS for c in w['links']), w['id']
        keys = [k for _, items in w['refs'] for k, _ in items]
        assert len(keys) == len(set(keys)), f'{w["id"]} 文献重复'
    assert len({w['folder'] for w in works}) == len(works)
    for s, d, _ in common.EDGES:
        assert s in ids and d in ids, (s, d)
    for lp in common.LOOPS:
        assert all(m in ids for m in lp['members']), lp['id']
    text = json.dumps([works, common.LOOPS, common.STAGES, hg.DEFORM, hg.LICENSE], ensure_ascii=False)
    bad = [m.start() for m in re.finditer(r'(?<!不)推荐', text)]
    assert not bad, '正文出现“推荐”：' + text[bad[0] - 30: bad[0] + 30]
    assert '——' not in text, '正文出现破折号连用'


def page(works, src, totals):
    counts = {w['id']: f'论文方向 {len(w["papers"])} · 文献 {ref_count(w)} · 项目 {len(w["repos"])}' for w in works}
    data = dict(works={w['id']: dict(name=w['name'], html=hg.drawer_work(w, src)) for w in works},
                loops={lp['id']: dict(members=lp['members'], html=hg.drawer_loop(lp, src)) for lp in common.LOOPS},
                geom=GEOM, edges=[[s, d] for s, d, _ in common.EDGES])
    chips = ''.join(hg.lchip(lp) for lp in common.LOOPS)
    nav = [('overview', '总图'), ('loops', '六个闭环'), ('stages', '阶段与验收'), ('papers', '论文方向'),
           ('links', '与链路的对应'), ('cross', '跨阶段条件'), ('index', '文件夹索引')]
    secs = [
        ('overview', '总图', '从上到下是研究顺序，左侧是阶段。每张卡片是一项工作，对应 works/ 下的一个文件夹，底部是论文方向、文献和开源项目的数量。点击卡片查看上下游和精选文献，点击红色编号查看闭环。',
         '<div class="legend"><span><i></i>阶段之间的交付（标注交付物）</span><span><i class="f"></i>阶段内的顺序</span>'
         '<span><i class="r"></i>闭环回流，编号可点击</span><span><i class="u"></i>点击卡片后：上游</span><span><i class="d"></i>下游</span></div>'
         f'<div class="legend">闭环：{chips}</div><div class="mapwrap">{main_svg(works, counts)}</div>'
         '<p class="hint">读法：先看蓝色箭头弄清顺序，再看红色虚线弄清哪些步骤要反复做。窄屏上总图可以左右滑动。</p>'),
        ('loops', '六个闭环', '这些工作不是一次做完的：数据、模型和策略要反复迭代。每个闭环写明回流的内容、启动和停止的条件，以及依据。', hg.sec_loops(src)),
        ('stages', '各阶段的产物与进入下一阶段的证据', '“证据”是进入下一阶段前应当拿到的结果。阶段之间可以部分重叠，例如 S2 可以在 S1 的数据还在扩充时开始。', hg.sec_stages(works, src)),
        ('papers', '可以写成论文的方向', '按工作排列。“已有工作与空白”只写所列论文报告的内容；“本轮检索没有找到”只说明在本次检索范围内没有找到，不等于不存在。', hg.sec_papers(works, src)),
        ('links', '与链路的对应', '链路/ 按技术做法组织，本目录按研究步骤组织。● 表示该工作会用到这条链路的内容，点击打开链路文件夹。', hg.sec_matrix(works, src)),
        ('cross', '跨阶段的条件', '下面几项不属于某一项工作，但会影响多个阶段。', hg.sec_cross(src)),
        ('index', '文件夹与文献', '每个文件夹的 README 列出全部文献（带一句话说明）、开源项目和论文方向的依据。', hg.sec_index(works, src)),
    ]
    body = ''.join(f'<section id="{i}"><h2><span class="no">{n:02d}</span>{E(t)}</h2><p class="sub">{E(s)}</p>{c}</section>'
                   for n, (i, t, s, c) in enumerate(secs, 1))
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    meta = (f'{totals["works"]} 项工作 · 6 个阶段 · 6 个闭环 · {totals["papers"]} 个论文方向 · 引用 {totals["refs"]} 篇文献与文档 · '
            f'{totals["repos"]} 个开源项目 · {DATE} 生成')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>工厂级世界模型：研究步骤看板</title><style>{hg.asset('board.css')}</style></head><body>
<header class="mast"><div class="mast-in"><p class="kicker">工业世界模型 · works</p><h1>从零开始做工厂级世界模型：研究步骤看板</h1>
<p class="lede">目前没有公开的工厂级世界模型，也没有对应的数据集。下图按研究顺序列出 17 项工作：先定义问题和评测，再解决数据，然后做子级（机器人与工位）和整厂层的模型与决策，最后做安全校核、评测和部署。每项工作在 <a href="README.md">works/</a> 下有一个文件夹，列出具体任务、可以写成论文的方向和高价值参考文献。</p>
<p class="lede">整厂层的目标按 WWC（Whole World Control，全场统一控制）表述：比 WBC 高一级，场景内的机器人和设备由同一个模型统一控制，而不是每台机器人一个控制器、上层再由 Agent 协调。工厂中的 WWC 即 FWAM，定义见 <a href="../链路/00_总览_工厂级世界动作模型/README.md">00 总览</a> 第 1.3 节。</p>
<p class="lede">本看板不推荐技术路线。STEP 资产化、扫描孪生、JEPA、视频模型等做法见 <a href="../链路/README.md">链路/</a> 和 <a href="../pipeline_board.html">链路看板</a>；本看板回答的是按什么顺序做、每一步做什么、哪里能出论文。</p>
<p class="meta">{E(meta)}</p></div></header>
<nav class="toc"><div class="in">{''.join(f'<a href="#{i}"><b>{n:02d}</b>{t}</a>' for n, (i, t) in enumerate(nav, 1))}<a href="README.md">works/README.md</a><a href="../report.html">调研报告</a></div></nav>
<main>{body}</main>
<aside id="drawer" aria-hidden="true" aria-label="详情"><div class="dh"><span class="dt"></span><button class="x" type="button">关闭 Esc</button></div><div class="body"></div></aside>
<footer><div class="in">arXiv 文献的标题取自 arXiv 页面元数据，2026-11-22 核对、2026-11-27 补充；P 编号是 <a href="../papers/README.md">papers/</a> 中的本地 PDF；GitHub 仓库用 gh api 核对，均未归档；ISO 和出版社页面拒绝脚本访问，已用网页搜索和 Crossref 核对。“分析判断”表示本看板的推断，未经验证。重新生成：<code>python3 scripts/verify_works_sources.py &amp;&amp; python3 scripts/build_works.py</code>（数据在 scripts/works_src/）。</div></footer>
<script type="application/json" id="board-data">{blob}</script><script>{hg.asset('board.js')}</script></body></html>
'''


def main():
    works = load_works()
    check(works)
    src = Sources(works)
    OUT.mkdir(exist_ok=True)
    for w in works:
        d = OUT / w['folder']
        d.mkdir(exist_ok=True)
        (d / 'README.md').write_text(work_md(w, src))
    repos = {n for w in works for n, _ in w['repos']}
    totals = dict(works=len(works), papers=sum(len(w['papers']) for w in works))
    html = page(works, src, dict(totals, refs=0, repos=0))  # 先跑一遍，收集全部引用
    used = src.used
    totals.update(refs=len(used['A']) + len(used['P']) + len(used['S']) + len(used['D']), repos=len(repos | used['R']))
    (OUT / 'README.md').write_text(index_md(works, src, totals))
    html = page(works, src, totals)
    (OUT / 'research_board.html').write_text(html)
    known = {w['folder'] for w in works}
    stray = [p.name for p in OUT.iterdir() if p.is_dir() and p.name not in known]
    print(f'works/: {len(works)} 个文件夹；论文方向 {totals["papers"]}；文献与文档 {totals["refs"]}'
          f'（arXiv {len(used["A"])}，本地 P {len(used["P"])}，S {len(used["S"])}，文档 {len(used["D"])}）；项目 {totals["repos"]}；'
          f'HTML {len(html) // 1024} KB' + (f'；未知文件夹 {stray}' if stray else ''))


if __name__ == '__main__':
    main()
