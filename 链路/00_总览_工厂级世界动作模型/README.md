# 00 总览：工厂级世界动作模型

## 1. 问题从哪里来

### 1.1 单机器人层面：VLA 不直接做全身控制

现有 VLA 大多输出手臂或末端动作，下半身（腿、AGV 底盘）由另一个专门的跟踪控制器执行。几篇代表工作都是这种分层：

| 工作 | 上层（大脑） | 下层（小脑） | 接口 |
|---|---|---|---|
| π0.5 [arXiv 2504.16054] | 同一模型先预测高层语义子任务，再输出低层动作 | 机器人自身控制器 | 动作块 |
| GR00T N1 [arXiv 2503.14734] | System 2：视觉语言模块理解环境与指令 | System 1：扩散 Transformer 实时生成动作 | 两者端到端联合训练 |
| NaVILA [arXiv 2412.04453] | VLA 生成语言形式的中层动作，如"向前 75 cm" | 视觉运动 RL 策略控制腿 | 中层语言动作 |
| LeVERB [arXiv 2506.13751] | 视觉语言策略学习潜在动作词表 | RL 训练的 WBC 策略 | 潜在"动词" |
| Being-0 [arXiv 2503.12533] | 基础模型做规划 | 运动与操作技能库 | 轻量 VLM 作为 Connector |
| HOVER [arXiv 2410.21229] | — | 多模式统一的全身控制器 | 根速度、关节角等多种命令模式 |

LeVERB 的摘要直接指出：多数 VLA 系统假设有一个精确的低层控制器，带手工设定的动作"词表"，如末端位姿或根速度。WBC（全身控制）就是在这个背景下被强调的：它把下层的跟踪器做成通用的，向上层暴露一个统一端口。人形机器人上，这一层常用运动跟踪来训练：

- SONIC：模型 1.2M–42M 参数，700 小时动捕数据，2.1 万 GPU 小时 [arXiv 2511.07820]；
- GMT [arXiv 2506.14770]、BeyondMimic [arXiv 2508.08241]、AMO [arXiv 2505.03738]。

### 1.2 把同样的分层放大到整厂

你的类比可以直接延伸：

| 层级 | 单个人形或轮臂 | 整个工厂 |
|---|---|---|
| 小脑 | 腿或 AGV 的跟踪控制器（WBC） | 每台机器人自己的"VLA＋WBC"，以及每台机床的 PLC／NC |
| 大脑 | VLA，给出手臂动作和底盘目标 | 整厂层：给每台机器人和机床分配任务、路径、时机，并预测结果 |
| 端口 | 根速度、末端位姿、潜在动作 | 技能调用、目标位姿、工位指令、设备命令 |

于是在整厂层面，每台机器人的 VLA 或技能策略退成"子级"，就像单机器人中的 WBC 退成小脑。整厂层需要一个模型：输入全厂状态和所有子级的候选动作，预测全厂接下来会怎样，并据此选动作。这正是 world action model（WAM）在多主体、多时间尺度上的推广。

## 2. 这个概念已经有名字了吗

### 2.1 已定义的相关术语

- **World Action Model（WAM）**：已有正式定义。综述 "World Action Models: The Next Frontier in Embodied AI" [arXiv 2605.12090] 把 WAM 定义为"统一预测状态建模与动作生成、目标是未来状态与动作的联合分布"的具身基础模型。另一篇综述 [arXiv 2609.16074] 也用这个名字。
- **分层 WAM 是公认的开放问题**：同一篇综述 [arXiv 2605.12090] 写道，把高层语义任务分解与低层物理预测连接在统一可学习架构中的分层世界—动作建模框架，仍是关键的开放挑战。它提出三条路径：一是模块化分层，WAM 作为低层执行器、由高层规划器指挥；二是内在分层 WAM，同时生成粗粒度和细粒度的预测；三是扩展时间上下文。
- **多机器人 WAM 已有初步工作**：
  - World Dreamer v5-lite [arXiv 2610.37518] 是多机器人 WAM：在工作空间坐标中建立共享世界状态，每台机器人一个查询，各自输出动作流。它在 RoboFactory 上平均成功率 74.0%，在 4 个真实机器人任务上 78.8%，但都是共享工作台的协作操作。
  - MA-WAM [arXiv 2609.31281] 用世界模型在测试时评估多智能体的联合动作，但只在 MAMuJoCo、SMAC、MPE 等仿真基准上验证。
  - MAPF-World [arXiv 2508.12087] 是多智能体路径规划的动作世界模型。
