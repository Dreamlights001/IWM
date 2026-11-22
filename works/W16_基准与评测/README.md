# W16 基准与评测

> 阶段：S4 安全校核与评测　·　总看板：[research_board.html](../research_board.html#W16)

定义分层的评测指标和长时、不复位的评测方式，用同一套缩小版工厂比较各条链路和方法。评测协议从 S0 开始写。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md)：评测协议草案<br>[W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：待评测模型<br>[W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：待评测模型<br>[W12（子级技能与端口）](../W12_子级技能与端口/README.md)：待评测技能<br>[W13（多机器人协作）](../W13_多机器人协作/README.md)：待评测方法<br>[W14（整厂规划与调度）](../W14_整厂规划与调度/README.md)：待评测策略 | [W17（部署与数据飞轮）](../W17_部署与数据飞轮/README.md)：验收结果 | ⑥ 评测—部署飞轮 |

## 1. 为什么要做

现有基准分三类：世界模型基准（World-in-World [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)、WorldScore [arXiv 2504.00983](https://arxiv.org/abs/2504.00983)、WorldModelBench [P41](../../papers/P41_WorldModelBench_2502.20694v1.pdf)、Physics-IQ [arXiv 2501.09038](https://arxiv.org/abs/2501.09038)）；机器人操作基准（LIBERO [arXiv 2306.03310](https://arxiv.org/abs/2306.03310)、BEHAVIOR-1K [arXiv 2403.09227](https://arxiv.org/abs/2403.09227)、CALVIN [arXiv 2112.03227](https://arxiv.org/abs/2112.03227)、RoboCasa [P11](../../papers/P11_RoboCasa_2406.02523v1.pdf)、RoboTwin 2.0 [arXiv 2506.18088](https://arxiv.org/abs/2506.18088)）；工业任务基准（NIST 装配任务板 [arXiv 2103.05140](https://arxiv.org/abs/2103.05140)、IndustReal [P97](../../papers/P97_IndustReal_2305.17110v1.pdf)、AlphaNIST [arXiv 2610.13354](https://arxiv.org/abs/2610.13354)、RoCo Challenge [arXiv 2603.15469](https://arxiv.org/abs/2603.15469)、HolidayFactory 的 24/7-Bench [arXiv 2611.11789](https://arxiv.org/abs/2611.11789)）。World-in-World 发现，视觉质量本身不保证任务成功，可控性更重要 [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)。本轮检索没有找到覆盖整厂层预测和决策的基准。

## 2. 输入与产物

**输入**

- [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的评测协议草案
- [W03（车间场景生成）](../W03_车间场景生成/README.md) 的场景
- [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的事件日志
- 各工作的模型与策略

**产物**

- 分层基准：工位预测、整厂预测、子级技能、多机器人协作、整厂决策
- 长时、不复位的运行协议
- 评测脚本与结果表

## 3. 具体工作

1. 分层指标：几何与外观误差；设备状态准确率；事件时间误差；技能成功率与耗时；整厂吞吐、在制品、平均等待、死锁次数。
2. 同初态不同动作的对照试验，见 report.html“怎样判断它已经是世界模型”一节。
3. 长时、不复位评测：参考 24/7-Bench 统计已完成、失败、未完成的工单，以及吞吐、时延和电机能耗 [arXiv 2611.11789](https://arxiv.org/abs/2611.11789)。
4. 闭环评测世界模型：World-in-World [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)。用世界模型评估策略：微调后的 Veo 作为 Gemini Robotics 策略的评估仿真器 [P73](../../papers/P73_Veo_Robot_Policy_Evaluation_2512.10675v2.pdf)。分布式真实评测：RoboArena [arXiv 2506.18123](https://arxiv.org/abs/2506.18123)。
5. 检验仿真评测与真实结果的相关性：SimplerEnv [arXiv 2405.05941](https://arxiv.org/abs/2405.05941)。
6. 统计：多随机种子与置信区间。整厂收益要长时间运行才看得出（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 风险一节）。
7. 任务涉及形变、加工时，加入物理真实性测试，参考 GaussianBench [P49](../../papers/P49_GaussianBench_2610.10554v1.pdf) 和 [形变专题](../../链路/专题_形变流体断裂与加工/README.md)。

## 4. 可以写成论文的方向

### 4.1 工厂级世界模型基准

- 类型：基准
- 研究问题：在同一套缩小版工厂上，分层评测工位预测、整厂预测、技能、协作和调度，并给出各条链路的基线。
- 已有工作与空白：上述基准各自覆盖一层；HolidayFactory 的作者说明，他们用脚本轨迹评估了工单级指标，但尚未在持续运行中比较策略 [arXiv 2611.11789](https://arxiv.org/abs/2611.11789)。
- 怎样验证：基准被多种方法使用；分析各层指标之间的相关性。

### 4.2 世界模型作为工厂策略的评估器

- 类型：实证
- 研究问题：用工位层或整厂层世界模型评估策略，得到的排名能否与真实或高保真仿真一致？
- 已有工作与空白：Veo 世界模拟器被用来评估 Gemini Robotics 策略 [P73](../../papers/P73_Veo_Robot_Policy_Evaluation_2512.10675v2.pdf)；SimplerEnv 验证了仿真评估与真实结果的相关性 [arXiv 2405.05941](https://arxiv.org/abs/2405.05941)。工厂任务上还没有对应研究（分析判断）。
- 怎样验证：排名相关系数；评估成本对比。

## 5. 所在闭环

- ⑥ 评测—部署飞轮：W16 评测，找出失败模式 → W17 部署，记录失败与人工干预 → W07·W04 采集真实片段与事件日志 → W11·W05 生成反事实与针对性数据 → 回训后再评测。Fleet-DAgger 研究多台机器人共享少量人工监督 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人上做车队级离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 6. 对应的链路

- [L1](../../链路/L1_STEP资产化与物理仿真/README.md)：L1 STEP 资产化＋物理仿真作为世界模型
- [L2](../../链路/L2_扫描配准与数字孪生/README.md)：L2 扫描配准到 STEP 资产，并校准成数字孪生
- [L3](../../链路/L3_扫描单体化生成资产/README.md)：L3 没有 STEP 的设备：扫描单体化后生成资产
- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L7](../../链路/L7_三维动作条件动力学/README.md)：L7 扫描场景中的三维动作条件动力学
- [L8](../../链路/L8_JEPA特征空间世界模型/README.md)：L8 JEPA 特征空间世界模型
- [L9](../../链路/L9_潜变量模型式强化学习/README.md)：L9 潜变量模型式强化学习
- [L10](../../链路/L10_视频世界模型/README.md)：L10 视频世界模型：合成数据与策略评估
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）
- [形变专题](../../链路/专题_形变流体断裂与加工/README.md)：专题：形变、流体、断裂与加工

## 7. 高价值参考文献

### 世界模型评测

- **World-in-World: World Models in a Closed-Loop World**（2025），[arXiv 2510.18135](https://arxiv.org/abs/2510.18135)：World-in-World：在闭环中评测世界模型。
- **WorldScore: A Unified Evaluation Benchmark for World Generation**（2025），[arXiv 2504.00983](https://arxiv.org/abs/2504.00983)：WorldScore：世界生成的统一评测。
- **WorldModelBench: Judging Video Generation Models As World Models**（2025），[P41 本地 PDF](../../papers/P41_WorldModelBench_2502.20694v1.pdf)：WorldModelBench：把视频生成模型当作世界模型来评判。
- **Do generative video models understand physical principles?**（2025），[arXiv 2501.09038](https://arxiv.org/abs/2501.09038)：Physics-IQ：视频生成模型是否理解物理原理。
- **GaussianBench: Physics-Fidelity Evaluation for Gaussian Scene Representations**（2026），[P49 本地 PDF](../../papers/P49_GaussianBench_2610.10554v1.pdf)：GaussianBench：高斯场景表示的物理真实性评测。
- **Do Robotic World Models Really Follow Actions? Diagnosing and Aligning Action-Conditioned Generation for Policy Learning**（2026），[P77 本地 PDF](../../papers/P77_WorldEcho_2608.24885v2.pdf)：WorldEcho：动作遵循性诊断。

### 机器人操作基准

- **LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning**（2023），[arXiv 2306.03310](https://arxiv.org/abs/2306.03310)：LIBERO：终身机器人学习基准。
- **BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation**（2024），[arXiv 2403.09227](https://arxiv.org/abs/2403.09227)：BEHAVIOR-1K：1000 个日常活动。
- **CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks**（2021），[arXiv 2112.03227](https://arxiv.org/abs/2112.03227)：CALVIN：语言条件的长时程操作。
- **RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots**（2024），[P11 本地 PDF](../../papers/P11_RoboCasa_2406.02523v1.pdf)：RoboCasa：日常任务的大规模仿真。
- **RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots**（2026），[P12 本地 PDF](../../papers/P12_RoboCasa365_2603.04356v1.pdf)：RoboCasa365：扩展任务与泛化评测。
- **RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation**（2025），[arXiv 2506.18088](https://arxiv.org/abs/2506.18088)：RoboTwin 2.0：双臂操作的数据生成与基准。
- **RoboVerse: Towards a Unified Platform, Dataset and Benchmark for Scalable and Generalizable Robot Learning**（2025），[arXiv 2504.18904](https://arxiv.org/abs/2504.18904)：RoboVerse：统一平台与基准。
- **RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies**（2025），[arXiv 2506.18123](https://arxiv.org/abs/2506.18123)：RoboArena：分布式真实世界策略评测。
- **HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation**（2024），[arXiv 2403.10506](https://arxiv.org/abs/2403.10506)：HumanoidBench：人形基准。

### 工业任务与装配

- **Benchmarking Off-The-Shelf Solutions to Robotic Assembly Tasks**（2021），[arXiv 2103.05140](https://arxiv.org/abs/2103.05140)：NIST 装配任务板上的现成方案评测。
- **Robust Multi-Modal Policies for Industrial Assembly via Reinforcement Learning and Demonstrations: A Large-Scale Study**（2021），[arXiv 2103.11512](https://arxiv.org/abs/2103.11512)：工业装配的大规模 RL＋示范研究。
- **Factory: Fast Contact for Robotic Assembly**（2022），[arXiv 2205.03532](https://arxiv.org/abs/2205.03532)：Factory：装配任务的快速接触仿真。
- **AutoMate: Specialist and Generalist Assembly Policies over Diverse Geometries**（2024），[arXiv 2407.08028](https://arxiv.org/abs/2407.08028)：AutoMate：多种几何的装配策略。
- **ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility**（2023），[arXiv 2309.16909](https://arxiv.org/abs/2309.16909)：ASAP：考虑物理可行性的装配序列规划。
- **IndustReal: Transferring Contact-Rich Assembly Tasks from Simulation to Reality**（2023），[P97 本地 PDF](../../papers/P97_IndustReal_2305.17110v1.pdf)：IndustReal：接触密集装配从仿真到真实。
- **AlphaNIST: Emergent Assembly Skills from Binary Task Rewards**（2026），[arXiv 2610.13354](https://arxiv.org/abs/2610.13354)：AlphaNIST：只用二值任务奖励，单一策略在仿真中学会任务板上全部 20 个装配任务。
- **RoCo Challenge at AAAI 2026: Benchmarking Robotic Collaborative Manipulation for Assembly Towards Industrial Automation**（2026），[arXiv 2603.15469](https://arxiv.org/abs/2603.15469)：RoCo Challenge：面向工业装配的协作操作基准。
- **HolidayFactory 1.0: Simulating, Generating, and Evaluating Industrial Robot Tasks**（2026），[arXiv 2611.11789](https://arxiv.org/abs/2611.11789)：HolidayFactory：24/7-Bench，7 个工业任务，不复位评测。
- **IndustryEQA: Pushing the Frontiers of Embodied Question Answering in Industrial Scenarios**（2025），[arXiv 2505.20640](https://arxiv.org/abs/2505.20640)：IndustryEQA：仓储场景的具身问答。
- **IndustryAssetEQA: A Neurosymbolic Operational Intelligence System for Embodied Question Answering in Industrial Asset Maintenance**（2026），[arXiv 2604.23446](https://arxiv.org/abs/2604.23446)：IndustryAssetEQA：工业资产维护中的具身问答。

### 用模型评估策略

- **Evaluating Gemini Robotics Policies in a Veo World Simulator**（2025），[P73 本地 PDF](../../papers/P73_Veo_Robot_Policy_Evaluation_2512.10675v2.pdf)：用 Veo 世界模拟器评估 Gemini Robotics 策略。
- **Evaluating Real-World Robot Manipulation Policies in Simulation**（2024），[arXiv 2405.05941](https://arxiv.org/abs/2405.05941)：SimplerEnv：仿真评测与真实结果的相关性。

## 8. 参考项目

- [Lifelong-Robot-Learning/LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)：LIBERO
- [StanfordVL/BEHAVIOR-1K](https://github.com/StanfordVL/BEHAVIOR-1K)：BEHAVIOR-1K
- [mees/calvin](https://github.com/mees/calvin)：CALVIN
- [robocasa/robocasa](https://github.com/robocasa/robocasa)：RoboCasa
- [NVlabs/industreallib](https://github.com/NVlabs/industreallib)：IndustReal 的真实机器人库
- [HaoranZhangumich/Awesome-Robotic-Benchmarks](https://github.com/HaoranZhangumich/Awesome-Robotic-Benchmarks)：机器人基准列表

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
