#!/usr/bin/env python3
"""Archive the papers added on 2026-11-11: world-model routes, simulator-to-world-model
mechanisms, scene instance decomposition and latency evidence (P51 onward).

Reuses collect() from collect_papers.py, so every record has the same provenance fields.
Re-running is safe: existing PDFs and source pages are reused, not downloaded again.
"""
import concurrent.futures as cf
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_papers import collect, EVIDENCE, PAPERS  # noqa: E402

ACCESSED = '2026-11-11'
SEEDS = [
 ('P51','I_JEPA','2301.08243','jepa'),
 ('P52','PLDM','2502.14819','jepa'),
 ('P53','LeJEPA','2511.08544','jepa'),
 ('P54','JEPA_WM_Physical_Planning','2512.24497','jepa'),
 ('P55','LeWorldModel','2603.19312','jepa'),
 ('P56','H_JEPA','2610.06805','jepa'),
 ('P57','RoboJEPA','2610.10515','jepa'),
 ('P58','Real_is_Sim','2504.03597','sim2wm'),
 ('P59','RialTo','2403.03949','sim2wm'),
 ('P60','ASID','2404.12308','sim2wm'),
 ('P61','MuJoCo_MPC_Predictive_Sampling','2212.00541','sim2wm'),
 ('P62','DROP','2409.14562','sim2wm'),
 ('P63','Simulator_Residual_Pushing','1808.03246','sim2wm'),
 ('P64','Cosmos_Transfer1','2503.14492','video'),
 ('P65','DreamGen','2505.12705','video'),
 ('P66','LLM_Virtual_Commissioning','2606.03255','sim2wm'),
 ('P67','GameNGen','2408.14837','video'),
 ('P68','Matrix_Game_2','2508.13009','video'),
 ('P69','Dreamer_4','2509.24527','latent'),
 ('P70','Navigation_World_Models','2412.03572','video'),
 ('P71','Genie_Envisioner','2508.05635','video'),
 ('P72','Ctrl_World','2510.10125','video'),
 ('P73','Veo_Robot_Policy_Evaluation','2512.10675','video'),
 ('P74','Cosmos_Predict2_5','2511.00062','video'),
 ('P75','DreamDojo','2602.06949','video'),
 ('P76','DreamZero','2602.15922','video'),
 ('P77','WorldEcho','2608.24885','evaluation'),
 ('P78','HY_WorldPlay','2512.14614','video'),
 ('P79','HunyuanWorld_1','2507.21809','spatial'),
 ('P80','HY_World_2','2604.14268','spatial'),
 ('P81','Lyra','2509.19296','spatial'),
 ('P82','Lyra_2','2604.13036','spatial'),
 ('P83','Aether','2503.18945','spatial'),
 ('P84','TesserAct','2504.20995','spatial'),
 ('P85','GWM_Gaussian_World_Model','2508.17600','spatial'),
 ('P86','Kinema4D','2603.16669','spatial'),
 ('P87','RynnWorld_4D','2607.06559','spatial'),
 ('P88','MRO_GWM','2606.01950','spatial'),
 ('P89','Gaussian_Grouping','2312.00732','segmentation'),
 ('P90','SAGA','2312.00860','segmentation'),
 ('P91','OpenGaussian','2406.02058','segmentation'),
 ('P92','InstaScene','2507.08416','segmentation'),
 ('P93','DecoupledGaussian','2503.05484','segmentation'),
 ('P94','SceneAgent','2610.34745','segmentation'),
 ('P95','WorldAct','2605.15843','segmentation'),
]

def main():
    PAPERS.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(lambda s: collect(s, accessed=ACCESSED), SEEDS))
    failed = [r['id'] for r in records if not r['status'].startswith('downloaded')]
    print(f"Completed {len(records)-len(failed)}/{len(records)}; failed: {failed}", flush=True)
    return 1 if failed else 0

if __name__ == '__main__':
    raise SystemExit(main())
