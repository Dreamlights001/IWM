# IWM Zotero 导入记录

已完成并通过读回校验：50 篇论文、7 项官方技术文档位于 IWM 的 12 个子分类；50 份归档 PDF 的 SHA-256 均匹配。

- 目标：我的文库 / IWM（CBS6V74B）。
- 50 篇论文、7 项官方技术文档已导入；50 份 PDF 已核验 SHA-256。
- 12 个子分类已创建。连接器会话会覆盖 RDF 导入后的分类归属，因此需要一次额外的归属写入。
- 3 篇 JEPA 在原文库已存在：已复用原条目并保留既有集合／字段，本次 PDF 与注释已关联过去；仅将本次新建的 3 个重复父条目移入回收站。
- Zotero 10 的本地 API 写入需要 `/api/local/authorize` 原生弹窗授权。选择“允许”时，每个键只用于一次请求；66 次对象更新按最多 50 对象拆成两个批次。授权密钥不输出、不写入项目文件。

## 分类清单

- 01 潜变量与模型式控制（ASMHMCPK）
- 02 JEPA与特征预测（LXUHF7TE）
- 03 可交互资产与仿真环境（KVBKW525）
- 04 工业过程、生产与多机协同（XR8WT5A3）
- 05 高斯表示与动态重建（IJJ2B3JK）
- 06 高斯与物理数字孪生（VGIJN6UI）
- 07 生成式视频与交互模型（M6CWN3GY）
- 08 三维动力学与场景图（LCAJR5RR）
- 09 几何重建（LYTEIXN3）
- 10 世界模型与物理评测（L3EYJMKM）
- 11 形变、切削与材料去除（NRMHUQ62）
- 12 标准与官方技术文档（S6TTKP38）

完整变更计划：`zotero_classification_plan.json`；导入响应：`zotero_import_receipt.json`；核验记录见 `zotero_finalization_receipt.json` 与 `zotero_verified_inventory.json`。
