# L7 扫描场景中的三维动作条件动力学

在 FWAM 中的位置：机器人层与工位层的几何预测。整厂层可以调用它估计"上料、装夹能否成功"。

## 思考

- L7 只覆盖几何层：工件、门、夹具在机器人动作下怎样移动。设备内部状态、工艺、生产流都要另外接入。
- 机器人有 URDF，可以用正向运动学把关节动作转成三维点或末端轨迹，正好对应 PointWorld 这类以三维点流表示动作的模型。
- 点流和高斯可以直接表示形变；但断裂和切割会产生新表面，点之间的对应关系会断开（见[专题](../专题_形变流体断裂与加工/README.md)）。

## Idea

1. **几何成功率作为子级自报告**：用 L7 的模型对一次上料预测"工件最终位姿与目标位姿的偏差"，转成成功概率，报告给整厂层（L11 Idea 1）。
2. **以对象为单位的预测**：MRO-GWM 把每个对象建成独立的一组高斯，预测各自的刚体运动 [P88]，正好与整厂层以实体为单位的状态对齐。

## 实施路线

1. 三维状态：用深度相机或扫描得到场景点云或高斯。
2. 机器人动作接地：用 URDF 正向运动学把机器人动作变成三维点或末端轨迹。
3. 学习转移：训练模型预测动作引起的点流、高斯运动或对象刚体运动。
4. 规划：用 MPPI 或 CEM 在模型中搜索动作。
5. 补设备状态：门锁、PLC 模式等不能从点位移看出，需要作为额外条件输入。

算力：PointWorld 一次批量前向约 0.1 秒 [P44]，推理一张 4090 足够；从头训练大模型不可行，以微调为主。

## 推荐文献

- PointWorld [P44]：约 200 万条轨迹训练；单个预训练模型让真实 Franka 无需额外示范或后训练即可完成多种操作
- GWM [P85]：以三维高斯为状态的模型式强化学习
- MRO-GWM [P88]：以对象为单位的刚体运动预测
- PhysGaussian [P19]、PhysTwin [P21]

## 参考项目

[NVlabs/PointWorld](https://github.com/NVlabs/PointWorld)、[XPandora/PhysGaussian](https://github.com/XPandora/PhysGaussian)、[Jianghanxiao/PhysTwin](https://github.com/Jianghanxiao/PhysTwin)、[nerfstudio-project/gsplat](https://github.com/nerfstudio-project/gsplat)、[NVlabs/FoundationPose](https://github.com/NVlabs/FoundationPose)
