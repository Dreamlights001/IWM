"""works/ 研究看板的数据与生成模块。入口：scripts/build_works.py。"""
import importlib

WORK_IDS = [f'W{i:02d}' for i in range(1, 18)]


def load_works():
    works = []
    for wid in WORK_IDS:
        mod = importlib.import_module(f'works_src.{wid.lower()}')
        w = dict(mod.W)
        assert w['id'] == wid, (wid, w['id'])
        works.append(w)
    return works
