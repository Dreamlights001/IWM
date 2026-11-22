# W06 全身动作数据

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W06)

机器人是人形或轮式人形时，把人体动作重定向到你的 URDF，补充工厂作业动作，训练全身控制器（WBC）。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| — | [W12（子级技能与端口）](../W12_子级技能与端口/README.md)：全身动作库与跟踪器 | — |

## 1. 为什么要做

全身控制器通常先学会跟踪人体动作。重定向质量直接影响策略：GMR 发现，重定向数据中的伪影会明显降低策略的鲁棒性，动态或长序列动作尤其明显 [arXiv 2510.02252](https://arxiv.org/abs/2510.02252)。公开动作库多是日常动作，工厂里的搬运、推车、弯腰上料需要补充。机器人和人体拓扑不同时（如轮式人形），重定向要专门处理 [arXiv 2609.11357](https://arxiv.org/abs/2609.11357)。机器人是机械臂或移动底座时，本工作可以跳过。

## 2. 输入与产物

**输入**

- 你的机器人 URDF
- 人体动作捕捉数据或视频
- 第一人称人手数据（可选）

**产物**

- 适配你的 URDF 的动作库，含工厂作业动作
- 动作跟踪策略或 WBC
- 向上层暴露的命令端口：根速度、末端位姿或关键点（供 [W12（子级技能与端口）](../W12_子级技能与端口/README.md)）

## 3. 具体工作

1. 重定向：GMR [arXiv 2510.02252](https://arxiv.org/abs/2510.02252)、PHC [arXiv 2305.06456](https://arxiv.org/abs/2305.06456)；要保持与物体、地形的接触关系时用 OmniRetarget [arXiv 2509.26633](https://arxiv.org/abs/2509.26633)；轮式人形参考 [arXiv 2609.11357](https://arxiv.org/abs/2609.11357)。
2. 补充工厂作业动作：搬运（MOVER 用多阶段 RL 从人体动作学习人形搬运 [arXiv 2610.14561](https://arxiv.org/abs/2610.14561)）、推车、蹲下取放。可以自己动捕，也可以从视频估计人体动作。
3. 训练跟踪策略：GMT [arXiv 2506.14770](https://arxiv.org/abs/2506.14770)、BeyondMimic [arXiv 2508.08241](https://arxiv.org/abs/2508.08241)、AMO [arXiv 2505.03738](https://arxiv.org/abs/2505.03738)；统一的命令端口参考 HOVER [arXiv 2410.21229](https://arxiv.org/abs/2410.21229)。
4. 仿真到真实：ASAP 用真实数据学习动作差值模型来对齐仿真与真实动力学 [arXiv 2502.01143](https://arxiv.org/abs/2502.01143)。
5. 遥操作采集：H2O、OmniH2O、HumanPlus 用人体动作实时遥操作人形并采集数据 [arXiv 2403.04436](https://arxiv.org/abs/2403.04436) [arXiv 2406.08858](https://arxiv.org/abs/2406.08858) [arXiv 2406.10454](https://arxiv.org/abs/2406.10454)。
6. 第一人称人手数据：Ego4D [arXiv 2110.07058](https://arxiv.org/abs/2110.07058)；EgoDex 有 829 小时第一人称视频，带 3D 手部与手指跟踪，覆盖 194 个桌面任务 [arXiv 2505.11709](https://arxiv.org/abs/2505.11709)。

## 4. 可以写成论文的方向

### 4.1 工厂作业动作库与重定向质量评估

- 类型：数据集＋方法
- 研究问题：搬运、推车、弯腰上料这类动作重定向到不同机器人后，哪些伪影最影响跟踪策略？能否自动检测和修正？
- 已有工作与空白：GMR 在 LAFAN1 的一个子集上评估重定向质量对策略的影响 [arXiv 2510.02252](https://arxiv.org/abs/2510.02252)；OmniRetarget 保持人、物体、地形之间的交互关系 [arXiv 2509.26633](https://arxiv.org/abs/2509.26633)。工厂作业动作的数据和评估还很少（分析判断）。
- 怎样验证：跟踪误差、跌倒率、真实机器人上的成功率；对比不同重定向方法。

### 4.2 拓扑不匹配机器人的全身动作迁移

- 类型：方法
- 研究问题：轮式人形、带移动底座的双臂机器人，怎样从人体动作得到可执行的全身动作？
- 已有工作与空白：[arXiv 2609.11357](https://arxiv.org/abs/2609.11357) 针对轮式人形提出形态感知的重定向与全身遥操作；更一般的拓扑不匹配情况仍是开放问题（分析判断）。
- 怎样验证：在你的 URDF 上执行工厂动作的成功率与能耗。

## 6. 对应的链路

- [L1](../../链路/L1_STEP资产化与物理仿真/README.md)：L1 STEP 资产化＋物理仿真作为世界模型
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 算力

- MuJoCo Playground 的摘要称，在单张 GPU 上几分钟即可训练出策略 [arXiv 2502.08844](https://arxiv.org/abs/2502.08844)。
- Learning to Walk in Minutes 在单张工作站 GPU 上训练 ANYmal：平地不到 4 分钟，不平地形 20 分钟 [arXiv 2109.11978](https://arxiv.org/abs/2109.11978)。
- SONIC 把动作跟踪扩展到 1.2M–42M 参数、700 小时动捕、约 2.1 万 GPU 小时 [arXiv 2511.07820](https://arxiv.org/abs/2511.07820)，超出本项目算力，建议直接用开源跟踪器。

## 8. 高价值参考文献

### 重定向

- **Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking**（2025），[arXiv 2510.02252](https://arxiv.org/abs/2510.02252)：GMR：系统评估重定向质量对动作跟踪策略的影响。
- **OmniRetarget: Interaction-Preserving Data Generation for Humanoid Whole-Body Loco-Manipulation and Scene Interaction**（2025），[arXiv 2509.26633](https://arxiv.org/abs/2509.26633)：OmniRetarget：用交互网格保持人、物体、地形的接触关系。
- **Perpetual Humanoid Control for Real-time Simulated Avatars**（2023），[arXiv 2305.06456](https://arxiv.org/abs/2305.06456)：PHC：物理仿真中的人体动作模仿。
- **Morphology-Aware Human Motion Retargeting for Wheeled-Humanoid Loco-Manipulation**（2026），[arXiv 2609.11357](https://arxiv.org/abs/2609.11357)：轮式人形的形态感知重定向与全身遥操作。

### 动作跟踪与全身控制

- **GMT: General Motion Tracking for Humanoid Whole-Body Control**（2025），[arXiv 2506.14770](https://arxiv.org/abs/2506.14770)：GMT：一个策略跟踪多种动作。
- **BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion**（2025），[arXiv 2508.08241](https://arxiv.org/abs/2508.08241)：BeyondMimic：从动作跟踪到用引导扩散组合动作。
- **SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control**（2025），[arXiv 2511.07820](https://arxiv.org/abs/2511.07820)：SONIC：动作跟踪的规模化研究。
- **HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots**（2024），[arXiv 2410.21229](https://arxiv.org/abs/2410.21229)：HOVER：把多种控制模式统一到一个命令端口。
- **AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control**（2025），[arXiv 2505.03738](https://arxiv.org/abs/2505.03738)：AMO：RL 与轨迹优化结合的实时全身控制。
- **ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills**（2025），[arXiv 2502.01143](https://arxiv.org/abs/2502.01143)：ASAP：对齐仿真与真实物理。
- **From Video to Vision: Learning Generalizable Humanoid Carrying from Human Motion**（2026），[arXiv 2610.14561](https://arxiv.org/abs/2610.14561)：MOVER：从人体动作学习人形搬运。

### 人形遥操作与数据采集

- **Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation**（2024），[arXiv 2403.04436](https://arxiv.org/abs/2403.04436)：H2O：人到人形的实时遥操作。
- **OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning**（2024），[arXiv 2406.08858](https://arxiv.org/abs/2406.08858)：OmniH2O：通用的人形遥操作与学习。
- **HumanPlus: Humanoid Shadowing and Imitation from Humans**（2024），[arXiv 2406.10454](https://arxiv.org/abs/2406.10454)：HumanPlus：人形从人类影子跟随与模仿。

### 训练框架与基准

- **MuJoCo Playground**（2025），[arXiv 2502.08844](https://arxiv.org/abs/2502.08844)：MuJoCo Playground：基于 MJX 的开源机器人学习框架。
- **Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning**（2021），[arXiv 2109.11978](https://arxiv.org/abs/2109.11978)：大规模并行 RL：单卡几分钟训练腿式行走。
- **HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation**（2024），[arXiv 2403.10506](https://arxiv.org/abs/2403.10506)：HumanoidBench：人形全身行走与操作基准。

### 人类第一人称数据

- **Ego4D: Around the World in 3,000 Hours of Egocentric Video**（2021），[arXiv 2110.07058](https://arxiv.org/abs/2110.07058)：Ego4D：3000 小时第一人称视频。
- **EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video**（2025），[arXiv 2505.11709](https://arxiv.org/abs/2505.11709)：EgoDex：829 小时第一人称视频，带手部跟踪。

## 9. 参考项目

- [LeCAR-Lab/human2humanoid](https://github.com/LeCAR-Lab/human2humanoid)：H2O 与 OmniH2O
- [MarkFzp/humanplus](https://github.com/MarkFzp/humanplus)：HumanPlus
- [YanjieZe/GMR](https://github.com/YanjieZe/GMR)：GMR 重定向
- [ZhengyiLuo/PHC](https://github.com/ZhengyiLuo/PHC)：PHC
- [NVlabs/HOVER](https://github.com/NVlabs/HOVER)：HOVER
- [LeCAR-Lab/ASAP](https://github.com/LeCAR-Lab/ASAP)：ASAP
- [zixuan417/humanoid-general-motion-tracking](https://github.com/zixuan417/humanoid-general-motion-tracking)：GMT
- [google-deepmind/mujoco_playground](https://github.com/google-deepmind/mujoco_playground)：MuJoCo Playground
- [leggedrobotics/rsl_rl](https://github.com/leggedrobotics/rsl_rl)：腿式机器人 RL 训练库
- [google-deepmind/mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie)：常见机器人的 MuJoCo 模型

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
