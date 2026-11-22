# L11 工厂级世界动作模型（FWAM）

这是在 L1–L10 之上新增的一条链路：把各链路组织成"整厂层—工位层—机器人层"的分层结构，并在整厂层训练一个可预测、可规划的世界动作模型。概念与命名的讨论见 [00 总览](../00_总览_工厂级世界动作模型/README.md)。

## 1. 思考

### 1.1 整厂层的"动作"是什么

单机器人 WAM 的动作是关节量或末端位姿。整厂层的动作应当是**对子级的调用**，粒度与子级暴露的端口一致：

| 子级           | 端口（整厂层可发出的动作）                                                        | 子级返回的观测与事件              |
| ------------ | -------------------------------------------------------------------- | ----------------------- |
| 机器人（VLA＋WBC） | 技能调用，如 `pick(part_17, rack_A)`、`load(CNC_1)`、`goto(station_3)`；或目标位姿 | 技能开始、完成、失败及原因；当前位姿；夹爪状态 |
| 机床（PLC／NC）   | `cycle_start(program)`、`door_open`、`clamp` 等设备命令                     | 模式、互锁、报警、程序段、完工         |
| AGV／小车       | 目标点、路径约束、预约通道                                                        | 到达、阻塞、电量                |
| 工单与物料        | 派工、改路由、插单、换型                                                         | 工单状态、在制品、缓存占用           |

这和 VLA 与 WBC 的关系一样：WBC 向 VLA 暴露根速度或潜在动作，子级向整厂层暴露技能和设备命令。

### 1.2 整厂层的"状态"是什么

整厂状态不适合用像素表示：工厂太大，关键状态（PLC 模式、工单、质量）在画面里看不到。可以用**实体—关系图加事件流**：

- 节点：机器人、机床、工件、工单、缓存、通道段、工位；
- 节点属性：位姿、模式、电量、加工进度、剩余时间、故障标记等；
- 边：占用（机器人占用通道段）、装夹（工件在机床内）、隶属（工件属于工单）、相邻（通道连通）；
- 事件：技能开始与完成、设备完工、报警、到料。

需要细节时，再由工位层（L1、L2、L7、L8）提供几何或视觉预测，汇总成整厂层节点的属性，例如"上料预计耗时"和"成功概率"。加工时长、质量和报废概率由[专题：形变、流体、断裂与加工](../专题_形变流体断裂与加工/README.md)第 4 节的加工代理提供。

### 1.3 为什么这是 WAM，而不只是排产

- 传统排产（AWMP [P38] 这类）假设"上料一次要多久"是常数或分布，不关心机器人和设备实际做了什么。
- FWAM 预测的是**动作的后果**：派某台机器人去上料，它要走哪条路、会不会和另一台 AGV 抢通道、上料成功概率多少、机床什么时候真的启动。这些后果由子级的实际能力决定，所以整厂层要能"看到"子级。
- 这正是 WAM 的定义：联合预测未来状态与动作 [arXiv 2605.12090]，只是状态和动作都换成了整厂粒度。

### 1.4 三种可能的模型形态

| 形态         | 做法                                                      | 优点                 | 缺点                      |
| ---------- | ------------------------------------------------------- | ------------------ | ----------------------- |
| A 显式仿真＋规划器 | 用 L4 的离散事件仿真接 L1 的物理仿真作为转移函数，上面接搜索或规划算法                 | 可解释，可从快照复位，不需要大量数据 | 慢；每种子级行为都要建模            |
| B 学习式图世界模型 | 在实体图上训练图网络或 Transformer，预测下一时刻的节点属性与事件；动作作为输入；规划时在模型里搜索 | 快，可微，可批量评估大量候选     | 需要大量"状态—动作—结果"数据，主要来自 A |
| C 联合世界动作模型 | 在 B 的基础上增加动作头，同时输出未来状态和整厂层动作（与单机器人 WAM 同构）              | 推理时一次前向即可出动作       | 训练目标更难，需要好的示范或 RL       |

本目录不在三者中做选择。三者可以按阶段叠加：A 生成数据并做最终校核，B 做快速预测，C 做快速决策。

## 2. Idea

以下是可以作为研究点的想法，均未验证：

