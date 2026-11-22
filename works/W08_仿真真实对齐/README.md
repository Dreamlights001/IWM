# W08 仿真—真实对齐

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W08)

用真实数据校准仿真的物理参数、设备节拍和失败率，为仿真缺的部分学残差，并检验仿真评测能否预测真实结果。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W07（真实数据采集与同步）](../W07_真实数据采集与同步/README.md)：真实轨迹与日志 | [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：校准参数与残差 | ② 仿真—真实校准 |

## 1. 为什么要做

S1 的大部分数据来自仿真。仿真与现场的差距有两层：机器人层是动力学、接触和外观；整厂层是节拍分布、失败率和人工干预。机器人层已有较多方法：Sim-and-Real Co-Training 报告，仿真数据使真实任务成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)；SimplerEnv 显示仿真评测与真实结果强相关 [arXiv 2405.05941](https://arxiv.org/abs/2405.05941)。整厂层的校准还很少有人系统地做（分析判断）。

## 2. 输入与产物

**输入**

- [W07（真实数据采集与同步）](../W07_真实数据采集与同步/README.md) 的真实数据
- [W02（设备资产生成）](../W02_设备资产生成/README.md)–[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的仿真模型
- [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md) 的仿真数据

**产物**

- 校准后的物理参数与设备节拍分布
- 残差模型
- 仿真—真实混合训练的配方
- 仿真评测与真实结果的相关性报告

## 3. 具体工作

1. 以域随机化为起点：视觉随机化 [arXiv 1703.06907](https://arxiv.org/abs/1703.06907)、动力学随机化 [arXiv 1710.06537](https://arxiv.org/abs/1710.06537)。
2. 系统辨识：ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；SimOpt 用真实轨迹调整仿真参数分布 [arXiv 1810.05687](https://arxiv.org/abs/1810.05687)；BayesSim 推断参数后验 [arXiv 1906.01728](https://arxiv.org/abs/1906.01728)；RMA 让策略在线估计环境参数 [arXiv 2107.04034](https://arxiv.org/abs/2107.04034)。
3. 现场到仿真：RialTo 扫描现场并把真实示范迁入仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；Real-is-Sim 用以 60 Hz 与现场同步的动态数字孪生作为策略接口 [P58](../../papers/P58_Real_is_Sim_2504.03597v2.pdf)。
4. 残差：在解析仿真之上学残差分布 [P63](../../papers/P63_Simulator_Residual_Pushing_1808.03246v1.pdf)；人形用动作差值模型 [arXiv 2502.01143](https://arxiv.org/abs/2502.01143)。
5. 混合训练：参考 [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)；平推任务上的系统实验显示，仿真数据带来的提升会到达平台，增加真实数据能提高上限 [arXiv 2503.22634](https://arxiv.org/abs/2503.22634)；机理分析见 [arXiv 2604.13645](https://arxiv.org/abs/2604.13645)。
6. 整厂层校准：用真实事件日志校准节拍和失败率分布；可借鉴计算机模型的贝叶斯校准框架 [Kennedy & O’Hagan 2001](https://doi.org/10.1111/1467-9868.00294)。
7. 评测相关性：对同一组策略，比较仿真评测与真实评测的排名是否一致 [arXiv 2405.05941](https://arxiv.org/abs/2405.05941)。

## 4. 可以写成论文的方向

### 4.1 分层校准：同时校准机器人层物理与整厂层节拍

- 类型：方法
- 研究问题：机器人层参数（摩擦、质量、延迟）和整厂层参数（节拍、失败率）相互影响。能否联合校准，并量化各层残差对整厂吞吐预测的影响？
- 已有工作与空白：ASID、SimOpt、BayesSim 校准机器人层的物理参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf) [arXiv 1810.05687](https://arxiv.org/abs/1810.05687) [arXiv 1906.01728](https://arxiv.org/abs/1906.01728)；Kennedy–O’Hagan 框架校准一般计算机模型 [Kennedy & O’Hagan 2001](https://doi.org/10.1111/1467-9868.00294)。本轮检索没有找到把两层放在一起校准的工作。
- 怎样验证：校准前后的事件时间误差和吞吐预测误差；所需真实数据量。

### 4.2 工厂任务的仿真评测与真实结果相关性

- 类型：实证
- 研究问题：上下料、装夹等任务上，仿真中的策略排名能否预测真实排名？哪些仿真因素影响最大？
- 已有工作与空白：SimplerEnv 在桌面操作任务上显示强相关 [arXiv 2405.05941](https://arxiv.org/abs/2405.05941)；工厂任务涉及设备状态和长时程，还没有类似研究（分析判断）。
- 怎样验证：多组策略的仿真与真实成功率的相关系数；逐项去掉仿真因素后的变化。

### 4.3 工厂场景的仿真—真实混合训练

- 类型：实证
- 研究问题：设备状态、反光金属外观、高精度装夹，会怎样改变混合训练的最佳配比？
- 已有工作与空白：混合训练的经验规律来自桌面操作和平推任务 [arXiv 2503.24361](https://arxiv.org/abs/2503.24361) [arXiv 2503.22634](https://arxiv.org/abs/2503.22634) [arXiv 2604.13645](https://arxiv.org/abs/2604.13645)。
- 怎样验证：不同配比下的真实成功率曲线。

## 5. 所在闭环

- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。

## 6. 对应的链路

- [L2](../../链路/L2_扫描配准与数字孪生/README.md)：L2 扫描配准到 STEP 资产，并校准成数字孪生
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理

## 7. 高价值参考文献

### 随机化

- **Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World**（2017），[arXiv 1703.06907](https://arxiv.org/abs/1703.06907)：域随机化：随机化视觉。
- **Sim-to-Real Transfer of Robotic Control with Dynamics Randomization**（2017），[arXiv 1710.06537](https://arxiv.org/abs/1710.06537)：动力学随机化：随机化物理参数。

### 系统辨识与参数推断

- **ASID: Active Exploration for System Identification in Robotic Manipulation**（2024），[P60 本地 PDF](../../papers/P60_ASID_2404.12308v2.pdf)：ASID：主动探索做系统辨识。
- **Closing the Sim-to-Real Loop: Adapting Simulation Randomization with Real World Experience**（2018），[arXiv 1810.05687](https://arxiv.org/abs/1810.05687)：SimOpt：用真实经验闭环调整仿真随机化分布。
- **BayesSim: adaptive domain randomization via probabilistic inference for robotics simulators**（2019），[arXiv 1906.01728](https://arxiv.org/abs/1906.01728)：BayesSim：仿真参数的贝叶斯推断。
- **RMA: Rapid Motor Adaptation for Legged Robots**（2021），[arXiv 2107.04034](https://arxiv.org/abs/2107.04034)：RMA：快速运动适应，在线估计环境参数。
- **Bayesian calibration of computer models**（Kennedy & O’Hagan, JRSS-B, 2001），[链接](https://doi.org/10.1111/1467-9868.00294)：计算机模型的贝叶斯校准，含模型偏差项。

### 现场到仿真与残差

- **Reconciling Reality through Simulation: A Real-to-Sim-to-Real Approach for Robust Manipulation**（2024），[P59 本地 PDF](../../papers/P59_RialTo_2403.03949v3.pdf)：RialTo：现场到仿真再到现场。
- **Real-is-Sim: Bridging the Sim-to-Real Gap with a Dynamic Digital Twin**（2025），[P58 本地 PDF](../../papers/P58_Real_is_Sim_2504.03597v2.pdf)：Real-is-Sim：动态数字孪生作为策略接口。
- **Augmenting Physical Simulators with Stochastic Neural Networks: Case Study of Planar Pushing and Bouncing**（2018），[P63 本地 PDF](../../papers/P63_Simulator_Residual_Pushing_1808.03246v1.pdf)：在解析仿真之上用随机神经网络学残差。
- **ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills**（2025），[arXiv 2502.01143](https://arxiv.org/abs/2502.01143)：ASAP：学习动作差值来对齐仿真与真实。

### 混合训练

- **Sim-and-Real Co-Training: A Simple Recipe for Vision-Based Robotic Manipulation**（2025），[arXiv 2503.24361](https://arxiv.org/abs/2503.24361)：仿真—真实混合训练：真实成功率平均提高 38%。
- **Empirical Analysis of Sim-and-Real Cotraining of Diffusion Policies for Planar Pushing from Pixels**（2025），[arXiv 2503.22634](https://arxiv.org/abs/2503.22634)：平推任务上 50 多个真实策略的系统实验。
- **A Mechanistic Analysis of Sim-and-Real Co-Training in Generative Robot Policies**（2026），[arXiv 2604.13645](https://arxiv.org/abs/2604.13645)：混合训练为何有效的机理分析。

### 仿真评测

- **Evaluating Real-World Robot Manipulation Policies in Simulation**（2024），[arXiv 2405.05941](https://arxiv.org/abs/2405.05941)：SimplerEnv：仿真评测与真实结果强相关。

## 8. 参考项目

- [real-to-sim-to-real/RialToGUI](https://github.com/real-to-sim-to-real/RialToGUI)：RialTo 的场景搭建界面
- [rai-opensource/embodied_gaussians](https://github.com/rai-opensource/embodied_gaussians)：Real-is-Sim 使用的 Embodied Gaussians
- [simpler-env/SimplerEnv](https://github.com/simpler-env/SimplerEnv)：SimplerEnv

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
