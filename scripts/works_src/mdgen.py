"""生成 works/README.md 与各工作文件夹的 README.md。"""
from . import common
from .refs import ROOT

STAGE = {s['id']: s for s in common.STAGES}
CIRC = '①②③④⑤⑥'
NOTE = ('说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；'
        'GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。')


def l_title(key):
    first = (ROOT / '链路' / common.L_DIRS[key] / 'README.md').read_text().splitlines()[0]
    return first.lstrip('# ').strip()


def neighbors(wid):
    ups = [(s, lab) for s, d, lab in common.EDGES if d == wid]
    downs = [(d, lab) for s, d, lab in common.EDGES if s == wid]
    loops = [lp for lp in common.LOOPS if wid in lp['members']]
    return ups, downs, loops


def loop_text(lp):
    steps = ' → '.join(f'{who} {act}' for who, act in lp['cycle'])
    return f'{steps} → {lp["back"]}'


def ref_count(w):
    return sum(len(items) for _, items in w['refs'])


def work_md(w, src):
    here = f'works/{w["folder"]}'
    st = STAGE[w['stage']]
    ups, downs, loops = neighbors(w['id'])
    rel = lambda lst: '<br>'.join(src.md(f'[[W:{x}]]', here) + f'：{lab}' for x, lab in lst) or '—'
    L = [f'# {w["id"]} {w["name"]}', '',
         f'> 阶段：{st["id"]} {st["name"]}　·　总看板：[research_board.html](../research_board.html#{w["id"]})', '',
         src.md(w['oneline'], here), '',
         '| 上游（交付物） | 下游（交付物） | 所在闭环 |', '|---|---|---|',
         f'| {rel(ups)} | {rel(downs)} | ' + ('<br>'.join(f'{CIRC[lp["id"]-1]} {lp["name"]}' for lp in loops) or '—') + ' |', '',
         '## 1. 为什么要做', '', src.md(w['why'], here), '',
         '## 2. 输入与产物', '', '**输入**', '']
    L += [f'- {src.md(x, here)}' for x in w['inputs']] + ['', '**产物**', '']
    L += [f'- {src.md(x, here)}' for x in w['outputs']] + ['', '## 3. 具体工作', '']
    L += [f'{i}. {src.md(x, here)}' for i, x in enumerate(w['tasks'], 1)] + ['', '## 4. 可以写成论文的方向', '']
    for i, p in enumerate(w['papers'], 1):
        L += [f'### 4.{i} {p["t"]}', '', f'- 类型：{p["kind"]}', f'- 研究问题：{src.md(p["q"], here)}',
              f'- 已有工作与空白：{src.md(p["gap"], here)}', f'- 怎样验证：{src.md(p["check"], here)}', '']
    if loops:
        L += ['## 5. 所在闭环', '']
        L += [f'- {CIRC[lp["id"]-1]} {lp["name"]}：{loop_text(lp)}。{src.md(lp["evidence"], here)}' for lp in loops] + ['']
    L += ['## 6. 对应的链路', '']
    for k in w['links']:
        L.append(f'- {src.md(f"[[L:{k}]]", here)}：{l_title(k)}')
    L.append('')
    n = 7
    if w.get('compute'):
        L += [f'## {n}. 算力', ''] + [f'- {src.md(x, here)}' for x in w['compute']] + ['']
        n += 1
    L += [f'## {n}. 高价值参考文献', '']
    for group, items in w['refs']:
        L += [f'### {group}', ''] + [src.entry(k, note, here) for k, note in items] + ['']
    L += [f'## {n + 1}. 参考项目', '']
    L += [src.repo(name, note, here) for name, note in w['repos']] or [src.md(w.get('repo_note', '—'), here)]
    L += ['', '---', '', NOTE, '']
    return '\n'.join(L)


def index_md(works, src, totals):
    here = 'works'
    byst = {}
    for w in works:
        byst.setdefault(w['stage'], []).append(w)
    L = ['# works：工厂级世界模型的研究步骤', '',
         '目前没有公开的工厂级世界模型，也没有对应的数据集。这个目录把研究拆成 17 项工作、6 个阶段：先定义问题和评测，再解决数据，'
         '然后做子级（机器人与工位）和整厂层的模型与决策，最后做安全校核、评测和部署。有些工作之间要反复迭代，用 6 个闭环表示。', '',
         '打开 [research_board.html](research_board.html) 看总图：蓝色实线是顺序交付，红色虚线是闭环；点击卡片可看上下游和精选文献。'
         '每项工作有一个文件夹，写明要解决的问题、具体任务、可以写成论文的方向和高价值参考文献。', '',
         '本目录不推荐技术路线。各条链路（STEP 资产化、扫描孪生、JEPA、视频模型等）的做法见 [../链路/](../链路/README.md)；'
         '本目录回答的是“按什么顺序做研究、每一步做什么、哪里能出论文”。', '',
         f'统计：{totals["works"]} 项工作，{totals["papers"]} 个论文方向，引用 {totals["refs"]} 篇不重复的文献和文档，{totals["repos"]} 个开源项目。', '',
         '## 阶段与工作', '', '| 阶段 | 工作 | 一句话 |', '|---|---|---|']
    for st in common.STAGES:
        for i, w in enumerate(byst[st['id']]):
            head = f'{st["id"]} {st["name"]}' if i == 0 else ''
            L.append(f'| {head} | [{w["id"]} {w["name"]}]({w["folder"]}/README.md) | {src.md(w["oneline"], here)} |')
    L += ['', '## 六个闭环', '']
    L += [f'- {CIRC[lp["id"]-1]} **{lp["name"]}**：{loop_text(lp)}。{src.md(lp["when"], here)}' for lp in common.LOOPS]
    L += ['', '## 各阶段进入下一阶段的证据', '', '| 阶段 | 产物 | 进入下一阶段的证据 |', '|---|---|---|']
    L += [f'| {s["id"]} {s["name"]} | {s["outputs"]} | {s["gate"]} |' for s in common.STAGES]
    L += ['', '## 可以写成论文的方向', '', '| 工作 | 方向 | 类型 |', '|---|---|---|']
    for w in works:
        for p in w['papers']:
            L.append(f'| [{w["id"]}]({w["folder"]}/README.md) | {p["t"]} | {p["kind"]} |')
    L += ['', '## 与链路的对应', '', '| 工作 | ' + ' | '.join(common.L_LABEL.get(c, c) for c in common.MATRIX_COLS) + ' |',
          '|---|' + '---|' * len(common.MATRIX_COLS)]
    for w in works:
        L.append(f'| {w["id"]} {w["name"]} | ' + ' | '.join('●' if c in w['links'] else '' for c in common.MATRIX_COLS) + ' |')
    L += ['', '## 约定', '',
          '- 形变、流体、断裂和加工是任务条件，不是单独的工作或阶段；任务涉及它们时，按 [../链路/专题_形变流体断裂与加工](../链路/专题_形变流体断裂与加工/README.md) 补相应能力（主要影响 W02、W03、W05、W09、W16）。',
          '- 算力假设：几张 RTX 3090／4090，加极少量 40 GB／80 GB 级别的卡。各文件夹的“算力”一节只写论文或官方文档报告的数字。',
          '- 新增的 arXiv 文献没有下载到 `papers/`，也没有导入 Zotero。',
          '- 重新生成：`python3 scripts/verify_works_sources.py && python3 scripts/build_works.py`。', '', NOTE, '']
    return '\n'.join(L)
