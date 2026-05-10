# InjectionMolding-AI-Skill (注塑成型全栈 AI 专家系统)

🚀 **一个基于材料物理引擎与 LLM 逻辑链的注塑工艺闭环优化模型。**

## 📖 项目简介
[cite_start]本项目旨在将资深注塑工程师的经验转化为可计算的数字化 Skill。系统采用“数据层 → 推理层 → 模拟层 → 反馈层”四层架构 [cite: 3, 4]：
- [cite_start]**数据层**：基于 CAMPUS/ISO 标准的 7 种核心材料物性库 [cite: 25-37]。
- [cite_start]**推理层**：结合流长比（L/t）与壁厚修正算法的工艺推理引擎 [cite: 46-51]。
- [cite_start]**模拟层**：内置基于非牛顿流体变稀效应与傅里叶导热定律的物理仿真器 [cite: 68-84]。
- [cite_start]**反馈层**：针对 9 种常见注塑缺陷的专家级诊断矩阵 [cite: 97-120]。

## 📂 文件结构
- `manifest.json`: 系统配置文件，定义 Skill 的身份与调用接口。
- [cite_start]`material_db.json`: 结构化物性数据库，包含热学、流变学及加工限制数据 [cite: 20]。
- `instructions.md`: 核心逻辑内核，封装了注塑工艺 SOP 与安全红线。
- [cite_start]`physics_engine.py`: 物理引擎核心，执行压降估算与冷却时间计算 [cite: 65, 68]。

## 🛠️ 核心功能展示

### 1. 智能工艺推荐
输入塑料牌号与制品几何信息，系统自动计算：
- [cite_start]**温度分布**：料筒四段分区温度及喷嘴温度建议 [cite: 52, 53]。
- [cite_start]**压力方案**：注射压力基准及基于流长比的动态修正 [cite: 53-56]。
- [cite_start]**时间预估**：基于物理公式的精确冷却与保压时间 [cite: 58-61]。

### 2. 物理仿真模拟 (Internal Simulation)
在正式试模前，系统会预测：
- [cite_start]**填充压降**：预估所需压力并对比机台极限 [cite: 76, 77]。
- [cite_start]**质量预警**：自动判定短射、缩水及材料降解风险 [cite: 84-93]。

### 3. 闭环缺陷调整
[cite_start]当制品出现缩水、飞边或气泡时，系统根据“单变量微调”原则提供 Primary/Secondary 优化策略 [cite: 96, 97]。

## 🚀 快速开始
1. 下载本项目所有文件。
2. 将 `instructions.md` 与 `material_db.json` 挂载至您的 AI Agent 平台。
3. 按照 `manifest.json` 定义的格式开始输入您的注塑需求。

## ⚖️ 免责声明
[cite_start]本系统生成的工艺参数和模拟结果仅供技术选型和试模参考，实际生产需结合设备与环境条件进行最终确认 。