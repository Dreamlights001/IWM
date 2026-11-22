# W02 设备资产生成

> 阶段：S1 数据基础　·　总看板：[research_board.html](../research_board.html#W02)

把机床 STEP 和设备扫描变成带关节、碰撞体、物理参数和部件语义的可仿真资产，并能批量生成同类变体。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md)：实体与资产规范 | [W03（车间场景生成）](../W03_车间场景生成/README.md)：可仿真资产 | ② 仿真—真实校准 |

## 1. 为什么要做

STEP 是 B-rep 实体，不含关节语义、碰撞体和质量参数；扫描有外观，但没有部件和关节。现有的关节物体生成方法多以家具、家电为测试对象：URDFormer 从图像预测 URDF [P14](../../papers/P14_URDFormer_2405.11656v3.pdf)，Articulate-Anything 用 VLM 生成关节代码 [P15](../../papers/P15_Articulate_Anything_2410.13882v4.pdf)。机床有多个运动部件（门、主轴、工作台、刀库、夹具），表面多为反光金属，这两点都不在这些工作的主要测试范围内。

## 2. 输入与产物

**输入**

- STEP 装配体
- 实物扫描：点云、照片、RGB-D 视频
- 设备手册中的行程、限位与运动关系
- 机器人 URDF

**产物**

- 每台设备的 URDF／MJCF／USD：部件树、关节类型与限位、凸分解后的碰撞体、质量与惯量估计
- 部件语义：门、按钮、夹具、主轴、料位，以及它们与 PLC 信号的对应（交给 [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md)）
- 配准到 STEP 坐标系的外观（纹理网格或高斯）
- 同类设备的参数化变体，供 [W03（车间场景生成）](../W03_车间场景生成/README.md) 生成场景

## 3. 具体工作

