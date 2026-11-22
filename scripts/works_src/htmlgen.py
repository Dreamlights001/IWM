"""拼装 works/research_board.html 的各节。正文记号统一经 Sources.html 解析。"""
from html import escape as E
from pathlib import Path

from . import common
from .diagram import loop_svg
from .mdgen import neighbors, loop_text, ref_count

HERE = 'works'
STAGE = {s['id']: s for s in common.STAGES}
CIRC = '①②③④⑤⑥'
COMPUTE = [
    ('VLA 微调（openpi）', '推理 8 GB 以上；LoRA 22.5 GB 以上；全参数 70 GB 以上', '一张 4090 可做推理和 LoRA；全参数要 80 GB 卡', '[[R:Physical-Intelligence/openpi]] README'),
    ('小型 JEPA 世界模型（LeWorldModel）', '15M 参数，单张 GPU 几小时', '3090／4090 可做', '[[P55]]'),
    ('整厂层图模型（DeepFleet 图—地面模型）', '13M 参数', '[[L:L11]] 估计 1–2 张 3090／4090 可训练', '[[A:2508.08574]]'),
    ('测试时规划（MA-WAM）', 'RTX 3090、8 个候选：生成加评分 428.0 ms，其中评分 13.4 ms', '相对分钟级的整厂决策周期可忽略', '[[A:2609.31281]]'),
    ('全身控制与 RL（MuJoCo Playground）', '单张 GPU 几分钟训练出策略', '可在单卡上反复迭代', '[[A:2502.08844]]'),
    ('腿式行走（Learning to Walk in Minutes）', '单张工作站 GPU：平地不到 4 分钟，不平地形 20 分钟', '同上', '[[A:2109.11978]]'),
    ('视频模型生成数据（DreamGen）', '24 万条样本：1500 张 L40，约 54 小时', '不可行，只能小规模试验', '[[P65]]'),
    ('大规模动作跟踪（SONIC）', '约 2.1 万 GPU 小时', '不可行，直接用开源跟踪器', '[[A:2511.07820]]'),
    ('视频 WAM 预训练（OpenWAM）', '从 Wan2.2-5B 出发，1 万小时以上视频', '不复现预训练，只用公开权重', '[[A:2610.07922]]'),
]
DEFORM = ('形变、流体、断裂与加工不是单独的工作或阶段，而是任务条件（[[L:专题]]）。任务涉及它们时：[[W:W02]] 的资产要带材料与过程参数；'
          '[[W:W03]]、[[W:W04]] 的仿真要能表示形变或材料去除，或接入加工过程模型；[[W:W05]] 的数据要覆盖这些现象；'
          '[[W:W09]] 要加过程代理，如 PINN [[A:1711.10561]]、神经算子 [[A:2010.08895]]、MeshGraphNets [[P32]]；'
          '[[W:W16]] 要加物理真实性指标，可参考 GaussianBench [[P49]]。')
LICENSE = ('公开论文不代表代码、数据和权重可以商用，用于工厂前要逐项核对许可证。工厂现场数据通常涉及保密，'
           '[[W:W07]] 的数据集论文要事先确定可以公开的范围（分析判断）。')


def wchip(src, wid, lab=None):
    t = f'{wid} {src.works[wid]["name"]}' + (f'：{lab}' if lab else '')
    return f'<a class="chip wref" href="#{wid}" data-w="{wid}">{E(t)}</a>'


def lchip(lp):
    return f'<a class="chip lp" href="#loop{lp["id"]}" data-loopchip="{lp["id"]}">{CIRC[lp["id"]-1]} {E(lp["name"])}</a>'


def top_refs(w, k=8):
    groups = [list(items) for _, items in w['refs']]
    out = []
    while len(out) < k and any(groups):
        for g in groups:
            if g and len(out) < k:
                out.append(g.pop(0))
    return out


def drawer_work(w, src):
    st = STAGE[w['stage']]
    ups, downs, loops = neighbors(w['id'])
    h = src.html
    o = [f'<p class="dk">{st["id"]} {E(st["name"])}</p><h3>{w["id"]} {E(w["name"])}</h3><p class="one">{h(w["oneline"], HERE)}</p>',
         '<div class="rel"><div><b>上游</b>' + (''.join(wchip(src, x, lab) for x, lab in ups) or '—') + '</div>',
         '<div><b>下游</b>' + (''.join(wchip(src, x, lab) for x, lab in downs) or '—') + '</div>',
         '<div><b>闭环</b>' + (''.join(lchip(lp) for lp in loops) or '—') + '</div></div>',
         '<h4>具体工作</h4><ol>' + ''.join(f'<li>{h(t, HERE)}</li>' for t in w['tasks']) + '</ol>',
         '<h4>可以写成论文的方向</h4><ul class="pd">' +
         ''.join(f'<li><b>{E(p["t"])} <span class="kind">{E(p["kind"])}</span></b>{h(p["q"], HERE)}</li>' for p in w['papers']) + '</ul>',
         '<h4>精选文献</h4><ul class="refs">' + ''.join(src.entry(k, n, HERE, 'html') for k, n in top_refs(w)) + '</ul>',
         f'<p><a href="{E(w["folder"])}/README.md">打开文件夹 README：全部 {ref_count(w)} 条文献、{len(w["repos"])} 个开源项目、论文方向的依据</a></p>']
    return ''.join(o)


