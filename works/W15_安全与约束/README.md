# W15 安全与约束

> 阶段：S4 安全校核与评测　·　总看板：[research_board.html](../research_board.html#W15)

把互锁、安全区域和人员规则写成约束，用于过滤和修正学习式模型提出的动作，并在上线前做校核。约束清单从 S0 开始写，屏蔽层在 S3 就要接入。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md)：约束清单<br>[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md)：互锁逻辑 | [W12（子级技能与端口）](../W12_子级技能与端口/README.md)：约束检查<br>[W14（整厂规划与调度）](../W14_整厂规划与调度/README.md)：约束与屏蔽<br>[W17（部署与数据飞轮）](../W17_部署与数据飞轮/README.md)：上线前校核 | — |

## 1. 为什么要做

学习式世界模型和策略可能提出违反互锁或安全距离的动作，预测误差还会在多步规划中累积。工业机器人安全有专门标准：ISO 10218-1:2025 规定工业机器人本体的安全要求 [ISO 10218-1:2025](https://www.iso.org/standard/73933.html)，ISO 10218-2:2025 涉及机器人应用的集成、调试、运行和维护 [ISO 工业机器人安全标准包](https://www.iso.org/publication/PUB200102.html)。研究原型上线前，需要由有资质的人员按这些标准做风险评估；本目录没有核对标准条文。

## 2. 输入与产物

**输入**

- [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的约束清单
- [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的互锁逻辑
- [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)、[W14（整厂规划与调度）](../W14_整厂规划与调度/README.md) 的候选动作

**产物**

- 约束规范：硬约束与软约束
- 屏蔽层：位于规划器与子级之间
- 不确定时请求人工的规则
- 上线前的校核流程与安全指标

## 3. 具体工作

1. 把约束分为硬约束（互锁、限位、安全区、人员区域）和软约束（节拍、能耗）。
2. 约束强化学习：CPO [arXiv 1705.10528](https://arxiv.org/abs/1705.10528)；带稳定性保证的模型式安全 RL [arXiv 1705.08551](https://arxiv.org/abs/1705.08551)。
3. 屏蔽：在执行前用规则或形式化方法过滤不安全动作 [arXiv 1708.08611](https://arxiv.org/abs/1708.08611)。
4. 不确定时请求人工：KnowNo [arXiv 2307.01928](https://arxiv.org/abs/2307.01928)。
5. PLC 代码的形式化验证：LLM4PLC、Agents4PLC 把生成的代码接入验证工具 [arXiv 2401.05443](https://arxiv.org/abs/2401.05443) [arXiv 2410.14209](https://arxiv.org/abs/2410.14209)。
6. 在 [W16（基准与评测）](../W16_基准与评测/README.md) 中加入安全指标：违规次数、急停次数、近距离事件。

## 4. 可以写成论文的方向

### 4.1 世界模型规划的安全屏蔽

- 类型：方法
- 研究问题：用 PLC 互锁和显式仿真校核学习式模型提出的候选动作，能在多大程度上消除违规，同时保留规划收益？
- 已有工作与空白：屏蔽方法在形式化的有限状态模型上给出保证 [arXiv 1708.08611](https://arxiv.org/abs/1708.08611)；学习式整厂模型的预测误差会影响屏蔽的可靠性（分析判断）。
- 怎样验证：违规次数、吞吐损失、屏蔽触发率。

## 6. 对应的链路

- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 高价值参考文献

### 约束与安全学习

- **Constrained Policy Optimization**（2017），[arXiv 1705.10528](https://arxiv.org/abs/1705.10528)：CPO：约束策略优化。
- **Safe Model-based Reinforcement Learning with Stability Guarantees**（2017），[arXiv 1705.08551](https://arxiv.org/abs/1705.08551)：带稳定性保证的安全模型式 RL。
- **Safe Reinforcement Learning via Shielding**（2017），[arXiv 1708.08611](https://arxiv.org/abs/1708.08611)：用屏蔽做安全强化学习。

### 不确定性与求助

- **Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners**（2023），[arXiv 2307.01928](https://arxiv.org/abs/2307.01928)：KnowNo：知道自己不知道时请求帮助。

### PLC 验证

- **LLM4PLC: Harnessing Large Language Models for Verifiable Programming of PLCs in Industrial Control Systems**（2024），[arXiv 2401.05443](https://arxiv.org/abs/2401.05443)：LLM4PLC：可验证的 PLC 编程。
- **Agents4PLC: Automating Closed-loop PLC Code Generation and Verification in Industrial Control Systems using LLM-based Agents**（2024），[arXiv 2410.14209](https://arxiv.org/abs/2410.14209)：Agents4PLC：闭环生成与验证 PLC 代码。

### 标准

- **ISO 10218-1:2025 Robotics — Safety requirements — Part 1: Industrial robots**（ISO），[链接](https://www.iso.org/standard/73933.html)：ISO 10218-1:2025：工业机器人本体的安全要求。
- **Industrial robot safety bundle（ISO 10218-1:2025 与 ISO 10218-2:2025）**（ISO），[链接](https://www.iso.org/publication/PUB200102.html)：ISO 10218-1:2025 与 10218-2:2025 的标准包页面。

## 8. 参考项目

- [PKU-Alignment/safety-gymnasium](https://github.com/PKU-Alignment/safety-gymnasium)：安全 RL 环境
- [PKU-Alignment/omnisafe](https://github.com/PKU-Alignment/omnisafe)：安全 RL 算法库

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对，2026-11-27 补充）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