- **车队级预测模型**：DeepFleet [arXiv 2508.08574] 在 Amazon 仓库数十万台机器人的运动数据上训练车队基础模型，比较了四种结构，参数从 13M 到 900M。它只预测移动机器人的交通，评审指出它停在预测，没有测试规划效果。
- **大脑—小脑的多机器人框架**：RoboOS [arXiv 2505.03673] 和 RoboOS-NeXT [arXiv 2510.26536] 采用大脑—小脑分层：云端大脑模型做任务分解与分配，分布式小脑执行技能，并有共享记忆。但大脑是 LLM 规划器，不是预测动作后果的世界模型。
- **工业控制中的"整厂控制"**：化工领域的 plantwide control 研究整厂的控制结构，按时间尺度分层：排产以周计，全厂优化以天计，局部优化以小时计，监督控制（MPC）以分钟计，调节控制以秒计 [Skogestad 2004，见下文链接]。这和"整厂世界动作模型"要解决的分层问题高度对应，但那里没有学习式世界模型。

### 2.2 检索结论

截至 2026-11-20，我检索到的文献里：

- **没有**一篇提出"整厂级"世界模型或世界动作模型，即同时预测多台异构机器人、机床设备状态和生产流的模型。
- 最接近的是上面几类：多机器人 WAM 只覆盖单个共享工作台；车队模型只有移动机器人的交通；大脑—小脑框架没有预测；plantwide control 没有学习。
- 有工业界人士使用"工业世界模型""过程世界模型"等说法，但都指单个工艺或设备，不是整厂。

所以，**"整厂级世界动作模型"目前没有被定义的说法**，可以作为一个新概念提出。下面给出几个候选命名，附上与已有术语的区别。

### 2.3 命名候选

| 候选名 | 英文缩写 | 侧重点 | 与已有术语的区别 |
|---|---|---|---|
| 工厂级世界动作模型 | Factory World Action Model，FWAM | 直接继承 WAM 的定义，范围扩到整厂 | 与 WAM 一脉相承，最易被理解；本目录采用这个名字 |
| 分层车间世界动作模型 | Hierarchical Shop-floor WAM，HS-WAM | 强调分层（整厂层—工位层—机器人层） | 对应综述中"内在分层 WAM"的开放问题 |
| 车队—设备联合世界动作模型 | Fleet-Equipment WAM | 强调机器人车队和机床设备的联合预测 | 区别于 DeepFleet 只有机器人 |
| 编排世界模型 | Orchestration World Model | 强调预测"编排动作"（派工、路由、时机）的后果 | 动作不是关节量，而是对子级的调用 |
| 工厂小脑—大脑模型 | Factory Cerebrum–Cerebellum WAM | 延续 RoboOS 的大脑—小脑比喻 | 大脑本身是可预测的世界动作模型，而不只是 LLM 规划器 |

**FWAM 的工作定义**（本目录提出，供讨论）：

> 给定整厂的观测历史 o≤t（多机器人传感器、设备 PLC/NC 信号、工单与物料状态），以及一组子级执行器（机器人的 VLA／WBC 策略、设备控制器）暴露的动作端口，FWAM 预测未来的整厂状态与事件 p(s_{t+1:t+H}, e_{t:t+H} | o≤t, a_{t:t+H})，并在同一模型或配套规划器中生成整厂层动作 a，即对各子级的指令、时机和路由。整厂层动作在子级端口上执行，子级负责把它变成关节量或设备命令。

和单机器人 WAM 的关键差别：

1. **动作是对子级的调用，不是关节量**：例如"机器人 2 去 CNC-1 上料"，"CNC-1 在 t 时刻启动程序 O1001"。
2. **状态是混合的**：连续量（位姿、温度）、离散量（设备模式、工单状态）和事件同时存在。
3. **多时间尺度**：秒级的机器人动作和小时级的生产流共存。
4. **主体数量可变**：机器人和设备会增加、停机、维修。