def drawer_loop(lp, src):
    h = src.html
    return (f'<p class="dk">闭环</p><h3>{CIRC[lp["id"]-1]} {E(lp["name"])}</h3>{loop_svg(lp)}'
            f'<p>{E(loop_text(lp))}</p><div class="rel"><b>涉及</b>' + ''.join(wchip(src, m) for m in lp['members']) + '</div>'
            f'<h4>回流的内容</h4><p>{h(lp["flows"], HERE)}</p><h4>何时启动、何时停止</h4><p>{h(lp["when"], HERE)}</p>'
            f'<h4>依据</h4><p>{h(lp["evidence"], HERE)}</p><h4>相关论文方向</h4><p>{h(lp["paper"], HERE)}</p>')


def sec_loops(src):
    h = src.html
    cards = []
    for lp in common.LOOPS:
        cards.append(f'<article class="lcard" id="loop-{lp["id"]}"><h3>{CIRC[lp["id"]-1]} {E(lp["name"])}</h3>{loop_svg(lp)}<dl>'
                     f'<dt>回流的内容</dt><dd>{h(lp["flows"], HERE)}</dd><dt>何时启动、何时停止</dt><dd>{h(lp["when"], HERE)}</dd>'
                     f'<dt>依据</dt><dd>{h(lp["evidence"], HERE)}</dd><dt>相关论文方向</dt><dd>{h(lp["paper"], HERE)}</dd></dl></article>')
    return '<div class="loopgrid">' + ''.join(cards) + '</div>'


def sec_stages(works, src):
    rows = []
    for s in common.STAGES:
        ws = ''.join(wchip(src, w['id']) for w in works if w['stage'] == s['id'])
        rows.append(f'<tr><td class="st" style="color:{s["color"]}">{s["id"]} {E(s["name"])}</td><td>{E(s["goal"])}</td>'
                    f'<td>{ws}</td><td>{E(s["outputs"])}</td><td>{E(s["gate"])}</td></tr>')
    return ('<div class="tw"><table><thead><tr><th>阶段</th><th>目标</th><th>工作</th><th>产物</th><th>进入下一阶段的证据</th></tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table></div>')


def sec_papers(works, src):
    h, rows = src.html, []
    for w in works:
        for p in w['papers']:
            rows.append(f'<tr><td>{wchip(src, w["id"])}</td><td><b>{E(p["t"])}</b><br><span class="kind">{E(p["kind"])}</span></td>'
                        f'<td>{h(p["q"], HERE)}<details><summary>已有工作与空白、怎样验证</summary><p>{h(p["gap"], HERE)}</p>'
                        f'<p>验证：{h(p["check"], HERE)}</p></details></td></tr>')
    return ('<div class="tw"><table><thead><tr><th>工作</th><th>方向</th><th>研究问题</th></tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table></div>')


def sec_matrix(works, src):
    head = ''.join(f'<th class="m">{E(common.L_LABEL.get(c, c))}</th>' for c in common.MATRIX_COLS)
    rows = []
    for w in works:
        cells = ''.join(f'<td class="m">{"<a href=" + chr(34) + "../链路/" + common.L_DIRS[c] + "/README.md" + chr(34) + ">●</a>" if c in w["links"] else ""}</td>'
                        for c in common.MATRIX_COLS)
        rows.append(f'<tr><td>{wchip(src, w["id"])}</td>{cells}</tr>')
    return f'<div class="tw"><table class="matrix"><thead><tr><th>工作</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def sec_cross(src):
    h = src.html
    rows = ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td>{h(c, HERE)}</td><td>{h(d, HERE)}</td></tr>' for a, b, c, d in COMPUTE)
    return (f'<div class="cross"><div class="box"><h3>形变、流体、断裂与加工</h3><p>{h(DEFORM, HERE)}</p></div>'
            f'<div class="box"><h3>许可与数据保密</h3><p>{h(LICENSE, HERE)}</p></div>'
            '<div class="box wide"><h3>算力：已报告的数字与对本项目的含义</h3><p class="sub">算力假设：几张 RTX 3090／4090，加极少量 40 GB／80 GB 级别的卡。</p>'
            f'<div class="tw"><table><thead><tr><th>事项</th><th>已报告的数据</th><th>对本项目的含义</th><th>来源</th></tr></thead><tbody>{rows}</tbody></table></div></div></div>')


def sec_index(works, src):
    rows = ''.join(f'<tr><td>{wchip(src, w["id"])}</td><td>{STAGE[w["stage"]]["id"]} {E(STAGE[w["stage"]]["name"])}</td>'
                   f'<td>{len(w["papers"])}</td><td>{ref_count(w)}</td><td>{len(w["repos"])}</td>'
                   f'<td><a href="{E(w["folder"])}/README.md">{E(w["folder"])}/</a></td></tr>' for w in works)
    return ('<div class="tw"><table><thead><tr><th>工作</th><th>阶段</th><th>论文方向</th><th>文献</th><th>项目</th><th>文件夹</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def asset(name):
    return (Path(__file__).parent / name).read_text()
