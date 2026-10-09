# Overview figure — drawing prompt (v2)

> 用 `paper-flowchart` skill 执行。内容以《读、用、写：实验重新编号与数据总表》（2026-10-09）为准，不以旧版 main.tex 为准。

## 1. 目的与版式

- ACL 论文 Figure 1（取代原 g·f 概念图），只展示研究设计主线，**不放数值、结论或对照细节**。
- 通栏 `figure*`，横向，约 16 cm × 5.5 cm，宽高比约 3:1。单页。
- 全部标签英文；按缩放到 16 cm 宽后字号 ≥ 7 pt 设计。数学符号用衬线斜体。
- 风格参考：用具体对象（例句、层叠块、激活空间散点、概率条）讲机制，文字只做标签。分区标签为浅灰底、斜体无衬线（如 *Direction Construction*）。

## 2. 核心叙事约束

- **Read / Use / Write 三栏并列，彼此之间不画箭头**（不是已成立的因果链）。
- 唯一跨栏连线：FPpred → Write 栏的门控菱形，**虚线**，标注 `external gate`。
- 全图主线是两个关键比对：**Rate（how many, g）** 与 **Placement（where, f）**。

## 3. 布局

```
┌ Direction Construction ┐ ┌ Activation space ┐ ┌──── Read ────┬──── Use ────┬──── Write ────┐
│ ① 例句对 → LM 层叠块    │ │ ② 散点 + 方向箭头 │ │ ③ 残差流挂钩：  project · ⊖ ablate · ⊕ add   │
│   → h差 → 方向立体块    │ │                   │ │   条目列表（短名 + 色点）                     │
└────────────────────────┘ └───────────────────┘ └──────────────────────────────────────────────┘
                                ┌──────────── Rate vs. Placement（横跨 Use + Write 下方）────────────┐
                                │ ④ 词串 + 概率条：左 gain（全部升高） │ 右 timing（仅 FP 位置升高） │
                                └────────────────────────────────────────────────────────────────────┘
```

### ① Direction Construction（左列）

- 两行自拟示意句（Cookie Theft 场景，**不使用语料原句**）：
  - disfluent：`the boy is uh taking a cookie`（`uh` 用橙色底标出）
  - fluent：`the boy is taking a cookie`
- 两句各入一个窄的竖向 Transformer 层叠块（约 6 层示意，标 `block 21/28` 的那层高亮），右侧标三个模型名小字：`Llama-3.2-3B · Qwen2.5-1.5B · Qwen2.5-7B`。
- 取出末位置激活 `h_disfl`、`h_fluent`，经 `−` 运算小圆节点得到方向。
- 方向集合：4 个小立体块竖排，旁注一行构造方式：

| 方向 | 颜色 | 旁注 |
|---|---|---|
| FP | 暖色 | disfluent − fluent |
| FPpred | 冷色 | pre-FP − pre-ordinary positions |

- 例句对只画 FP 的构造；FPpred 只用旁注说明，不另画句子。

### ② Activation space（中列，参考图的"嵌入空间"）

- 浅色圆形区域内散点：★ = upcoming-FP positions（橙色描边），○ = ordinary positions（灰）。
- 两支实线箭头从同一原点出发，**彼此正交**：`v_FP`（暖色）、`v_FPpred`（冷色）。
- 沿 `v_FPpred` 画一条细虚线投影轴，★ 大多落在轴的一端、○ 在另一端，示意"projection separates positions"。
- 一支灰色虚线短箭头，标 `matched random controls`——全图唯一的对照标记。
- 角落标 `schematic`（小号灰字）。

### ③ Read / Use / Write（右侧三栏，冰蓝 / 薄荷 / 淡紫底）

三栏顶部共用一条横向残差流箭头 `residual stream h`，在每栏上方各有一个挂钩点：

| 栏 | 挂钩符号 | 公式（衬线斜体） |
|---|---|---|
| Read | 投影小圆 `·` | *h·v* |
| Use | ⊖ | *h − (h·v − μ)v* |
| Write | ⊕ | *h + ασ_F v* |

Write 栏挂钩前放门控菱形 `FPpred high?`，接收来自 ② 的 `external gate` 虚线；菱形"yes"分支连到 ⊕。

各栏条目（2–4 词短名 + 色点；`TF` / `Gen` 灰色小标签表示 teacher forcing / 自由生成）：

