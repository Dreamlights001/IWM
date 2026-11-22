#!/usr/bin/env python3
"""Build pipeline_board.html: candidate pipelines (链路) for the given inputs.

Inputs assumed by the board: STEP files of machine tools and other production
equipment, 3D scans of the same physical equipment, and one robot with a URDF
(humanoid, mobile base or arm).

The board lists pipelines side by side. It does not rank them or recommend one.
Every paper reference must exist in research/P*.json; every external link was
checked on 2026-11-14 (GitHub repos via the GitHub API, docs via HTTP 200).
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
papers = {p.stem: json.loads(p.read_text()) for p in (ROOT / 'research').glob('P[0-9][0-9].json')}
sources = {s['id']: s for s in json.loads((ROOT / 'research/supplementary_sources.json').read_text())}

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- external links
# GitHub repos: verified with `gh api repos/<name>` on 2026-11-14 (exists, not archived
# unless noted). Docs: verified HTTP 200 on 2026-11-14.
GH = {
 # CAD → asset
 'freecad': ('FreeCAD/FreeCAD', 'STEP 打开、简化、导出网格'),
 'cross': ('galou/freecad.cross', 'FreeCAD 中生成 URDF／xacro'),
 'sw2urdf': ('ros/solidworks_urdf_exporter', 'SolidWorks 装配导出 URDF'),
 'onshape': ('Rhoban/onshape-to-robot', 'Onshape 装配导出 URDF／SDF／MJCF'),
 'cadquery': ('CadQuery/cadquery', '用 Python 读写 STEP（基于 OCCT）'),
 'build123d': ('gumyr/build123d', '用 Python 读写和修改 STEP'),
 'pythonocc': ('tpaviot/pythonocc-core', 'OCCT 的 Python 绑定'),
 'coacd': ('SarahWeiii/CoACD', '凸分解，生成碰撞体'),
 'vhacd': ('kmammou/v-hacd', '凸分解，生成碰撞体'),
 'xacro': ('ros/xacro', 'URDF 宏'),
 'urdfpy': ('ros/urdf_parser_py', '用 Python 解析 URDF'),
 # simulators
 'mujoco': ('google-deepmind/mujoco', '物理引擎，可直接加载 URDF'),
 'menagerie': ('google-deepmind/mujoco_menagerie', '现成机器人模型（含 Unitree G1／H1、Franka、UR、FANUC CRX 等）'),
 'mjwarp': ('google-deepmind/mujoco_warp', 'MuJoCo 的 GPU 版本'),
 'mjpc': ('google-deepmind/mujoco_mpc', '以 MuJoCo 为模型的实时 MPC'),
 'playground': ('google-deepmind/mujoco_playground', '基于 MuJoCo 的仿真与实机示例'),
 'isaacsim': ('isaac-sim/IsaacSim', 'USD 场景、URDF 导入、传感器仿真'),
 'isaaclab': ('isaac-sim/IsaacLab', '并行环境与机器人学习'),
 'newton': ('newton-physics/newton', '基于 Warp 的多求解器物理引擎'),
 'maniskill': ('mani-skill/ManiSkill', 'GPU 并行操作仿真'),
 'sapien': ('haosulab/SAPIEN', '基于部件的交互仿真'),
 'genesis': ('Genesis-Embodied-AI/genesis-world', '多物理仿真平台'),
 'gz': ('gazebosim/gz-sim', 'Gazebo，ROS 生态的仿真器'),
 'drake': ('RobotLocomotion/drake', '模型化设计与验证'),
 'pinocchio': ('stack-of-tasks/pinocchio', '刚体动力学算法'),
 # robot control
 'ros2control': ('ros-controls/ros2_control', 'ROS 2 控制框架'),
 'gzros2control': ('ros-controls/gz_ros2_control', 'Gazebo 与 ros2_control 对接'),
 'moveit': ('moveit/moveit2', '机械臂运动规划'),
 'curobo': ('NVlabs/curobo', 'GPU 运动规划'),
 'nav2': ('ros-navigation/navigation2', '移动底盘导航'),
 'rslrl': ('leggedrobotics/rsl_rl', '腿式与人形机器人的强化学习'),
 'lerobot': ('huggingface/lerobot', '机器人数据采集与策略学习'),
 'dp': ('real-stanford/diffusion_policy', 'Diffusion Policy'),
 'openpi': ('Physical-Intelligence/openpi', 'π0 系列 VLA'),
 # scan & reconstruction
 'colmap': ('colmap/colmap', 'SfM／MVS 相机位姿与稠密重建'),
 'open3d': ('isl-org/Open3D', '点云处理与配准'),
 'fastlio': ('hku-mars/FAST_LIO', '激光惯导里程计，用于大范围扫描'),
 'dust3r': ('naver/dust3r', '前馈多视图重建'),
 'mast3r': ('naver/mast3r', '前馈多视图重建与匹配'),
 'vggt': ('facebookresearch/vggt', '前馈相机、深度与点图预测'),
 'gs': ('graphdeco-inria/gaussian-splatting', '3DGS 原始实现'),
 'gsplat': ('nerfstudio-project/gsplat', 'CUDA 高斯渲染库'),
 'nerfstudio': ('nerfstudio-project/nerfstudio', '重建训练框架'),
 '2dgs': ('hbb1/2d-gaussian-splatting', '几何更准确的高斯，便于取网格'),
 'sugar': ('Anttwo/SuGaR', '从高斯提取网格'),
 # segmentation / instance
 'sam2': ('facebookresearch/sam2', '图像与视频分割'),
 'sam3': ('facebookresearch/sam3', '可提示的概念分割'),
 'sam3d': ('facebookresearch/sam-3d-objects', '单张图像重建物体三维'),
 'ggroup': ('lkeab/gaussian-grouping', '给每个高斯打实例标签'),
 'saga': ('Jumpat/SegAnyGAussians', '可提示的三维高斯分割'),
 'opengs': ('yanmin-wu/OpenGaussian', '开放词表三维实例'),
 'instascene': ('zju3dv/InstaScene', '实例分解并补全'),
 'decoupled': ('wangmiaowei/DecoupledGaussian', '物体与接触面分离'),
 'foundationpose': ('NVlabs/FoundationPose', '已知 CAD 的 6D 位姿估计与跟踪'),
 'urdformer': ('WEIRDLabUW/urdformer', '由图像生成关节资产'),
 'artanything': ('vlongle/articulate-anything', '由图像或视频生成关节资产'),
 'conceptgraphs': ('concept-graphs/concept-graphs', '开放词表三维场景图'),
 'hydra': ('MIT-SPARK/Hydra', '实时三维场景图'),
 # Gaussian + physics, 3D dynamics
 'physgaussian': ('XPandora/PhysGaussian', '高斯＋MPM 物理'),
 'phystwin': ('Jianghanxiao/PhysTwin', '可变形物体的物理孪生'),
 'embgs': ('rai-opensource/embodied_gaussians', 'Real-is-Sim 使用的高斯＋粒子仿真器'),
 'pointworld': ('NVlabs/PointWorld', '动作条件三维点流'),
 'gns': ('google-deepmind/deepmind-research', 'GNS 与 MeshGraphNets（learning_to_simulate、meshgraphnets 目录）'),
 'disect': ('NVlabs/DiSECt', '可微切割仿真'),
 'opencamlib': ('aewallin/opencamlib', 'CAM 刀路与几何算法'),
 # deformable / fluid / fracture simulators and benchmarks (cross-cutting section)
 'sofa': ('sofa-framework/sofa', '有限元交互仿真，支持动态拓扑变化'),
 'softgym': ('Xingyu-Lin/softgym', '布、绳、液体基准（FleX）'),
 'adaptigraph': ('Boey-li/AdaptiGraph', '材料自适应图神经动力学；DINO-WM 的 PyFleX 编译方法来源'),
 'plasticinelab': ('hzaskywalker/PlasticineLab', '可微弹塑性软体基准'),
 'fluidlab': ('zhouxian/FluidLab', '可微流体操作基准'),
 'daxbench': ('AdaCompNUS/DaXBench', '可微形变操作基准（JAX）'),
 'warp': ('NVIDIA/warp', 'GPU 仿真编程框架，Newton 构建在其上'),
 'taichi': ('taichi-dev/taichi', 'GPU 编程框架'),
 # real-to-sim
 'rialtogui': ('real-to-sim-to-real/RialToGUI', 'RialTo 的扫描建孪生界面'),
 'rialtopl': ('real-to-sim-to-real/RialToPolicyLearning', 'RialTo 策略学习流程'),
 'industreal': ('NVlabs/industreallib', 'IndustReal 实机部署库'),
 # JEPA / latent
 'vjepa2': ('facebookresearch/vjepa2', 'V-JEPA 2 与 V-JEPA 2-AC'),
 'jepawms': ('facebookresearch/jepa-wms', 'JEPA 世界模型对照研究'),
 'dinowm': ('gaoyuezhou/dino_wm', 'DINO-WM'),
 'lewm': ('lucas-maes/le-wm', 'LeWorldModel'),
 'intact': ('zju3dv/INTACT-JEPA', 'INTACT：意图到动作、无搜索的 JEPA 世界模型'),
 'dreamerv3': ('danijar/dreamerv3', 'DreamerV3'),
 'tdmpc2': ('nicklashansen/tdmpc2', 'TD-MPC2'),
 # video
 'ctrlworld': ('Robert-gyj/Ctrl-World', 'Ctrl-World'),
 'dreamdojo': ('NVIDIA/DreamDojo', 'DreamDojo'),
 'ge': ('AgibotTech/Genie-Envisioner-V1', 'Genie Envisioner'),
 'gesim2': ('AgibotTech/GE-Sim-V2', 'GE-Sim 2.0'),
 'cosmost1': ('nvidia-cosmos/cosmos-transfer1', 'Cosmos-Transfer1，仿真画面转照片级'),
 'cosmosp25': ('nvidia-cosmos/cosmos-predict2.5', 'Cosmos-Predict2.5'),
 'dreamgen': ('NVIDIA/GR00T-Dreams', 'DreamGen'),
 # industrial control & co-sim
 'linuxcnc': ('LinuxCNC/linuxcnc', '开源 CNC 控制器，带仿真配置'),
 'openplc': ('Autonomy-Logic/openplc-runtime', 'OpenPLC Runtime v4，开源软 PLC'),
 'opcua': ('FreeOpcUa/opcua-asyncio', 'Python OPC UA'),
 'open62541': ('open62541/open62541', 'C 语言 OPC UA'),
 'mtconnect': ('mtconnect/cppagent', 'MTConnect 代理'),
 'fmpy': ('CATIA-Systems/FMPy', '在 Python 中运行 FMU'),
 'maestro': ('INTO-CPS-Association/maestro', 'FMI 联仿主控'),
 'openmodelica': ('OpenModelica/OpenModelica', 'Modelica 建模与 FMU 导出'),
}
DOCS = {
 'mj_urdf': ('MuJoCo 建模文档（支持加载 URDF）', 'https://mujoco.readthedocs.io/en/stable/modeling.html'),
 'mj_xml': ('MuJoCo XML 参考（网格支持 STL／OBJ）', 'https://mujoco.readthedocs.io/en/stable/XMLreference.html'),
 'mj_comp': ('MuJoCo 计算与重放', 'https://mujoco.readthedocs.io/en/stable/computation/'),
 'isaac_urdf': ('Isaac Sim URDF 导入', 'https://docs.isaacsim.omniverse.nvidia.com/latest/importer_exporter/ext_isaacsim_asset_importer_urdf.html'),
 'isaac_mjcf': ('Isaac Sim MJCF 导入', 'https://docs.isaacsim.omniverse.nvidia.com/latest/importer_exporter/ext_isaacsim_asset_importer_mjcf.html'),
 'isaac_perf': ('Isaac Sim 性能手册', 'https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/sim_performance_optimization_handbook.html'),
 'gz_urdf': ('Gazebo 加载 URDF', 'https://gazebosim.org/docs/latest/spawn_urdf/'),
 'onshape_docs': ('onshape-to-robot 文档', 'https://onshape-to-robot.readthedocs.io/en/latest/'),
 'open3d_icp': ('Open3D ICP 配准教程', 'https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html'),
 'newton_docs': ('Newton 文档', 'https://newton-physics.github.io/newton/'),
 'linuxcnc_sim': ('LinuxCNC 仿真配置说明', 'http://linuxcnc.org/docs/html/getting-started/running-linuxcnc.html'),
 'linuxcnc_arch': ('LinuxCNC 架构概览', 'https://linuxcnc.org/docs/stable/html/code/code-notes.html#_architecture_overview'),
 'plcsim': ('Siemens S7-PLCSIM Advanced', 'https://www.siemens.com/en-us/products/simatic/s7-plcsim-advanced/'),
 'vc_guide': ('Siemens 虚拟调试指南（PLCSIM Advanced＋SIMIT＋NX MCD）', 'https://cache.industry.siemens.com/dl/files/864/109963864/att_1277519/v1/Guideline_VC_SIMIT_PSA_MCD_V1.0.0.pdf'),
 'sinumerik': ('SINUMERIK 虚拟机床系统手册', 'https://cache.industry.siemens.com/dl/files/129/109988129/att_1326187/v1/ONE_828D_cmvm_sys_man_0325_en-US.pdf?download=true'),
 'opcua_mt': ('OPC UA for Machine Tools', 'https://reference.opcfoundation.org/specs/OPC-40501-1/6'),
 'mtconnect_site': ('MTConnect', 'https://www.mtconnect.org/'),
 'fmi': ('FMI 3.0.2 规范', 'https://fmi-standard.org/docs/3.0.2/'),
 'simpy': ('SimPy 文档（离散事件仿真）', 'https://simpy.readthedocs.io/en/latest/'),
 'openusd': ('OpenUSD', 'https://openusd.org/release/index.html'),
 'realissim': ('Real-is-Sim 项目页', 'https://real-is-sim.github.io/'),
 'rialto': ('RialTo 项目页', 'https://real-to-sim-to-real.github.io/RialTo/'),
 'asid': ('ASID 项目页', 'https://weirdlabuw.github.io/asid/'),
 'embgs_site': ('Embodied Gaussians 项目页', 'https://embodied-gaussians.github.io/'),
 'pointworld_site': ('PointWorld 项目页', 'https://point-world.github.io/'),
 'ctrlworld_site': ('Ctrl-World 项目页', 'https://ctrl-world.github.io/'),
 'dreamzero_site': ('DreamZero 项目页', 'https://dreamzero0.github.io/'),
 'ge_site': ('Genie Envisioner 项目页', 'https://genie-envisioner.github.io/'),
 'dreamdojo_site': ('DreamDojo 项目页', 'https://dreamdojo-world.github.io/'),
 # JEPA additions
 'intact_paper': ('INTACT 论文（arXiv 2607.26056）', 'https://arxiv.org/abs/2607.26056'),
 'intact_site': ('INTACT 项目页', 'https://zju3dv.github.io/INTACT-JEPA/'),
 'intact_hf': ('INTACT 权重（Hugging Face）', 'https://huggingface.co/INTACT-JEPA/INTACT'),
 'sadl_paper': ('SADL 论文（arXiv 2611.21596）', 'https://arxiv.org/abs/2611.21596'),
 'sadl_site': ('SADL 项目页（代码未发布）', 'https://ctnkrl.github.io/SADLwebsite/'),
 # deformable / fluid / fracture capability docs
 'mj_flex': ('MuJoCo：Deformable objects（flex／flexcomp）', 'https://mujoco.readthedocs.io/en/stable/modeling.html#deformable-objects'),
 'mj_fluid': ('MuJoCo：流体力', 'https://mujoco.readthedocs.io/en/stable/computation/fluid.html'),
 'newton_solvers': ('Newton 1.7.0 求解器特性表', 'https://newton-physics.github.io/newton/1.7.0/solvers/index.html'),
 'newton_mpm': ('Newton SolverImplicitMPM', 'https://newton-physics.github.io/newton/1.7.0/api/_generated/newton.solvers.SolverImplicitMPM.html'),
 'isaaclab_assets': ('Isaac Lab 资产 API（DeformableObject、CableObject）', 'https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html'),
 'physx_particles': ('PhysX 5.8.0 粒子系统（PBD）', 'https://nvidia-omniverse.github.io/PhysX/physx/5.8.0/docs/ParticleSystem.html'),
 'physx_defvol': ('PhysX 5.8.0 Deformable Volume', 'https://nvidia-omniverse.github.io/PhysX/physx/5.8.0/docs/DeformableVolume.html'),
 'genesis_cut': ('Genesis 示例 cut_dragon.py', 'https://github.com/Genesis-Embodied-AI/genesis-world/blob/main/examples/coupling/cut_dragon.py'),
 'sofa_topo': ('SOFA 拓扑与拓扑变化', 'https://sofa-framework.github.io/doc/simulation-principles/topology/'),
}

# ---------------------------------------------------------------- pipelines
# Each pipeline: inputs used, stages (sequence), what it predicts, evidence, repos, docs, papers, limits.
# kind: which world-model route the pipeline belongs to.
INPUTS = {
 'step': 'STEP 文件',
 'scan': '实物扫描',
 'urdf': '机器人 URDF',
 'plc': 'PLC／NC 程序或日志',
 'video': '现场视频＋动作记录',
 'proc': '工艺信号（力、热、压力）',
}
PIPELINES = [
 dict(id='L1', name='STEP 资产化＋物理仿真作为世界模型', route='显式仿真',
  uses=['step','urdf'], opt=['scan'],
  stages=[
   ('STEP 清理', '去掉螺钉、倒角等小特征；拆出运动部件（轴、门、卡盘、夹具、按钮）；统一单位与坐标系'),
   ('导出视觉网格与碰撞体', '视觉用细网格；碰撞体做凸分解或用简单形状；装夹面、按钮、插接面保留能分辨任务公差的几何'),
   ('写关节与驱动', '机床轴、门、夹具写成关节（URDF／MJCF／USD），设定行程、限位、驱动方式；机器人直接加载已有 URDF'),
   ('组装场景', '机床、机器人、料架、工件放进同一坐标系；校核质心、惯量、摩擦'),
   ('推演与规划', '仿真器作为转移函数：给定动作推演结果，做 MPC 或离线评估策略'),
  ],
  predicts='机器人与机床部件的运动、接触、夹持；PLC 逻辑接入后还包括设备模式与事件（见 L4）',
  latency='MuJoCo MPC 每次规划更新 1–20 ms（仿真中）；DROP 在真实灵巧手上 25–50 Hz（128 线程 CPU）[[P61]][[P62]]',
  evidence='MuJoCo、Isaac Sim、Gazebo 都能加载 URDF；ManiSkill3 原生支持 URDF 与 MJCF；IndustReal 在仿真中训练插装、齿轮装配并迁移到实机，实机插入成功率 80%、齿轮 97.5% [[P96]][[P09]][[P97]]',
  repos=['freecad','cross','sw2urdf','onshape','cadquery','coacd','vhacd','mujoco','menagerie','mjpc','isaacsim','isaaclab','maniskill','gz','ros2control','moveit','curobo','nav2','rslrl'],
  docs=['mj_urdf','mj_xml','isaac_urdf','isaac_mjcf','gz_urdf','onshape_docs'],
  papers=['P96','P61','P62','P08','P09','P10','P97'],
  limits='每台机型都要人工拆部件、写关节和校参数；STEP 不含质量、摩擦、驱动和延迟；不含形变、流体、切削、磨损等（任务涉及时见下文“跨链路条件”）；仿真与现场会有偏差（见 L2、L3）。',
 ),
 dict(id='L2', name='扫描配准到 STEP 资产，并校准成数字孪生', route='显式仿真＋空间智能',
  uses=['step','scan','urdf'], opt=['plc'],
  stages=[
   ('扫描现场', '激光或多视角相机扫描机床、工位与通道；记录尺度基准'),
   ('重建', '得到点云或高斯（大范围可用激光惯导，局部用 SfM／前馈重建）'),
   ('与 STEP 配准', '把 L1 的 STEP 资产与扫描点云做 ICP 配准，得到每台设备在现场的实际位姿；扫描里 STEP 没有的东西（线缆、护罩、料架）另作静态物体'),
   ('外观与观测', '用扫描得到的高斯渲染现场外观，使仿真图像接近真实相机'),
   ('辨识与同步', '用少量真实动作辨识摩擦、惯量、驱动增益、延迟；运行时用编码器与 PLC 信号持续把仿真状态拉回现场'),
  ],
  predicts='与 L1 相同，但初态、布局和外观来自现场，可与真实观测逐帧比较',
  latency='Real-is-Sim 的数字孪生以 60 Hz 与现场同步 [[P58]]；RialTo 搭一个场景约 15 分钟人工，每个任务训练约 2 天 [[P59]]',
  evidence='RialTo 扫描后导出 USD 到 Isaac Sim；ASID 主动设计少量真实交互来辨识物理参数；Real-is-Sim 用高斯＋粒子仿真器持续同步；DreMa、Robo-GS 用高斯渲染、物理引擎推进 [[P59]][[P60]][[P58]][[P23]][[P22]]',
  repos=['colmap','open3d','fastlio','vggt','dust3r','gsplat','gs','nerfstudio','foundationpose','embgs','rialtogui','rialtopl'],
  docs=['open3d_icp','realissim','rialto','asid','embgs_site'],
  papers=['P59','P60','P58','P23','P22','P36','P16'],
  limits='机床多为反光金属和透明防护罩，扫描与重建容易出错；ASID 假设真实动力学落在已知参数化模型内；Real-is-Sim 的同步依赖视觉校正，封闭机床内部看不到。',
 ),
 dict(id='L3', name='没有 STEP 的设备：扫描单体化后生成资产', route='空间智能→显式仿真',
  uses=['scan','urdf'], opt=['video'],
  stages=[
   ('扫描并重建', '同 L2 的前两步'),
   ('单体化', '把整片场景拆成对象实例：给高斯打实例标签，或用 2D 分割提升到 3D'),
   ('补全', '补上被遮挡面、底面和接触面，得到完整对象'),
   ('恢复关节', '从多个构型（门开／关、夹具开／合）的扫描中恢复部件与关节'),
   ('转成可仿真资产', '估计或人工指定质量、摩擦，生成碰撞体，导出 URDF／USD，进入 L1'),
  ],
  predicts='与 L1 相同；资产精度取决于扫描与补全质量',
  latency='SAGA 一次可提示三维分割约 4 ms [[P90]]；SceneAgent 转换一个场景需要反复调用 VLM，速度慢 [[P94]]',
  evidence='Gaussian Grouping、SAGA、OpenGaussian 给出实例标签；InstaScene、DecoupledGaussian 补全对象；SceneAgent 从扫描生成含物理参数和关节的 OpenUSD；ArticulatedGS、ArtiTwinSplat 从多构型恢复关节 [[P89]][[P90]][[P91]][[P92]][[P93]][[P94]][[P26]][[P27]]',
  repos=['sam2','sam3','sam3d','ggroup','saga','opengs','instascene','decoupled','urdformer','artanything','2dgs','sugar','coacd'],
  docs=['open3d_icp'],
  papers=['P89','P90','P91','P92','P93','P94','P95','P26','P27','P14','P15'],
  limits='没有一种方法同时完成实例分离、补全、关节恢复并在工业场景中验证；透明、高反射物体普遍失效；物理参数未经实测校准；锁止、驱动、PLC 语义不能从外观恢复。',
 ),
 dict(id='L4', name='设备逻辑联仿：PLC／NC 接入仿真，再接产线离散事件', route='显式仿真＋结构化流程',
  uses=['step','urdf','plc'], opt=['scan'],
  stages=[
   ('设备 I/O 映射', '把 L1 资产中的门、夹具、按钮、轴与 PLC／NC 的输入输出变量一一对应'),
   ('接入控制器', '软件在环：虚拟 PLC／NC 运行真实程序或行为模型；或硬件在环：真实控制器连仿真对象'),
   ('统一时钟', '物理步长、PLC 扫描周期、NC 插补周期在同一主循环或 FMI 联仿中对齐；记录请求、确认、到位三类事件'),
   ('产线层', '工单、工艺路线、缓存、搬运、故障进离散事件队列；详细仿真的机床由仿真反馈完工，其余用校准过的周期模型'),
   ('反事实', '换单、换路由、机床停机、机器人阻塞、返工的多场景推演'),
  ],
  predicts='设备模式、互锁、报警、程序推进、完工事件；吞吐、在制品、延期、资源争用',
  latency='离散事件层运行很快；SIL 若控制器只支持实时时钟，则按实时推进；HIL 受真实通信周期约束 [[P98]]',
  evidence='Siemens 指南示范 PLCSIM Advanced 运行 PLC 程序、SIMIT 模拟驱动、NX MCD 做机械仿真；LLM 智能体已能半自动生成 PLC 变量到仿真对象的映射；AWMP 在排产中预测外生订单 [[S30]][[P66]][[P38]]',
  repos=['openplc','linuxcnc','opcua','open62541','mtconnect','fmpy','maestro','openmodelica'],
  docs=['plcsim','vc_guide','sinumerik','linuxcnc_sim','linuxcnc_arch','opcua_mt','mtconnect_site','fmi','simpy'],
  papers=['P66','P98','P99','P38'],
  limits='需要拿到 PLC／NC 程序或至少 I/O 变量表；商用虚拟控制器与特定机型绑定；规则维护成本高；日志中的相关关系不等于干预因果。',
 ),
 dict(id='L6', name='仿真＋学习混合：残差、外观与快速代理', route='显式仿真＋学习',
  uses=['step','urdf','video'], opt=['scan'],
  stages=[
   ('以 L1／L2 为底', '仿真负责已知物理和设备逻辑'),
   ('残差', '用真实数据学习仿真与现场之间的偏差'),
   ('外观', '仿真渲染图转成照片级图像，缩小视觉差距'),
   ('快速代理', '用仿真数据训练图网络或三维动力学模型，替代慢的求解器'),
   ('对照', '与原仿真、真实数据分别比较，确认代理没有引入新偏差'),
  ],
  predicts='与 L1 相同，但更接近现场或更快',
  latency='MeshGraphNets 比原求解器快 11–289 倍；Cosmos-Transfer1 生成 5 秒 1280×704 视频，1 张 B200 约 142 s，64 张约 4.2 s [[P32]][[P64]]',
  evidence='在解析仿真上学习残差优于纯解析和纯学习模型；GNS、MeshGraphNets 学习粒子与网格物理 [[P63]][[P31]][[P32]]',
  repos=['gns','cosmost1','pointworld','mujoco','isaaclab'],
  docs=[],
  papers=['P63','P31','P32','P64'],
  limits='学到的代理会继承仿真偏差：只用仿真数据预训练的 PointWorld 不能零样本泛化到真实场景 [[P44]]；Cosmos-Transfer1 只重新渲染给定的仿真画面，不做动作条件预测。',
 ),
 dict(id='L7', name='扫描场景中的三维动作条件动力学', route='空间智能',
  uses=['scan','urdf','video'], opt=['plc'],
  stages=[
   ('三维状态', '用深度相机或扫描得到场景点云或高斯'),
   ('机器人动作接地', '用 URDF 正向运动学把机器人动作变成三维点或末端轨迹'),
   ('学习转移', '训练模型预测动作引起的点流、高斯运动或对象刚体运动'),
   ('规划', '用 MPPI／CEM 在模型中搜索动作'),
   ('补设备状态', '门锁、PLC 模式等不能从点位移看出，需要作为额外条件输入'),
  ],
  predicts='机器人操作引起的三维几何变化（工件、门、夹具的位移）',
  latency='PointWorld 一次批量前向约 0.1 s，预测 10 步 [[P44]]',
  evidence='PointWorld 用约 200 万条轨迹训练，单个预训练模型让真实 Franka 无需额外示范或后训练即可完成推、可变形物体和关节物体操作；GWM 以高斯为状态做模型式强化学习；MRO-GWM 以对象为单位预测刚体运动 [[P44]][[P85]][[P88]]',
  repos=['pointworld','physgaussian','phystwin','gsplat','foundationpose'],
  docs=['pointworld_site'],
  papers=['P44','P85','P88','P19','P21'],
  limits='只覆盖几何层；设备内部状态、工艺、生产流都要另外接入；多为刚体与桌面规模。',
 ),
 dict(id='L8', name='JEPA 特征空间世界模型', route='JEPA',
  uses=['video','urdf'], opt=['plc','proc'],
  stages=[
   ('采集', '多视角视频＋机器人动作（来自 URDF 关节或末端）＋设备信号，时间对齐'),
   ('编码', '用预训练视频编码器（如 V-JEPA 2）或从头训练小模型'),
   ('动作条件预测器', '在特征空间预测动作后的未来特征；设备状态和工艺信号作为条件或额外输入'),
   ('读出与验证', '用读出头检查特征是否保留了门锁、夹紧、位置等关键状态'),
   ('规划或监控', '用 CEM 规划，或用 INTACT 式意图头直接输出动作（不搜索）；也可以用预测误差做异常检测'),
  ],
  predicts='动作之后的观测特征；接读出头后可得到可量测的状态',
  latency='V-JEPA 2-AC 每个动作约 16 s（单张 RTX 4090）；LeWorldModel 完整规划不到 1 s；DINO-WM 一次 CEM 规划 53 s [[P05]][[P55]][[P07]]；INTACT 不搜索、直接输出动作，2.9–5.5 ms，对照 CEM 300×30 的 1.48 s（arXiv 2607.26056）',
  evidence='V-JEPA 2-AC 在两个实验室的 Franka 上零样本抓放；工业过程 JEPA 在注塑过程上推断参数调整；DINO-WM 在 FleX 仿真的绳和颗粒任务上用 1000 条随机动作轨迹训练，倒角距离 0.41 和 0.26 [[P05]][[P37]][[P07]]。INTACT 在四个仿真任务上训练一个 epoch、不搜索，成功率 85.78%–100%；SADL 把 LeWM 和 INTACT 十个种子中的塌缩率从 50% 降到 0%（arXiv 2607.26056、2611.21596）',
  repos=['vjepa2','jepawms','dinowm','lewm','intact','adaptigraph'],
  docs=['intact_paper','intact_site','intact_hf','sadl_paper','sadl_site'],
  papers=['P05','P55','P07','P54','P57','P37'],
  limits='需要带动作的交互数据；潜空间要靠读出头验证；仅用视频时分不清“门关但未锁”这类情况；INTACT 和 SADL 只在刚体仿真任务上验证，形变、流体、断裂和真实机器人上都没有数据。',
 ),
 dict(id='L9', name='潜变量模型式强化学习（单工位任务）', route='潜变量控制',
  uses=['urdf'], opt=['step','scan','video'],
  stages=[
   ('定义任务', '观测、动作、奖励、终止条件，例如“上料并夹紧”'),
   ('数据', '在 L1／L2 仿真中或真实机器人上采集交互'),
   ('学潜模型', '学习潜状态转移、奖励与价值'),
   ('想象中训练', 'Dreamer 式在想象中训练策略，或 TD-MPC 式在潜空间做 MPC'),
   ('迁移与验收', '到真实工位验证，按真实结果而不是模型自评判定成功'),
  ],
  predicts='与任务相关的潜状态与奖励，不是通用状态',
  latency='Dreamer 4 的视频世界模型在单张 H100 上 21 帧/秒 [[P69]]',
  evidence='DreamerV3 用同一套超参数在 150 多个任务上优于专用方法；TD-MPC2 训练 3.17 亿参数的多任务智能体 [[P02]][[P03]]',
  repos=['dreamerv3','tdmpc2','rslrl','isaaclab'],
  docs=[],
  papers=['P02','P03','P69'],
  limits='模型与奖励绑定，换目标难复用；不可逆过程（切削、报废）难以靠试错覆盖；策略可能利用模型漏洞。',
 ),
 dict(id='L10', name='视频世界模型：合成数据与策略评估', route='生成式视频',
  uses=['video','urdf'], opt=['scan'],
  stages=[
   ('采集', '现场视频＋机器人动作或位姿'),
   ('微调', '在预训练视频模型上用目标机器人数据后训练'),
   ('生成', '以动作或指令为条件生成未来视频'),
   ('用途', '在想象中评估策略，或生成合成轨迹后用逆动力学补出动作再训练策略'),
   ('核对', '与真实成功率对照；检查非专家动作下是否仍遵循动作'),
  ],
  predicts='动作或指令之后的画面；不直接给出数值状态',
  latency='DreamDojo 蒸馏后 10.81 帧/秒（单张 H100）；当规划模型时 Cosmos 每个动作约 4 分钟；DreamGen 生成 24 万条样本用了 1500 张 L40 约 54 小时 [[P75]][[P05]][[P65]]',
  evidence='Veo 机器人评估与 1600 多次真实试验相关 0.88；Ctrl-World 把新指令上的成功率从 38.7% 提到 83.4% [[P73]][[P72]]',
  repos=['ctrlworld','dreamdojo','ge','gesim2','cosmosp25','dreamgen','lerobot'],
  docs=['ctrlworld_site','dreamdojo_site','ge_site','dreamzero_site'],
  papers=['P73','P72','P75','P65','P71','P76','P77'],
  limits='推理开销大；物理与几何一致性没有保证；会高估或低估成功率；只用专家数据训练的模型在偏离专家的动作上常不遵循动作 [[P77]]。',
 ),
]

ROUTE_ORDER = ['显式仿真','显式仿真＋空间智能','空间智能→显式仿真','显式仿真＋结构化流程','显式仿真＋学习','空间智能','JEPA','潜变量控制','生成式视频']

# Combinations: pipelines that share an interface and can run together.
COMBOS = [
 ('L1＋L2＋L4', '有 STEP、能扫描、能拿到 PLC 程序时：资产来自 STEP，布局与外观来自扫描，设备逻辑来自 PLC。'),
 ('L3＋L1', '部分设备没有 STEP：先单体化生成资产，再与有 STEP 的设备放进同一场景。'),
 ('L1／L2＋L6', '仿真与现场差距大，或求解太慢时：保留仿真，补残差、外观或快速代理。'),
 ('L1／L2＋L8 或 L10', '有现场视频时：仿真提供设备状态与动作接地，视觉模型提供外观层预测或数据。'),
]

# Robot form → what changes in each pipeline.
ROBOTS = [
 ('机械臂', 'URDF 直接进 L1；运动规划可用 MoveIt 2、cuRobo；L7、L8、L10 的公开数据与模型大多基于机械臂（Franka、DROID 等）。', ['moveit','curobo','menagerie']),
 ('移动底盘（小车）', '需要整厂地图与通道（L2 的扫描）；导航可用 Nav2；L4 的产线层管搬运与资源占用。', ['nav2','fastlio','gz']),
 ('人形', '平衡与步态通常先在仿真中用强化学习训练；Menagerie 收录了 Unitree G1／H1、Apptronik Apollo、Booster T1 等模型；L10 中 GE、DreamZero 使用的是 AgiBot 平台。', ['rslrl','menagerie','isaaclab','mjwarp']),
]

# Cross-cutting task conditions: deformation, fluids, fracture, machining.
# Not a pipeline (the old L5 was folded in here); each pipeline needs extra capability when a task involves them.
TOPIC_DOC = '链路/专题_形变流体断裂与加工/README.md'
TOPIC_NEEDS = [
 ('L1', '换用或接入支持该材料的求解器；STEP 只给几何，软体要生成四面体网格或粒子，并补弹性模量、粘度、摩擦等参数'),
 ('L2', '材料参数要用现场观测辨识，例如 PhysTwin 用视频做逆物理 [[P21]]；形变体状态维度高，运行时同步比刚体难'),
 ('L3', '软体要从接触面上分离并指定材料；切开或断裂后露出的内部没有扫描观测 [[P93]][[P47]]'),
 ('L4', '产线层不模拟材料，只需要工序时长、质量和报废概率，由下面的加工代理或实测统计提供'),
 ('L6', '形变和流体仿真慢，适合训练快速代理：DINO-WM 报告形变环境中仿真推进一步约 3.0 s，模型前向一步约 0.014 s [[P07]]'),
 ('L7', '点流和高斯能直接表示形变；断裂和切割会产生新表面，点之间的对应关系会断开 [[P44]][[P21]][[P19]]'),
 ('L8', '训练数据要来自能表示该现象的仿真器或现场；DINO-WM 在 FleX 绳与颗粒任务上可行 [[P07]]；INTACT、SADL 还没有在这类任务上测试'),
 ('L9', '切割、断裂不可逆，只能在仿真或学习式模型里试错'),
 ('L10', '能生成形变和流体的画面，但不保证材料守恒和物理一致'),
]
# name, rope/cloth/soft body, granular/elasto-plastic, liquid, cutting/fracture, docs, repos
SIM_CAPS = [
 ('MuJoCo 3', 'flex／flexcomp：一维胶囊（绳）、二维带半径三角形（布、壳）、三维四面体（软体）', '未见', '只有刚体在介质中受的流体力，流体本身没有状态', '未见', ['mj_flex','mj_fluid'], ['mujoco']),
 ('Newton 1.7.0', 'VBD：布、软体与刚体在同一求解器（实验性）；Style3D：布；Featherstone、SemiImplicit：软体，布无自碰撞；XPBD：软体为实验性', 'ImplicitMPM：颗粒和弹塑性材料（Drucker–Prager 屈服、粘性、剪胀、硬化与软化）', '特性表未列', '未见', ['newton_solvers','newton_mpm'], ['newton']),
 ('Isaac Lab／PhysX 5', 'DeformableObject（软体、布）；CableObject', '未见', 'PhysX 的 PBD 粒子系统可模拟流体', '切割、撕裂改变拓扑时，要更新预计算的碰撞结构、质量与体积和网格映射 [[S6]]', ['isaaclab_assets','physx_particles','physx_defvol'], ['isaaclab']),
 ('Genesis', 'FEM 软体；PBD 布；IPC', 'MPM（沙轮示例）', 'PBD 液体；SPH', '示例 cut dragon：刚体刀具切开 MPM 弹性体', ['genesis_cut'], ['genesis']),
 ('SOFA', '以有限元为主，侧重医疗与机器人', '未见', '未见', '动态拓扑变化：删除、增加、分离单元；另有 SofaCarving 插件', ['sofa_topo'], ['sofa']),
]
# name, phenomena, note (may cite), repos
BENCHES = [
 ('SoftGym', '布、绳、液体', '基于 NVIDIA FleX；最近一次提交在 2022-11', ['softgym']),
 ('AdaptiGraph', '材料自适应的图神经动力学', 'DINO-WM 的绳任务出自这项工作，用 FleX 仿真 [[P07]]', ['adaptigraph']),
 ('PlasticineLab', '弹性与塑性形变', '可微，基于 DiffTaichi；最近一次提交在 2023-03', ['plasticinelab']),
 ('FluidLab', '液体、固体、气体', '多材料、全可微；最近一次提交在 2023-12', ['fluidlab']),
 ('DaXBench', '液体、布、弹塑性及其混合', '可微，基于 JAX；最近一次提交在 2023-11', ['daxbench']),
 ('DiSECt', '软材料切割', '有限元＋SDF 接触＋连续损伤，可微；不能直接外推到金属切削 [[P46]]', ['disect']),
 ('PhysGaussian', '弹性、塑性、断裂、沙、粘塑性', '高斯＋MPM [[P19]]', ['physgaussian']),
 ('GaussianFluent', '脆性断裂、新的内部表面', '补内部高斯，用连续损伤 MPM 求解 [[P47]]', []),
 ('PhysTwin', '绳、布、毛绒玩具、包裹', '弹簧质点＋高斯外观，从视频辨识参数 [[P21]]', ['phystwin']),
]
# Machining (material removal): content of the former L5.
MACHINING = dict(
 stages=[
  ('毛坯与刀具几何', '工件 STEP 作为毛坯；刀具几何与刀路来自 NC 程序'),
  ('材料去除', '用 dexel、体素或 SDF 扫掠更新工件占用域，输出去除体积与新表面'),
  ('力、热与变形', '需要时耦合切削力、热流与结构变形模型'),
  ('回写', '在同步点同时更新几何版本、碰撞体与质量；工件 ID 不变'),
  ('校准', '用实测力、温度、尺寸与表面质量校准'),
 ],
 evidence='Tri-Dexel 机器人铣削模拟器经铣削实验验证；热—力耦合 NC 模型预测宏观形状误差；DiSECt 做软材料切割的参数辨识，不能直接外推到金属切削 [[P48]][[P50]][[P46]]。论文未给统一时延：几何去除可较快，耦合有限元一般远慢于实时。',
 repos=['opencamlib','disect','cadquery','pythonocc'],
 papers=['P48','P50','P46','P37'],
)

# ---------------------------------------------------------------- helpers
def gh_link(key):
    full, note = GH[key]
    return f'<a class="repo" href="https://github.com/{full}">{esc(full)}</a><span class="note">{esc(note)}</span>'

def doc_link(key):
    title, url = DOCS[key]
    return f'<a class="doc" href="{esc(url)}">{esc(title)}</a>'

def paper_link(pid):
    r = papers[pid]
    year = (r.get('submitted_date') or r.get('publication_date') or '')[:4]
    return (f'<a class="paper" href="{esc(r["local_pdf"])}" title="本地 PDF">{pid}</a>'
            f'<span class="ptitle">{esc(r["title"])}（{year}）</span>'
            f'<a class="src" href="{esc(r["source_url"])}">原文</a>')

import re
def cite(text):
    def p(m):
        pid=m[1]; r=papers[pid]
        return f'<a class="cite" href="{esc(r["local_pdf"])}" title="{esc(r["title"])}">{pid}</a>'
    def s(m):
        sid=m[1]; d=sources[sid]
        return f'<a class="cite" href="{esc(d["url"])}" title="{esc(d["title"])}">{sid}</a>'
    text = re.sub(r'\[\[(P\d{2})\]\]', p, esc(text).replace('[[', '[[').replace(']]', ']]'))
    text = re.sub(r'\[\[(S\d+)\]\]', s, text)
    return text

# integrity checks
for L in PIPELINES:
    for k in L['repos']: assert k in GH, (L['id'], k)
    for k in L['docs']: assert k in DOCS, (L['id'], k)
    for k in L['papers']: assert k in papers, (L['id'], k)
    for k in L['uses'] + L.get('opt', []): assert k in INPUTS, (L['id'], k)
    assert not set(L['uses']) & set(L.get('opt', [])), L['id']
    for field in ('latency','evidence','limits'):
        for pid in re.findall(r'\[\[(P\d{2})\]\]', L[field]): assert pid in papers, (L['id'], pid)
        for sid in re.findall(r'\[\[(S\d+)\]\]', L[field]): assert sid in sources, (L['id'], sid)
assert len({L['id'] for L in PIPELINES}) == len(PIPELINES)
assert 'L5' not in {L['id'] for L in PIPELINES}, 'L5 was folded into the cross-cutting section'
assert (ROOT / TOPIC_DOC).is_file(), TOPIC_DOC
_pids = {L['id'] for L in PIPELINES}
for k, v in TOPIC_NEEDS: assert k in _pids, k
_texts = [v for _, v in TOPIC_NEEDS] + [c for row in SIM_CAPS for c in row[1:5]] + [b[2] for b in BENCHES] + [MACHINING['evidence']]
for t in _texts:
    for pid in re.findall(r'\[\[(P\d{2})\]\]', t): assert pid in papers, pid
    for sid in re.findall(r'\[\[(S\d+)\]\]', t): assert sid in sources, sid
for row in SIM_CAPS:
    for k in row[5]: assert k in DOCS, k
    for k in row[6]: assert k in GH, k
for b in BENCHES:
    for k in b[3]: assert k in GH, k
for k in MACHINING['repos']: assert k in GH, k
for k in MACHINING['papers']: assert k in papers, k

# ---------------------------------------------------------------- matrix
matrix_rows = ''
for L in PIPELINES:
    def cell(k):
        if k in L['uses']: return f'<td class="dot on" aria-label="{esc(INPUTS[k])}：需要">●</td>'
        if k in L.get('opt',[]): return f'<td class="dot opt" aria-label="{esc(INPUTS[k])}：可选">○</td>'
        return f'<td class="dot" aria-label="{esc(INPUTS[k])}：不用"></td>'
    cells = ''.join(cell(k) for k in INPUTS)
    matrix_rows += f'<tr><th scope="row"><a href="#{L["id"]}">{L["id"]}</a></th><td class="mname">{esc(L["name"])}</td><td class="mroute">{esc(L["route"])}</td>{cells}</tr>'
matrix = ('<div class="matrix-wrap"><table class="matrix"><thead><tr><th scope="col">链路</th><th scope="col">名称</th><th scope="col">所属路线</th>'
          + ''.join(f'<th scope="col" class="in">{esc(v)}</th>' for v in INPUTS.values())
          + '</tr></thead><tbody>' + matrix_rows + '</tbody></table></div>')

# ---------------------------------------------------------------- cards
cards = ''
for L in PIPELINES:
    stages = ''.join(f'<li><b>{esc(t)}</b><span>{esc(d)}</span></li>' for t, d in L['stages'])
    uses = ''.join(f'<span class="tag in-{k}">{esc(INPUTS[k])}</span>' for k in L['uses']) + ''.join(f'<span class="tag opt in-{k}" title="可选">{esc(INPUTS[k])}（可选）</span>' for k in L.get('opt',[]))
    repos = ''.join(f'<li>{gh_link(k)}</li>' for k in L['repos'])
    docs = ''.join(f'<li>{doc_link(k)}</li>' for k in L['docs'])
    pl = ''.join(f'<li>{paper_link(k)}</li>' for k in L['papers'])
    cards += f'''
<article class="line" id="{L['id']}">
  <header class="line-head">
    <span class="lid">{L['id']}</span>
    <div><h3>{esc(L['name'])}</h3><p class="route">所属路线：{esc(L['route'])}</p></div>
    <div class="uses">{uses}</div>
  </header>
  <ol class="stages">{stages}</ol>
  <dl class="facts">
    <div><dt>预测什么</dt><dd>{cite(L['predicts'])}</dd></div>
    <div><dt>时延与成本</dt><dd>{cite(L['latency'])}</dd></div>
    <div><dt>已有证据</dt><dd>{cite(L['evidence'])}</dd></div>
    <div><dt>局限</dt><dd>{cite(L['limits'])}</dd></div>
  </dl>
  <details class="refs" open>
    <summary>参考项目与文献</summary>
    <div class="refcols">
      <section><h4>GitHub 项目</h4><ul class="repolist">{repos}</ul></section>
      <section><h4>文献（本地 PDF／原文）</h4><ul class="paperlist">{pl}</ul>{('<h4>文档与项目页</h4><ul class="doclist">'+docs+'</ul>') if docs else ''}</section>
    </div>
  </details>
</article>'''

combos = ''.join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td></tr>' for a, b in COMBOS)
robots = ''.join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}<div class="mini">{"".join(gh_link(k) for k in ks)}</div></td></tr>' for a, b, ks in ROBOTS)
toc = ''.join(f'<a href="#{L["id"]}"><span>{L["id"]}</span>{esc(L["name"])}</a>' for L in PIPELINES)

# ---------------------------------------------------------------- cross-cutting section
from urllib.parse import quote
topic_href = quote(TOPIC_DOC)
def ref_links(docs, repos):
    items = ''.join(doc_link(k) for k in docs) + ''.join(gh_link(k) for k in repos)
    return f'<div class="mini">{items}</div>' if items else ''
needs_rows = ''.join(f'<tr><th scope="row"><a href="#{k}">{k}</a></th><td>{cite(v)}</td></tr>' for k, v in TOPIC_NEEDS)
caps_rows = ''.join(
    f'<tr><th scope="row">{esc(n)}{ref_links(d, r)}</th><td>{cite(a)}</td><td>{cite(b)}</td><td>{cite(c)}</td><td>{cite(e)}</td></tr>'
    for n, a, b, c, e, d, r in SIM_CAPS)
caps = ('<div class="caps-wrap"><table class="plain caps"><thead><tr><th scope="col">仿真器</th><th scope="col">绳、布、软体</th>'
        '<th scope="col">颗粒与弹塑性</th><th scope="col">液体</th><th scope="col">切割、断裂（拓扑变化）</th></tr></thead>'
        f'<tbody>{caps_rows}</tbody></table></div>')
bench_rows = ''.join(f'<tr><th scope="row">{esc(n)}{ref_links([], r)}</th><td>{esc(ph)}</td><td>{cite(note)}</td></tr>' for n, ph, note, r in BENCHES)
benches = ('<div class="caps-wrap"><table class="plain caps"><thead><tr><th scope="col">项目</th><th scope="col">覆盖的现象</th><th scope="col">说明</th></tr></thead>'
           f'<tbody>{bench_rows}</tbody></table></div>')
mach_stages = ''.join(f'<li><b>{esc(t)}</b><span>{esc(d)}</span></li>' for t, d in MACHINING['stages'])
mach_repos = ''.join(f'<li>{gh_link(k)}</li>' for k in MACHINING['repos'])
mach_papers = ''.join(f'<li>{paper_link(k)}</li>' for k in MACHINING['papers'])
cross = f'''
<section class="block" aria-labelledby="h-cross" id="cross">
<h2 id="h-cross">跨链路条件：形变、流体、断裂与加工</h2>
<p>这些不是单独的链路，而是任务中可能出现的物理情况。任务涉及它们时，走孪生路线（L1、L2，以及在其上运行的 L4、L6）需要能表示这些材料的仿真器；走学习路线（L7–L10）需要包含这些现象的数据，并检查模型是否学到了。原 L5「加工与形变过程模型」已并入本节，L5 编号空缺。详细说明见 <a href="{topic_href}">链路/专题_形变流体断裂与加工</a>。</p>
<h3 class="sub">任务涉及这些情况时，各链路要补什么</h3>
<table class="plain"><tbody>{needs_rows}</tbody></table>
<h3 class="sub">通用仿真器能力</h3>
<p class="subnote">2026-11-22 按官方文档或 README 核对。“未见”表示在这些文档里没有找到，不等于一定不支持；只列能力，不排序。</p>
{caps}
<h3 class="sub">专门的基准与研究代码</h3>
{benches}
<p class="subnote">自己写求解器时可用的 GPU 框架：{gh_link('warp')}；{gh_link('taichi')}。</p>
<h3 class="sub">加工（材料去除）</h3>
<p class="subnote">整厂层不直接预测切削，只需要加工时长、质量和报废概率，作为机床节点的属性。</p>
<ol class="stages">{mach_stages}</ol>
<p class="subnote">{cite(MACHINING['evidence'])}</p>
<div class="refcols">
  <section><h4>GitHub 项目</h4><ul class="repolist">{mach_repos}</ul></section>
  <section><h4>文献（本地 PDF／原文）</h4><ul class="paperlist">{mach_papers}</ul></section>
</div>
</section>'''

# ---------------------------------------------------------------- figure: inputs → pipelines (inline SVG)
# Columns: three primary inputs on the left, ten pipelines on the right, edges where a pipeline uses an input.
prim = [('step','STEP 文件'),('scan','实物扫描'),('urdf','机器人 URDF'),('plc','PLC／NC'),('video','视频＋动作'),('proc','工艺信号')]
W, rowh, top = 920, 34, 40
lx, rx = 30, 560
in_y = {k: top + 20 + i * 58 for i, (k, _) in enumerate(prim)}
out_y = {L['id']: top + i * rowh for i, L in enumerate(PIPELINES)}
H = top + len(PIPELINES) * rowh + 20
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="输入数据与各链路的对应关系">']
for L in PIPELINES:
    for k in L['uses'] + L.get('opt', []):
        y1 = in_y[k] + 12; y2 = out_y[L['id']] + 12
        dash = ' opt' if k in L.get('opt', []) else ''
        svg.append(f'<path class="edge e-{k}{dash}" d="M{lx+170} {y1} C {lx+330} {y1}, {rx-150} {y2}, {rx-6} {y2}"/>')
for k, label in prim:
    y = in_y[k]
    svg.append(f'<g class="node in-{k}"><rect x="{lx}" y="{y}" width="170" height="26" rx="4"/><text x="{lx+12}" y="{y+18}">{esc(label)}</text></g>')
for L in PIPELINES:
    y = out_y[L['id']]
    svg.append(f'<a href="#{L["id"]}"><g class="node out"><rect x="{rx}" y="{y}" width="{W-rx-10}" height="26" rx="4"/><text x="{rx+10}" y="{y+18}"><tspan class="lidt">{L["id"]}</tspan>  {esc(L["name"])}</text></g></a>')
svg.append('</svg>')
svg = '\n'.join(svg)

CSS = r'''
:root{
 --paper:#eef1f2;      /* drawing-sheet grey */
 --sheet:#ffffff;
 --ink:#1e2a30;        /* graphite */
 --muted:#5b6a72;
 --rule:#c9d2d6;
 --steel:#3b6e8f;      /* machinist blue, for links and STEP */
 --safety:#e3a21a;     /* safety yellow, used once per card for the ID */
 --scan:#2f8f72;       /* scan green */
 --robot:#8a4fbf;      /* robot violet */
 --plc:#b4543a;        /* PLC rust */
 --data:#6d7b85;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);font:15.5px/1.75 "Noto Sans CJK SC","Source Han Sans SC","PingFang SC","Microsoft YaHei",sans-serif}
a{color:var(--steel);text-underline-offset:2px}
a:focus-visible{outline:2px solid var(--safety);outline-offset:2px}
.wrap{max-width:1200px;margin:0 auto;padding:0 28px}
/* title block, like the corner block of an engineering drawing */
.titleblock{border-bottom:2px solid var(--ink);background:var(--sheet)}
.titleblock .wrap{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end;padding-top:36px;padding-bottom:22px}
h1{font:600 34px/1.3 "Noto Serif CJK SC","Source Han Serif SC",serif;margin:0;letter-spacing:.5px}
.lede{margin:10px 0 0;max-width:62ch;color:var(--muted)}
.stamp{border:1.5px solid var(--ink);font-size:12.5px;line-height:1.6;min-width:250px}
.stamp div{display:grid;grid-template-columns:72px 1fr;border-top:1px solid var(--rule)}
.stamp div:first-child{border-top:0}
.stamp span{padding:4px 8px}
.stamp span:first-child{border-right:1px solid var(--rule);color:var(--muted)}
main .wrap{padding-top:28px;padding-bottom:60px}
section.block{background:var(--sheet);border:1px solid var(--rule);margin:0 0 26px;padding:26px 30px}
h2{font:600 22px/1.4 "Noto Serif CJK SC","Source Han Serif SC",serif;margin:0 0 6px}
.block>p{max-width:72ch;margin:6px 0 14px;color:var(--muted)}
.notice{border-left:4px solid var(--safety);background:#fbf6ea;padding:12px 16px;margin:0 0 26px;max-width:none}
.notice b{color:var(--ink)}
/* figure */
.fig{overflow-x:auto}
.fig svg{width:100%;min-width:760px;height:auto;font-family:inherit;font-size:13px}
.fig .node rect{fill:var(--sheet);stroke:var(--ink);stroke-width:1}
.fig .node.out rect{fill:#f6f8f9;stroke:var(--rule)}
.fig a:hover .node.out rect,.fig a:focus .node.out rect{stroke:var(--steel);stroke-width:1.5}
.fig .node text{fill:var(--ink)}
.fig .lidt{font-weight:700;fill:var(--ink)}
.fig .edge{fill:none;stroke-width:1.4;opacity:.55}
.fig .e-step{stroke:var(--steel)}.fig .e-scan{stroke:var(--scan)}.fig .e-urdf{stroke:var(--robot)}
.fig .e-plc{stroke:var(--plc)}.fig .e-video{stroke:var(--data)}.fig .e-proc{stroke:#9a7b2f}
.fig .in-step rect{stroke:var(--steel);stroke-width:2}.fig .in-scan rect{stroke:var(--scan);stroke-width:2}
.fig .in-urdf rect{stroke:var(--robot);stroke-width:2}.fig .in-plc rect{stroke:var(--plc);stroke-width:2}
.fig .in-video rect{stroke:var(--data);stroke-width:2}.fig .in-proc rect{stroke:#9a7b2f;stroke-width:2}
/* matrix */
.matrix-wrap{overflow-x:auto;border:1px solid var(--rule)}
table{border-collapse:collapse;width:100%}
.matrix{min-width:860px;font-size:14px}
.matrix th,.matrix td{border-bottom:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:middle}
.matrix thead th{background:#f3f5f6;font-weight:600;font-size:13px;color:var(--muted)}
.matrix th.in{text-align:center;width:84px}
.matrix tbody th a{font-weight:700;color:var(--ink);text-decoration:none}
.matrix tbody th a:hover{text-decoration:underline}
.matrix td.dot{text-align:center;color:var(--rule)}
.matrix td.dot.on{color:var(--ink);font-size:15px}
.matrix td.dot.opt{color:var(--muted);font-size:15px}
.tag.opt{border-style:dashed;opacity:.85}
.fig .edge.opt{stroke-dasharray:4 4;opacity:.45}
.matrix .mroute{color:var(--muted);font-size:13px;white-space:nowrap}
/* jump list */
.jump{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 26px;margin-top:6px;font-size:14px}
.jump a{display:flex;gap:10px;text-decoration:none;color:var(--ink);padding:5px 0;border-bottom:1px dotted var(--rule)}
.jump a span{font-weight:700;min-width:34px}
.jump a:hover{color:var(--steel)}
/* pipeline cards */
.line{background:var(--sheet);border:1px solid var(--rule);border-top:3px solid var(--ink);margin:0 0 22px;padding:22px 28px 18px;scroll-margin-top:16px}
.line:target{border-top-color:var(--safety)}
.line-head{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start}
.lid{font:700 20px/1 "Noto Sans CJK SC",sans-serif;background:var(--safety);color:var(--ink);padding:9px 10px;min-width:50px;text-align:center}
.line h3{margin:0;font:600 19px/1.45 "Noto Serif CJK SC","Source Han Serif SC",serif}
.route{margin:2px 0 0;color:var(--muted);font-size:13.5px}
.uses{display:flex;flex-wrap:wrap;gap:6px;justify-content:flex-end;max-width:330px}
.tag{font-size:12.5px;padding:2px 8px;border:1.5px solid;line-height:1.6;white-space:nowrap}
.tag.in-step{border-color:var(--steel);color:var(--steel)}
.tag.in-scan{border-color:var(--scan);color:var(--scan)}
.tag.in-urdf{border-color:var(--robot);color:var(--robot)}
.tag.in-plc{border-color:var(--plc);color:var(--plc)}
.tag.in-video{border-color:var(--data);color:var(--data)}
.tag.in-proc{border-color:#9a7b2f;color:#9a7b2f}
/* stages: a process strip with arrows, because these steps are a real sequence */
.stages{list-style:none;counter-reset:st;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0;margin:18px 0 16px;padding:0;border:1px solid var(--rule)}
.stages li{counter-increment:st;position:relative;padding:12px 14px 12px 14px;border-left:1px solid var(--rule);font-size:13.5px;line-height:1.65}
.stages li:first-child{border-left:0}
.stages li::before{content:counter(st);display:inline-block;font-weight:700;color:var(--muted);margin-right:6px}
.stages li:not(:last-child)::after{content:"";position:absolute;right:-7px;top:16px;width:12px;height:12px;background:var(--sheet);border-top:1px solid var(--rule);border-right:1px solid var(--rule);transform:rotate(45deg);z-index:1}
.stages b{font-weight:600}
.stages span{display:block;color:var(--muted);margin-top:4px}
.facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 30px;margin:0 0 12px}
.facts div{border-top:1px solid var(--rule);padding-top:8px}
.facts dt{font-size:13px;font-weight:600;color:var(--muted)}
.facts dd{margin:3px 0 0;font-size:14.5px}
.cite{font-size:12px;font-weight:600;text-decoration:none;border:1px solid var(--rule);padding:0 4px;margin:0 1px;white-space:nowrap;color:var(--steel)}
.cite:hover{border-color:var(--steel)}
details.refs{border-top:1px solid var(--rule);padding-top:8px}
details.refs summary{cursor:pointer;font-weight:600;font-size:14px;padding:4px 0}
.refcols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:8px 36px;margin-top:6px}
.refcols h4{margin:10px 0 4px;font-size:13px;color:var(--muted);font-weight:600}
.refcols ul{list-style:none;margin:0;padding:0;font-size:13.5px}
.refcols li{padding:3px 0;border-bottom:1px dotted #e1e6e8;overflow-wrap:anywhere}
.repo{font-weight:600}
.note{color:var(--muted);margin-left:8px}
.paper{font-weight:700;margin-right:8px}
.ptitle{color:var(--ink)}
.src{margin-left:8px;font-size:12.5px}
.mini{margin-top:6px;font-size:13px;display:flex;flex-wrap:wrap;gap:4px 16px}
.mini .note{display:none}
/* plain tables */
.plain{font-size:14.5px}
.plain th,.plain td{border-bottom:1px solid var(--rule);padding:10px 12px;text-align:left;vertical-align:top}
.plain th[scope=row]{white-space:nowrap;font-weight:600;width:150px}
/* cross-cutting section */
.sub{font-size:16px;font-weight:600;margin:22px 0 6px}
.subnote{font-size:13.5px;color:var(--muted);margin:4px 0 10px}
.caps-wrap{overflow-x:auto}
.caps{min-width:860px}
.caps th,.caps td{font-size:13.5px}
.caps thead th{background:#f3f5f6;font-weight:600;font-size:13px;color:var(--muted)}
.caps th[scope=row]{white-space:normal;width:200px}
footer{color:var(--muted);font-size:13px;padding:10px 0 40px}
@media (max-width:900px){
 .titleblock .wrap{grid-template-columns:1fr}
 .stages{grid-template-columns:1fr}
 .stages li{border-left:0;border-top:1px solid var(--rule)}
 .stages li:first-child{border-top:0}
 .stages li:not(:last-child)::after{right:auto;left:18px;top:auto;bottom:-7px;transform:rotate(135deg)}
 .facts,.refcols,.jump{grid-template-columns:1fr}
 .line-head{grid-template-columns:auto 1fr}
 .uses{grid-column:1/-1;justify-content:flex-start;max-width:none}
 section.block,.line{padding:18px 16px}
 .wrap{padding:0 14px}
 h1{font-size:26px}
}
@media print{body{background:#fff}.line,section.block{break-inside:avoid-page}details.refs{display:block}}
'''

page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>链路看板：STEP、实物扫描与机器人 URDF 的工业世界模型链路</title>
<style>{CSS}</style></head><body>
<header class="titleblock"><div class="wrap">
 <div><h1>链路看板：从 STEP、扫描和 URDF 出发</h1>
 <p class="lede">假设手头有：机床等生产设备的 STEP 文件，这些设备实物的三维扫描，以及一台带 URDF 的机器人（人形、小车或机械臂）。下面列出能用这些输入搭起来的世界模型链路，每条附实现步骤、时延、证据、局限和参考项目。</p></div>
 <div class="stamp" aria-label="文档信息">
  <div><span>版本</span><span>2026-11-22</span></div>
  <div><span>链路数</span><span>{len(PIPELINES)}</span></div>
  <div><span>参考论文</span><span>本地 papers/ 目录，点编号打开 PDF</span></div>
  <div><span>配套报告</span><span><a href="report.html">report.html</a></span></div>
 </div>
</div></header>
<main><div class="wrap">
<p class="notice"><b>本看板只列举链路，不做推荐。</b>链路之间不互斥，常常组合使用；排列顺序按输入从“只用 STEP”到“需要更多现场数据”，不代表优先级。时延数字来自各论文在各自硬件上的报告，不能直接横向比较。形变、流体、断裂与加工不作为单独链路，而是任务条件，见<a href="#cross">跨链路条件</a>一节。</p>

<section class="block" aria-labelledby="h-map">
<h2 id="h-map">输入与链路的对应</h2>
<p>左边是输入，右边是链路。实线表示该链路需要这项输入，虚线表示可选。STEP、扫描和 URDF 是已有的；PLC／NC、视频和工艺信号是部分链路额外需要的。点右边的链路名跳到详情。</p>
<div class="fig">{svg}</div>
</section>

<section class="block" aria-labelledby="h-matrix">
<h2 id="h-matrix">需要哪些输入</h2>
<p>● 表示需要，○ 表示可选。“所属路线”对应 <a href="report.html#wmroutes">报告第 03 节</a> 的六条世界模型路线。</p>
{matrix}
</section>


{cards}

{cross}

<section class="block" aria-labelledby="h-combo">
<h2 id="h-combo">常见组合</h2>
<p>链路之间通过共享资产、坐标系、实体 ID 和事件时钟组合。下表列出接口上能直接衔接的组合，不是推荐。</p>
<table class="plain"><tbody>{combos}</tbody></table>
</section>

<section class="block" aria-labelledby="h-robot">
<h2 id="h-robot">机器人形态带来的差别</h2>
<p>URDF 在各链路中的用法相同：给出关节、连杆、碰撞体和运动学。不同形态的差别主要在控制与数据。</p>
<table class="plain"><tbody>{robots}</tbody></table>
</section>

<footer>
<p>GitHub 项目于 2026-11-14 用 GitHub API 核对存在；文档与项目页于同日核对可访问。2026-11-22 把原 L5 改为“跨链路条件”一节，并在 L8 补充 INTACT 与 SADL；新增的项目、文档与 arXiv 链接于同日核对。论文编号与报告一致，PDF 位于相邻的 <code>papers/</code> 目录，请保持本文件与 <code>papers/</code> 的相对位置。由 <code>scripts/build_pipeline_board.py</code> 生成。</p>
</footer>
</div></main>
</body></html>'''

out = ROOT / 'pipeline_board.html'
out.write_text(page)
print(f'Built {out.name}: {len(page):,} characters, {len(PIPELINES)} pipelines, '
      f'{sum(len(L["repos"]) for L in PIPELINES)} repo links, {len(GH)} distinct repos')
