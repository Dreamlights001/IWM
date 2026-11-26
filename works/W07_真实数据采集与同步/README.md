# W07 真实数据采集与同步

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W07)

在真实工位上采集机器人示范、传感器流、PLC 信号和工单事件，统一时钟，用于校准和混合训练。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md)：数据记录格式 | [W08（仿真—真实对齐）](../W08_仿真真实对齐/README.md)：真实轨迹与日志<br>[W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：真实数据 | ② 仿真—真实校准<br>⑥ 评测—部署飞轮 |

## 1. 为什么要做

只用仿真数据训练的模型会继承仿真偏差：只用仿真数据预训练的 PointWorld 不能零样本泛化到真实场景，混入真实数据后才行 [P44](../../papers/P44_PointWorld_2601.03782v1.pdf)。工厂里采集真实数据还受安全、停产时间和保密的限制，所以采集方式要低成本、少打扰生产。真实数据不一定要很多：数据缩放研究中，4 名采集员一个下午采集的数据，就让两个任务在新环境、新物体上达到约 90% 成功率 [arXiv 2410.18647](https://arxiv.org/abs/2410.18647)。

## 2. 输入与产物

**输入**

- [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的数据格式
- 遥操作设备
- 相机、力传感器
- PLC／NC 信号接口
- MES 或工单记录

**产物**

- 时间同步的多模态数据：视频、关节、力、PLC 信号、事件
- 采集规范与工具
- 标注：任务分段、失败原因、人工干预（供 [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)、[W17（部署与数据飞轮）](../W17_部署与数据飞轮/README.md)）

## 3. 具体工作

1. 选遥操作方式：ALOHA 与 Mobile ALOHA [arXiv 2304.13705](https://arxiv.org/abs/2304.13705) [arXiv 2401.02117](https://arxiv.org/abs/2401.02117)、GELLO [arXiv 2309.13037](https://arxiv.org/abs/2309.13037)、UMI 手持夹爪 [arXiv 2402.10329](https://arxiv.org/abs/2402.10329)，视觉遥操作 AnyTeleop [arXiv 2307.04577](https://arxiv.org/abs/2307.04577) 和 Open-TeleVision [arXiv 2407.01512](https://arxiv.org/abs/2407.01512)。
2. 多臂和多机器人采集：HATS 让一名操作员在 MLLM 智能体协助下采集多臂数据 [arXiv 2606.16491](https://arxiv.org/abs/2606.16491)；GHOST 让一名操作员用 VR 同时遥操作两台移动操作机器人 [arXiv 2608.29080](https://arxiv.org/abs/2608.29080)；SAI 用单操作员的课程学习得到耦合的多机器人策略 [arXiv 2606.16490](https://arxiv.org/abs/2606.16490)。
3. 同步：机器人状态、相机、PLC 信号和工单事件统一时钟和 ID，并记录同步误差。
4. 存储：机器人部分用 LeRobot 数据格式，设备与工单事件按 [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的规范另存。
5. 标注失败和人工干预。
6. 参考已有数据集的采集与组织方式：DROID [arXiv 2403.12945](https://arxiv.org/abs/2403.12945)、Open X-Embodiment [arXiv 2310.08864](https://arxiv.org/abs/2310.08864)、AgiBot World（100 万条以上轨迹、217 个任务）[arXiv 2503.06669](https://arxiv.org/abs/2503.06669)、RH20T [arXiv 2307.00595](https://arxiv.org/abs/2307.00595)、BridgeData V2 [arXiv 2308.12952](https://arxiv.org/abs/2308.12952)。
7. 装配类任务参考：REASSEMBLE（围绕 NIST 装配任务板 1 的多模态装拆数据）[arXiv 2502.05086](https://arxiv.org/abs/2502.05086)、HA-ViD 人类装配视频 [arXiv 2307.05721](https://arxiv.org/abs/2307.05721)、IKEA ASM [arXiv 2007.00394](https://arxiv.org/abs/2007.00394)、FurnitureBench [arXiv 2305.12821](https://arxiv.org/abs/2305.12821)、RoCo Challenge 的协作装配数据 [arXiv 2603.15469](https://arxiv.org/abs/2603.15469)。

## 4. 可以写成论文的方向

### 4.1 带设备信号的多模态工厂操作数据集

- 类型：数据集
- 研究问题：采集上下料、装夹、检测任务的真实数据，同时记录视频、关节、力、PLC／NC 信号和工单事件，并报告同步误差。
- 已有工作与空白：上面列出的大规模数据集记录机器人和相机数据；REASSEMBLE 增加了力、音频等模态 [arXiv 2502.05086](https://arxiv.org/abs/2502.05086)。本轮检索没有找到同时含 PLC／NC 信号和工单事件的公开机器人数据集。
- 怎样验证：数据规模与同步误差；在 [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md) 和 [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md) 上的基线结果。

### 4.2 少打扰生产的工厂数据采集

- 类型：系统＋方法
- 研究问题：在不停产的条件下，怎样用最少的人工采到最有价值的数据，例如结合 [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md) 的主动选择？
- 已有工作与空白：HATS、GHOST 降低了多臂、多机器人遥操作的人力 [arXiv 2606.16491](https://arxiv.org/abs/2606.16491) [arXiv 2608.29080](https://arxiv.org/abs/2608.29080)；考虑停产成本的采集策略还很少研究（分析判断）。
- 怎样验证：单位人工时间带来的模型改进；对生产节拍的影响。

## 5. 所在闭环

- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。
- ⑥ 评测—部署飞轮：W16 评测，找出失败模式 → W17 部署，记录失败与人工干预 → W07·W04 采集真实片段与事件日志 → W11·W05 生成反事实与针对性数据 → 回训后再评测。Fleet-DAgger 研究多台机器人共享少量人工监督 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人上做车队级离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 6. 对应的链路

- [L2](../../链路/L2_扫描配准与数字孪生/README.md)：L2 扫描配准到 STEP 资产，并校准成数字孪生
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L7](../../链路/L7_三维动作条件动力学/README.md)：L7 扫描场景中的三维动作条件动力学
- [L8](../../链路/L8_JEPA特征空间世界模型/README.md)：L8 JEPA 特征空间世界模型

## 7. 高价值参考文献

### 遥操作与采集设备

- **Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware**（2023），[arXiv 2304.13705](https://arxiv.org/abs/2304.13705)：ALOHA：低成本双臂遥操作与 ACT。
- **Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation**（2024），[arXiv 2401.02117](https://arxiv.org/abs/2401.02117)：Mobile ALOHA：移动双臂遥操作。
- **GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators**（2023），[arXiv 2309.13037](https://arxiv.org/abs/2309.13037)：GELLO：低成本同构主手。
- **Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots**（2024），[arXiv 2402.10329](https://arxiv.org/abs/2402.10329)：UMI：手持夹爪采集，不需要机器人在场。
- **AnyTeleop: A General Vision-Based Dexterous Robot Arm-Hand Teleoperation System**（2023），[arXiv 2307.04577](https://arxiv.org/abs/2307.04577)：AnyTeleop：基于视觉的通用灵巧手遥操作。
- **Open-TeleVision: Teleoperation with Immersive Active Visual Feedback**（2024），[arXiv 2407.01512](https://arxiv.org/abs/2407.01512)：Open-TeleVision：沉浸式视觉遥操作。

### 多臂与多机器人采集

- **HATS: A Human-Agent Teleoperation System for Multi-Arm Data Collection**（2026），[arXiv 2606.16491](https://arxiv.org/abs/2606.16491)：HATS：单人加智能体协助的多臂数据采集。
- **GHOST in the Robots: Real-Time Exocentric Dual-Robot VR Teleoperation from Onboard Cameras**（2026），[arXiv 2608.29080](https://arxiv.org/abs/2608.29080)：GHOST：单人 VR 遥操作两台移动操作机器人。
- **Robots that Collaborate: Sequential Asymmetric Imitation for Learning Coupled Robot Policies**（2026），[arXiv 2606.16490](https://arxiv.org/abs/2606.16490)：SAI：不需要双人同步示范的耦合多机器人模仿学习。

### 大规模机器人数据集

- **DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset**（2024），[arXiv 2403.12945](https://arxiv.org/abs/2403.12945)：DROID：大规模真实场景操作数据。
- **Open X-Embodiment: Robotic Learning Datasets and RT-X Models**（2023），[arXiv 2310.08864](https://arxiv.org/abs/2310.08864)：Open X-Embodiment：多机构、多机器人数据汇总。
- **AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems**（2025），[arXiv 2503.06669](https://arxiv.org/abs/2503.06669)：AgiBot World：100 万条以上轨迹、217 个任务、五类部署场景。
- **RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot**（2023），[arXiv 2307.00595](https://arxiv.org/abs/2307.00595)：RH20T：多技能、多模态的接触操作数据。
- **BridgeData V2: A Dataset for Robot Learning at Scale**（2023），[arXiv 2308.12952](https://arxiv.org/abs/2308.12952)：BridgeData V2：可扩展的机器人学习数据。

### 装配与工业任务数据

- **REASSEMBLE: A Multimodal Dataset for Contact-rich Robotic Assembly and Disassembly**（2025），[arXiv 2502.05086](https://arxiv.org/abs/2502.05086)：REASSEMBLE：接触密集装拆的多模态数据。
- **HA-ViD: A Human Assembly Video Dataset for Comprehensive Assembly Knowledge Understanding**（2023），[arXiv 2307.05721](https://arxiv.org/abs/2307.05721)：HA-ViD：人类装配视频数据。
- **The IKEA ASM Dataset: Understanding People Assembling Furniture through Actions, Objects and Pose**（2020），[arXiv 2007.00394](https://arxiv.org/abs/2007.00394)：IKEA ASM：家具装配的多视角视频数据。
- **FurnitureBench: Reproducible Real-World Benchmark for Long-Horizon Complex Manipulation**（2023），[arXiv 2305.12821](https://arxiv.org/abs/2305.12821)：FurnitureBench：长时程家具装配的真实世界基准。
- **RoCo Challenge at AAAI 2026: Benchmarking Robotic Collaborative Manipulation for Assembly Towards Industrial Automation**（2026），[arXiv 2603.15469](https://arxiv.org/abs/2603.15469)：RoCo Challenge：面向工业装配的协作操作挑战赛与数据。
- **Benchmarking Off-The-Shelf Solutions to Robotic Assembly Tasks**（2021），[arXiv 2103.05140](https://arxiv.org/abs/2103.05140)：NIST 装配任务板上的现成方案评测。

### 数据量

- **Data Scaling Laws in Imitation Learning for Robotic Manipulation**（2024），[arXiv 2410.18647](https://arxiv.org/abs/2410.18647)：数据缩放规律与高效采集策略。

## 8. 参考项目

- [tonyzhaozh/aloha](https://github.com/tonyzhaozh/aloha)：ALOHA 硬件与软件
- [tonyzhaozh/act](https://github.com/tonyzhaozh/act)：ACT 策略
- [MarkFzp/mobile-aloha](https://github.com/MarkFzp/mobile-aloha)：Mobile ALOHA
- [real-stanford/universal_manipulation_interface](https://github.com/real-stanford/universal_manipulation_interface)：UMI
- [wuphilipp/gello_software](https://github.com/wuphilipp/gello_software)：GELLO
- [dexsuite/dex-retargeting](https://github.com/dexsuite/dex-retargeting)：人手到灵巧手的重定向
- [OpenTeleVision/TeleVision](https://github.com/OpenTeleVision/TeleVision)：Open-TeleVision
- [droid-dataset/droid](https://github.com/droid-dataset/droid)：DROID 采集平台
- [google-deepmind/open_x_embodiment](https://github.com/google-deepmind/open_x_embodiment)：Open X-Embodiment
- [OpenDriveLab/AgiBot-World](https://github.com/OpenDriveLab/AgiBot-World)：AgiBot World
- [huggingface/lerobot](https://github.com/huggingface/lerobot)：LeRobot：数据格式、采集与训练

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对，2026-11-27 补充）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
