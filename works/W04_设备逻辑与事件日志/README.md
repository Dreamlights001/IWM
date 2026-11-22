# W04 设备逻辑与事件日志

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W04)

给机床、输送线等设备补上 PLC／NC 行为模型并接进仿真，再生成带因果真值的车间事件日志。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md)：事件类型与端口定义 | [W03（车间场景生成）](../W03_车间场景生成/README.md)：设备行为模型<br>[W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)：离散事件仿真<br>[W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：事件日志与显式仿真<br>[W15（安全与约束）](../W15_安全与约束/README.md)：互锁逻辑 | ① 主动与反事实数据<br>② 仿真—真实校准<br>⑥ 评测—部署飞轮 |

## 1. 为什么要做

场景里只有几何时，机床不会开门、不会完工，也不会报警。设备行为由 PLC／NC 决定：模式、互锁、报警、程序段和节拍。虚拟调试把 PLC 程序接到仿真模型上，但 PLC 变量与仿真对象的对应主要靠人工建立；一项 2026 年的工作用知识图谱和多智能体 LLM 半自动生成这些对应，只在实验室规模的产线上验证，最终仍需人工验收 [P66](../../papers/P66_LLM_Virtual_Commissioning_2606.03255v1.pdf)。整厂层模型的训练数据主要是事件序列，公开数据很少：半导体工厂有用离散事件仿真生成的时间序列基准 [arXiv 2408.09307](https://arxiv.org/abs/2408.09307)，作业车间调度有 13 万个实例的 Starjob [arXiv 2503.01877](https://arxiv.org/abs/2503.01877)，它们都不含机器人的执行过程。

## 2. 输入与产物

**输入**

- 设备手册；PLC 程序与 NC 程序（如能取得）
- OPC UA／MTConnect 信号点表
- 工艺节拍
- [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的事件类型表

**产物**

- 每类设备的行为模型：手写状态机，或在软 PLC 中运行的真实程序
- 仿真与 PLC 之间的信号映射
- 离散事件层（SimPy [SimPy 文档](https://simpy.readthedocs.io/en/latest/) 或自写事件循环），可保存与恢复事件队列
- 带因果真值的合成事件日志：每个事件由哪个动作、哪个设备状态引起

## 3. 具体工作

1. 为每类设备写状态机：模式（手动、自动、急停）、门与夹具互锁、程序段、完工、报警。没有真实程序时先手写。
2. 有真实 PLC 程序时，用软 PLC（OpenPLC runtime）运行，通过 OPC UA（opcua-asyncio、open62541）与仿真交换信号；NC 侧参考 LinuxCNC 的架构 [S32](https://linuxcnc.org/docs/stable/html/code/code-notes.html#_architecture_overview) 和 SINUMERIK 虚拟机床 [S31](https://cache.industry.siemens.com/dl/files/129/109988129/att_1326187/v1/ONE_828D_cmvm_sys_man_0325_en-US.pdf?download=true)。
3. 联合仿真：物理仿真、PLC 和离散事件层的时钟同步与回滚，参考联合仿真综述 [P98](../../papers/P98_Co_Simulation_Survey_1702.00686v1.pdf) 和 FMI 3.0 [S4](https://fmi-standard.org/docs/3.0.2/)；工具可用 FMPy、Maestro、OpenModelica。
4. 按 [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的格式生成事件日志，并保留因果真值。
5. 从日志学模型：自动机学习（FlexFringe [arXiv 2203.16331](https://arxiv.org/abs/2203.16331)）和过程挖掘（PM4Py [arXiv 1905.06169](https://arxiv.org/abs/1905.06169)）都能把日志变成可执行模型，二者的比较见 [arXiv 2604.03686](https://arxiv.org/abs/2604.03686)；随机 Petri 网的参数可用神经代理从部分观测的轨迹推断 [arXiv 2507.10714](https://arxiv.org/abs/2507.10714)。
6. LLM 生成 PLC 代码并做形式化验证：LLM4PLC [arXiv 2401.05443](https://arxiv.org/abs/2401.05443)、Agents4PLC [arXiv 2410.14209](https://arxiv.org/abs/2410.14209)。

## 4. 可以写成论文的方向

### 4.1 从设备信号日志学习可执行的设备行为模型

- 类型：方法
- 研究问题：只有 OPC UA／MTConnect 信号日志、没有 PLC 源码时，能否学出可接入仿真的设备状态机，并给出它与真实设备的一致率？
- 已有工作与空白：FlexFringe 从软件日志学习概率自动机 [arXiv 2203.16331](https://arxiv.org/abs/2203.16331)，PM4Py 做过程挖掘 [arXiv 1905.06169](https://arxiv.org/abs/1905.06169)，[arXiv 2604.03686](https://arxiv.org/abs/2604.03686) 在用户旅程日志上比较这两类方法；它们的对象是软件和业务流程。虚拟调试中的信号映射目前仍以人工为主 [P66](../../papers/P66_LLM_Virtual_Commissioning_2606.03255v1.pdf)。
- 怎样验证：在有真值的合成日志和真实日志上，比较学到的状态机与真实逻辑的转移一致率；接入仿真后比较节拍误差。

### 4.2 带因果真值的合成车间事件数据集

- 类型：数据集
- 研究问题：用 [W03（车间场景生成）](../W03_车间场景生成/README.md)＋本工作的仿真生成大规模事件日志，保留“动作—设备状态—事件”的因果真值，供 [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md) 训练和评测。
- 已有工作与空白：已有的制造数据集是时间序列或调度实例，不含机器人执行和设备互锁 [arXiv 2408.09307](https://arxiv.org/abs/2408.09307) [arXiv 2503.01877](https://arxiv.org/abs/2503.01877)。
- 怎样验证：在同一数据集上比较 [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md) 中的多种模型；测量数据量对预测误差的影响。

### 4.3 LLM 生成设备行为模型并自动验证

- 类型：方法
- 研究问题：能否让 LLM 从设备手册生成状态机或 PLC 代码，再用仿真和形式化检查自动验证？
- 已有工作与空白：LLM4PLC、Agents4PLC 用 LLM 生成 PLC 代码并接入验证工具 [arXiv 2401.05443](https://arxiv.org/abs/2401.05443) [arXiv 2410.14209](https://arxiv.org/abs/2410.14209)，目标是控制程序本身；生成供世界模型使用的设备行为模型还很少有人做（分析判断）。
- 怎样验证：生成模型的验证通过率；与人工模型比较事件一致率。

## 5. 所在闭环

- ① 主动与反事实数据：W09·W10 找出误差大或不确定的状态 → W11 选状态，设计动作扰动 → W03·W04·W05 从快照复位，执行并记录 → 回训模型。OpenWAM 报告，加入反事实监督后前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)；Plan2Explore 用模型集成的分歧选择探索目标 [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)。
- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。
- ⑥ 评测—部署飞轮：W16 评测，找出失败模式 → W17 部署，记录失败与人工干预 → W07·W04 采集真实片段与事件日志 → W11·W05 生成反事实与针对性数据 → 回训后再评测。Fleet-DAgger 研究多台机器人共享少量人工监督 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人上做车队级离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 6. 对应的链路

- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件

## 7. 高价值参考文献

### 虚拟调试与联合仿真

- **Multi-Agent Framework Leveraging Knowledge Graphs for Virtual Commissioning Models**（2026），[P66 本地 PDF](../../papers/P66_LLM_Virtual_Commissioning_2606.03255v1.pdf)：知识图谱＋多智能体 LLM 半自动生成虚拟调试的信号映射。
- **虚拟调试综述（Striffler & Voigt, 2023）**（journal review (metadata only)），[链接](https://doi.org/10.1016/j.jmsy.2023.10.013)：虚拟调试系统综述。
- **Siemens 虚拟调试指南**（official documentation），[链接](https://cache.industry.siemens.com/dl/files/864/109963864/att_1277519/v1/Guideline_VC_SIMIT_PSA_MCD_V1.0.0.pdf)：Siemens 虚拟调试指南。
- **Co-simulation: State of the art**（2017），[P98 本地 PDF](../../papers/P98_Co_Simulation_Survey_1702.00686v1.pdf)：联合仿真综述：主控、同步、耦合误差与回滚。
- **FMI 3.0.2**（official documentation），[链接](https://fmi-standard.org/docs/3.0.2/)：FMI 3.0 标准。

### 设备数据接口

- **OPC UA for Machine Tools, Part 1**（official documentation），[链接](https://reference.opcfoundation.org/specs/OPC-40501-1/6)：OPC UA for Machine Tools。
- **MTConnect Device Information Model 2.1.0**（official documentation），[链接](https://docs.mtconnect.org/MBSD_MTConnect_Part_2_2-1-0.pdf)：MTConnect 设备信息模型。
- **SINUMERIK 虚拟机床手册**（official documentation），[链接](https://cache.industry.siemens.com/dl/files/129/109988129/att_1326187/v1/ONE_828D_cmvm_sys_man_0325_en-US.pdf?download=true)：SINUMERIK 虚拟机床手册。
- **LinuxCNC 架构概览**（official documentation），[链接](https://linuxcnc.org/docs/stable/html/code/code-notes.html#_architecture_overview)：LinuxCNC 架构概览。
- **A Core Manufacturing Simulation Data Information Model for Manufacturing Applications**（2006），[P99 本地 PDF](../../papers/P99_NIST_CMSD.pdf)：NIST CMSD。

### 从日志学模型

- **FlexFringe: Modeling Software Behavior by Learning Probabilistic Automata**（2022），[arXiv 2203.16331](https://arxiv.org/abs/2203.16331)：FlexFringe：从软件行为日志学习概率自动机。
- **Process Mining for Python (PM4Py): Bridging the Gap Between Process- and Data Science**（2019），[arXiv 1905.06169](https://arxiv.org/abs/1905.06169)：PM4Py：Python 过程挖掘库。
- **Automata Learning versus Process Mining: The Case for User Journeys**（2026），[arXiv 2604.03686](https://arxiv.org/abs/2604.03686)：自动机学习与过程挖掘的比较。
- **A Simple Approximate Bayesian Inference Neural Surrogate for Stochastic Petri Net Models**（2025），[arXiv 2507.10714](https://arxiv.org/abs/2507.10714)：随机 Petri 网的神经代理：从带噪、部分观测的轨迹推断速率函数。

### LLM 与 PLC

- **LLM4PLC: Harnessing Large Language Models for Verifiable Programming of PLCs in Industrial Control Systems**（2024），[arXiv 2401.05443](https://arxiv.org/abs/2401.05443)：LLM4PLC：可验证的 PLC 编程流程。
- **Agents4PLC: Automating Closed-loop PLC Code Generation and Verification in Industrial Control Systems using LLM-based Agents**（2024），[arXiv 2410.14209](https://arxiv.org/abs/2410.14209)：Agents4PLC：基于 LLM 智能体的闭环 PLC 代码生成与验证。

### 制造事件、调度与资产数据

- **A Benchmark Time Series Dataset for Semiconductor Fabrication Manufacturing Constructed using Component-based Discrete-Event Simulation Models**（2024），[arXiv 2408.09307](https://arxiv.org/abs/2408.09307)：用组件化离散事件仿真生成的半导体工厂时间序列基准。
- **Starjob: Dataset for LLM-Driven Job Shop Scheduling**（2025），[arXiv 2503.01877](https://arxiv.org/abs/2503.01877)：Starjob：13 万个作业车间调度实例，用于训练 LLM。
- **LLM-Based Exogenous World Modeling for Dynamic Scheduling**（2026），[P38 本地 PDF](../../papers/P38_AWMP_Dynamic_Scheduling_2610.29308v1.pdf)：AWMP：把已知的车间转移与不确定的订单到达分开建模。
- **IndustryAssetEQA: A Neurosymbolic Operational Intelligence System for Embodied Question Answering in Industrial Asset Maintenance**（2026），[arXiv 2604.23446](https://arxiv.org/abs/2604.23446)：IndustryAssetEQA：结合遥测与 FMEA 知识图谱做工业资产问答，评估反事实推理。
- **SimPy 文档**（离散事件仿真库），[链接](https://simpy.readthedocs.io/en/latest/)：SimPy 离散事件仿真。

## 8. 参考项目

- [Autonomy-Logic/openplc-runtime](https://github.com/Autonomy-Logic/openplc-runtime)：软 PLC 运行时（OpenPLC_v3 已归档，用这个）
- [LinuxCNC/linuxcnc](https://github.com/LinuxCNC/linuxcnc)：开源数控系统
- [FreeOpcUa/opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio)：Python OPC UA 客户端与服务器
- [open62541/open62541](https://github.com/open62541/open62541)：C 语言 OPC UA 实现
- [CATIA-Systems/FMPy](https://github.com/CATIA-Systems/FMPy)：运行 FMU 的 Python 库
- [INTO-CPS-Association/maestro](https://github.com/INTO-CPS-Association/maestro)：FMI 联合仿真主控
- [OpenModelica/OpenModelica](https://github.com/OpenModelica/OpenModelica)：Modelica 建模与仿真
- [tudelft-cda-lab/FlexFringe](https://github.com/tudelft-cda-lab/FlexFringe)：自动机学习
- [process-intelligence-solutions/pm4py](https://github.com/process-intelligence-solutions/pm4py)：过程挖掘

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
