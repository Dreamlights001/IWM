# L6 仿真＋学习混合：残差、外观与快速代理

在 FWAM 中的位置：连接显式仿真（L1、L4）与学习式模型（L11 形态 B）的桥梁。L11 的整厂层图世界模型本质上就是 L4 离散事件仿真的"快速代理"。

## 思考

- 显式仿真准但慢，学习式模型快但需要数据。L6 的做法是：用仿真生成数据，训练快速代理；用真实数据学残差，修正仿真的偏差。
- 学到的代理会继承仿真的偏差：只用仿真数据预训练的 PointWorld 不能零样本泛化到真实场景，混入真实数据后才行 [P44]。
- 形变和流体仿真尤其慢：DINO-WM 报告形变环境中仿真推进一步约 3.0 s，学到的模型前向一步约 0.014 s [P07]，这类任务更需要快速代理（见[专题](../专题_形变流体断裂与加工/README.md)）。

## Idea

1. **整厂层快速代理**：L11 阶段 3 就是这个想法在整厂层的实现：用 L4 仿真数据训练图世界模型。
2. **两级残差**：工位层学物理残差（仿真与实测的位姿、力差异），整厂层学事件残差（仿真与真实的完工时间差异）。
3. **代理的不确定性**：让代理输出不确定性，不确定性高时回退到显式仿真。

## 实施路线

1. 以 L1／L2 为底，仿真负责已知物理和设备逻辑。
2. 残差：用真实数据学习仿真与现场的偏差（参考在解析仿真上学残差的工作 [P63]，以及人形上的 ASAP [arXiv 2502.01143]）。
3. 外观：仿真渲染图转成照片级图像（Cosmos-Transfer1 [P64]），用于训练视觉策略。
4. 快速代理：用仿真数据训练图网络或三维动力学模型（GNS [P31]、MeshGraphNets [P32]）。
5. 对照：与原仿真、真实数据分别比较。

算力：代理模型和残差模型在一张 3090／4090 上可训练；Cosmos-Transfer1 推理需要大显存，单张 B200 生成 5 秒视频约 142 秒 [P64]，在本算力下只适合少量离线使用。

## 推荐文献

- 仿真＋随机神经网络残差 [P63]
- GNS [P31]、MeshGraphNets [P32]（比原求解器快 11–289 倍）
- Cosmos-Transfer1 [P64]
- ASAP：用真实数据训练残差动作模型来对齐仿真，[arXiv 2502.01143](https://arxiv.org/abs/2502.01143)

## 参考项目

[google-deepmind/deepmind-research](https://github.com/google-deepmind/deepmind-research)（learning_to_simulate、meshgraphnets 目录）、[nvidia-cosmos/cosmos-transfer1](https://github.com/nvidia-cosmos/cosmos-transfer1)、[NVlabs/PointWorld](https://github.com/NVlabs/PointWorld)、[LeCAR-Lab/ASAP](https://github.com/LeCAR-Lab/ASAP)
