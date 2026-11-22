# L2 扫描配准到 STEP 资产，并校准成数字孪生

在 FWAM 中的位置：给工位层和整厂层提供"现场真实的布局、外观和初态"，使仿真与现场可以逐帧比较；是 L11 阶段 0 和阶段 5 的基础。

## 思考

- 有 STEP 又能扫描时，两者分工：STEP 给精确几何和部件结构，扫描给设备在现场的实际位姿、STEP 里没有的东西（线缆、护罩、料架），以及真实外观。
- 机床多是反光金属和透明防护罩，扫描和重建容易出错，需要在验收时专门检查这些区域。
- 数字孪生要"跟着现场走"，需要持续同步：编码器、PLC 信号、相机观测。同步频率决定了整厂层能多快拿到准确的状态。
- 任务涉及形变或流体时，材料参数也要用现场观测辨识，例如 PhysTwin 用视频做逆物理 [P21]；形变体的状态维度高，运行时同步比刚体难（见[专题](../专题_形变流体断裂与加工/README.md)）。

## Idea

1. **以 STEP 为准、扫描为辅的配准**：先用 ICP 把 STEP 网格配准到扫描点云，得到每台设备的位姿；配准残差大的区域标为"STEP 与现场不符"，作为人工检查清单。
2. **整厂级同步状态**：整厂层（L11）需要的状态不是像素，而是每个实体的位姿和模式。把同步结果直接写进整厂状态图。
3. **辨识动作的排期**：ASID 主动设计少量真实交互来辨识物理参数 [P60]。在工厂里，可以把辨识动作排进设备空闲时段，由整厂层调度。

## 实施路线

1. 扫描：激光或多视角相机；大范围用激光惯导里程计（如 FAST-LIO），局部用 COLMAP 或前馈重建（VGGT、DUSt3R）。
2. 重建：点云或高斯（gsplat、3DGS）。
3. 配准：Open3D 的 ICP，把 L1 的 STEP 资产对齐到扫描。
4. 外观：用扫描得到的高斯渲染现场外观（参考 DreMa [P23]、Robo-GS [P22]）。
5. 辨识与同步：用少量真实动作辨识摩擦、惯量、驱动增益、延迟；运行时用编码器与 PLC 信号持续把仿真状态拉回现场（参考 Real-is-Sim [P58]）。

算力：高斯重建一张 3090／4090 可以完成单个工位；整厂扫描需要分块处理。

## 推荐文献

- RialTo [P59]：扫描后导出 USD 到 Isaac Sim；搭一个场景约 15 分钟人工，每个任务训练平均约 2 天 3 小时
- ASID [P60]：主动探索做系统辨识
- Real-is-Sim [P58]：数字孪生以 60 Hz 与现场同步
- DreMa [P23]、Robo-GS [P22]：高斯外观＋物理引擎
- VGGT [P36]、3D Gaussian Splatting [P16]
- [Open3D ICP 配准教程](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html)；[RialTo 项目页](https://real-to-sim-to-real.github.io/RialTo/)；[Real-is-Sim 项目页](https://real-is-sim.github.io/)

## 参考项目

[colmap/colmap](https://github.com/colmap/colmap)、[isl-org/Open3D](https://github.com/isl-org/Open3D)、[hku-mars/FAST_LIO](https://github.com/hku-mars/FAST_LIO)、[facebookresearch/vggt](https://github.com/facebookresearch/vggt)、[naver/dust3r](https://github.com/naver/dust3r)、[nerfstudio-project/gsplat](https://github.com/nerfstudio-project/gsplat)、[NVlabs/FoundationPose](https://github.com/NVlabs/FoundationPose)、[rai-opensource/embodied_gaussians](https://github.com/rai-opensource/embodied_gaussians)、[real-to-sim-to-real/RialToGUI](https://github.com/real-to-sim-to-real/RialToGUI)
