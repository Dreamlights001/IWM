# 工厂级工业世界模型调研

打开 [report.html](report.html) 阅读中文报告。报告不作技术路线推荐。

[pipeline_board.html](pipeline_board.html) 是链路看板：假设已有设备 STEP、实物扫描和一台带 URDF 的机器人，列出 9 条可搭建的世界模型链路（编号 L1–L10，L5 空缺），附步骤、时延、证据、局限、GitHub 项目与文献链接；形变、流体、断裂与加工不是单独链路，作为“跨链路条件”单独成节。同样不做推荐。重新生成：`python3 scripts/build_pipeline_board.py`。

[链路/](链路/README.md) 把看板中的每条链路拆成单独文件夹，每个文件夹有思考、idea、有限算力下的实施路线和推荐文献；另新增 L11「工厂级世界动作模型（FWAM）」，讨论整厂层的分层模型与命名。`专题_形变流体断裂与加工` 说明任务涉及这些情况时各链路要补什么，并对照仿真器能力；L8 补充了参考 INTACT 与 SADL 在仿真中训练 JEPA 世界模型的可行性分析。

[works/](works/README.md) 回答“要做研究需要经过哪些步骤”：把工厂级世界模型的研究拆成 6 个阶段、17 项工作（问题定义、设备资产与车间场景生成、设备逻辑与事件日志、机器人与全身动作数据、真实采集、仿真—真实对齐、工位层与整厂层世界模型、反事实数据、技能端口、多机器人协作、整厂调度、安全、基准、部署与数据飞轮），并用 6 个闭环表示需要反复迭代的步骤。总看板是 [works/research_board.html](works/research_board.html)；每项工作一个文件夹，写明具体任务、可以写成论文的方向和高价值参考文献。同样不做路线推荐。重新生成：`python3 scripts/verify_works_sources.py && python3 scripts/build_works.py`，检查：`node scripts/check_works.cjs`。

- 覆盖 6 条世界模型路线（显式仿真、空间智能、生成式视频、JEPA、潜变量控制、结构化流程）及其 8 个实现方案 A–H；资产路线怎样成为世界模型；各路线优缺点（含场景单体化与推理时延）；机床建模的两个选择；形变与切削；实现步骤、数据、评测与未解问题。
- 2026-11-11 按世界模型路线重组全文，新增 45 篇论文（P51–P95）与补充来源 S8–S25；改动前的版本保存在 `backup/2026-11-11_before_logic_revision/`。新增论文尚未导入 Zotero。
- 2026-11-12 补入工厂仿真器实现专题，涉及物理步进、PLC／NC、工艺与产线联仿，新增 P96–P99 和 S26–S32。
- 2026-11-22 把链路看板和 `链路/` 中的原 L5「加工与形变过程模型」改为跨链路专题，并在 L8 补充 INTACT（arXiv 2607.26056）与 SADL（arXiv 2611.21596）；改动前的看板、脚本、`链路/` 目录和本文件保存在 `backup/2026-11-22_before_L5_to_topic/`。
- 2026-11-22 新增 `works/` 研究步骤看板与 17 个工作文件夹，引用 213 篇 arXiv 文献（标题按 arXiv 页面元数据核对）和 104 个 GitHub 项目（用 `gh api` 核对，均未归档）；新增文献没有下载到 `papers/`，也没有导入 Zotero。
- `papers/` 保存 99 篇公开论文全文，正文编号 P01–P99 可定位到本地 PDF。
- `papers/README.md` 是论文索引；`manifest.json` 保存来源、版本、页数和 SHA-256；`references.bib` 可用于文献管理。
- `research/` 保留来源元数据、可检索全文文本与逐篇注释；本报告未运行论文代码或复现实验。
- 调研日：2026-11-09，2026-11-11 与 2026-11-12 补充（Asia/Shanghai）。纳入论文的修订版本均不晚于获取日；不是穷尽性系统综述。

HTML 的正文、样式、示意图、目录和检索脚本均在单文件中，可离线使用。请保持 `report.html` 与 `papers/` 的相对位置。外部来源链接需要联网。

如果本地文件预览器限制跳转，可在该目录运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

然后在浏览器打开 `http://127.0.0.1:8000/report.html`。

重新生成报告：

```bash
python3 scripts/build_report.py
```

新增形变、切削、材料去除、断裂和变拓扑专题；补充 5 篇论文与 3 项官方技术文档。

重新下载／核对论文需要 Python `requests`、`beautifulsoup4` 及 Poppler 的 `pdftotext`、`pdfinfo`：

```bash
python3 scripts/collect_papers.py
python3 scripts/collect_machining_papers.py
python3 scripts/collect_world_model_papers.py
python3 scripts/collect_simulator_papers.py
python3 scripts/build_report.py
```

PDF 保留原作者与发布方版权／许可证。公开论文不意味着代码、数据集与模型权重的许可证相同。

## Zotero

2026-11-09 已导入“我的文库 / IWM”：P01–P50 共 50 篇论文（含全文与调研注释）、7 项官方技术文档，按 12 个子分类组织。“11 形变、切削与材料去除”含 11 篇专题交叉收录文献，同一书目条目可属于多个分类。已复用原库 3 篇 JEPA 条目并保留其原有信息；本次新建的重复父条目已移入回收站。

50 份 Zotero 归档 PDF 均已校验 SHA-256。分类、附件与条目对应记录见 `research/zotero_verified_inventory.json`；导入过程说明见 `research/ZOTERO_IMPORT.md`。
