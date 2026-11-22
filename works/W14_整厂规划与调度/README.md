# W14 整厂规划与调度

> 阶段：S3 整厂层：预测与决策　·　总看板：[research_board.html](../research_board.html#W14)

用整厂层世界模型做派工、路由和插单决策，并与规则派工、运筹优化和学习式调度比较。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W13（多机器人协作）](../W13_多机器人协作/README.md)：协作原语<br>[W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：整厂预测器<br>[W15（安全与约束）](../W15_安全与约束/README.md)：约束与屏蔽 | [W16（基准与评测）](../W16_基准与评测/README.md)：待评测策略 | ④ 世界模型—策略协同<br>⑤ 跨层一致 |

## 1. 为什么要做

传统排产把“上料一次要多久”当作常数或分布，不关心机器人和设备实际做了什么（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 1.3 节）。有了整厂层世界模型，规划器可以预测动作的后果：会不会抢通道，上料成功概率多少，机床什么时候真正启动。测试时规划的开销很小：MA-WAM 在 RTX 3090 上为 8 个候选做生成加评分共 428.0 ms，其中世界模型评分只占 13.4 ms [arXiv 2609.31281](https://arxiv.org/abs/2609.31281)，相对整厂层分钟级的决策周期可以忽略。

## 2. 输入与产物

**输入**

- [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md) 的整厂预测器
- [W13（多机器人协作）](../W13_多机器人协作/README.md) 的协作方法
- [W15（安全与约束）](../W15_安全与约束/README.md) 的约束
- [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的离散事件仿真

**产物**

- 整厂层规划器
- 与规则基线、OR-Tools、学习式调度的对比
- 混合运行时的决策收益

## 3. 具体工作

1. 基线：规则派工；用 OR-Tools 的 CP-SAT 求解作业车间调度。
2. 学习式调度：L2D 用图网络和 RL 学习派工 [arXiv 2010.12367](https://arxiv.org/abs/2010.12367)；神经组合优化 [arXiv 1611.09940](https://arxiv.org/abs/1611.09940)、注意力路由模型 [arXiv 1803.08475](https://arxiv.org/abs/1803.08475)；RL4CO 提供统一实现。
3. 在模型中搜索：MuZero [arXiv 1911.08265](https://arxiv.org/abs/1911.08265)、EfficientZero [arXiv 2111.00210](https://arxiv.org/abs/2111.00210)；扩散规划 Diffuser [arXiv 2205.09991](https://arxiv.org/abs/2205.09991)；测试时规划 MA-WAM [arXiv 2609.31281](https://arxiv.org/abs/2609.31281)。
4. 在模型中训练整厂层策略：DreamerV3 [P02](../../papers/P02_DreamerV3_2301.04104v2.pdf)、TD-MPC2 [P03](../../papers/P03_TD_MPC2_2310.16828v2.pdf)（见 [L9](../../链路/L9_潜变量模型式强化学习/README.md)）；分层规划 Director [arXiv 2206.04114](https://arxiv.org/abs/2206.04114)。
5. 处理外生扰动：AWMP 把已知的车间转移和不确定的订单到达分开，用 LLM 预测后者 [P38](../../papers/P38_AWMP_Dynamic_Scheduling_2610.29308v1.pdf)。
6. LLM 调度：Starjob [arXiv 2503.01877](https://arxiv.org/abs/2503.01877)、LLMs can Schedule [arXiv 2408.06993](https://arxiv.org/abs/2408.06993)、ReflecSched（动态柔性作业车间，平均 RPD 6.09%）[arXiv 2508.01724](https://arxiv.org/abs/2508.01724)。
7. 推理服务：ROSA 按工厂目标调度机器人基础模型的推理，报告工厂生产率最高提高 12.06 倍 [arXiv 2607.01088](https://arxiv.org/abs/2607.01088)。

## 4. 可以写成论文的方向

### 4.1 调度与机器人执行的联合优化

- 类型：方法
- 研究问题：把机器人执行的不确定性（耗时、失败）纳入派工决策后，吞吐和准时率能提高多少？
- 已有工作与空白：AWMP 处理订单到达的不确定性 [P38](../../papers/P38_AWMP_Dynamic_Scheduling_2610.29308v1.pdf)；L2D 等学习式调度在已知加工时间的作业车间实例上训练 [arXiv 2010.12367](https://arxiv.org/abs/2010.12367)。用子级自报告驱动调度，还未见研究（分析判断）。
- 怎样验证：与常数耗时假设的调度比较吞吐、在制品、准时率。

### 4.2 学习式整厂世界模型上的测试时规划

- 类型：方法
- 研究问题：用学习式模型代替离散事件仿真做规划，决策质量和速度怎样权衡？
- 已有工作与空白：MA-WAM 在 MARL 基准上做测试时规划 [arXiv 2609.31281](https://arxiv.org/abs/2609.31281)；MuZero 类方法在学习式模型中搜索 [arXiv 1911.08265](https://arxiv.org/abs/1911.08265)。工厂调度上还没有对照研究（分析判断）。
- 怎样验证：候选数、搜索深度与决策收益的关系；与在显式仿真中规划的对比。

## 5. 所在闭环

- ④ 世界模型—策略协同：W09·W10 预测动作后果 → W12·W14 在模型中规划或训练 → 仿真或真实执行 记录新轨迹 → 更新模型。World-in-World 发现，用动作—观测数据做后训练，比换用更强的预训练视频生成器更有效 [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)；DreamerV3、TD-MPC2 交替更新模型与策略 [P02](../../papers/P02_DreamerV3_2301.04104v2.pdf) [P03](../../papers/P03_TD_MPC2_2310.16828v2.pdf)。
- ⑤ 跨层一致：W12 执行技能，返回事件与实际耗时 → W09 工位层预测同一事件 → W10 整厂层预测同一事件 → W14 按预测下发新命令 → 下发命令。[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) Idea 3 提出跨层一致性训练，尚未验证；H-WM 联合预测逻辑状态和视觉状态的转移 [arXiv 2602.11291](https://arxiv.org/abs/2602.11291)。

## 6. 对应的链路

- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件
- [L9](../../链路/L9_潜变量模型式强化学习/README.md)：L9 潜变量模型式强化学习
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 高价值参考文献

### 学习式调度与组合优化

- **Learning to Dispatch for Job Shop Scheduling via Deep Reinforcement Learning**（2020），[arXiv 2010.12367](https://arxiv.org/abs/2010.12367)：L2D：用深度 RL 学习作业车间派工。
- **Neural Combinatorial Optimization with Reinforcement Learning**（2016），[arXiv 1611.09940](https://arxiv.org/abs/1611.09940)：用 RL 训练的神经组合优化。
- **Attention, Learn to Solve Routing Problems!**（2018），[arXiv 1803.08475](https://arxiv.org/abs/1803.08475)：注意力模型求解路由问题。

### 模型中的搜索与规划

- **Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model**（2019），[arXiv 1911.08265](https://arxiv.org/abs/1911.08265)：MuZero：在学到的模型中规划。
- **Mastering Atari Games with Limited Data**（2021），[arXiv 2111.00210](https://arxiv.org/abs/2111.00210)：EfficientZero：样本高效的 MuZero 变体。
- **Planning with Diffusion for Flexible Behavior Synthesis**（2022），[arXiv 2205.09991](https://arxiv.org/abs/2205.09991)：Diffuser：用扩散模型做规划。
- **MA-WAM: Multi-Agent World-Action Model for Test-Time Planning**（2026），[arXiv 2609.31281](https://arxiv.org/abs/2609.31281)：MA-WAM：多智能体测试时规划，给出 RTX 3090 与 A100 上的耗时。

### 模型式强化学习

- **Mastering Diverse Domains through World Models**（2023），[P02 本地 PDF](../../papers/P02_DreamerV3_2301.04104v2.pdf)：DreamerV3：在想象轨迹中训练策略。
- **TD-MPC2: Scalable, Robust World Models for Continuous Control**（2023），[P03 本地 PDF](../../papers/P03_TD_MPC2_2310.16828v2.pdf)：TD-MPC2：潜空间中的模型预测控制。
- **Deep Hierarchical Planning from Pixels**（2022），[arXiv 2206.04114](https://arxiv.org/abs/2206.04114)：Director：分层规划。

### 外生扰动与 LLM 调度

- **LLM-Based Exogenous World Modeling for Dynamic Scheduling**（2026），[P38 本地 PDF](../../papers/P38_AWMP_Dynamic_Scheduling_2610.29308v1.pdf)：AWMP：动态排产的外生世界模型。
- **Starjob: Dataset for LLM-Driven Job Shop Scheduling**（2025），[arXiv 2503.01877](https://arxiv.org/abs/2503.01877)：Starjob：面向 LLM 的作业车间调度数据集。
- **LLMs can Schedule**（2024），[arXiv 2408.06993](https://arxiv.org/abs/2408.06993)：LLMs can Schedule：LLM 求解作业车间调度。
- **ReflecSched: Solving Dynamic Flexible Job-Shop Scheduling via LLM-Powered Hierarchical Reflection**（2025），[arXiv 2508.01724](https://arxiv.org/abs/2508.01724)：ReflecSched：LLM 分层反思求解动态柔性作业车间调度。

### 推理服务

- **ROSA: A Robotics Foundation Model Serving System for Robot Factories**（2026），[arXiv 2607.01088](https://arxiv.org/abs/2607.01088)：ROSA：机器人工厂的基础模型推理服务系统。

## 8. 参考项目

- [zcaicaros/L2D](https://github.com/zcaicaros/L2D)：L2D
- [ai4co/rl4co](https://github.com/ai4co/rl4co)：组合优化 RL 库
- [google/or-tools](https://github.com/google/or-tools)：OR-Tools，含 CP-SAT
- [danijar/dreamerv3](https://github.com/danijar/dreamerv3)：DreamerV3
- [nicklashansen/tdmpc2](https://github.com/nicklashansen/tdmpc2)：TD-MPC2
- [danijar/director](https://github.com/danijar/director)：Director

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