1. STEP 处理：用 CadQuery 或 FreeCAD 读取装配体，按装配结构拆分部件并简化网格；用 CoACD 做凸分解得到碰撞体。
2. 关节推断：从装配约束和部件几何推断关节类型、轴线和限位。JoinABLe 从 CAD B-rep 学习部件连接 [arXiv 2111.12772](https://arxiv.org/abs/2111.12772)，可作为起点；结果用手册核对。
3. 没有 STEP 的设备：从扫描或视频重建关节物体，参考 Real2Code [arXiv 2406.08474](https://arxiv.org/abs/2406.08474)、ArtiTwinSplat [P27](../../papers/P27_ArtiTwinSplat_2606.24628v1.pdf)、ArticulatedGS [P26](../../papers/P26_ArticulatedGS_2503.08135v2.pdf)；已有网格时可用 Articulate AnyMesh 补关节 [arXiv 2502.02590](https://arxiv.org/abs/2502.02590)。
4. 外观：把扫描配准到 STEP 坐标系。反光金属表面参考 NeRO、Ref-NeRF、GaussianShader 的反射建模 [arXiv 2305.17398](https://arxiv.org/abs/2305.17398) [arXiv 2112.03907](https://arxiv.org/abs/2112.03907) [arXiv 2311.17977](https://arxiv.org/abs/2311.17977)。
5. 物理参数：质量、摩擦、驱动增益先取手册值或估计值，留给 [W08（仿真—真实对齐）](../W08_仿真真实对齐/README.md) 校准。
6. 变体生成：对尺寸、门的开向、工作台行程等做参数化，批量导出；程序化生成关节物体可参考 Infinite Mobility [arXiv 2503.13424](https://arxiv.org/abs/2503.13424)。
7. 验收脚本：关节能否按限位运动；碰撞体是否互相穿透；机器人能否到达上下料位。

## 4. 可以写成论文的方向

### 4.1 从 STEP 装配体自动生成带关节的可仿真设备资产

- 类型：方法＋数据集
- 研究问题：能否从装配约束、部件几何和手册文本，自动得到机床的部件树、关节和限位，并输出可直接仿真的 URDF／USD？
- 已有工作与空白：JoinABLe 在 Fusion 360 Gallery 的装配数据上学习 CAD 部件连接 [arXiv 2111.12772](https://arxiv.org/abs/2111.12772)；URDFormer、Articulate-Anything 从图像或网格生成关节物体，测试对象主要是家具和家电 [P14](../../papers/P14_URDFormer_2405.11656v3.pdf) [P15](../../papers/P15_Articulate_Anything_2410.13882v4.pdf)。本轮检索没有找到以机床等生产设备为对象、并检验仿真可用性的工作。
- 怎样验证：在一批设备上统计关节类型、轴线和限位的误差；在仿真中执行上下料、开关门并统计失败率；比较人工修正时间与纯手工建模时间。

### 4.2 生产设备可仿真资产数据集

- 类型：数据集
- 研究问题：整理一批机床、料架、输送线的带关节资产，附部件语义、PLC 信号对应和任务点位，作为公开数据集。
- 已有工作与空白：ABC 提供一百万个 CAD 模型 [arXiv 1812.06216](https://arxiv.org/abs/1812.06216)，Fusion 360 Gallery 提供设计序列与装配连接数据 [arXiv 2010.02392](https://arxiv.org/abs/2010.02392) [arXiv 2111.12772](https://arxiv.org/abs/2111.12772)；它们不含仿真所需的质量、驱动参数和 PLC 语义。
- 怎样验证：在 [W03（车间场景生成）](../W03_车间场景生成/README.md) 的场景生成和 [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md) 的数据生成中实际使用，报告设备类型数和可执行任务数。

### 4.3 反光金属设备的扫描—CAD 配准与外观重建

- 类型：方法
- 研究问题：对反光、少纹理的金属设备，能否用 CAD 几何作先验，提高扫描配准和外观重建的质量？
- 已有工作与空白：NeRO、Ref-NeRF、GaussianShader 处理一般场景中的反射表面 [arXiv 2305.17398](https://arxiv.org/abs/2305.17398) [arXiv 2112.03907](https://arxiv.org/abs/2112.03907) [arXiv 2311.17977](https://arxiv.org/abs/2311.17977)；RialTo 报告薄、透明、反光物体的深度测量会失败 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)。用 CAD 作先验的工业设备重建是可做的方向（分析判断）。
- 怎样验证：与不用 CAD 先验的重建比较几何误差和新视角渲染质量。

## 5. 所在闭环

- ② 仿真—真实校准：W07 真实工位采集轨迹与日志 → W08 比对仿真，辨识参数，学残差 → W02·W03·W04 更新资产参数、场景与节拍 → W05·W12 重新生成数据，重训技能 → 上真机执行。ASID 设计信息量最大的真实交互来辨识参数 [P60](../../papers/P60_ASID_2404.12308v2.pdf)；RialTo 把真实示范迁入扫描得到的仿真 [P59](../../papers/P59_RialTo_2403.03949v3.pdf)；混合训练使真实成功率平均提高 38% [arXiv 2503.24361](https://arxiv.org/abs/2503.24361)。

## 6. 对应的链路

- [L1](../../链路/L1_STEP资产化与物理仿真/README.md)：L1 STEP 资产化＋物理仿真作为世界模型
- [L2](../../链路/L2_扫描配准与数字孪生/README.md)：L2 扫描配准到 STEP 资产，并校准成数字孪生
- [L3](../../链路/L3_扫描单体化生成资产/README.md)：L3 没有 STEP 的设备：扫描单体化后生成资产

## 7. 高价值参考文献

### CAD 与关节数据

- **ABC: A Big CAD Model Dataset For Geometric Deep Learning**（2018），[arXiv 1812.06216](https://arxiv.org/abs/1812.06216)：ABC：一百万个 CAD 模型，用于几何深度学习。
- **Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences**（2020），[arXiv 2010.02392](https://arxiv.org/abs/2010.02392)：Fusion 360 Gallery：人类 CAD 设计序列的数据集与环境。
- **JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints**（2021），[arXiv 2111.12772](https://arxiv.org/abs/2111.12772)：JoinABLe：从 B-rep 学习参数化 CAD 部件之间的连接。

### 从图像、网格或视频得到关节物体

- **URDFormer: A Pipeline for Constructing Articulated Simulation Environments from Real-World Images**（2024），[P14 本地 PDF](../../papers/P14_URDFormer_2405.11656v3.pdf)：URDFormer：从图像预测分层 URDF。
- **Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model**（2024），[P15 本地 PDF](../../papers/P15_Articulate_Anything_2410.13882v4.pdf)：Articulate-Anything：VLM 生成关节代码并迭代修正。
- **Real2Code: Reconstruct Articulated Objects via Code Generation**（2024），[arXiv 2406.08474](https://arxiv.org/abs/2406.08474)：Real2Code：用代码生成重建关节物体。
- **Articulate AnyMesh: Open-Vocabulary 3D Articulated Objects Modeling**（2025），[arXiv 2502.02590](https://arxiv.org/abs/2502.02590)：Articulate AnyMesh：把任意刚体网格转成关节物体，开放词表。
- **Infinite Mobility: Scalable High-Fidelity Synthesis of Articulated Objects via Procedural Generation**（2025），[arXiv 2503.13424](https://arxiv.org/abs/2503.13424)：Infinite Mobility：程序化合成高保真关节物体。
- **ArticulatedGS: Self-supervised Digital Twin Modeling of Articulated Objects using 3D Gaussian Splatting**（2025），[P26 本地 PDF](../../papers/P26_ArticulatedGS_2503.08135v2.pdf)：ArticulatedGS：从两个关节构型的多视图估计部件和运动参数。
- **ArtiTwinSplat: Interactable Digital Twin Reconstruction via Gaussian Splatting from RGB-D videos**（2026），[P27 本地 PDF](../../papers/P27_ArtiTwinSplat_2606.24628v1.pdf)：ArtiTwinSplat：从 RGB-D 视频恢复部件、关节和可交互高斯孪生，可导出 URDF。
- **SceneAgent: An Agentic Pipeline from 3D and 4D Captures to Simulation Environments**（2026），[P94 本地 PDF](../../papers/P94_SceneAgent_2610.34745v1.pdf)：SceneAgent：把 3DGS、摄影测量、LiDAR 等采集结果转成仿真环境。

### 反光表面重建

- **NeRO: Neural Geometry and BRDF Reconstruction of Reflective Objects from Multiview Images**（2023），[arXiv 2305.17398](https://arxiv.org/abs/2305.17398)：NeRO：从多视图重建反光物体的几何与 BRDF。
- **Ref-NeRF: Structured View-Dependent Appearance for Neural Radiance Fields**（2021），[arXiv 2112.03907](https://arxiv.org/abs/2112.03907)：Ref-NeRF：结构化的视角相关外观。
- **GaussianShader: 3D Gaussian Splatting with Shading Functions for Reflective Surfaces**（2023），[arXiv 2311.17977](https://arxiv.org/abs/2311.17977)：GaussianShader：带着色函数的高斯，用于反光表面。

### 扫描到仿真的完整流程

- **Reconciling Reality through Simulation: A Real-to-Sim-to-Real Approach for Robust Manipulation**（2024），[P59 本地 PDF](../../papers/P59_RialTo_2403.03949v3.pdf)：RialTo：扫描现场、在界面里补关节、导出 USD；搭一个场景约 15 分钟人工。

## 8. 参考项目

- [SarahWeiii/CoACD](https://github.com/SarahWeiii/CoACD)：凸分解，生成碰撞体
- [Rhoban/onshape-to-robot](https://github.com/Rhoban/onshape-to-robot)：把 Onshape 装配体导出为 URDF、SDF 或 MuJoCo 模型
- [galou/freecad.cross](https://github.com/galou/freecad.cross)：FreeCAD 的 ROS 工作台，可在 FreeCAD 中搭建并导出机器人描述
- [CadQuery/cadquery](https://github.com/CadQuery/cadquery)：Python 参数化 CAD，可读写 STEP
- [AutodeskAILab/Fusion360GalleryDataset](https://github.com/AutodeskAILab/Fusion360GalleryDataset)：Fusion 360 Gallery 数据集与工具
- [MandiZhao/real2code](https://github.com/MandiZhao/real2code)：Real2Code 实现
- [vlongle/articulate-anything](https://github.com/vlongle/articulate-anything)：Articulate-Anything 实现
- [WEIRDLabUW/urdformer](https://github.com/WEIRDLabUW/urdformer)：URDFormer 实现

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