1. **端口化子级**：把每台机器人的"VLA＋WBC"和每台机床的"PLC＋物理"包装成统一接口，提供技能调用、状态查询和"预计耗时及成功率"的自报告。自报告可以来自子级自身的小世界模型（L8 或 L1 中的 MPC）。整厂层只读这些自报告，不需要看像素。这相当于把 HOVER 式的"统一命令端口"推广到整厂。
2. **事件驱动的图世界模型**：时间不按固定步长推进，而是按"下一个事件"推进，节省计算并对齐离散事件仿真的语义。DeepFleet 发现异步更新机器人状态、利用局部交互结构的模型（机器人中心与图—地面两种）表现最好 [arXiv 2508.08574]，可以作为参考。
3. **跨层一致性训练**：同一事件在整厂层和工位层都有预测，例如"CNC-1 在 t 时刻完工"。可以让两层的预测互相监督，减少层间不一致。
4. **反事实数据生成**：在 L4 数字孪生里，从同一快照出发，对派工、路由做大量扰动，生成"同初态、不同动作"的数据。这正是 WAM 学到动作因果所需要的，真实工厂日志几乎不含这种数据。OpenWAM 发现，加入反事实转移后，前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922]。
5. **用 MA-WAM 的方式做测试时规划**：先用一个轻量策略为整厂层提出 M 个候选联合动作，再用世界模型给每个候选打分，选分最高的执行。MA-WAM 在 RTX 3090 上，M=8 时生成加评分共 428 ms，其中评分只占 13.4 ms [arXiv 2609.31281]，这个开销在整厂层（分钟级决策）可以忽略。
6. **把 World Dreamer 的"共享世界状态"放大到车间**：World Dreamer v5-lite 把多台机器人的相机特征投影到共享的工作空间坐标中，每台机器人用一个查询读取 [arXiv 2610.37518]。车间层可以把每个工位的状态嵌入写到车间平面图的对应格子里，形成整厂的共享状态，每台机器人或设备用一个查询读取。

## 3. 实施路线（有限算力版）

假设算力：几张 RTX 3090／4090，加一两张 40 GB／80 GB 卡。下表是阶段性路线，每个阶段都有可检验的产物。

### 阶段 0：缩小版工厂与统一接口（约 1–2 个月，不训练模型）

- 选两台 CNC、一台机器人（你的 URDF）、一个料架、一个检测台。
- 用 L1 把 STEP 资产化，用 L2 把扫描配准进来，搭出数字孪生。
- 用 L4 把 PLC／NC 接进来；没有真实程序时，先写行为模型（状态机）。
- 定义整厂层接口：实体、事件、子级端口、自报告字段。可以参考 NIST CMSD [P99] 和 OPC UA for Machine Tools。
- 产物：能从快照复位、能注入派工动作、能记录事件的仿真环境；用 SimPy 或自写事件循环做离散事件层。

### 阶段 1：子级就位（约 1–2 个月，单卡可做）

- 机械臂：用 openpi 或 LeRobot 做 LoRA 微调。openpi 的 LoRA 微调需要 22.5 GB 以上显存，一张 RTX 4090 即可（openpi README）。也可用 SmolVLA。
- 腿式或人形下半身：用开源 WBC（HOVER、GMT 等）或在 MuJoCo Playground、Isaac Lab 里训练速度跟踪策略。MuJoCo Playground 在两块 RTX 4090 上训练 G1 平地行走不到 30 分钟 [arXiv 2502.08844]。
- AGV：Nav2 加通道预约。
- 产物：每个子级都能被整厂层用端口调用，并返回事件和自报告。

### 阶段 2：整厂层显式基线（形态 A）（约 1 个月）

- 在阶段 0 的仿真上，用规则派工、启发式和 MPC 或树搜索做整厂层决策。
- 记录大量轨迹：整厂状态图、动作、事件、吞吐、等待。
- 产物：基线指标，包括吞吐、在制品、平均等待、死锁次数；以及第一批训练数据。

### 阶段 3：学习式图世界模型（形态 B）（约 2 个月，1–2 张 4090）

- 输入：整厂状态图加候选动作。输出：下一个事件的类型和时间，以及各节点属性的变化。
- 结构：图 Transformer 或 GNN，参数量在 10M–100M。DeepFleet 的图—地面模型只有 13M 参数 [arXiv 2508.08574]，这个量级在一张 4090 上训练没有问题。
- 数据：阶段 2 的轨迹，加上 Idea 4 的反事实扰动。
- 验收：与显式仿真比较多步预测误差、事件时间误差，以及吞吐预测误差。
- 产物：一个比显式仿真快几个数量级的整厂预测器。

### 阶段 4：测试时规划与联合动作头（形态 C）（约 2 个月）

- 先做测试时规划：轻量策略提出 M 个候选整厂动作，用阶段 3 的模型打分，选最优（Idea 5）。
- 再加动作头：用阶段 2 和阶段 4 的最优轨迹做监督，或者在学习式世界模型内用 RL（参考 L9 的 Dreamer 和 TD-MPC2 思路）。
- 产物：整厂层决策的实测收益，与阶段 2 的规则基线比较。

### 阶段 5：接入真实工位（时间取决于现场条件）

- 先只把一个真实工位接进来，其余仍在仿真里。
- 用真实事件校准整厂层模型（残差，参考 L6）。
- 产物：仿真与真实混合运行时的预测误差和决策收益。

### 算力分配建议

| 任务 | 硬件 |
|---|---|
| VLA LoRA 微调、视频或 JEPA 小模型训练 | 40／80 GB 卡（显存最紧张） |
| 整厂层图世界模型训练 | 1–2 张 3090／4090 |
| 仿真数据生成（MuJoCo／Isaac） | 其余 3090／4090，CPU 并行跑离散事件 |
| 在线推理 | 一张 4090 同时跑整厂层模型和一个 VLA 推理服务；ROSA 指出多机器人共享 GPU 池能显著提高利用率 [arXiv 2607.01088] |

## 4. 主要风险

