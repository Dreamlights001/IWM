# W12 子级技能与端口

> 阶段：S2 子级：机器人与工位　·　总看板：[research_board.html](../research_board.html#W12)

训练机器人技能（VLA、扩散策略、全身控制），包装成整厂层可以调用的端口，并附带可校准的耗时与成功率自报告。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md)：示范数据<br>[W06（全身动作数据）](../W06_全身动作数据/README.md)：全身动作库与跟踪器<br>[W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：模型内规划与评估<br>[W15（安全与约束）](../W15_安全与约束/README.md)：约束检查 | [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：技能事件与自报告<br>[W13（多机器人协作）](../W13_多机器人协作/README.md)：技能端口<br>[W16（基准与评测）](../W16_基准与评测/README.md)：待评测技能 | ② 仿真—真实校准<br>④ 世界模型—策略协同<br>⑤ 跨层一致 |

## 1. 为什么要做

整厂层的动作是对子级的调用（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 1.1 节）：机器人技能、设备命令、AGV 目标和派工。每个子级要有稳定的端口，以及“预计耗时、成功概率”的自报告。RoboOS 用大脑—小脑结构组织多机器人的技能库 [arXiv 2505.03673](https://arxiv.org/abs/2505.03673)；HOVER 把人形的多种控制模式统一到一个命令端口 [arXiv 2410.21229](https://arxiv.org/abs/2410.21229)。

## 2. 输入与产物

**输入**

- [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md)、[W06（全身动作数据）](../W06_全身动作数据/README.md) 的数据与动作库
- [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md) 的工位模型
- [W15（安全与约束）](../W15_安全与约束/README.md) 的约束

**产物**

- 技能库：pick、place、load、unload、goto 等，每个技能带前置条件和返回事件
- 自报告：预计耗时、成功概率、置信度
- 失败检测与进度估计

## 3. 具体工作

1. 机械臂技能：微调 VLA（π0 [arXiv 2410.24164](https://arxiv.org/abs/2410.24164)、π0.5 [arXiv 2504.16054](https://arxiv.org/abs/2504.16054)、OpenVLA [arXiv 2406.09246](https://arxiv.org/abs/2406.09246)、GR00T N1 [arXiv 2503.14734](https://arxiv.org/abs/2503.14734)、SmolVLA [arXiv 2506.01844](https://arxiv.org/abs/2506.01844)），或训练扩散策略 [arXiv 2303.04137](https://arxiv.org/abs/2303.04137)。
2. 分层：高层 VLM 决定下一步，低层执行，参考 Hi Robot [arXiv 2502.19417](https://arxiv.org/abs/2502.19417)、HAMSTER [arXiv 2502.05485](https://arxiv.org/abs/2502.05485)；语言规划结合技能可行性，参考 SayCan [arXiv 2204.01691](https://arxiv.org/abs/2204.01691)；不确定时请求人工，参考 KnowNo [arXiv 2307.01928](https://arxiv.org/abs/2307.01928)。
3. 人形与移动操作：NaVILA [arXiv 2412.04453](https://arxiv.org/abs/2412.04453)、LeVERB [arXiv 2506.13751](https://arxiv.org/abs/2506.13751)、Being-0 [arXiv 2503.12533](https://arxiv.org/abs/2503.12533)、BRS [arXiv 2503.05652](https://arxiv.org/abs/2503.05652)；下层用 [W06（全身动作数据）](../W06_全身动作数据/README.md) 的全身控制器。
4. 失败检测与进度估计：AHA [arXiv 2410.00371](https://arxiv.org/abs/2410.00371)、FAIL-Detect [arXiv 2503.08558](https://arxiv.org/abs/2503.08558)；进度或奖励模型 VIP [arXiv 2210.00030](https://arxiv.org/abs/2210.00030)、LIV [arXiv 2306.00958](https://arxiv.org/abs/2306.00958)。
5. 端口包装：统一前置条件检查、超时、返回事件和自报告字段（[W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的规范）。
6. 标定自报告：在仿真和真实中重复执行，拟合耗时分布和成功率。

## 4. 可以写成论文的方向

### 4.1 带可校准自报告的机器人技能端口

- 类型：方法
- 研究问题：能否让 VLA 或扩散策略在执行前给出耗时和成功率估计，并在统计上校准，供上层规划使用？
- 已有工作与空白：KnowNo、FAIL-Detect 用保形预测处理规划器的不确定性和运行时失败检测 [arXiv 2307.01928](https://arxiv.org/abs/2307.01928) [arXiv 2503.08558](https://arxiv.org/abs/2503.08558)；AHA 检测并解释操作失败 [arXiv 2410.00371](https://arxiv.org/abs/2410.00371)。执行前的耗时与成功率预测还未见系统研究（分析判断）。
- 怎样验证：校准误差；整厂层用自报告规划时，与用常数估计相比的吞吐差异。

### 4.2 感知设备状态的 VLA

- 类型：方法
- 研究问题：把 PLC／NC 状态作为 VLA 的输入，能否减少上下料等任务中“设备未就绪就动手”的失败？
- 已有工作与空白：所列 VLA 的输入是图像、语言和机器人本体状态（依据其论文描述判断）。
- 怎样验证：失败类型统计与成功率对比。

## 5. 所在闭环

- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。
- ④ 世界模型—策略协同：W09·W10 预测动作后果 → W12·W14 在模型中规划或训练 → 仿真或真实执行 记录新轨迹 → 更新模型。World-in-World 发现，用动作—观测数据做后训练，比换用更强的预训练视频生成器更有效 [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)；DreamerV3、TD-MPC2 交替更新模型与策略 [P02](../../papers/P02_DreamerV3_2301.04104v2.pdf) [P03](../../papers/P03_TD_MPC2_2310.16828v2.pdf)。
- ⑤ 跨层一致：W12 执行技能，返回事件与实际耗时 → W09 工位层预测同一事件 → W10 整厂层预测同一事件 → W14 按预测下发新命令 → 下发命令。[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) Idea 3 提出跨层一致性训练，尚未验证；H-WM 联合预测逻辑状态和视觉状态的转移 [arXiv 2602.11291](https://arxiv.org/abs/2602.11291)。

## 6. 对应的链路

- [L7](../../链路/L7_三维动作条件动力学/README.md)：L7 扫描场景中的三维动作条件动力学
- [L8](../../链路/L8_JEPA特征空间世界模型/README.md)：L8 JEPA 特征空间世界模型
- [L9](../../链路/L9_潜变量模型式强化学习/README.md)：L9 潜变量模型式强化学习
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 算力

- openpi README 给出的显存需求：推理 8 GB 以上，LoRA 微调 22.5 GB 以上（一张 RTX 4090 可做），全参数微调 70 GB 以上（A100 80 GB 或 H100）[Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)。
- SmolVLA 的摘要称，它的性能可与大 10 倍的 VLA 相当 [arXiv 2506.01844](https://arxiv.org/abs/2506.01844)。

## 8. 高价值参考文献

### VLA 与策略

- **$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control**（2024），[arXiv 2410.24164](https://arxiv.org/abs/2410.24164)：π0：基于流匹配的 VLA。
- **$\pi_{0.5}$: a Vision-Language-Action Model with Open-World Generalization**（2025），[arXiv 2504.16054](https://arxiv.org/abs/2504.16054)：π0.5：异构任务混合训练，面向开放世界泛化。
- **OpenVLA: An Open-Source Vision-Language-Action Model**（2024），[arXiv 2406.09246](https://arxiv.org/abs/2406.09246)：OpenVLA：开源 7B VLA。
- **GR00T N1: An Open Foundation Model for Generalist Humanoid Robots**（2025），[arXiv 2503.14734](https://arxiv.org/abs/2503.14734)：GR00T N1：人形机器人的开放基础模型，双系统结构。
- **SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics**（2025），[arXiv 2506.01844](https://arxiv.org/abs/2506.01844)：SmolVLA：小型、低成本的 VLA。
- **RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control**（2023），[arXiv 2307.15818](https://arxiv.org/abs/2307.15818)：RT-2：把网络知识迁移到机器人控制。
- **Diffusion Policy: Visuomotor Policy Learning via Action Diffusion**（2023），[arXiv 2303.04137](https://arxiv.org/abs/2303.04137)：Diffusion Policy：扩散模型生成动作。

### 分层与语言规划

- **Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models**（2025），[arXiv 2502.19417](https://arxiv.org/abs/2502.19417)：Hi Robot：分层 VLA，处理开放指令与用户反馈。
- **HAMSTER: Hierarchical Action Models For Open-World Robot Manipulation**（2025），[arXiv 2502.05485](https://arxiv.org/abs/2502.05485)：HAMSTER：高层 VLM 输出二维路径，低层执行。
- **Do As I Can, Not As I Say: Grounding Language in Robotic Affordances**（2022），[arXiv 2204.01691](https://arxiv.org/abs/2204.01691)：SayCan：语言模型结合技能可行性。
- **Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners**（2023），[arXiv 2307.01928](https://arxiv.org/abs/2307.01928)：KnowNo：保形预测，不确定时请求帮助。

### 人形与移动操作

- **HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots**（2024），[arXiv 2410.21229](https://arxiv.org/abs/2410.21229)：HOVER：人形的统一控制端口。
- **NaVILA: Legged Robot Vision-Language-Action Model for Navigation**（2024），[arXiv 2412.04453](https://arxiv.org/abs/2412.04453)：NaVILA：腿式机器人的视觉语言导航。
- **LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction**（2025），[arXiv 2506.13751](https://arxiv.org/abs/2506.13751)：LeVERB：潜空间视觉语言指令驱动的人形全身控制。
- **Being-0: A Humanoid Robotic Agent with Vision-Language Models and Modular Skills**（2025），[arXiv 2503.12533](https://arxiv.org/abs/2503.12533)：Being-0：基础模型加模块化技能库的人形智能体。
- **BEHAVIOR Robot Suite: Streamlining Real-World Whole-Body Manipulation for Everyday Household Activities**（2025），[arXiv 2503.05652](https://arxiv.org/abs/2503.05652)：BRS：家务任务的全身操作框架，含遥操作接口。

### 失败检测与进度

- **AHA: A Vision-Language-Model for Detecting and Reasoning Over Failures in Robotic Manipulation**（2024），[arXiv 2410.00371](https://arxiv.org/abs/2410.00371)：AHA：检测并推理操作失败的 VLM。
- **Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies**（2025），[arXiv 2503.08558](https://arxiv.org/abs/2503.08558)：FAIL-Detect：不需要失败数据的运行时失败检测。
- **VIP: Towards Universal Visual Reward and Representation via Value-Implicit Pre-Training**（2022），[arXiv 2210.00030](https://arxiv.org/abs/2210.00030)：VIP：从人类视频学通用的价值与奖励表示。
- **LIV: Language-Image Representations and Rewards for Robotic Control**（2023），[arXiv 2306.00958](https://arxiv.org/abs/2306.00958)：LIV：语言与图像对齐的价值表示。

### 大脑—小脑框架

- **RoboOS: A Hierarchical Embodied Framework for Cross-Embodiment and Multi-Agent Collaboration**（2025），[arXiv 2505.03673](https://arxiv.org/abs/2505.03673)：RoboOS：大脑模型、小脑技能库与共享记忆。

## 9. 参考项目

- [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)：π0、π0.5 及微调脚本；README 列出显存需求
- [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)：GR00T N1
- [openvla/openvla](https://github.com/openvla/openvla)：OpenVLA
- [huggingface/lerobot](https://github.com/huggingface/lerobot)：LeRobot，含 SmolVLA 与多种策略
- [real-stanford/diffusion_policy](https://github.com/real-stanford/diffusion_policy)：Diffusion Policy

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
