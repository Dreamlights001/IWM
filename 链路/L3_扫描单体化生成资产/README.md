# L3 没有 STEP 的设备：扫描单体化后生成资产

在 FWAM 中的位置：资产与数据层。整厂里总有设备没有 STEP（老设备、外购件、料架），L3 把它们变成可仿真、可被整厂层调用的实体。

## 思考

- 单体化（把整片扫描拆成对象实例）只是第一步。要能仿真，还要补被遮挡面和接触面、恢复关节、估计物理参数。
- 目前没有一种方法同时完成实例分离、补全、关节恢复，并在工业场景中验证。
- 对整厂层来说，最关键的是**实例 ID 要和 MES、PLC 里的设备 ID 对上**。这一步目前没有现成方法。
- 软体要从接触面上分离出来并指定材料；切开或断裂后露出的内部没有扫描观测（见[专题](../专题_形变流体断裂与加工/README.md)）。

## Idea

1. **以端口为中心的单体化**：不必把每个零件都拆出来，只拆出"整厂层要调用或要感知"的实体：设备整体、门、料架、工件。其余部分作为静态背景。
2. **ID 对齐**：用二维码、RFID 或人工标注把扫描中的实例与设备台账对上，作为 L11 整厂状态图的节点。
3. **由多构型扫描恢复关节**：门开、门关各扫一次，参考 ArticulatedGS、ArtiTwinSplat 恢复关节。

## 实施路线

1. 扫描并重建（同 L2）。
2. 单体化：SAM 2／SAM 3 在 2D 分割，Gaussian Grouping、SAGA、OpenGaussian 提升到 3D。
3. 补全：InstaScene 补全被遮挡部分；DecoupledGaussian 把物体与接触面分开；或用 SAM 3D Objects 从单张图重建物体。
4. 恢复关节：ArticulatedGS、ArtiTwinSplat；或从图像生成关节资产（URDFormer、Articulate-Anything）。
5. 转成可仿真资产：估计或人工指定质量、摩擦，生成碰撞体，导出 URDF／USD，进入 L1。

算力：多数方法单张 3090／4090 可运行；SceneAgent 一类智能体流程需要反复调用 VLM，较慢。

## 推荐文献

- Gaussian Grouping [P89]、SAGA [P90]（一次可提示分割约 4 ms）、OpenGaussian [P91]
- InstaScene [P92]、DecoupledGaussian [P93]
- SceneAgent [P94]：从扫描生成含物理参数和关节的 OpenUSD
- WorldAct [P95]：把整体式三维世界拆成对象
- ArticulatedGS [P26]、ArtiTwinSplat [P27]、URDFormer [P14]、Articulate-Anything [P15]

## 参考项目

[facebookresearch/sam2](https://github.com/facebookresearch/sam2)、[facebookresearch/sam3](https://github.com/facebookresearch/sam3)、[facebookresearch/sam-3d-objects](https://github.com/facebookresearch/sam-3d-objects)、[lkeab/gaussian-grouping](https://github.com/lkeab/gaussian-grouping)、[Jumpat/SegAnyGAussians](https://github.com/Jumpat/SegAnyGAussians)、[yanmin-wu/OpenGaussian](https://github.com/yanmin-wu/OpenGaussian)、[zju3dv/InstaScene](https://github.com/zju3dv/InstaScene)、[wangmiaowei/DecoupledGaussian](https://github.com/wangmiaowei/DecoupledGaussian)、[WEIRDLabUW/urdformer](https://github.com/WEIRDLabUW/urdformer)、[vlongle/articulate-anything](https://github.com/vlongle/articulate-anything)
