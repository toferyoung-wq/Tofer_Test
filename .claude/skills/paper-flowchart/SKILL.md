---
name: paper-flowchart
description: 用论文插图风格（PaperBanana / NeurIPS 2025 风格指南）把用户写好的流程画成可编辑的 draw.io 流程图。用户给出流程（步骤、分支、分组），要"论文风格""学术风格""paper style"的流程图、方法框架图、计算语言学/NLP 流水线图时使用。
---

# 论文风格流程图（draw.io）

**分工：流程由用户写，风格由本 skill 定，XML 写法由 `drawio` skill 定。**

1. 先读 `.claude/skills/drawio/SKILL.md`，按它的规则写 draw.io XML（结构、网格、禁止 XML 注释、转义）。
2. 用户的流程是唯一的内容来源：**不增删步骤、不改名、不擅自补分支**。流程有歧义时先问，再画。
3. 所有视觉决定按下面的"风格规范"执行，不再另行发挥。
4. 输出：`figures/<描述性名称>.drawio`，并按 drawio skill 的 "Browser URL output" 生成 app.diagrams.net 链接。没有 draw.io 桌面 CLI 时直接写 XML（不用 Mermaid）。

风格规范提炼自 PaperBanana 的 `references/neurips2025_diagram_style_guide.md`（Apache-2.0，见同目录 LICENSE）。需要更细的依据时读原文。

## 风格规范

总基调："Soft Tech & Scientific Pastels"：浅色底分区，饱和色只留给关键元素，整体从左到右或从上到下有清晰叙事流。

### 1. 分区 / 阶段容器（泳道或分组）

浅色马卡龙底 + 同色系细边框，按顺序轮换使用，不用饱和底色：

| 用途 | fillColor | strokeColor |
|---|---|---|
| 阶段 1 | `#E6F3FF`（冰蓝） | `#9DC3E6` |
| 阶段 2 | `#E0F2F1`（薄荷） | `#80CBC4` |
| 阶段 3 | `#F3E5F5`（淡紫） | `#CE93D8` |
| 阶段 4 | `#FFF8E1`（奶油） | `#FFD54F` |

容器样式：`rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=…;strokeColor=…;dashed=1;verticalAlign=top;align=left;spacingLeft=10;spacingTop=6;fontStyle=1;fontSize=13;fontColor=#37474F;container=1;`
（逻辑阶段用虚线边框；表示真实组件的容器用实线，去掉 `dashed=1`。）

### 2. 节点形状

| 语义 | 形状 | 样式要点 |
|---|---|---|
| 处理步骤 / 模块（默认） | 圆角矩形 | `rounded=1;arcSize=12;` |
| 判断 | 菱形 | `rhombus;` |
| 语料、文档、文本输入 | 文档形 | `shape=document;boundedLbl=1;size=0.15;` |
| 数据库、词典、知识库、缓存 | 圆柱 | `shape=cylinder3;boundedLbl=1;size=8;` |
| 张量、嵌入、矩阵 | 立体块（有维度含义时）或直角方块 | 立体：`shape=cube;size=8;`；平面：`rounded=0;` |
| 起止 | 胶囊 | `rounded=1;arcSize=50;` |
| 人工环节（标注员、专家） | 人形 | `shape=umlActor;` |

所有节点：`whiteSpace=wrap;html=1;fontFamily=Helvetica;fontSize=12;fontColor=#263238;strokeWidth=1.2;`

### 3. 节点颜色（按状态，不按类型）

| 状态 | fillColor | strokeColor |
|---|---|---|
| 可训练 / 本文提出 / 活跃模块（暖色） | `#FFE0CC` | `#F08A4B` |
| 冻结 / 预训练不更新 / 静态资源（冷色） | `#E3EEF7` | `#7FA7C9` |
| 普通处理步骤（中性） | `#FFFFFF` | `#90A4AE` |
| 数据 / 语料 | `#F5F5F5` | `#9E9E9E` |
| 最终输出、损失、金标准（唯一高饱和） | `#FDE2E2` | `#D9534F`，`fontStyle=1` |

一张图里高饱和强调色最多 1–2 处。不要用 PowerPoint 默认蓝橙 + 粗黑边框。

### 4. 连线

| 语义 | 样式 |
|---|---|
| 主数据流（前向） | `edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#546E7A;strokeWidth=1.4;endArrow=blockThin;endFill=1;html=1;` |
| 辅助流：梯度、损失、跳连、可选路径、外部资源引用 | 同上加 `dashed=1;strokeColor=#90A4AE;` |
| 反馈回路、高层系统逻辑 | `curved=1;` 代替 orthogonal，`dashed=1` |
| 错误 / 失败分支 | `strokeColor=#D9534F;dashed=1;` |

数据流和梯度流（或辅助流）绝不能用同一种线型。运算符（⊕ 加、⊗ 拼接/乘）可直接作为小圆节点放在线的交汇处。

### 5. 文字

- 模块名用无衬线（Helvetica）；阶段标题加粗，细节常规。
- 数学变量必须是衬线斜体：`<i style="font-family:Times New Roman">x</i>`、`<i style="font-family:Times New Roman">θ</i>`、`ℒ`。节点 `value` 里写 HTML 时要转义成 `&lt;i …&gt;`。
- 标签语言跟随用户。中英对照写成两行：`分词<br><span style="font-size:10px;color:#607D8B">Tokenization</span>`。
- 次要信息（工具名、超参数）放进节点第二行小字，不单独拉线。

### 6. 图标（可选，克制使用）

在节点标签前加 emoji 表示状态或内容：🔥 可训练、❄️ 冻结、📄 文本/语料、💬 提示词、🔍 检索/分析、⚙️ 计算。每个节点最多一个，全图风格统一（要么都用，要么都不用）。

### 7. 计算语言学 / NLP 领域约定

- LLM / Agent 类流程：可用对话气泡、文档图标，叙事感更强。
- 理论 / 形式语言类（自动机、文法推导）：极简教科书风格，圆形节点，黑白灰为主，不用马卡龙底色。
- 外部语言资源（词典、WordNet、知网、树库）放在主流程外侧，用虚线连入。
- 标注流程中的人工环节用人形或单独泳道，与模型流程区分。

### 8. 版式

- 默认从左到右；步骤超过 6 个或含多层嵌套时用从上到下。
- 每张图不超过约 20 个节点，超出时拆成多页（drawio 支持多页）。
- 先确保结构正确，再交给 ELK / libavoid（有 CLI 时）或按 drawio skill 的网格摆放。

## 自检清单（写完 XML 后过一遍）

- [ ] 用户流程中的每个步骤、分支、分组都在，且没有多出来的。
- [ ] 分区底色是浅色马卡龙，没有饱和底色。
- [ ] 高饱和色只出现在最终输出 / 损失 / 金标准上。
- [ ] 主数据流实线，辅助流虚线，二者不混用。
- [ ] 数学变量是衬线斜体，模块名是无衬线。
- [ ] XML 无注释、特殊字符已转义、id 唯一。
