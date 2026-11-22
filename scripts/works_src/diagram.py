"""总图与闭环小图（SVG）。坐标手工排布，保证箭头不穿过卡片。"""
import math
import re
from html import escape as E

from . import common

STAGE = {s['id']: s for s in common.STAGES}
RED, BLUE, INK, MUTED = '#c2412d', '#2b5c8a', '#1d2b36', '#5b6b77'
CIRC = '①②③④⑤⑥'
SVG_W, SVG_H = 1200, 1222

GEOM = {
    'W01': (120, 62, 878, 70),
    'W02': (120, 200, 200, 86), 'W03': (346, 200, 200, 86), 'W05': (572, 200, 200, 86), 'W06': (798, 200, 200, 86),
    'W04': (346, 322, 200, 86), 'W07': (572, 322, 200, 86), 'W08': (798, 322, 200, 86),
    'W09': (120, 516, 400, 86), 'W12': (598, 516, 400, 86),
    'W10': (120, 680, 400, 86), 'W13': (598, 680, 400, 86),
    'W11': (120, 800, 400, 86), 'W14': (598, 800, 400, 86),
    'W15': (120, 956, 400, 86), 'W16': (598, 956, 400, 86),
    'W17': (120, 1110, 878, 70),
}
BANDS = {'S0': (50, 144), 'S1': (182, 462), 'S2': (500, 616), 'S3': (664, 902), 'S4': (940, 1056), 'S5': (1094, 1196)}
STAGE_LINES = {'S0': ['定义问题', '与评测'], 'S1': ['数据基础'], 'S2': ['子级：', '机器人与工位'],
               'S3': ['整厂层：', '预测与决策'], 'S4': ['安全校核', '与评测'], 'S5': ['部署与', '数据飞轮']}
SUBLABELS = {'S1': [(272, '上排：仿真生成'), (372, '下排：设备与真实')],
             'S2': [(590, '左：预测'), (605, '右：决策')], 'S3': [(756, '左：预测'), (771, '右：决策')]}
# 顺序交付（蓝色实线）：x1, y1, x2, y2, 标签, 标签 x, 标签 y, 对齐
HANDOFF = [(220, 132, 220, 200, '交付：接口规范、记录格式、评测协议草案、约束清单', 232, 170, 'start'),
           (320, 462, 320, 516, '仿真示范、真实数据、校准参数', 332, 492, 'start'),
           (798, 462, 798, 516, '示范数据、全身动作库', 810, 492, 'start'),
           (260, 602, 260, 680, '工位预测与自报告', 250, 646, 'end'),
           (798, 602, 798, 680, '技能端口与自报告', 810, 646, 'start'),
           (798, 886, 798, 956, '待评测的模型与策略', 810, 926, 'start'),
           (320, 1042, 320, 1110, '上线前校核', 332, 1080, 'start'),
           (798, 1042, 798, 1110, '验收通过的模型与策略', 810, 1080, 'start')]
INBAND = [(320, 243, 346, 243), (546, 243, 572, 243), (446, 322, 446, 286), (772, 365, 798, 365),
          (520, 548, 598, 548), (520, 712, 598, 712), (798, 766, 798, 800), (290, 800, 290, 766)]
# 局部闭环（红色虚线）：闭环号, 路径, 徽标位置, 说明
LOCAL = [(3, 'M 640 200 C 640 182 480 182 480 200', (560, 188), None),
         (2, 'M 898 408 L 898 434 L 220 434 L 220 286', (560, 434), (576, 453, '校准结果回写资产、场景与设备参数')),
         (4, 'M 598 576 L 520 576', (559, 576), None),
         (4, 'M 598 826 C 559 826 559 752 520 752', (559, 789), None),
         (1, 'M 340 766 L 340 800', (356, 783), None),
         (5, 'M 300 680 L 300 602', (316, 641), (330, 646, '跨层一致'))]
