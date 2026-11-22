# W03 车间场景生成

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W03)

按工艺路线、物流通道和安全距离批量生成可仿真的车间场景，设备带逻辑，可从快照复位，并配上任务与成功判据。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W02（设备资产生成）](../W02_设备资产生成/README.md)：可仿真资产<br>[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md)：设备行为模型 | [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md)：可复位场景与任务<br>[W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)：快照与复位接口 | ① 主动与反事实数据<br>② 仿真—真实校准<br>③ 场景—任务联合生成 |

## 1. 为什么要做

公开的场景生成工作面向住宅和室内：ProcTHOR 程序化生成房屋 [arXiv 2206.06994](https://arxiv.org/abs/2206.06994)，Holodeck 用语言生成室内环境 [arXiv 2312.09067](https://arxiv.org/abs/2312.09067)，Infinigen Indoors [arXiv 2406.11824](https://arxiv.org/abs/2406.11824)、PhyScene [arXiv 2404.09465](https://arxiv.org/abs/2404.09465)、SceneFoundry [arXiv 2601.05810](https://arxiv.org/abs/2601.05810) 生成室内或公寓场景，InternScenes 约 4 万个场景，覆盖 15 种室内场景类型 [arXiv 2509.10813](https://arxiv.org/abs/2509.10813)。车间布局受工艺路线、物流通道、缓存和安全距离约束，设备还带逻辑。工业方向已有 IndustryEQA（仓储场景的具身问答基准）[arXiv 2505.20640](https://arxiv.org/abs/2505.20640)，以及 HolidayFactory：按人给定的工作场所和任务，智能体式地生成仿真资产和场景变体，并做几何与交互检查 [arXiv 2611.11789](https://arxiv.org/abs/2611.11789)。

## 2. 输入与产物

**输入**

- [W02（设备资产生成）](../W02_设备资产生成/README.md) 的资产库
- [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的设备行为模型
- 工艺路线与节拍
- 车间平面与通道规范
- [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的规范

**产物**

- 参数化的车间布局生成器
- 可从快照复位的仿真场景（MJCF／USD），设备已接逻辑
- 每个场景的任务清单与成功判据
- 场景分布参数，供 [W08（仿真—真实对齐）](../W08_仿真真实对齐/README.md) 校准、[W11（反事实与主动数据）](../W11_反事实与主动数据/README.md) 主动采样

## 3. 具体工作

1. 写布局语法：工艺路线 → 工位顺序 → 设备摆放 → 通道与缓存 → 料架与检测台。
2. 约束检查：碰撞、机器人可达、AGV 通行宽度、安全距离；不满足时回退或修正。PhyScene 用物理与可交互约束引导生成 [arXiv 2404.09465](https://arxiv.org/abs/2404.09465)。
3. 用语言或 VLM 生成布局：参考 LayoutGPT [arXiv 2305.15393](https://arxiv.org/abs/2305.15393)、Holodeck [arXiv 2312.09067](https://arxiv.org/abs/2312.09067)、RoboLayout（在 LayoutVLM 上加入面向智能体的推理）[arXiv 2603.05522](https://arxiv.org/abs/2603.05522)。
4. 任务生成：用 LLM 写任务代码与成功判据，参考 GenSim [arXiv 2310.01361](https://arxiv.org/abs/2310.01361)、GenSim2 [arXiv 2410.03645](https://arxiv.org/abs/2410.03645)、RoboGen [arXiv 2311.01455](https://arxiv.org/abs/2311.01455)；给定任务生成环境可参考 SAGE [arXiv 2602.10116](https://arxiv.org/abs/2602.10116)。
5. 场景与任务交替改进（闭环 ③）：EmbodiedSmith 让场景生成预判任务需求，任务生成反过来指导场景编辑 [arXiv 2610.07969](https://arxiv.org/abs/2610.07969)。
6. 外观与物理随机化 [arXiv 1703.06907](https://arxiv.org/abs/1703.06907)。
7. 评估生成质量：按质量、多样性、泛化三方面评估生成的仿真任务 [arXiv 2410.08172](https://arxiv.org/abs/2410.08172)。

## 4. 可以写成论文的方向

### 4.1 工艺约束驱动的车间布局与任务联合生成

- 类型：方法＋数据集
- 研究问题：给定工艺路线和设备清单，能否生成满足物流、可达和安全约束的车间场景，同时生成配套任务，并保证任务在仿真里可执行？
- 已有工作与空白：上面列出的场景生成方法以住宅和室内为主。HolidayFactory 生成工业场景变体，但其报告指出模型评审有局限，生成的评测也不一定准确反映任务要求 [arXiv 2611.11789](https://arxiv.org/abs/2611.11789)。
- 怎样验证：统计约束违反率和任务可执行率；用生成场景训练的策略在未见布局上的成功率；与人工布局比较物流距离和节拍。

### 4.2 带设备逻辑、可复位的车间场景数据集

- 类型：数据集／基准
- 研究问题：发布一批车间场景，每个场景带设备逻辑、快照复位接口和任务，供世界模型和多机器人研究使用。
- 已有工作与空白：RoboFactory 提供多具身智能体协作任务 [P13](../../papers/P13_RoboFactory_2503.16408v1.pdf)，RoboCasa 提供厨房场景与任务 [P11](../../papers/P11_RoboCasa_2406.02523v1.pdf)。本轮检索没有找到带 PLC 逻辑和工单的公开车间场景集。
- 怎样验证：场景数、设备类型数、任务数；几种基线方法在其上的结果。

## 5. 所在闭环

- ① 主动与反事实数据：W09·W10 找出误差大或不确定的状态 → W11 选状态，设计动作扰动 → W03·W04·W05 从快照复位，执行并记录 → 回训模型。OpenWAM 报告，加入反事实监督后前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)；Plan2Explore 用模型集成的分歧选择探索目标 [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)。
- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。
- ③ 场景—任务联合生成：W03 生成或编辑场景 → W05 生成任务与示范 → W03·W05 统计失败、不可达与遮挡原因 → 按原因编辑场景。EmbodiedSmith 让场景生成预判任务需求、任务生成反过来指导场景编辑，二者交替改进 [arXiv 2610.07969](https://arxiv.org/abs/2610.07969)；生成任务的质量、多样性和泛化可按 [arXiv 2410.08172](https://arxiv.org/abs/2410.08172) 评估。

## 6. 对应的链路

- [L1](../../链路/L1_STEP资产化与物理仿真/README.md)：L1 STEP 资产化＋物理仿真作为世界模型
- [L2](../../链路/L2_扫描配准与数字孪生/README.md)：L2 扫描配准到 STEP 资产，并校准成数字孪生
- [L3](../../链路/L3_扫描单体化生成资产/README.md)：L3 没有 STEP 的设备：扫描单体化后生成资产
- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件

## 7. 高价值参考文献

### 室内场景生成（方法可迁移）

- **ProcTHOR: Large-Scale Embodied AI Using Procedural Generation**（2022），[arXiv 2206.06994](https://arxiv.org/abs/2206.06994)：ProcTHOR：程序化生成大量可交互房屋。
- **Holodeck: Language Guided Generation of 3D Embodied AI Environments**（2023），[arXiv 2312.09067](https://arxiv.org/abs/2312.09067)：Holodeck：用语言生成三维具身环境。
- **Infinite Photorealistic Worlds using Procedural Generation**（2023），[arXiv 2306.09310](https://arxiv.org/abs/2306.09310)：Infinigen：程序化生成照片级自然场景。
- **Infinigen Indoors: Photorealistic Indoor Scenes using Procedural Generation**（2024），[arXiv 2406.11824](https://arxiv.org/abs/2406.11824)：Infinigen Indoors：程序化生成室内场景，带约束求解。
- **PhyScene: Physically Interactable 3D Scene Synthesis for Embodied AI**（2024），[arXiv 2404.09465](https://arxiv.org/abs/2404.09465)：PhyScene：可物理交互的三维场景合成。
- **SceneFoundry: Generating Interactive Infinite 3D Worlds**（2026），[arXiv 2601.05810](https://arxiv.org/abs/2601.05810)：SceneFoundry：语言引导的扩散框架，生成带可动家具的公寓级场景，并保证可行走空间。
- **InternScenes: A Large-scale Simulatable Indoor Scene Dataset with Realistic Layouts**（2025），[arXiv 2509.10813](https://arxiv.org/abs/2509.10813)：InternScenes：约 4 万个可仿真室内场景、196 万个物体。
- **EmbodiedGen: Towards a Generative 3D World Engine for Embodied Intelligence**（2025），[arXiv 2506.10600](https://arxiv.org/abs/2506.10600)：EmbodiedGen：面向具身智能的生成式三维世界引擎。

### 布局生成与面向任务的环境生成

- **LayoutGPT: Compositional Visual Planning and Generation with Large Language Models**（2023），[arXiv 2305.15393](https://arxiv.org/abs/2305.15393)：LayoutGPT：用 LLM 做组合式布局规划。
- **RoboLayout: Differentiable 3D Scene Generation for Embodied Agents**（2026），[arXiv 2603.05522](https://arxiv.org/abs/2603.05522)：RoboLayout：可微的三维场景布局生成，考虑智能体。
- **SAGE: Scalable Agentic 3D Scene Generation for Embodied AI**（2026），[arXiv 2602.10116](https://arxiv.org/abs/2602.10116)：SAGE：给定具身任务，智能体式地生成可仿真环境。

### 任务与场景联合生成

- **GenSim: Generating Robotic Simulation Tasks via Large Language Models**（2023），[arXiv 2310.01361](https://arxiv.org/abs/2310.01361)：GenSim：用 LLM 生成仿真任务。
- **GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs**（2024），[arXiv 2410.03645](https://arxiv.org/abs/2410.03645)：GenSim2：用多模态与推理 LLM 扩大机器人数据生成。
- **RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation**（2023），[arXiv 2311.01455](https://arxiv.org/abs/2311.01455)：RoboGen：生成式仿真，自动提出任务、场景和训练方式。
- **EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation**（2026），[arXiv 2610.07969](https://arxiv.org/abs/2610.07969)：EmbodiedSmith：资产、场景、任务统一生成，场景与任务交替改进。
- **On the Evaluation of Generative Robotic Simulations**（2024），[arXiv 2410.08172](https://arxiv.org/abs/2410.08172)：生成式机器人仿真的评估框架：质量、多样性、泛化。

### 工业场景

- **HolidayFactory 1.0: Simulating, Generating, and Evaluating Industrial Robot Tasks**（2026），[arXiv 2611.11789](https://arxiv.org/abs/2611.11789)：HolidayFactory：工业场景与评测的生成，以及不复位的 24/7-Bench。
- **IndustryEQA: Pushing the Frontiers of Embodied Question Answering in Industrial Scenarios**（2025），[arXiv 2505.20640](https://arxiv.org/abs/2505.20640)：IndustryEQA：仓储场景的具身问答基准，含有人和无人场景。
- **RoboFactory: Exploring Embodied Agent Collaboration with Compositional Constraints**（2025），[P13 本地 PDF](../../papers/P13_RoboFactory_2503.16408v1.pdf)：RoboFactory：用逻辑、空间、时间组合约束组织多智能体协作。

### 随机化

- **Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World**（2017），[arXiv 1703.06907](https://arxiv.org/abs/1703.06907)：域随机化：随机化渲染以迁移到真实。

## 8. 参考项目

- [allenai/procthor](https://github.com/allenai/procthor)：ProcTHOR
- [allenai/Holodeck](https://github.com/allenai/Holodeck)：Holodeck
- [princeton-vl/infinigen](https://github.com/princeton-vl/infinigen)：Infinigen 与 Infinigen Indoors
- [PhyScene/PhyScene](https://github.com/PhyScene/PhyScene)：PhyScene
- [HorizonRobotics/EmbodiedGen](https://github.com/HorizonRobotics/EmbodiedGen)：EmbodiedGen
- [Genesis-Embodied-AI/RoboGen](https://github.com/Genesis-Embodied-AI/RoboGen)：RoboGen
- [liruiw/GenSim](https://github.com/liruiw/GenSim)：GenSim
- [UCSB-AI/LayoutGPT](https://github.com/UCSB-AI/LayoutGPT)：LayoutGPT

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