- **子级自报告不可靠**：如果 VLA 报告的成功率不准，整厂层的预测会系统性偏差。需要在阶段 1 用真实或仿真试验标定。
- **仿真数据的偏差**：整厂层模型主要用仿真数据训练，会继承仿真偏差（参考 L6 中 PointWorld 只用仿真数据时不能零样本泛化到真实场景 [P44]）。
- **评估难**：整厂层收益（吞吐、准时率）需要长时间运行才能看出，仿真评估要足够多的随机种子。
- **新概念的说服力**：FWAM 需要用实验说明，相比"排产＋独立机器人"，联合预测带来了可测的收益。阶段 2 的规则基线就是为此准备的。

## 5. 推荐文献

整厂层与多主体：
- MA-WAM，[arXiv 2609.31281](https://arxiv.org/abs/2609.31281)：测试时用世界模型评估联合动作；给出 RTX 3090 上的耗时
- World Dreamer v5-lite，[arXiv 2610.37518](https://arxiv.org/abs/2610.37518)：共享世界状态的多机器人 WAM
- DeepFleet，[arXiv 2508.08574](https://arxiv.org/abs/2508.08574)：车队预测的四种结构比较
- MAPF-World，[arXiv 2508.12087](https://arxiv.org/abs/2508.12087)：多智能体路径规划的动作世界模型
- AWMP [P38]：已知车间转移与外生到达分离的排产世界模型
- FMAPPO [P39]：多机器人、多机台服务的分工与导航
- RoboFactory [P13]：多臂协作的组合约束基准
- RoboOS，[arXiv 2505.03673](https://arxiv.org/abs/2505.03673)；RoboOS-NeXT，[arXiv 2510.26536](https://arxiv.org/abs/2510.26536)：大脑—小脑多机器人框架
- ROSA，[arXiv 2607.01088](https://arxiv.org/abs/2607.01088)：机器人工厂的模型服务与按工厂目标调度
- COMBO：组合式多智能体世界模型，[arXiv 2404.10775](https://arxiv.org/abs/2404.10775)
- Scalable Multi-Agent Model-Based Reinforcement Learning，[arXiv 2205.15023](https://arxiv.org/abs/2205.15023)
- MAPPO（The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games），[arXiv 2103.01955](https://arxiv.org/abs/2103.01955)

WAM 本身：
- WAM 综述，[arXiv 2605.12090](https://arxiv.org/abs/2605.12090)、[arXiv 2609.16074](https://arxiv.org/abs/2609.16074)
- OpenWAM，[arXiv 2610.07922](https://arxiv.org/abs/2610.07922)：可组合 WAM 框架；反事实数据改善动力学模型
- Unified World Models（UWM），[arXiv 2504.02792](https://arxiv.org/abs/2504.02792)：视频与动作联合扩散；4 张 A100 训练 24 小时
- Unified Video Action Model，[arXiv 2503.00200](https://arxiv.org/abs/2503.00200)
- WorldVLA，[arXiv 2506.21539](https://arxiv.org/abs/2506.21539)
- H-WM：逻辑世界模型与视觉世界模型分层，[arXiv 2602.11291](https://arxiv.org/abs/2602.11291)

分层控制：
- Director（Deep Hierarchical Planning from Pixels），[arXiv 2206.04114](https://arxiv.org/abs/2206.04114)
- FeUdal Networks，[arXiv 1703.01161](https://arxiv.org/abs/1703.01161)
- H-JEPA [P56]：分层 JEPA 世界模型
- Skogestad 2004，[作者 PDF](https://skoge.folk.ntnu.no/publications/2004/control_structure_design_cce/cce04_skogestad.pdf)：整厂控制按时间尺度分层

## 6. 参考项目

- 多智能体环境与算法：[Farama-Foundation/PettingZoo](https://github.com/Farama-Foundation/PettingZoo)、[marlbenchmark/on-policy](https://github.com/marlbenchmark/on-policy)（MAPPO）、[bold-lab-ai/JaxMARL](https://github.com/bold-lab-ai/JaxMARL)、[instadeepai/Mava](https://github.com/instadeepai/Mava)
- 大脑—小脑框架：[FlagOpen/RoboOS](https://github.com/FlagOpen/RoboOS)
- 多臂协作基准：[IranQin/robofactory](https://github.com/IranQin/robofactory)
- 离散事件仿真：[SimPy 文档](https://simpy.readthedocs.io/en/latest/)
- 子级 VLA：[Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)、[NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)、[huggingface/lerobot](https://github.com/huggingface/lerobot)
- 子级 WBC：[NVlabs/HOVER](https://github.com/NVlabs/HOVER)、[zixuan417/humanoid-general-motion-tracking](https://github.com/zixuan417/humanoid-general-motion-tracking)（GMT）、[LeCAR-Lab/ASAP](https://github.com/LeCAR-Lab/ASAP)、[YanjieZe/TWIST](https://github.com/YanjieZe/TWIST)
- 资源列表：[OpenMOSS/Awesome-WAM](https://github.com/OpenMOSS/Awesome-WAM)、[LMD0311/Awesome-World-Model](https://github.com/LMD0311/Awesome-World-Model)