| Read | Use | Write |
|---|---|---|
| Position readout ●P | Ablate FP ●R | Add FP `TF` `Gen` ●R●P |
| Beyond covariates ●P | Ablate FPpred ●R●P | Add FPpred `TF` ●R●P |
| Surprisal link ●P | | Oracle timing `Gen` ●R●P |
| | | Gated by FPpred `TF` `Gen` ●R●P |

### ④ Rate vs. Placement（底部条，横跨 Use + Write）

- 居中一行：*P*(filler at *t*) = ***g*** · ***f***(context*_t*)，g 用 Rate 色、f 用 Placement 色。
- 左右两半各画同一个词串 `the boy is ▢ taking a cookie`，▢ 为橙色底的 FP 位置；每个位置下方一根细概率条（灰为 baseline，彩色为干预后增量）：
  - 左 **Rate (g)**：所有条同比升高（琥珀色增量）；下方小字 `net Δlog P(filler), all positions · valid FPs per output`
  - 右 **Placement (f)**：只有 ▢ 的条升高（青绿色增量）；下方小字 `FP vs. matched ordinary sites · O/E of generated FPs`

## 4. 配色

- 栏底色：Read `#E6F3FF`、Use `#E0F2F1`、Write `#F3E5F5`；其余区域白底，分区标签浅灰 `#EEEEEE`。
- FP 位置 / `uh` 高亮：浅橙 `#FAD7B5`。
- **Rate = 琥珀 `#E69F00`，Placement = 青绿 `#009E73`**（Okabe–Ito）：仅用于色点、g/f、④ 的增量条与两格边框。
- 不使用高饱和红色。

## 5. 不画的内容（放图注或正文）

- 数值、CI、p 值、结论标记；E1–E12 编号。
- 对照数量（3 / 20 条）、剂量网格（±2/4/8 σ_F、s_pos）、门控预算（2.5% / 10%）、own / always 条件。
- 解码设置、prompt 基线、层比较、大激活修正。
- REP / REPpred 与全部补充项（S0、S-REP、S-ROB、W-S1）。

## 6. 已定事项

1. 本图取代现有 Figure 1。
2. 不显示 E 编号。
3. Rate / Placement = 琥珀 / 青绿。
4. 实验列表只保留主线短名；对照仅保留"FP vs. matched ordinary sites"（④）和一个统一的随机控制标记（②）。
5. ② 中 v_FP 与 v_FPpred 画成正交，标 `schematic`。
6. 例句自拟。
7. 图中只保留 FP 与 FPpred 两个方向；PSEUDO / FP⊥ 及其特异性检验移到图注和正文。

## 7. v3 布局修订（2026-10-09）

- 改为上下两行：(a) Direction construction 在上，(b) Interventions on the residual stream 在下，中间一支粗箭头 `apply v at block 21` 表明两部分关系。
- 删除 Rate vs. Placement 概念演示（词串 + 概率条与 g·f 公式）；Rate / Placement 只以色点和右上角图例 `Scored for` 体现。
- FPpred 也画出构造方式（`the boy [is] uh …`，pre-FP vs. pre-ordinary positions），与 FP 共用同一 LM 层叠块。
- 门控虚线从 v_FPpred 出发，沿 (a) 行下方走到 Write 栏的门控分数条。
- 当前布局以 `figures/gen_overview.py` 为准。

## 8. v4 修订

- 删除残差空间示意与 Data/Models 信息框；(a) 压缩为一行窄带，重点放在 (b) 三个阶段。
- 每个阶段加机制小图：Read = 各位置 h·v 分数条（pre-FP 位置突出）；Use = 下一词分布，消融前虚框 / 后实心（"does P(uh) drop?"）；Write = 两个子面板，Ungated 每个位置都 ⊕，Externally timed 只在超过 top k% 阈值的位置 ⊕。
- 阶段框加深色表头条；右上角图例同时解释 rate/placement 色点与 TF/Gen 标签。

## 9. v5 修订

- 删除右上角图例框和 (a)/(b) 分区标签；rate/placement 色点与 TF/Gen 标签的含义改由图注说明。

## 10. v6 修订

- 三个模型：LM 画成三层错位叠放的层叠块，下方一行写明 Llama-3.2-3B · Qwen2.5-1.5B · Qwen2.5-7B (block 21)。
- Write 栏底部新增 Free generation 条：prompt → 注入 ⊕ 的 LM → 含 uh/um 的生成描述。

## 11. v7 修订

- 自由生成示例改为灰色 `[FP]` 占位。
- 整体压缩：上方例句区收紧，(b) 上移，宽高比约 2.5:1。

## 12. v8 修订