# 跨阶段闭环（右侧通道）：闭环号, 通道 x, 起点 y, 终点 y, 竖排说明, 徽标 y。
# 内层通道放起止范围最短的 ②；说明文字都从 ⑥ 的回流线（y=390）下方开始，避免被横线穿过。
GUTTER = [(2, 1030, 548, 352, '仿真—真实校准：W12 → W07', 406),
          (1, 1082, 843, 243, '主动与反事实数据：W11 → W03·W04·W05', 406),
          (6, 1134, 1145, 390, '评测—部署飞轮：W17 → W07·W04·W11', 406)]


def _units(tok):
    return sum(1.0 if ord(c) > 0x2E7F else 0.56 for c in tok)


def wrap(text, maxu, maxlines):
    toks = re.findall(r'[A-Za-z0-9.\-+/]+|\s|.', text)
    lines, cur, cu = [], '', 0.0
    for t in toks:
        u = _units(t)
        if cu + u > maxu and cur and t not in '，。、；：）”' and not t.isspace():
            lines.append(cur.rstrip())
            cur, cu = '', 0.0
        if not cur and t.isspace():
            continue
        cur += t
        cu += u
    if cur.strip():
        lines.append(cur.rstrip())
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        lines[-1] = lines[-1][:-1] + '…'
    return lines


def _badge(n, x, y):
    return (f'<g class="loopbadge" data-loop="{n}" tabindex="0" role="button" aria-label="闭环 {CIRC[n-1]}">'
            f'<circle cx="{x}" cy="{y}" r="9"/><text x="{x}" y="{y + 4.2}">{n}</text></g>')


def _card(w, counts):
    x, y, cw, ch = GEOM[w['id']]
    col = STAGE[w['stage']]['color']
    full = cw > 800
    maxu = (cw - 28) / 12.2
    lines = wrap(w['card'], maxu, 1 if full else 2)
    out = [f'<g class="card" id="c-{w["id"]}" data-w="{w["id"]}" tabindex="0" role="button" '
           f'aria-label="{E(w["id"] + " " + w["name"])}">',
           f'<rect class="card-bg" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="5" style="--sc:{col}"/>',
           f'<rect x="{x}" y="{y}" width="5" height="{ch}" rx="2" fill="{col}"/>',
           f'<text class="cid" x="{x + 15}" y="{y + 22}" fill="{col}">{w["id"]}</text>',
           f'<text class="cname" x="{x + 52}" y="{y + 22}">{E(w["name"])}</text>']
    for i, ln in enumerate(lines):
        out.append(f'<text class="csum" x="{x + 15}" y="{y + 42 + 17 * i}">{E(ln)}</text>')
    out.append(f'<text class="cmeta" x="{x + 15}" y="{y + ch - 10}">{E(counts)}</text></g>')
    return ''.join(out)


