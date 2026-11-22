# W01 问题定义、接口与评测协议

> 阶段：S0 定义问题与评测　·　总看板：[research_board.html](../research_board.html#W01)

写清整厂层的状态、动作、事件、时间尺度和评测指标，作为后面所有数据采集和模型训练的共同规范。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| — | [W02（设备资产生成）](../W02_设备资产生成/README.md)：实体与资产规范<br>[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md)：事件类型与端口定义<br>[W07（真实数据采集与同步）](../W07_真实数据采集与同步/README.md)：数据记录格式<br>[W15（安全与约束）](../W15_安全与约束/README.md)：约束清单<br>[W16（基准与评测）](../W16_基准与评测/README.md)：评测协议草案 | — |

## 1. 为什么要做

本轮检索没有找到已发表的工厂级世界动作模型（[00 总览](../../链路/00_总览_工厂级世界动作模型/README.md)、[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)）。最接近的工作是：多机器人共享世界状态的 World Dreamer v5-lite [arXiv 2610.37518](https://arxiv.org/abs/2610.37518)、多智能体测试时规划的 MA-WAM [arXiv 2609.31281](https://arxiv.org/abs/2609.31281)、仓储车队预测的 DeepFleet [arXiv 2508.08574](https://arxiv.org/abs/2508.08574)、大脑—小脑多机器人框架 RoboOS [arXiv 2505.03673](https://arxiv.org/abs/2505.03673)。从摘要看，它们的状态里没有机床的 PLC／NC 模式和工单。没有统一的定义，后面的仿真、数据和模型就无法对齐，结果也无法比较。

## 2. 输入与产物

**输入**

- 现场设备清单、工艺路线与节拍
- 设备 STEP、实物扫描、机器人 URDF
- 可获得的 PLC／NC 信号点表、MES 或工单字段（如有）

**产物**

- 实体—关系图模式：节点类型、属性、边类型；事件类型表（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 1.2 节）
- 子级端口与自报告字段：技能调用、设备命令、AGV 目标、派工；预计耗时、成功概率、置信度
- 时间约定：哪些量按事件更新、哪些按固定频率采样；整厂、工位、机器人三层的决策周期
- 数据记录格式：时钟、坐标系、ID 体系、单位，以及与 OPC UA for Machine Tools [S2](https://reference.opcfoundation.org/specs/OPC-40501-1/6)、MTConnect [S3](https://docs.mtconnect.org/MBSD_MTConnect_Part_2_2-1-0.pdf)、NIST CMSD [P99](../../papers/P99_NIST_CMSD.pdf) 字段的对应
- 评测协议草案（交给 [W16（基准与评测）](../W16_基准与评测/README.md) 维护）和约束清单（交给 [W15（安全与约束）](../W15_安全与约束/README.md)）

## 3. 具体工作

1. 选一个缩小版工厂作为第一个研究对象，例如两台 CNC、一台机器人、一个料架、一个检测台（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 阶段 0）。
2. 列出实体、属性、关系和事件类型，写成机器可读的模式文件（如 JSON Schema），再用一段真实或手写的生产过程检查能否完整记录。
3. 定义每个子级端口的前置条件（如门已开、夹具松开）、返回事件和自报告字段。
4. 规定时间尺度：整厂层决策周期（分钟级）与机器人控制周期的关系。按时间尺度分层是整厂控制结构设计的常用做法 [Skogestad 2004](https://skoge.folk.ntnu.no/publications/2004/control_structure_design_cce/cce04_skogestad.pdf)。
5. 写评测协议草案：同初态不同动作的对照；多步预测误差，按几何、设备状态、事件时间分开统计；决策收益，包括吞吐、在制品、平均等待、死锁次数。
6. 和 [W15（安全与约束）](../W15_安全与约束/README.md) 一起列出约束：安全区域、互锁、人员区域、设备限位。

## 4. 可以写成论文的方向

### 4.1 工厂级世界动作模型的问题定义与分层接口

- 类型：立场／形式化（可与 W03 的数据集或 W16 的基准合写）
- 研究问题：整厂层的状态、动作和观测怎样定义，才能同时接住机器人的 VLA＋WBC、机床的 PLC／NC 和工单系统？
- 已有工作与空白：两篇 WAM 综述把 WAM 定义为联合预测未来状态与动作的模型，讨论的对象以单个机器人为主 [arXiv 2605.12090](https://arxiv.org/abs/2605.12090) [arXiv 2609.16074](https://arxiv.org/abs/2609.16074)；柔性制造具身智能综述按“工业之眼、工业之手、工业之脑”组织，“脑”这一层是工艺规划与产线调度 [arXiv 2602.06966](https://arxiv.org/abs/2602.06966)；EIIR 框架提出世界模型、高层任务规划、底层技能控制、仿真器和物理系统五个模块 [arXiv 2505.09305](https://arxiv.org/abs/2505.09305)。本轮检索没有找到把这些层次写成同一个可训练世界模型的工作。
- 怎样验证：用缩小版工厂的完整生产过程检查规范能否记录全部事件；给出从规范自动生成仿真接口和数据记录器的示例。

### 4.2 面向工厂的“接口缺口”分析

- 类型：立场论文
- 研究问题：参照“机器人需要的不只是 VLA 和世界模型”一文的写法，系统列出工厂场景缺的数据接口、具身接口、世界模型接口和奖励接口。
- 已有工作与空白：该立场论文指出下一代机器人缺四类接口：自动标注非结构化行为的数据接口、把人体动作重定向到机器人的具身接口、基于物理的三维推理接口、从视频和语言推断任务进度的奖励接口 [arXiv 2606.06556](https://arxiv.org/abs/2606.06556)。它没有专门讨论工厂。
- 怎样验证：每个缺口给出可量化的现状数据和一个最小实验。

## 6. 对应的链路

- [00 总览](../../链路/00_总览_工厂级世界动作模型/README.md)：00 总览：工厂级世界动作模型
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）
- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件

## 7. 高价值参考文献

### WAM 的定义与综述

- **World Action Models: The Next Frontier in Embodied AI**（2026），[arXiv 2605.12090](https://arxiv.org/abs/2605.12090)：WAM 综述：VLA 只学反应式的观测到动作映射，WAM 显式建模世界在干预下怎样演化。
- **World-Action Models for Robot Learning and Control: A Survey**（2026），[arXiv 2609.16074](https://arxiv.org/abs/2609.16074)：面向机器人的 WAM 综述：按表示、转移建模、动作接口、架构、训练流程、数据模态和扩展策略分类。
- **From World Models to World Action Models: A Concise Tutorial for Robotics**（2026），[arXiv 2607.00836](https://arxiv.org/abs/2607.00836)：从世界模型到 WAM 的简明教程，适合统一组内术语。
- **Robots Need More than VLA and World Models**（2026），[arXiv 2606.06556](https://arxiv.org/abs/2606.06556)：立场论文：机器人还缺数据、具身、世界模型、奖励四类接口。

### 制造场景中的具身智能

- **Embodied Intelligence for Flexible Manufacturing: A Survey**（2025），[arXiv 2602.06966](https://arxiv.org/abs/2602.06966)：柔性制造具身智能综述，按感知、控制、决策三层整理。
- **Embodied intelligent industrial robotics: Framework and techniques**（2025），[arXiv 2505.09305](https://arxiv.org/abs/2505.09305)：工业具身智能框架 EIIR，含世界模型、任务规划、技能控制、仿真器、物理系统五个模块。
- **HolidayFactory 1.0: Simulating, Generating, and Evaluating Industrial Robot Tasks**（2026），[arXiv 2611.11789](https://arxiv.org/abs/2611.11789)：HolidayFactory：工业作业是连续工单，前一单影响后一单；提出不复位的评测。

### 整厂层的分层与多主体

- **World Dreamer v5-lite: A Multi-Robot World Action Model with One Dreamer**（2026），[arXiv 2610.37518](https://arxiv.org/abs/2610.37518)：World Dreamer v5-lite：多机器人共享世界状态，每台机器人一个查询。
- **MA-WAM: Multi-Agent World-Action Model for Test-Time Planning**（2026），[arXiv 2609.31281](https://arxiv.org/abs/2609.31281)：MA-WAM：多智能体测试时规划，用世界模型评估候选联合动作。
- **DeepFleet: Multi-Agent Foundation Models for Mobile Robots**（2025），[arXiv 2508.08574](https://arxiv.org/abs/2508.08574)：DeepFleet：仓储机器人车队的四种基础模型结构比较。
- **RoboOS: A Hierarchical Embodied Framework for Cross-Embodiment and Multi-Agent Collaboration**（2025），[arXiv 2505.03673](https://arxiv.org/abs/2505.03673)：RoboOS：大脑—小脑结构的多机器人系统。
- **Control structure design for complete chemical plants**（Skogestad, Computers & Chemical Engineering, 2004），[链接](https://skoge.folk.ntnu.no/publications/2004/control_structure_design_cce/cce04_skogestad.pdf)：整厂控制结构设计：按时间尺度把决策分层。

### 数据与接口标准

- **OPC UA for Machine Tools, Part 1**（official documentation），[链接](https://reference.opcfoundation.org/specs/OPC-40501-1/6)：OPC UA for Machine Tools：机床状态、程序、报警的信息模型。
- **MTConnect Device Information Model 2.1.0**（official documentation），[链接](https://docs.mtconnect.org/MBSD_MTConnect_Part_2_2-1-0.pdf)：MTConnect 设备信息模型。
- **FMI 3.0.2**（official documentation），[链接](https://fmi-standard.org/docs/3.0.2/)：FMI 3.0：模型交换与联合仿真接口。
- **A Core Manufacturing Simulation Data Information Model for Manufacturing Applications**（2006），[P99 本地 PDF](../../papers/P99_NIST_CMSD.pdf)：NIST CMSD：制造仿真数据的中立信息模型。

## 8. 参考项目

- [OpenMOSS/Awesome-WAM](https://github.com/OpenMOSS/Awesome-WAM)：WAM 文献列表，便于跟踪新工作
- [FlagOpen/RoboOS](https://github.com/FlagOpen/RoboOS)：大脑—小脑多机器人框架的实现，可参考其技能库接口
- [huggingface/lerobot](https://github.com/huggingface/lerobot)：LeRobotDataset 格式可作为机器人轨迹部分的记录格式参考

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