- Read 小图改为两排：h·v 峰值在 FP 前一位置（is），surprisal 峰值在 FP 后一词（taking），中间 uh 用浅橙色列标出。

## 13. v9：方向 × 阶段网格

- 改为左右排版：左侧三行例句 → 三个 LM → FP / FPpred 立体块；右侧网格，行 = FP、FPpred、LM 自身 P(filler)，列 = Read / Use / Write。
- 每个方向的箭头直接进入其所在行，各格内为使用该方向的实验；空格表示该方向未参与该阶段。
- Read/FP 格保留 “Position readout (comparison)”（灰色）。Surprisal link 单列一行（LM 自身 P(filler)，不使用方向）。
- Gated FP injection 放在 FP 行（注入的是 FP），FPpred 行引竖直虚线 “score as gate” 指向它。
- 各列表头下保留机制小图；Write 列下方加 Gen 条（prompt → ⊕ LM → “the boy [FP] is …”）。
- 去掉残差流横线；操作符号（· ⊖ ⊕）放进列表头。

## 14. v10：左构建 + 右侧上下三阶段

- 左：三行例句 → 三层错位 LM（不写模型名）→ FP / FPpred。
- 两个方向各一条彩色总线，向 Read / Use / Write 三个面板各引一支箭头；不再按方向分格。
- 每个面板：左侧竖排阶段名 + 操作公式 + 分析条目（条目前用 FP / FPpred / LM 彩色小标签表明用了哪个表征）；右侧一张分布示意图：
  - Read：h·v_FPpred 与 surprisal 两排位置分布（is / taking 峰值，uh 列高亮）。
  - Use：下一词概率分布，消融前虚框 / 后实心（filler 降低）。
  - Write：every position vs. selected positions（top k%），下方 Gen 条。

## 15. v11

- 左侧放大（例句 14 px、更高的三层网络、更大的方向块）。
- 去掉条目前的 FP / FPpred / LM 标签；两个方向都汇入一条竖直残差流，Read / Use / Write 通过流上的 · ⊖ ⊕ 挂钩接入。
- Use 图标题改为问句 "does P(filler) drop?"。

## 16. v12

- 回到上下结构：方向构建在上，Read / Use / Write 三个面板在下并排。
- FP 与 FPpred 两条线在汇合点合并，单支箭头落到残差流上，旁注 "both directions: v ∈ {FP, FPpred}, applied to the residual stream at block 21"。
- 残差流改为无方向的横条，避免落点位置暗示某个阶段先用或不用。
- 每个面板：上方分布示意图，下方分析条目；Write 内含 every / selected positions 两个小图与 Gen 条。

## 17. v13

- 构建部分水平镜像：例句在右 → 三层网络 → − → FP / FPpred 方向块在最左。
- 每个方向一条线（v_FP 橙、v_FPpred 蓝），从左往右横贯三个阶段上方；不画成两条残差流（模型只有一条残差流），右上注明 "two directions, both applied to the residual stream h at block 21"。
- 每个阶段从两条线各引一个接头；Read 的 FP 接头为虚线（仅作对照）。操作符号 · ⊖ ⊕ 移入面板表头。

## 18. v14

- 去掉各面板的实验条目，每个阶段只保留一张分布示意图（Write 含 every / selected positions 与 Gen 条）。
- FP 与 FPpred 在左侧汇合成一条线（v ∈ {FP, FPpred}），从左往右，每个阶段一个接头。
- 宽高比约 2.8:1。

## 19. v15

- Read 只保留 h·v 一排；Use 只保留消融前后分布图，去掉标题与图例文字；删除右上注释。
- Write 面板改为右侧整高，向上延伸占据右上空白；方向线从左往右，接 Read、Use 后直接进入 Write 左侧。
- Write 内上下三块：every position / selected positions (top k%) / free generation。

## 20. v16

- Write 门控块标题改为 "gated by FPpred score"（FPpred 蓝色），门控位置的 ⊕ 改为 FP 橙色：FPpred 选位置，FP 负责注入。

## 21. v17

- 门控改为图形表达：上行 FPpred 分数条（行首蓝色迷你方向块）+ 阈值线；只有超过阈值的位置有蓝色虚线箭头向下触发下行的橙色 ⊕（行首橙色迷你方向块），其余位置为灰点。
- every position 行首放橙 + 蓝两个迷你方向块，表示两个方向都逐位置添加。标题缩为 "gated"。

## 22. v18

- Write 内部分成三个白底子面板（every position / gated / free generation），统一内边距、标题位置与列对齐；top k% 标签移到 gated 子面板右上角。
