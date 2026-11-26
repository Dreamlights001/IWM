# W11 反事实与主动数据

> 阶段：S3 整厂层：预测与决策　·　总看板：[research_board.html](../research_board.html#W11)

从同一快照出发对动作做系统扰动，生成“同初态、不同动作”的数据；再按模型的不确定性，挑选最值得生成或采集的状态。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W03（车间场景生成）](../W03_车间场景生成/README.md)：快照与复位接口<br>[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md)：离散事件仿真 | [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：反事实数据<br>[W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：反事实数据 | ① 主动与反事实数据<br>⑥ 评测—部署飞轮 |

## 1. 为什么要做

真实工厂日志只记录实际执行过的派工和动作，几乎没有“如果当时派另一台机器人会怎样”的数据，而世界模型要学的正是动作的作用（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) Idea 4）。OpenWAM 报告，加入反事实监督后，前向动力学的 RGB 预测误差下降 34.5%；在 16 个同初态的结果中，识别出正确结果的比例从 21.1% 提高到 71.3% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)。

## 2. 输入与产物

**输入**

- [W03（车间场景生成）](../W03_车间场景生成/README.md)、[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的可复位仿真
- [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)、[W10（整厂层世界模型）](../W10_整厂层世界模型/README.md) 的模型与不确定性
- [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md) 的数据生成工具

**产物**

- 反事实数据集：同初态、多动作的转移
- 主动采样策略
- 稀有事件样本：故障、堵塞、死锁

## 3. 具体工作

1. 快照与复位：保证仿真能保存并恢复完整的运行状态，包括物理状态、PLC 状态和离散事件队列。
2. 设计扰动：整厂层扰动派工、路由、到料时间；工位层扰动技能参数和动作序列。
3. 反事实增强：CoDA 利用局部因果独立性拼接子状态 [arXiv 2007.02863](https://arxiv.org/abs/2007.02863)；MoCoDA 用学到的模型做反事实增强 [arXiv 2210.11287](https://arxiv.org/abs/2210.11287)。
4. 主动选择：按模型分歧或预测误差选状态，参考 Plan2Explore [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)、分歧探索 [arXiv 1906.04161](https://arxiv.org/abs/1906.04161)、好奇心 [arXiv 1705.05363](https://arxiv.org/abs/1705.05363)。
5. 学习生成分布：Learning to Simulate [arXiv 1810.02513](https://arxiv.org/abs/1810.02513)、Meta-Sim [arXiv 1904.11621](https://arxiv.org/abs/1904.11621) 让仿真参数分布朝对下游任务有用的方向调整。
6. 稀有事件：参考自动驾驶测试中的稀有事件仿真 [arXiv 1811.00145](https://arxiv.org/abs/1811.00145)，对故障和堵塞做重要性采样。
7. 用反事实数据训练后，检查模型对不同动作的预测是否真的不同 [P77](../../papers/P77_WorldEcho_2608.24885v2.pdf)。

## 4. 可以写成论文的方向

### 4.1 整厂层的反事实数据生成与主动采样

- 类型：方法
- 研究问题：在离散事件仿真加物理仿真的联合环境中，怎样选择要扰动的状态和动作，用最少的仿真预算降低整厂层模型的误差？
- 已有工作与空白：CoDA、MoCoDA 在 RL 基准上做反事实增强 [arXiv 2007.02863](https://arxiv.org/abs/2007.02863) [arXiv 2210.11287](https://arxiv.org/abs/2210.11287)；OpenWAM 在机器人视频上验证了反事实数据的作用 [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)。整厂层还没有对应研究（分析判断）。
- 怎样验证：相同仿真预算下，主动采样与随机采样的误差曲线；在派工决策上的收益。

### 4.2 工厂稀有事件的定向生成

- 类型：方法
- 研究问题：机床报警、夹具失败、AGV 堵塞这类事件少见但关键，怎样定向生成，同时保持分布可信？
- 已有工作与空白：稀有事件仿真用于自动驾驶测试 [arXiv 1811.00145](https://arxiv.org/abs/1811.00145)；工厂场景还未见对应研究（分析判断）。
- 怎样验证：稀有事件的预测召回率；生成样本与真实日志中事件分布的一致性。

## 5. 所在闭环

- ① 主动与反事实数据：W09·W10 找出误差大或不确定的状态 → W11 选状态，设计动作扰动 → W03·W04·W05 从快照复位，执行并记录 → 回训模型。OpenWAM 报告，加入反事实监督后前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)；Plan2Explore 用模型集成的分歧选择探索目标 [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)。
- ⑥ 评测—部署飞轮：W16 评测，找出失败模式 → W17 部署，记录失败与人工干预 → W07·W04 采集真实片段与事件日志 → W11·W05 生成反事实与针对性数据 → 回训后再评测。Fleet-DAgger 研究多台机器人共享少量人工监督 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人上做车队级离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 6. 对应的链路

- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 高价值参考文献

### 反事实数据

- **Counterfactual Data Augmentation using Locally Factored Dynamics**（2020），[arXiv 2007.02863](https://arxiv.org/abs/2007.02863)：CoDA：利用局部因果结构做反事实数据增强。
- **MoCoDA: Model-based Counterfactual Data Augmentation**（2022），[arXiv 2210.11287](https://arxiv.org/abs/2210.11287)：MoCoDA：基于模型的反事实数据增强。
- **OpenWAM: An Open Framework for Composable World-Action Models**（2026），[arXiv 2610.07922](https://arxiv.org/abs/2610.07922)：OpenWAM：反事实转移改善逆动力学与前向动力学模型。

### 主动与好奇心驱动的探索

- **Planning to Explore via Self-Supervised World Models**（2020），[arXiv 2005.05960](https://arxiv.org/abs/2005.05960)：Plan2Explore：用世界模型规划探索，模型分歧作为内在奖励。
- **Self-Supervised Exploration via Disagreement**（2019），[arXiv 1906.04161](https://arxiv.org/abs/1906.04161)：用模型集成的分歧做自监督探索。
- **Curiosity-driven Exploration by Self-supervised Prediction**（2017），[arXiv 1705.05363](https://arxiv.org/abs/1705.05363)：好奇心驱动的探索：自监督预测误差作为奖励。

### 学习生成分布与稀有事件

- **Learning To Simulate**（2018），[arXiv 1810.02513](https://arxiv.org/abs/1810.02513)：Learning to Simulate：学习仿真器参数以服务下游任务。
- **Meta-Sim: Learning to Generate Synthetic Datasets**（2019），[arXiv 1904.11621](https://arxiv.org/abs/1904.11621)：Meta-Sim：学习生成合成数据集的分布。
- **Scalable End-to-End Autonomous Vehicle Testing via Rare-event Simulation**（2018），[arXiv 1811.00145](https://arxiv.org/abs/1811.00145)：用稀有事件仿真做自动驾驶端到端测试。

### 动作遵循性

- **Do Robotic World Models Really Follow Actions? Diagnosing and Aligning Action-Conditioned Generation for Policy Learning**（2026），[P77 本地 PDF](../../papers/P77_WorldEcho_2608.24885v2.pdf)：WorldEcho：检查世界模型是否遵循动作。

## 8. 参考项目

暂未找到可直接复用的开源实现；实现主要依赖 [W03（车间场景生成）](../W03_车间场景生成/README.md)、[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的快照与复位接口。

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对，2026-11-27 补充）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
