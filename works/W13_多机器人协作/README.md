# W13 多机器人协作

> 阶段：S3 整厂层：预测与决策　·　总看板：[research_board.html](../research_board.html#W13)

两种尺度的协作：同一工位内多台机器人的紧耦合协作（共同装夹、交接工件），以及车间里机器人和 AGV 的任务分配与路径协调。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：联合动作打分<br>[W12（子级技能与端口）](../W12_子级技能与端口/README.md)：技能端口 | [W14（整厂规划与调度）](../W14_整厂规划与调度/README.md)：协作原语<br>[W16（基准与评测）](../W16_基准与评测/README.md)：待评测方法 | — |

## 1. 为什么要做

工厂场景中已有的相关工作：RoboFactory 用逻辑、空间、时间组合约束组织多具身智能体的协作 [P13](../../papers/P13_RoboFactory_2503.16408v1.pdf)；FMAPPO 在工厂中学习多机器人分工与导航 [P39](../../papers/P39_FMAPPO_Machine_Tending_2609.14567v1.pdf)；World Dreamer v5-lite 在 RoboFactory 上的平均成功率为 74.0%，比最强基线高 23.7 个百分点 [arXiv 2610.37518](https://arxiv.org/abs/2610.37518)。这些工作都没有把机床的设备状态和工单放进协作问题（依据其摘要判断）。

## 2. 输入与产物

**输入**

- [W12（子级技能与端口）](../W12_子级技能与端口/README.md) 的技能端口
- [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md) 的整厂预测
- [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md) 的多机器人数据

**产物**

- 协作策略或规划器
- 任务分配方法
- 通道与工位资源的冲突消解
- 协作基准任务

## 3. 具体工作

1. 多智能体 RL 基线：MAPPO [arXiv 2103.01955](https://arxiv.org/abs/2103.01955)、QMIX [arXiv 1803.11485](https://arxiv.org/abs/1803.11485)、HAPPO／HATRPO [arXiv 2109.11251](https://arxiv.org/abs/2109.11251)、异构的 HetGPPO [arXiv 2301.07137](https://arxiv.org/abs/2301.07137)；按 EPyMARL 的基准设置比较 [arXiv 2006.07869](https://arxiv.org/abs/2006.07869)。
2. LLM 协作规划：RoCo [arXiv 2307.04738](https://arxiv.org/abs/2307.04738)、CoELA [arXiv 2307.02485](https://arxiv.org/abs/2307.02485)、SMART-LLM [arXiv 2309.10062](https://arxiv.org/abs/2309.10062)、COHERENT [arXiv 2409.15146](https://arxiv.org/abs/2409.15146)、MHRC [arXiv 2409.16030](https://arxiv.org/abs/2409.16030)；集中式与分散式的比较见 [arXiv 2309.15943](https://arxiv.org/abs/2309.15943)。
3. 多机器人系统框架：RoboOS [arXiv 2505.03673](https://arxiv.org/abs/2505.03673)、基于共享记忆的 RoboOS-NeXT [arXiv 2510.26536](https://arxiv.org/abs/2510.26536)。
4. 路径协调：MAPF 的定义与评测 [arXiv 1906.08291](https://arxiv.org/abs/1906.08291)、PRIMAL [arXiv 1809.03531](https://arxiv.org/abs/1809.03531)、LaCAM [arXiv 2211.13432](https://arxiv.org/abs/2211.13432)、滚动时域的 RHCR [arXiv 2005.07371](https://arxiv.org/abs/2005.07371)。
5. 任务分配：图注意力协调 [arXiv 1912.02059](https://arxiv.org/abs/1912.02059)、人机团队调度 [arXiv 2301.13279](https://arxiv.org/abs/2301.13279)、胶囊注意力网络 [arXiv 2205.03321](https://arxiv.org/abs/2205.03321)。
6. 紧耦合协作：多机器人非抓取协作的流匹配联合生成 [arXiv 2511.10874](https://arxiv.org/abs/2511.10874)；SAI 用单操作员课程学习耦合策略 [arXiv 2606.16490](https://arxiv.org/abs/2606.16490)；数据生成见 [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md) 方向 3。
7. 用世界模型评估联合动作：MA-WAM 先由策略提出候选联合动作，再用世界模型打分 [arXiv 2609.31281](https://arxiv.org/abs/2609.31281)。
8. 人机共处：PARTNR [arXiv 2411.00081](https://arxiv.org/abs/2411.00081)、Habitat 3.0 [arXiv 2310.13724](https://arxiv.org/abs/2310.13724)。

## 4. 可以写成论文的方向

### 4.1 异构机器人与设备的联合动作生成

- 类型：方法
- 研究问题：机械臂、AGV、人形和机床共同完成一个工单时，怎样生成联合动作，并用世界模型评估？
- 已有工作与空白：MA-WAM 在 MAMuJoCo、SMAC、MPE 的 30 个离线 MARL 设置上，比直接执行平均提升 22.0% [arXiv 2609.31281](https://arxiv.org/abs/2609.31281)；这些环境中的智能体是同类的。工厂中的异构联合动作还未见研究（分析判断）。
- 怎样验证：工单完成时间、冲突次数；与独立规划和规则基线对比。

### 4.2 工厂多机器人协作基准

- 类型：基准
- 研究问题：设计含交接、共用工位、通道冲突的多机器人任务集，并给出 MARL、LLM 规划、MAPF 三类方法的基线。
- 已有工作与空白：RoboFactory 关注多臂操作的组合约束 [P13](../../papers/P13_RoboFactory_2503.16408v1.pdf)；robotic-warehouse 环境和 MAPF 基准关注仓储运输 [arXiv 2006.07869](https://arxiv.org/abs/2006.07869) [arXiv 1906.08291](https://arxiv.org/abs/1906.08291)。同时含机床状态的协作基准还没有（分析判断）。
- 怎样验证：任务覆盖面、基线结果、可复现性。

### 4.3 LLM 协作规划与学习式协调的分工

- 类型：方法
- 研究问题：LLM 负责任务分解、学习式方法负责实时协调时，怎样分工最合适？
- 已有工作与空白：[arXiv 2309.15943](https://arxiv.org/abs/2309.15943) 比较了集中式与分散式的 LLM 多机器人规划；COHERENT、MHRC 处理异构机器人 [arXiv 2409.15146](https://arxiv.org/abs/2409.15146) [arXiv 2409.16030](https://arxiv.org/abs/2409.16030)。
- 怎样验证：成功率、规划时延、通信量。

## 6. 对应的链路

- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 高价值参考文献

### 工厂中的多机器人

- **RoboFactory: Exploring Embodied Agent Collaboration with Compositional Constraints**（2025），[P13 本地 PDF](../../papers/P13_RoboFactory_2503.16408v1.pdf)：RoboFactory：多具身智能体协作的组合约束。
- **Learning Multi-Agent Task Assignment and Navigation in the Factory: from Simulation to Real Robots**（2026），[P39 本地 PDF](../../papers/P39_FMAPPO_Machine_Tending_2609.14567v1.pdf)：FMAPPO：工厂中多机器人的分工与导航，从仿真到真实。
- **World Dreamer v5-lite: A Multi-Robot World Action Model with One Dreamer**（2026），[arXiv 2610.37518](https://arxiv.org/abs/2610.37518)：World Dreamer v5-lite：共享世界状态的多机器人 WAM。
- **MA-WAM: Multi-Agent World-Action Model for Test-Time Planning**（2026），[arXiv 2609.31281](https://arxiv.org/abs/2609.31281)：MA-WAM：用世界模型评估候选联合动作。

### MARL 算法与基准

- **The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games**（2021），[arXiv 2103.01955](https://arxiv.org/abs/2103.01955)：MAPPO：PPO 在合作多智能体任务上的效果。
- **QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning**（2018），[arXiv 1803.11485](https://arxiv.org/abs/1803.11485)：QMIX：单调值分解。
- **Trust Region Policy Optimisation in Multi-Agent Reinforcement Learning**（2021），[arXiv 2109.11251](https://arxiv.org/abs/2109.11251)：HATRPO／HAPPO：异构智能体的信赖域方法。
- **Heterogeneous Multi-Robot Reinforcement Learning**（2023），[arXiv 2301.07137](https://arxiv.org/abs/2301.07137)：HetGPPO：异构多机器人的图策略。
- **Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks**（2020），[arXiv 2006.07869](https://arxiv.org/abs/2006.07869)：合作 MARL 算法的基准比较（EPyMARL）。

### LLM 多机器人协作

- **RoCo: Dialectic Multi-Robot Collaboration with Large Language Models**（2023），[arXiv 2307.04738](https://arxiv.org/abs/2307.04738)：RoCo：多机械臂的对话式协作。
- **Building Cooperative Embodied Agents Modularly with Large Language Models**（2023），[arXiv 2307.02485](https://arxiv.org/abs/2307.02485)：CoELA：模块化的协作具身智能体。
- **SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models**（2023），[arXiv 2309.10062](https://arxiv.org/abs/2309.10062)：SMART-LLM：多机器人任务规划。
- **COHERENT: Collaboration of Heterogeneous Multi-Robot System with Large Language Models**（2024），[arXiv 2409.15146](https://arxiv.org/abs/2409.15146)：COHERENT：异构多机器人协作。
- **MHRC: Closed-loop Decentralized Multi-Heterogeneous Robot Collaboration with Large Language Models**（2024），[arXiv 2409.16030](https://arxiv.org/abs/2409.16030)：MHRC：闭环、分散式的异构多机器人协作。
- **Scalable Multi-Robot Collaboration with Large Language Models: Centralized or Decentralized Systems?**（2023），[arXiv 2309.15943](https://arxiv.org/abs/2309.15943)：集中式与分散式 LLM 多机器人系统的比较。
- **RoboOS: A Hierarchical Embodied Framework for Cross-Embodiment and Multi-Agent Collaboration**（2025），[arXiv 2505.03673](https://arxiv.org/abs/2505.03673)：RoboOS：大脑—小脑的多机器人系统。
- **RoboOS-NeXT: A Unified Memory-based Framework for Lifelong, Scalable, and Robust Multi-Robot Collaboration**（2025），[arXiv 2510.26536](https://arxiv.org/abs/2510.26536)：RoboOS-NeXT：基于统一记忆的终身多机器人协作。

### 路径协调与任务分配

- **Multi-Agent Pathfinding: Definitions, Variants, and Benchmarks**（2019），[arXiv 1906.08291](https://arxiv.org/abs/1906.08291)：MAPF 的定义、变体与基准。
- **PRIMAL: Pathfinding via Reinforcement and Imitation Multi-Agent Learning**（2018），[arXiv 1809.03531](https://arxiv.org/abs/1809.03531)：PRIMAL：强化学习与模仿学习结合的分布式路径规划。
- **LaCAM: Search-Based Algorithm for Quick Multi-Agent Pathfinding**（2022），[arXiv 2211.13432](https://arxiv.org/abs/2211.13432)：LaCAM：大规模 MAPF 的搜索方法。
- **Lifelong Multi-Agent Path Finding in Large-Scale Warehouses**（2020），[arXiv 2005.07371](https://arxiv.org/abs/2005.07371)：RHCR：终身 MAPF 的滚动时域方法。
- **Learning to Dynamically Coordinate Multi-Robot Teams in Graph Attention Networks**（2019），[arXiv 1912.02059](https://arxiv.org/abs/1912.02059)：用图注意力网络动态协调多机器人团队。
- **Learning Coordination Policies over Heterogeneous Graphs for Human-Robot Teams via Recurrent Neural Schedule Propagation**（2023），[arXiv 2301.13279](https://arxiv.org/abs/2301.13279)：异构图上的人机团队调度策略。
- **Learning Scalable Policies over Graphs for Multi-Robot Task Allocation using Capsule Attention Networks**（2022），[arXiv 2205.03321](https://arxiv.org/abs/2205.03321)：胶囊注意力网络做可扩展的多机器人任务分配。

### 紧耦合协作与人机共处

- **Collaborative Multi-Robot Non-Prehensile Manipulation via Flow-Matching Co-Generation**（2025），[arXiv 2511.10874](https://arxiv.org/abs/2511.10874)：多机器人非抓取协作：流匹配联合生成加多机器人运动规划。
- **Robots that Collaborate: Sequential Asymmetric Imitation for Learning Coupled Robot Policies**（2026），[arXiv 2606.16490](https://arxiv.org/abs/2606.16490)：SAI：学习耦合的多机器人策略。
- **PARTNR: A Benchmark for Planning and Reasoning in Embodied Multi-agent Tasks**（2024），[arXiv 2411.00081](https://arxiv.org/abs/2411.00081)：PARTNR：多智能体具身任务的规划与推理基准。
- **Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots**（2023），[arXiv 2310.13724](https://arxiv.org/abs/2310.13724)：Habitat 3.0：人、虚拟人与机器人共处的仿真。

## 8. 参考项目

- [marlbenchmark/on-policy](https://github.com/marlbenchmark/on-policy)：MAPPO
- [oxwhirl/pymarl](https://github.com/oxwhirl/pymarl)：QMIX 等
- [uoe-agents/epymarl](https://github.com/uoe-agents/epymarl)：EPyMARL
- [semitable/robotic-warehouse](https://github.com/semitable/robotic-warehouse)：多机器人仓储环境
- [PKU-MARL/HARL](https://github.com/PKU-MARL/HARL)：HAPPO／HATRPO
- [bold-lab-ai/JaxMARL](https://github.com/bold-lab-ai/JaxMARL)：JAX 版 MARL 环境与算法
- [Farama-Foundation/PettingZoo](https://github.com/Farama-Foundation/PettingZoo)：多智能体环境接口
- [Kei18/lacam](https://github.com/Kei18/lacam)：LaCAM
- [Jiaoyang-Li/RHCR](https://github.com/Jiaoyang-Li/RHCR)：RHCR
- [gsartoretti/PRIMAL](https://github.com/gsartoretti/PRIMAL)：PRIMAL
- [MAPF-Competition/Start-Kit](https://github.com/MAPF-Competition/Start-Kit)：MAPF 竞赛起步代码
- [facebookresearch/habitat-lab](https://github.com/facebookresearch/habitat-lab)：Habitat
- [facebookresearch/partnr-planner](https://github.com/facebookresearch/partnr-planner)：PARTNR
- [FlagOpen/RoboOS](https://github.com/FlagOpen/RoboOS)：RoboOS
- [IranQin/robofactory](https://github.com/IranQin/robofactory)：RoboFactory

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