## 3. 有限算力下的总体思路

可用算力：几张 RTX 3090／4090（24 GB），加极少量 40 GB／80 GB 卡。以下是根据文献中的算力数据做的推导。

### 3.1 能做什么、不能做什么

| 事项 | 文献中的算力 | 在本算力下 |
|---|---|---|
| 从头训练大视频世界模型 | DreamGen 生成 24 万条样本用 1500 张 L40 约 54 小时 [P65] | 不可行 |
| 微调 VLA | openpi：推理需 8 GB 以上，LoRA 微调需 22.5 GB 以上（RTX 4090），全量微调需 70 GB 以上（A100／H100）（openpi README） | LoRA 微调可行 |
| 小 VLA | SmolVLA 设计为单 GPU 训练、消费级 GPU 或 CPU 部署 [arXiv 2506.01844] | 可行 |
| 腿式和人形运动 RL | Learning to Walk in Minutes：单块工作站 GPU，平地四分钟内 [arXiv 2109.11978]；MuJoCo Playground：两块 RTX 4090 上 G1 平地训练不到 30 分钟 [arXiv 2502.08844] | 可行 |
| 通用运动跟踪大模型 | SONIC 用了 2.1 万 GPU 小时 [arXiv 2511.07820] | 不可行，直接用开源权重 |
| 小 JEPA 世界模型 | LeWorldModel 约 1500 万参数，单 GPU 几小时可训，规划不到 1 秒 [P55] | 可行 |
| 视频＋动作联合扩散 | UWM 在 DROID 上训练 10 万步，用 4 张 A100 共 24 小时 [arXiv 2504.02792] | 勉强可行，需降分辨率 |
| 多智能体世界模型评分 | MA-WAM 在 RTX 3090 上，8 个候选的生成加评分共 428 ms，其中评分 13.4 ms [arXiv 2609.31281] | 可行 |
| 车队交通模型 | DeepFleet 的图—地面模型只有 13M 参数 [arXiv 2508.08574] | 结构可借鉴；没有 Amazon 那样的数据量 |

### 3.2 由此得到的思路

1. **整厂层不做像素预测**。整厂的状态用结构化表示：实体图、事件、设备模式、工单。像素和三维只在工位层或机器人层使用。整厂层模型因此可以很小，在一张 4090 上训练。
2. **子级尽量复用现成模型**：π0.5／openpi、GR00T、SmolVLA 做操作；HOVER、GMT、AMO 等开源 WBC 做全身控制；Nav2 做底盘导航。在本算力下只做 LoRA 微调。
3. **数据主要来自仿真**：L1、L2、L4 搭起来的数字孪生可以低成本大量生成"整厂状态—整厂动作—结果"数据。这是整厂层模型的主要数据源。
4. **整厂层可以是"学习式代理＋显式仿真校核"**：学习式模型负责快速搜索候选方案，显式仿真只对少数候选做精确验证。
5. **先在两到三个工位的缩小版工厂上做通**，再加机器人和设备。

## 4. 各链路在 FWAM 分层结构中的位置

| 层 | 时间尺度 | 作用 | 对应链路 |
|---|---|---|---|
| 整厂层（大脑） | 分钟到小时 | 派工、路由、排产；预测吞吐、拥堵、设备事件 | L4（离散事件与 PLC）、L11（学习式 FWAM）、L9（潜变量控制，用于整厂层动作） |
| 工位层 | 秒到分钟 | 单个工位内的多机器人与设备协作；预测上下料、装夹、加工完成 | L1、L2、L6、L8 |
| 机器人层（小脑） | 毫秒到秒 | VLA 加 WBC；预测接触与几何 | L7、L10（数据与评估）、L1 中的 MPC、L8（INTACT 式无搜索控制，只在仿真中验证过） |
| 资产与数据层 | 离线 | 提供场景、资产、仿真数据 | L1、L2、L3 |

