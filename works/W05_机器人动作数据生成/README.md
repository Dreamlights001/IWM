# W05 机器人动作数据生成

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W05)

用少量示范加自动生成，得到上下料、装夹、检测、搬运等工厂任务的大规模机器人示范和转移数据。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W03（车间场景生成）](../W03_车间场景生成/README.md)：可复位场景与任务 | [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：仿真示范与转移<br>[W12（子级技能与端口）](../W12_子级技能与端口/README.md)：示范数据 | ① 主动与反事实数据<br>② 仿真—真实校准<br>③ 场景—任务联合生成<br>⑥ 评测—部署飞轮 |

## 1. 为什么要做

DROID [arXiv 2403.12945](https://arxiv.org/abs/2403.12945)、Open X-Embodiment [arXiv 2310.08864](https://arxiv.org/abs/2310.08864) 等大规模数据集的场景以家庭、办公和实验室为主，很少有机床上下料、装夹这类任务（按其任务描述判断），工厂任务需要自己造数据。MimicGen 从约 200 条人工示范生成 18 个任务的 5 万多条示范 [arXiv 2310.17596](https://arxiv.org/abs/2310.17596)，这类“少量示范＋自动扩增”的方法是主要手段。

## 2. 输入与产物

**输入**

- [W03（车间场景生成）](../W03_车间场景生成/README.md) 的可复位场景与任务
- 仿真遥操作或脚本得到的少量源示范
- [W06（全身动作数据）](../W06_全身动作数据/README.md) 的全身动作（机器人是人形时）
- 运动规划器

**产物**

- 每个任务的示范数据：观测、动作、设备状态、事件
- 失败与恢复数据
- 同初态、不同动作的转移（供 [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)、[W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)）

## 3. 具体工作

1. 每个任务采集少量源示范（仿真中遥操作或写脚本），按物体中心的子任务切分。
2. 用 MimicGen 类方法扩增：SkillMimicGen（技能分段加运动规划）[arXiv 2410.18907](https://arxiv.org/abs/2410.18907)；DexMimicGen（双臂灵巧手）[arXiv 2410.24185](https://arxiv.org/abs/2410.24185)；MoMaGen（双臂移动操作，处理底座放置的可达性和主动相机的可见性）[arXiv 2510.18316](https://arxiv.org/abs/2510.18316)；ScheduleGen（多臂技能调度，28 个仿真任务变体上数据生成成功率 79.6%）[arXiv 2610.39429](https://arxiv.org/abs/2610.39429)。
3. 少用或不用仿真器的扩增：DemoGen 在点云上编辑示范 [arXiv 2502.16932](https://arxiv.org/abs/2502.16932)；MOMASPLAT 用三维重建从未见过的底座位姿合成移动操作示范 [arXiv 2611.08372](https://arxiv.org/abs/2611.08372)；WANDA 从一条示范出发，在由照片生成的三维世界上合成轨迹 [arXiv 2607.13154](https://arxiv.org/abs/2607.13154)。
4. 用规划器和 LLM 生成：cuRobo 并行运动规划 [arXiv 2310.17274](https://arxiv.org/abs/2310.17274)；Code as Policies [arXiv 2209.07753](https://arxiv.org/abs/2209.07753)；Scaling Up and Distilling Down 用 LLM 做高层规划、采样式规划器生成数据，再蒸馏成多任务策略 [arXiv 2307.14535](https://arxiv.org/abs/2307.14535)。
5. 用强化学习生成：Eureka 用 LLM 写奖励函数 [arXiv 2310.12931](https://arxiv.org/abs/2310.12931)；RLDG 用 RL 专家生成的数据训练通用策略 [arXiv 2412.09858](https://arxiv.org/abs/2412.09858)。
6. 每条轨迹都记录设备状态和事件（门开、夹紧、完工），按 [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的格式存储。
7. 估算数据量：真实数据上，策略的泛化性能与环境数、物体数大致成幂律 [arXiv 2410.18647](https://arxiv.org/abs/2410.18647)，可据此估算需要多少场景变体。

## 4. 可以写成论文的方向

### 4.1 带设备状态前置条件的长时程示范生成

- 类型：方法
- 研究问题：上下料等任务依赖设备状态（门已开、夹具松开、主轴停止）。能否让数据生成方法显式处理这些前置条件，并生成跨多个工位的长时程示范？
- 已有工作与空白：MimicGen 系列按物体中心的子任务切分并变换示范 [arXiv 2310.17596](https://arxiv.org/abs/2310.17596) [arXiv 2410.18907](https://arxiv.org/abs/2410.18907)；MoMaGen 处理底座可达和相机可见性约束 [arXiv 2510.18316](https://arxiv.org/abs/2510.18316)。这些约束都是几何的，与 PLC 状态的时序约束结合是可做的方向（分析判断）。
- 怎样验证：在 [W03（车间场景生成）](../W03_车间场景生成/README.md) 的车间场景中比较数据生成成功率，以及用生成数据训练的策略成功率；与只用几何约束的生成方法对比。

### 4.2 工厂任务的机器人示范数据集与数据量规律

- 类型：数据集＋实证
- 研究问题：用生成方法构建上下料、装夹、检测、搬运的大规模数据集，并测量策略性能随场景变体数、物体数和示范数的变化。
- 已有工作与空白：数据缩放规律目前在日常物体的操作任务上测量 [arXiv 2410.18647](https://arxiv.org/abs/2410.18647)，工厂任务上的规律还没有人测（分析判断）。
- 怎样验证：发布数据集；给出缩放曲线和仿真—真实对照（借助 [W08（仿真—真实对齐）](../W08_仿真真实对齐/README.md)）。

### 4.3 多机器人协同示范生成

- 类型：方法（与 W13 衔接）
- 研究问题：多台机器人共用工位或交接工件时，怎样生成时间上协调的示范？
- 已有工作与空白：ScheduleGen 用技能调度为多臂任务生成示范 [arXiv 2610.39429](https://arxiv.org/abs/2610.39429)，RoboFactory 用组合约束组织多智能体数据生成 [P13](../../papers/P13_RoboFactory_2503.16408v1.pdf)；机械臂、AGV、人形之间的交接还很少涉及（分析判断）。
- 怎样验证：生成成功率；训练出的协作策略成功率；与逐台独立生成对比。

## 5. 所在闭环

- ① 主动与反事实数据：W09·W10 找出误差大或不确定的状态 → W11 选状态，设计动作扰动 → W03·W04·W05 从快照复位，执行并记录 → 回训模型。OpenWAM 报告，加入反事实监督后前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)；Plan2Explore 用模型集成的分歧选择探索目标 [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)。
- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。
- ③ 场景—任务联合生成：W03 生成或编辑场景 → W05 生成任务与示范 → W03·W05 统计失败、不可达与遮挡原因 → 按原因编辑场景。EmbodiedSmith 让场景生成预判任务需求、任务生成反过来指导场景编辑，二者交替改进 [arXiv 2610.07969](https://arxiv.org/abs/2610.07969)；生成任务的质量、多样性和泛化可按 [arXiv 2410.08172](https://arxiv.org/abs/2410.08172) 评估。
- ⑥ 评测—部署飞轮：W16 评测，找出失败模式 → W17 部署，记录失败与人工干预 → W07·W04 采集真实片段与事件日志 → W11·W05 生成反事实与针对性数据 → 回训后再评测。Fleet-DAgger 研究多台机器人共享少量人工监督 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人上做车队级离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 6. 对应的链路

- [L1](../../链路/L1_STEP资产化与物理仿真/README.md)：L1 STEP 资产化＋物理仿真作为世界模型
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L10](../../链路/L10_视频世界模型/README.md)：L10 视频世界模型：合成数据与策略评估

## 7. 算力

- DreamGen 用视频世界模型生成 24 万条 RoboCasa 样本，用了 1500 张 L40 约 54 小时 [P65](../../papers/P65_DreamGen_2505.12705v2.pdf)，按本项目的算力不可行。
- MimicGen 在 robosuite（MuJoCo）中回放变换后的示范，开销主要是仿真时间，可以在多张 3090／4090 和 CPU 上并行。

## 8. 高价值参考文献

### 少量示范的自动扩增

- **MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations**（2023），[arXiv 2310.17596](https://arxiv.org/abs/2310.17596)：MimicGen：约 200 条人工示范生成 18 个任务的 5 万多条示范。
- **SkillMimicGen: Automated Demonstration Generation for Efficient Skill Learning and Deployment**（2024），[arXiv 2410.18907](https://arxiv.org/abs/2410.18907)：SkillMimicGen：按技能分段，接运动规划。
- **DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning**（2024），[arXiv 2410.24185](https://arxiv.org/abs/2410.24185)：DexMimicGen：双臂灵巧操作的数据生成。
- **MoMaGen: Generating Demonstrations under Soft and Hard Constraints for Multi-Step Bimanual Mobile Manipulation**（2025），[arXiv 2510.18316](https://arxiv.org/abs/2510.18316)：MoMaGen：多步双臂移动操作，处理软硬约束。
- **ScheduleGen: Demonstration Generation via Skill Scheduling for Multi-Arm Imitation Learning**（2026），[arXiv 2610.39429](https://arxiv.org/abs/2610.39429)：ScheduleGen：多臂技能调度式示范生成，28 个任务变体。
- **DemoGen: Synthetic Demonstration Generation for Data-Efficient Visuomotor Policy Learning**（2025），[arXiv 2502.16932](https://arxiv.org/abs/2502.16932)：DemoGen：点云编辑合成示范，几乎不需仿真。
- **MOMASPLAT: Dynamic Novel-View Demonstration Augmentation for Mobile Manipulation**（2026），[arXiv 2611.08372](https://arxiv.org/abs/2611.08372)：MOMASPLAT：为移动操作合成新视角、新底座位姿的示范。
- **Worlds in One Demo: A Synthetic Data Engine for Learning Open-World Mobile Manipulation**（2026），[arXiv 2607.13154](https://arxiv.org/abs/2607.13154)：WANDA：一条示范＋生成的三维世界，合成移动操作数据。

### 仿真数据平台与双臂数据

- **RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins (early version)**（2024），[arXiv 2409.02920](https://arxiv.org/abs/2409.02920)：RoboTwin：生成式数字孪生的双臂基准。
- **RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation**（2025），[arXiv 2506.18088](https://arxiv.org/abs/2506.18088)：RoboTwin 2.0：731 个物体实例的物体库，带强域随机化的双臂数据生成。
- **RoboVerse: Towards a Unified Platform, Dataset and Benchmark for Scalable and Generalizable Robot Learning**（2025），[arXiv 2504.18904](https://arxiv.org/abs/2504.18904)：RoboVerse：统一的仿真平台、合成数据集与基准。

### 用规划器、LLM 或 RL 生成

- **cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation**（2023），[arXiv 2310.17274](https://arxiv.org/abs/2310.17274)：cuRobo：GPU 并行的无碰撞运动生成。
- **Code as Policies: Language Model Programs for Embodied Control**（2022），[arXiv 2209.07753](https://arxiv.org/abs/2209.07753)：Code as Policies：LLM 写控制代码。
- **Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition**（2023），[arXiv 2307.14535](https://arxiv.org/abs/2307.14535)：Scaling Up and Distilling Down：LLM 规划生成数据，再蒸馏成策略。
- **Eureka: Human-Level Reward Design via Coding Large Language Models**（2023），[arXiv 2310.12931](https://arxiv.org/abs/2310.12931)：Eureka：LLM 写奖励函数。
- **RLDG: Robotic Generalist Policy Distillation via Reinforcement Learning**（2024），[arXiv 2412.09858](https://arxiv.org/abs/2412.09858)：RLDG：用 RL 专家数据训练通用策略。

### 视频模型生成数据与数据量

- **DreamGen: Unlocking Generalization in Robot Learning through Video World Models**（2025），[P65 本地 PDF](../../papers/P65_DreamGen_2505.12705v2.pdf)：DreamGen：用视频世界模型生成“神经轨迹”，再补出动作。
- **Data Scaling Laws in Imitation Learning for Robotic Manipulation**（2024），[arXiv 2410.18647](https://arxiv.org/abs/2410.18647)：模仿学习的数据缩放规律：泛化与环境数、物体数大致成幂律。

## 9. 参考项目

- [NVlabs/mimicgen](https://github.com/NVlabs/mimicgen)：MimicGen
- [NVlabs/dexmimicgen](https://github.com/NVlabs/dexmimicgen)：DexMimicGen
- [RoboTwin-Platform/RoboTwin](https://github.com/RoboTwin-Platform/RoboTwin)：RoboTwin 与 RoboTwin 2.0
- [TEA-Lab/DemoGen](https://github.com/TEA-Lab/DemoGen)：DemoGen
- [eureka-research/Eureka](https://github.com/eureka-research/Eureka)：Eureka
- [RoboVerseOrg/RoboVerse](https://github.com/RoboVerseOrg/RoboVerse)：RoboVerse
- [NVlabs/curobo](https://github.com/NVlabs/curobo)：cuRobo
- [Fanqi-Lin/Data-Scaling-Laws](https://github.com/Fanqi-Lin/Data-Scaling-Laws)：数据缩放规律实验代码

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
