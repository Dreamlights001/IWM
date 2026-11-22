# L1 STEP 资产化＋物理仿真作为世界模型

在 FWAM 中的位置：工位层与机器人层的显式转移函数；也是整厂层显式基线（L11 形态 A）和训练数据的来源。

## 思考

- STEP 只给几何，不给质量、摩擦、驱动、延迟，也不给设备逻辑。资产化的工作量主要在"补齐这些"。
- 机床上需要动的部件不多：轴、门、卡盘或夹具、按钮。其余外壳可以作为静态碰撞体。这些部件决定了建模工作量。
- 机器人已有 URDF，可以直接加载到 MuJoCo、Isaac Sim、Gazebo、ManiSkill。STEP 机床需要转成同一种格式（URDF、MJCF 或 USD），并放进同一坐标系。
- 仿真器本身就是一个动作条件世界模型：给定动作，推演结果。L11 的整厂层要调用它时，关键是"从快照复位"和"批量推演"。
- 任务涉及线缆、软体、液体、切割或断裂时，刚体和关节仿真不够，要换用或接入支持该材料的求解器，STEP 之外还要补材料参数。各仿真器的能力见[专题：形变、流体、断裂与加工](../专题_形变流体断裂与加工/README.md)第 3 节。

## Idea

1. **按部件角色分级建模**：只有被机器人接触或会动的部件才需要精确碰撞体和关节；外壳只用粗碰撞体。这样每台机床的建模成本大致和"会动的部件数"成正比。
2. **把资产与端口一起建**：给每个部件同时定义它在整厂层的端口，例如门对应 `door_open`，夹具对应 `clamp`。这样资产一建好就能被 L4、L11 调用。
3. **自报告接口**：仿真器给每个技能调用估计耗时和成功率，作为 L11 整厂层的输入。

## 实施路线

1. STEP 清理：在 FreeCAD 或 CadQuery 中去掉螺钉、倒角等小特征，拆出运动部件，统一单位和坐标系。
2. 导出网格：视觉用细网格，碰撞体用 CoACD 或 V-HACD 做凸分解；装夹面、按钮、插接面保留能分辨任务公差的几何。
3. 写关节：用 freecad.cross、onshape-to-robot 或手写 URDF／MJCF，设定行程、限位、驱动方式。
4. 组装场景：机床、机器人、料架、工件放进同一坐标系；核对质心、惯量、摩擦。
5. 验证：先测限位、驱动跟踪、接触穿透、到位反馈；再扫描步长和碰撞精度，与实测对照。
6. 作为世界模型使用：从快照推演候选动作（MPC），或离线评估策略。

算力：建模与仿真主要靠 CPU；Isaac Lab 和 ManiSkill 的并行仿真用一张 4090 即可。

## 推荐文献

- MuJoCo 原始论文 [P96]；MuJoCo MPC [P61]：每次规划更新 1–20 ms（在仿真中）
- DROP [P62]：真实灵巧手上的采样式 MPC，25–50 Hz，需 128 线程 CPU
- SAPIEN [P08]、ManiSkill3 [P09]（原生支持 URDF 与 MJCF）、Isaac Lab [P10]
- IndustReal [P97]：仿真训练装配后迁移到实机，实机插入成功率 80%、齿轮 97.5%
- Isaac Lab 与 Isaac Sim 文档：[URDF 导入](https://docs.isaacsim.omniverse.nvidia.com/latest/importer_exporter/ext_isaacsim_asset_importer_urdf.html)
- [MuJoCo 建模文档](https://mujoco.readthedocs.io/en/stable/modeling.html)（支持加载 URDF）

## 参考项目

[FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD)、[galou/freecad.cross](https://github.com/galou/freecad.cross)、[Rhoban/onshape-to-robot](https://github.com/Rhoban/onshape-to-robot)、[ros/solidworks_urdf_exporter](https://github.com/ros/solidworks_urdf_exporter)、[CadQuery/cadquery](https://github.com/CadQuery/cadquery)、[SarahWeiii/CoACD](https://github.com/SarahWeiii/CoACD)、[google-deepmind/mujoco](https://github.com/google-deepmind/mujoco)、[google-deepmind/mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie)、[google-deepmind/mujoco_mpc](https://github.com/google-deepmind/mujoco_mpc)、[isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab)、[mani-skill/ManiSkill](https://github.com/mani-skill/ManiSkill)、[gazebosim/gz-sim](https://github.com/gazebosim/gz-sim)
