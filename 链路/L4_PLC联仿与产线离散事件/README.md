# L4 PLC／NC 接入仿真，再接产线离散事件

在 FWAM 中的位置：整厂层的显式转移函数（L11 形态 A）。它预测设备模式、互锁、完工事件和生产流，是整厂层训练数据的主要来源。

## 思考

- 整厂层最关键的状态（设备模式、互锁、程序段、工单）只有显式模型能直接表达和审计。L4 正是提供这些状态的链路。
- 产线离散事件仿真运行很快，适合大量生成"整厂状态—整厂动作—结果"数据，喂给 L11 的学习式模型。
- 细节仿真（L1 物理）和产线仿真（L4 事件）的交接点要定义清楚：同一工序只能有一处负责发布完工。
- 加工、涂胶这类工艺在产线层只表现为工序时长、质量和报废概率，由[专题](../专题_形变流体断裂与加工/README.md)第 4 节的加工代理或实测统计提供。

## Idea

1. **事件语义对齐**：整厂层的事件（技能开始、完成、设备完工）用同一套定义，同时用于离散事件仿真、学习式模型和真实日志。这样三者的数据可以直接混合训练。
2. **反事实生成器**：离散事件仿真从同一快照出发，对派工、路由、插单做大量扰动，生成"同初态、不同动作"的数据（L11 Idea 4）。
3. **可变细度**：被关注的工位用 L1 物理细节仿真，其余工位用校准过的周期模型，按需要切换。

## 实施路线

1. 设备 I/O 映射：把 L1 资产中的门、夹具、按钮、轴与 PLC／NC 变量一一对应。
2. 接入控制器：
   - 软件在环：虚拟 PLC（如 OpenPLC，或商用的 S7-PLCSIM Advanced）运行真实程序或行为模型。
   - CNC：LinuxCNC 的仿真配置可以作为开源的 NC 行为参考。
   - 没有程序时，先写状态机行为模型。
3. 统一时钟：物理步长、PLC 扫描周期、NC 插补周期在同一主循环或 FMI 联仿中对齐，并记录请求、确认、到位三类事件。
4. 产线层：工单、工艺路线、缓存、搬运、故障进入离散事件队列（SimPy 或自写事件循环）。
5. 反事实：换单、换路由、机床停机、机器人阻塞、返工，进行多场景推演。

算力：主要是 CPU；离散事件仿真可以在多核上并行跑大量随机种子。

## 推荐文献

- LLM 智能体半自动生成虚拟调试模型 [P66]
- 联仿综述 [P98]；NIST CMSD 制造仿真数据模型 [P99]
- AWMP [P38]：已知车间转移与外生到达分离的排产世界模型
- [Siemens 虚拟调试指南（PLCSIM Advanced＋SIMIT＋NX MCD）](https://cache.industry.siemens.com/dl/files/864/109963864/att_1277519/v1/Guideline_VC_SIMIT_PSA_MCD_V1.0.0.pdf)
- [OPC UA for Machine Tools](https://reference.opcfoundation.org/specs/OPC-40501-1/6)；[MTConnect](https://www.mtconnect.org/)；[FMI 3.0.2](https://fmi-standard.org/docs/3.0.2/)
- [LinuxCNC 仿真配置说明](http://linuxcnc.org/docs/html/getting-started/running-linuxcnc.html)；[SimPy 文档](https://simpy.readthedocs.io/en/latest/)

## 参考项目

[Autonomy-Logic/openplc-runtime](https://github.com/Autonomy-Logic/openplc-runtime)、[LinuxCNC/linuxcnc](https://github.com/LinuxCNC/linuxcnc)、[FreeOpcUa/opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio)、[open62541/open62541](https://github.com/open62541/open62541)、[mtconnect/cppagent](https://github.com/mtconnect/cppagent)、[CATIA-Systems/FMPy](https://github.com/CATIA-Systems/FMPy)、[INTO-CPS-Association/maestro](https://github.com/INTO-CPS-Association/maestro)、[OpenModelica/OpenModelica](https://github.com/OpenModelica/OpenModelica)
