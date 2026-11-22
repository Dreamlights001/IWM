# L9 潜变量模型式强化学习

在 FWAM 中的位置：两处都可用。在机器人层，用于单工位技能（上料、装夹）；在整厂层，可以作为 L11 形态 C 的训练方法：在学习式整厂世界模型内用 RL 训练整厂层策略。

## 思考

- Dreamer、TD-MPC 一类方法的模型与奖励绑定：换目标（从吞吐换成准时率）往往要重新训练。
- 整厂层的奖励（吞吐、在制品、准时率）定义清楚、可以自动计算，比单机器人技能更适合这类方法。
- 不可逆过程（切削、报废）难以靠试错覆盖，所以训练应在 L11 的学习式模型或 L4 仿真里进行，不在真实工厂里试错。

## Idea

1. **在整厂图世界模型内做 Dreamer 式训练**：L11 阶段 3 的图世界模型就是"潜模型"，在其中想象整厂未来，训练派工策略。
2. **多智能体版本**：每台机器人一个策略，共享整厂世界模型，参考多智能体模型式 RL 的工作 [arXiv 2205.15023] 和 MAPPO [arXiv 2103.01955]。
3. **按时间尺度分层**：参考 Director 的分层规划 [arXiv 2206.04114]，整厂层管目标，机器人层管执行。

## 实施路线

1. 定义任务：观测、动作、奖励、终止条件。
2. 数据：在 L1／L2／L4 仿真中采集交互。
3. 学潜模型：学习潜状态转移、奖励与价值。
4. 想象中训练：Dreamer 式在想象中训练策略，或 TD-MPC 式在潜空间做 MPC。
5. 迁移与验收：按真实结果判定成功，不用模型自评。

算力：DreamerV3、TD-MPC2 在单张 GPU 上可训练；整厂图世界模型规模小，同样单卡即可。

## 推荐文献

- DreamerV3 [P02]：同一套超参数在 150 多个任务上优于专用方法
- TD-MPC2 [P03]：3.17 亿参数的多任务智能体
- Dreamer 4 [P69]：在视频世界模型内训练智能体
- Director，[arXiv 2206.04114](https://arxiv.org/abs/2206.04114)；Scalable Multi-Agent Model-Based RL，[arXiv 2205.15023](https://arxiv.org/abs/2205.15023)；MAPPO，[arXiv 2103.01955](https://arxiv.org/abs/2103.01955)

## 参考项目

[danijar/dreamerv3](https://github.com/danijar/dreamerv3)、[nicklashansen/tdmpc2](https://github.com/nicklashansen/tdmpc2)、[danijar/director](https://github.com/danijar/director)、[leggedrobotics/rsl_rl](https://github.com/leggedrobotics/rsl_rl)、[marlbenchmark/on-policy](https://github.com/marlbenchmark/on-policy)、[bold-lab-ai/JaxMARL](https://github.com/bold-lab-ai/JaxMARL)、[isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab)
