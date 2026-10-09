# Overview figure — drawing prompt (draft v1)

> 用 `paper-flowchart` skill 执行。内容以《读、用、写：实验重新编号与数据总表》（2026-10-09）为准，不以旧版 main.tex 为准。

## 1. 目的与版式

- ACL 论文 overview 图，只展示研究设计流程，**不放任何数值结果或结论**。
- 通栏 `figure*`，横向，宽高比约 3:1（约 16 cm × 5.5 cm）。单页。
- 全部标签英文；字号按缩放到 16 cm 宽后仍 ≥ 7 pt 设计。
- 节点总数控制在约 22 个以内；面板内实验以竖排条目呈现，条目之间不连线。

## 2. 核心叙事约束

- **Read / Use / Write 三个面板并列，彼此之间不画箭头。** 它们不是同一方向上已成立的因果链。
- 唯一跨面板的连线：FPpred → Write 面板内的 Gated 区，**虚线**，标注 `external gate`，表示外部使用该分数，不代表模型原生依赖。
- 全图主线是两个关键比对：**Rate（how many）** 与 **Placement（where）**。

## 3. 布局（从左到右）

### A. Inputs（窄列，中性灰）

- `Pitt Cookie Theft` 文档形：older adults' picture descriptions
- 两个小子项：`Construction: 629 minimal pairs`；`Test: 445 FP vs 17,836 ordinary sites, 168 participants`
- `Llama-3.2-3B · Qwen2.5-1.5B · Qwen2.5-7B`，`residual stream, block 21/28`

### B. Directions（4 个立体块，竖排）

| 方向 | 颜色 | 小字说明 |
|---|---|---|
| FP | 暖色（主干预方向） | disfluent − fluent, sentence-final |
| PSEUDO | 灰 | optional-word control (*well, so*) |
| FP⊥ | 暖色虚线描边 | FP with PSEUDO component removed |
| FPpred | 冷色（读出方向） | pre-FP − pre-ordinary positions |

Inputs → Directions 一条实线；Directions 到三个面板各一条实线（从方向列右侧分出，不连到具体条目）。

### C. 三个并列面板

每个面板顶部一行写操作公式，下面竖排实验条目。条目格式：`短名` + 右侧 Rate/Placement 色点（不显示 E 编号）。Q7 未覆盖的条目尾部加灰色小字 `3B/1.5B`。

**READ**（冰蓝底）— 操作：`project h·v`
- Surprisal vs. filler propensity — ● P — `3B/1.5B`
- Position readout (AUC) — ● P
- Incremental prediction over covariates (ΔAUC) — ● P

**USE**（薄荷底）— 操作：`mean-ablate ⊖  h − (h·v − μ)v`
- FP ablation vs. energy-matched controls — ● R
- PSEUDO / FP⊥ specificity — ● R
- FPpred ablation — ● R ● P

**WRITE**（淡紫底）— 操作：`add ⊕  h + ασ_F v`
分两个子组（细虚线小容器）：
- *Ungated*
  - FP addition: gain vs. timing (TF) — ● R ● P
  - Continuous FP injection (generation) — ● R ● P — `3B/1.5B`
  - FPpred addition (TF) — ● R ● P
  - Oracle-timed injection — ● R ● P — `3B/1.5B`
- *Gated*（内含一个菱形：`FPpred score in top k%?`，是 → `inject FP +8σ_F`；对照 `own / random / always`）
  - Gated teacher forcing — ● P
  - Gated generation — ● R ● P — `3B/1.5B`

### D. Evaluation 条（底部，横跨 USE 与 WRITE 面板下方）

一行公式居中：`P(filler at t) = g · f(context_t)`，其中 **g** 用 Rate 色、**f** 用 Placement 色。

| RATE — how many (g) | PLACEMENT — where (f) |
|---|---|
| TF: net Δlog P(filler) at all positions | TF: matched selectivity, FP vs. ordinary sites |
| Gen: valid-FP outputs, FPs / 100 words | Gen: O/E at segment-initial / before content words |

两格分别用实色细边框 + 极浅同色底。READ 面板条目的 P 色点表示"读出的是位置信息"，不连到 Evaluation 条。

## 4. 配色

- 面板底色按 `paper-flowchart` 规范：READ 冰蓝 `#E6F3FF`、USE 薄荷 `#E0F2F1`、WRITE 淡紫 `#F3E5F5`。
- **Rate = 琥珀 `#E69F00`，Placement = 青绿 `#009E73`**—— 全图仅这两处实色，用于色点、g/f 和 Evaluation 两格边框。
- 无高饱和红色（不展示结果）。

## 5. 不画的内容

- 任何数值、CI、p 值、结论标记。
- REP / REPpred 及 S-REP、W-S1、S0、S-ROB 等补充项。
- 剂量网格细节、解码参数、预算数值（仅在 Gated 菱形中写 `top k%`）。

## 6. 已定事项

1. 本图取代现有 Figure 1（g·f 概念图压缩进 Evaluation 条）。
2. 不显示 E1–E12 编号。
3. Rate / Placement = 琥珀 / 青绿（Okabe–Ito）。
