# W17 部署与数据飞轮

> 阶段：S5 部署与数据飞轮　·　总看板：[research_board.html](../research_board.html#W17)

先接入一个真实工位，其余仍在仿真里；记录失败和人工干预，自动转成新数据，持续更新子级和整厂层模型。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W16（基准与评测）](../W16_基准与评测/README.md)：验收结果<br>[W15（安全与约束）](../W15_安全与约束/README.md)：上线前校核 | — | ⑥ 评测—部署飞轮 |

## 1. 为什么要做

部署后会遇到训练数据没有覆盖的情况。已有的车队学习工作：Fleet-DAgger 研究多台机器人共享少量人工监督，在 100 台仿真机器人上，人工投入回报（ROHE）比基线高至多 8.8 倍 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人、8 个真实任务上做车队级的离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；物流场景的数据飞轮用世界模型合成分布外的恢复数据（WM-DAgger）[arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 2. 输入与产物

**输入**

- [W16（基准与评测）](../W16_基准与评测/README.md) 验收通过的模型与策略
- [W15（安全与约束）](../W15_安全与约束/README.md) 的上线前校核
- 真实工位
- 监控与人工干预工具

**产物**

- 混合运行（部分工位在仿真）的记录
- 失败与干预日志
- 数据选择与回训流程
- 回归测试

## 3. 具体工作

1. 混合运行：先接一个真实工位，其余在仿真（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 阶段 5），记录预测误差与决策收益。
2. 人工干预：按 Fleet-DAgger 的思路在机器人之间分配人工 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)，干预数据直接进入训练集。
3. 在线改进：SOAR 用基础模型做自主改进 [arXiv 2407.20635](https://arxiv.org/abs/2407.20635)；SERL、HIL-SERL 做真实世界 RL [arXiv 2401.16013](https://arxiv.org/abs/2401.16013) [arXiv 2410.21845](https://arxiv.org/abs/2410.21845)；RLDG 把 RL 专家蒸馏进通用策略 [arXiv 2412.09858](https://arxiv.org/abs/2412.09858)。
4. 车队级与数据飞轮：LWD [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；Robot-Powered Data Flywheel 让部署中的机器人成为数据来源 [arXiv 2511.19647](https://arxiv.org/abs/2511.19647)；F-ACIL 按因素分解与组合数据，在示范减少 5–10 倍时性能仍提高 45% 以上 [arXiv 2603.25583](https://arxiv.org/abs/2603.25583)；仿真中的自改进飞轮见 EmbodiedSmith [arXiv 2610.07969](https://arxiv.org/abs/2610.07969)。
5. 失败自动转成反事实：把失败片段的初态送入 [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)，在仿真中生成不同动作的结果（闭环 ⑥ 和 ①）。
6. 模型服务与监控：ROSA [arXiv 2607.01088](https://arxiv.org/abs/2607.01088)；失败检测 AHA [arXiv 2410.00371](https://arxiv.org/abs/2410.00371)。

## 4. 可以写成论文的方向

### 4.1 从部署失败到仿真反事实的自动回流

- 类型：系统＋方法
- 研究问题：部署中的失败片段能否自动重建为仿真初态，生成反事实数据并回训，减少同类失败？
- 已有工作与空白：WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)；Robot-Powered Data Flywheel 把部署中的机器人变成数据来源 [arXiv 2511.19647](https://arxiv.org/abs/2511.19647)。把失败回流到仿真反事实，还未见研究（分析判断）。
- 怎样验证：同类失败的复发率；所需的人工干预次数。

### 4.2 整厂层模型的在线校准与漂移检测

- 类型：方法
- 研究问题：整厂层模型上线后，怎样用新的事件日志持续校准，并及早发现分布漂移？
- 已有工作与空白：车队学习工作更新的是机器人策略 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349) [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；整厂层模型的持续更新还很少研究（分析判断）。
- 怎样验证：预测误差随时间的变化；漂移检测的提前量。

## 5. 所在闭环

- ⑥ 评测—部署飞轮：W16 评测，找出失败模式 → W17 部署，记录失败与人工干预 → W07·W04 采集真实片段与事件日志 → W11·W05 生成反事实与针对性数据 → 回训后再评测。Fleet-DAgger 研究多台机器人共享少量人工监督 [arXiv 2206.14349](https://arxiv.org/abs/2206.14349)；LWD 在 16 台双臂机器人上做车队级离线到在线 RL [arXiv 2605.00416](https://arxiv.org/abs/2605.00416)；WM-DAgger 用世界模型合成恢复数据 [arXiv 2606.05960](https://arxiv.org/abs/2606.05960)。

## 6. 对应的链路

- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 高价值参考文献

### 车队学习与人工监督

- **Fleet-DAgger: Interactive Robot Fleet Learning with Scalable Human Supervision**（2022），[arXiv 2206.14349](https://arxiv.org/abs/2206.14349)：Fleet-DAgger：机器人车队共享人工监督。
- **Learning While Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies**（2026），[arXiv 2605.00416](https://arxiv.org/abs/2605.00416)：LWD：车队级离线到在线 RL，持续后训练 VLA。

### 真实世界自主改进

- **Autonomous Improvement of Instruction Following Skills via Foundation Models**（2024），[arXiv 2407.20635](https://arxiv.org/abs/2407.20635)：SOAR：用基础模型自主改进指令跟随技能。
- **SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning**（2024），[arXiv 2401.16013](https://arxiv.org/abs/2401.16013)：SERL：样本高效的真实世界 RL 软件。
- **Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning**（2024），[arXiv 2410.21845](https://arxiv.org/abs/2410.21845)：HIL-SERL：人在回路的真实世界 RL。
- **RLDG: Robotic Generalist Policy Distillation via Reinforcement Learning**（2024），[arXiv 2412.09858](https://arxiv.org/abs/2412.09858)：RLDG：RL 专家数据蒸馏进通用策略。

### 数据飞轮

- **Towards a Data Flywheel for Embodied Intelligence in Logistics**（2026），[arXiv 2606.05960](https://arxiv.org/abs/2606.05960)：物流具身智能的数据飞轮，含 WM-DAgger。
- **Robot-Powered Data Flywheels: Deploying Robots in the Wild for Continual Data Collection and Foundation Model Adaptation**（2025），[arXiv 2511.19647](https://arxiv.org/abs/2511.19647)：Robot-Powered Data Flywheel：部署中持续采集并适配基础模型。
- **Towards Generalizable Robotic Data Flywheel: High-Dimensional Factorization and Composition**（2026），[arXiv 2603.25583](https://arxiv.org/abs/2603.25583)：F-ACIL：数据按因素分解与组合的数据飞轮。
- **EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation**（2026），[arXiv 2610.07969](https://arxiv.org/abs/2610.07969)：EmbodiedSmith：仿真中的递归自改进数据飞轮。

### 部署支撑

- **ROSA: A Robotics Foundation Model Serving System for Robot Factories**（2026），[arXiv 2607.01088](https://arxiv.org/abs/2607.01088)：ROSA：机器人工厂的模型推理服务。
- **AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation**（2024），[arXiv 2410.00371](https://arxiv.org/abs/2410.00371)：AHA：失败检测与推理。

## 8. 参考项目

- [rail-berkeley/serl](https://github.com/rail-berkeley/serl)：SERL
- [rail-berkeley/hil-serl](https://github.com/rail-berkeley/hil-serl)：HIL-SERL

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