def main_svg(works, counts):
    o = [f'<svg id="map" viewBox="0 0 {SVG_W} {SVG_H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="研究步骤总图：六个阶段、17 项工作与六个闭环">',
         '<defs>',
         f'<marker id="ah-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>',
         f'<marker id="ah-r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker>',
         '<marker id="ah-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#3d4f5c"/></marker>',
         '</defs>',
         f'<text class="gut-h" x="1012" y="36">右侧通道：跨阶段闭环</text>']
    for sid, (y0, y1) in BANDS.items():
        col = STAGE[sid]['color']
        o.append(f'<rect class="band" x="6" y="{y0}" width="994" height="{y1 - y0}" rx="7" style="--sc:{col}"/>')
        o.append(f'<text class="sid" x="18" y="{y0 + 30}" fill="{col}">{sid}</text>')
        for i, ln in enumerate(STAGE_LINES[sid]):
            o.append(f'<text class="sname" x="18" y="{y0 + 52 + 17 * i}">{E(ln)}</text>')
        for yy, txt in SUBLABELS.get(sid, []):
            o.append(f'<text class="ssub" x="18" y="{yy}">{E(txt)}</text>')
    o.append('<g class="static">')
    for x1, y1, x2, y2, lab, lx, ly, anc in HANDOFF:
        o.append(f'<line class="handoff" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#ah-b)"/>')
        o.append(f'<text class="hlab" x="{lx}" y="{ly}" text-anchor="{anc}">{E(lab)}</text>')
    for x1, y1, x2, y2 in INBAND:
        o.append(f'<line class="flow" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#ah-b)"/>')
    for n, d, (bx, by), lab in LOCAL:
        o.append(f'<path class="loop" data-loop="{n}" d="{d}" marker-end="url(#ah-r)"/>')
        if lab:
            o.append(f'<text class="llab" x="{lab[0]}" y="{lab[1]}">{E(lab[2])}</text>')
    for n, gx, ys, ye, lab, by in GUTTER:
        o.append(f'<path class="loop gut" data-loop="{n}" d="M 1000 {ys} L {gx} {ys} L {gx} {ye} L 1000 {ye}" marker-end="url(#ah-r)"/>')
        o.append(f'<text class="vlab" x="{gx + 14}" y="{by + 16}">{E(lab)}</text>')
    o.append('</g><g id="overlay"></g><g class="cards">')
    for w in works:
        o.append(_card(w, counts[w['id']]))
    o.append('</g><g class="badges">')
    for n, _, (bx, by), _ in LOCAL:
        o.append(_badge(n, bx, by))
    for n, gx, ys, ye, _, by in GUTTER:
        o.append(_badge(n, gx, by))
    o.append('</g></svg>')
    return ''.join(o)


def loop_svg(lp):
    nodes = lp['cycle']
    n = len(nodes)
    cx, cy, R = 180, 146, 100
    pts = [(cx + R * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    bw, bh = 124, 54
    o = [f'<svg viewBox="0 0 360 292" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="闭环 {CIRC[lp["id"]-1]} {E(lp["name"])}">',
         f'<defs><marker id="lah{lp["id"]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker></defs>',
         f'<text class="lnum" x="{cx}" y="{cy + 12}">{CIRC[lp["id"]-1]}</text>']
    def rim(p, q, pad=7):
        """从框 p 的中心朝 q 方向，取框边界外 pad 处的点。"""
        dx, dy = q[0] - p[0], q[1] - p[1]
        k = min((bw / 2 + pad) / abs(dx) if dx else 1e9, (bh / 2 + pad) / abs(dy) if dy else 1e9)
        return p[0] + dx * k, p[1] + dy * k

    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = mx - cx, my - cy
        L = math.hypot(dx, dy) or 1
        qx, qy = mx + dx / L * 30, my + dy / L * 30
        (sx, sy), (ex, ey) = rim(a, (qx, qy)), rim(b, (qx, qy))
        cls = 'lback' if i == n - 1 else 'lstep'
        o.append(f'<path class="{cls}" d="M {sx:.1f} {sy:.1f} Q {qx:.1f} {qy:.1f} {ex:.1f} {ey:.1f}" marker-end="url(#lah{lp['id']})"/>')
        if i == n - 1:
            ux, uy = dx / L, dy / L
            anchor = 'end' if ux < -0.3 else ('start' if ux > 0.3 else 'middle')
            o.append(f'<text class="lbacklab" text-anchor="{anchor}" x="{qx + ux * 10:.1f}" y="{qy + uy * 10 + 4:.1f}">{E(lp["back"])}</text>')
    for (px, py), (who, act) in zip(pts, nodes):
        o.append(f'<rect class="lnode" x="{px - bw / 2:.1f}" y="{py - bh / 2:.1f}" width="{bw}" height="{bh}" rx="5"/>')
        o.append(f'<text class="lwho" x="{px:.1f}" y="{py - bh / 2 + 17:.1f}">{E(who)}</text>')
        for j, ln in enumerate(wrap(act, 10.2, 2)):
            o.append(f'<text class="lact" x="{px:.1f}" y="{py - bh / 2 + 33 + 14 * j:.1f}">{E(ln)}</text>')
    o.append('</svg>')
    return ''.join(o)