形变、流体、断裂和材料去除不单列为一层或一条链路。它们是各层任务可能涉及的条件，任务涉及时各链路要补的能力见[专题：形变、流体、断裂与加工](../专题_形变流体断裂与加工/README.md)；工位层的加工时长、质量和报废概率由专题第 4 节的加工代理提供。

L11 文件夹详细写了怎样把这些层串起来。

## 5. 推荐文献（总览层）

概念与综述：
- World Action Models: The Next Frontier in Embodied AI，[arXiv 2605.12090](https://arxiv.org/abs/2605.12090)：WAM 的正式定义；把分层 WAM 列为开放问题
- World-Action Models for Robot Learning and Control: A Survey，[arXiv 2609.16074](https://arxiv.org/abs/2609.16074)
- From World Models to World Action Models: A Concise Tutorial for Robotics，[arXiv 2607.00836](https://arxiv.org/abs/2607.00836)
- Embodied Intelligence for Flexible Manufacturing: A Survey，[arXiv 2602.06966](https://arxiv.org/abs/2602.06966)：从"工业之眼、工业之手、工业之脑"三层综述制造业具身智能
- Robots Need More than VLA and World Models，[arXiv 2606.06556](https://arxiv.org/abs/2606.06556)：立场论文
- Skogestad, Control structure design for complete chemical plants, Computers & Chemical Engineering 28 (2004) 219–234，[作者 PDF](https://skoge.folk.ntnu.no/publications/2004/control_structure_design_cce/cce04_skogestad.pdf)：整厂控制的分层思想

多机器人与车队：
- World Dreamer v5-lite，[arXiv 2610.37518](https://arxiv.org/abs/2610.37518)
- MA-WAM，[arXiv 2609.31281](https://arxiv.org/abs/2609.31281)
- MAPF-World，[arXiv 2508.12087](https://arxiv.org/abs/2508.12087)
- DeepFleet，[arXiv 2508.08574](https://arxiv.org/abs/2508.08574)
- Gamma-World：多智能体生成式世界模型，[arXiv 2605.28816](https://arxiv.org/abs/2605.28816)
- RoboOS，[arXiv 2505.03673](https://arxiv.org/abs/2505.03673)；RoboOS-NeXT，[arXiv 2510.26536](https://arxiv.org/abs/2510.26536)
- ROSA：机器人工厂的基础模型服务系统，[arXiv 2607.01088](https://arxiv.org/abs/2607.01088)
- Learning While Deploying：16 台双臂机器人车队的在线强化学习，[arXiv 2605.00416](https://arxiv.org/abs/2605.00416)
- RoboFactory [P13]、FMAPPO 多机器人上下料 [P39]、AWMP 排产世界模型 [P38]

VLA 与 WBC 分层：
- π0.5 [arXiv 2504.16054](https://arxiv.org/abs/2504.16054)；GR00T N1 [arXiv 2503.14734](https://arxiv.org/abs/2503.14734)；Hi Robot [arXiv 2502.19417](https://arxiv.org/abs/2502.19417)；HAMSTER [arXiv 2502.05485](https://arxiv.org/abs/2502.05485)
- NaVILA [arXiv 2412.04453](https://arxiv.org/abs/2412.04453)；LeVERB [arXiv 2506.13751](https://arxiv.org/abs/2506.13751)；Being-0 [arXiv 2503.12533](https://arxiv.org/abs/2503.12533)
- HOVER [arXiv 2410.21229](https://arxiv.org/abs/2410.21229)；SONIC [arXiv 2511.07820](https://arxiv.org/abs/2511.07820)；GMT [arXiv 2506.14770](https://arxiv.org/abs/2506.14770)；BeyondMimic [arXiv 2508.08241](https://arxiv.org/abs/2508.08241)；AMO [arXiv 2505.03738](https://arxiv.org/abs/2505.03738)；ASAP [arXiv 2502.01143](https://arxiv.org/abs/2502.01143)
- BEHAVIOR Robot Suite：轮式双臂全身操作 [arXiv 2503.05652](https://arxiv.org/abs/2503.05652)；Mobile ALOHA [arXiv 2401.02117](https://arxiv.org/abs/2401.02117)
