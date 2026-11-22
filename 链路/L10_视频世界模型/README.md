# L10 视频世界模型：合成数据与策略评估

在 FWAM 中的位置：数据与评估层。在本算力下，主要用途是用现成模型离线评估子级策略、合成少量训练数据；不作为整厂层的在线预测模型。

## 思考

- 视频世界模型推理开销大，当规划模型时最慢：Cosmos 规划每个动作约 4 分钟 [P05]。
- 从头训练不可行：DreamGen 生成 24 万条样本用了 1500 张 L40 约 54 小时 [P65]。
- 可行的是用开源权重做推理或小规模微调，并且只用于工位层，不用于整厂层。

## Idea

1. **子级策略的离线评估**：用视频世界模型在"想象"中评估 VLA 子级在新工件、新布局上的表现，提前发现失败模式，再把估计的成功率报告给整厂层。
2. **只在关键工位使用**：只对几何复杂、接触多的工位（如装夹）做视频预测，其余工位不用。

## 实施路线

1. 采集：现场视频加机器人动作或位姿。
2. 微调：在预训练视频模型上用目标机器人数据后训练（受显存限制，优先 2B 量级模型或 LoRA）。
3. 生成：以动作或指令为条件生成未来视频。
4. 用途：在想象中评估策略，或生成合成轨迹后用逆动力学补出动作再训练策略。
5. 核对：与真实成功率对照；检查非专家动作下是否仍遵循动作 [P77]。

算力：微调与推理主要用 40／80 GB 卡；3090／4090 只适合推理小模型或蒸馏后的模型。

## 推荐文献

- Veo 机器人策略评估 [P73]：与 1600 多次真实试验相关 0.88
- Ctrl-World [P72]：新指令上的成功率从 38.7% 提到 83.4%
- DreamDojo [P75]、Genie Envisioner [P71]、DreamZero [P76]、DreamGen [P65]
- WorldEcho [P77]：只用专家数据训练的模型在偏离专家的动作上常不遵循动作
- 多智能体视频世界模型 Gamma-World，[arXiv 2605.28816](https://arxiv.org/abs/2605.28816)

## 参考项目

[Robert-gyj/Ctrl-World](https://github.com/Robert-gyj/Ctrl-World)、[NVIDIA/DreamDojo](https://github.com/NVIDIA/DreamDojo)、[AgibotTech/Genie-Envisioner-V1](https://github.com/AgibotTech/Genie-Envisioner-V1)、[nvidia-cosmos/cosmos-predict2.5](https://github.com/nvidia-cosmos/cosmos-predict2.5)、[NVIDIA/GR00T-Dreams](https://github.com/NVIDIA/GR00T-Dreams)、[huggingface/lerobot](https://github.com/huggingface/lerobot)
