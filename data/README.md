# data/ · 实验数据索引

> 本目录由实验脚本自动写入（三个脚本的 `--outdir` 默认值已改为 `data`）。
> **不要手动编辑这里的数据文件**——它们由脚本重新生成。

## 当前有效

| 文件 | 来源 | 说明 |
|---|---|---|
| `data/leak_durable_sensitivity_0.012.json` | `_ld_sensitivity.py` | 🏆 **主结果的机器可读出处**（40 seeds / 240 learners / 25 problems）：λ\*=0.30、gain\*=**0.5659**、left +0.438、right +0.3008、**control +0.0594**、**归因 0.8645（86%）**、θ=**0.3578** |
| `logs/_main_threshold.log` | `m2_lambda_sweep.py --seeds 40 --problems 25` | 🏆 **主 sweep 的完整网格**（同配置）。校准门 G1–G5、λ 网格 19 点、`P1 boundary located at lambda=0.3 (index 11 of 0..18)`、`P6 … scaffolding share=86%`。**论文的 λ\*=0.30 / 0.5659 / 86% 以本日志为准** |
| `m2_lambda_alr_summary.json` | `m2_lambda_sweep.py` | ⚠️ **不是主结果**：本文件当前是 `--selftest` 规模的 run（**16 seeds / 240 learners / 16 problems**，θ=0.1791，峰值 earned gain **0.5049**）。它**不含** 0.5659 / 86% / θ=0.3578。2026-09-22 审计更正（此前 README 误记为主结果） |
| `m2_lambda_alr_raw.csv` | 同上 | 与上面的 summary 同一次 run 的逐 seed 原始记录 |
| `m2_a9_sensitivity_v2.json` / `.csv` | `_a9_sensitivity.py` | ⚠️ **只含一个常数**：`collapse_sharpness`（4 个取值，λ\*∈[0.25,0.35]、share 0.83–0.86）。此前误记为"三常数"，另两个常数的权威记录在日志：`logs/_a9_threshold.log`（λ_c，6 值）与 `logs/_a9_damping.log`（D，5 值） |
| `m2_durable_factor_sensitivity.json` / `.csv` | `_df_sensitivity.py` | **`durable_factor`（A3）敏感性** —— 该参数修复后首次被检验 |

## ⚠️ 已作废，勿引用

| 文件 | 作废原因 |
|---|---|
| `m2_a9_sensitivity.json`<br>`m2_a9_sensitivity.csv` | **旧 `_a9_sensitivity.py` v1 的产物，且是旧「连续线性」衰减形式下的数据。**<br>2026-09-20 模型改为**阈值/边界**形式后，这两个文件与现行结果**不可比**。<br>保留仅为留痕。**请用 `m2_a9_sensitivity_v2.*`。** |

## 复现命令

```bash
python m2_lambda_sweep.py --seeds 40 --problems 25            # 主 sweep，写入 data/
python m2_lambda_sweep.py --selftest --seeds 16 --problems 16 # 变异检验（13 项），须 13/13
python _a9_sensitivity.py --which all --seeds 20 --problems 15 --learners 200 --boot 200
python _df_sensitivity.py --seeds 20 --problems 15 --learners 200
python _check_threshold_mutants.py                            # 阈值机制快速变异检查（7 项）
python _audit_dead_params.py                                  # 死参数审计，须 17/17 live
```

## 口径提醒（写作时）

- **λ\* 必须报成区间**（全 A9 范围 ∈ [0.20, 0.45]），**不得报单点**。
  → 出处 = `logs/_a9_threshold.log`（λ_c 六个非结构性取值 = 0.20 / 0.20 / 0.25 / 0.30 / 0.35 / 0.45，跨度 0.25）。
- **不得写「内部最优 / 最优强度」**——语义是**守约边界下沿**。
- 归因份额 **76–88%**（深度扫描下恒为 86%）是**最稳健**的量，应作第一宣称的依据。
  → 出处 = 同上日志的 `attribution share range = 76% – 88%`；"恒定 86%" 出自 `logs/_a9_damping.log`（5/5）。
- 该份额**必须带条件**：它依赖 `leak_durable`（泄露的答案有多教得会）。40 seeds 同配置下 ld=0.012 → 86%，
  翻转点在 **(0.20, 0.22)**，ld=0.50 → **28%**。出处 = `data/leak_durable_sensitivity_*.json`。

## 🔴 已作废的旧形式数字（勿引用，出现即错）

旧「连续线性 / 内部最优」形式作废后，下列值**不得出现在任何交付物**（`08` 中仅作审计轨迹保留）：

| 量 | 旧值（作废） | 现行（阈值形式） |
|---|---|---|
| λ\* | ~~0.35~~ | **0.30**，区间 [0.20, 0.45] |
| earned-solve 峰值 | ~~0.5204~~ | **0.5659** |
| 可归因份额 | ~~85% / 84%~~ | **86%** |
| 右分支效应量 | ~~+0.1394~~ | **+0.3008** |
| `leak_durable=0.50` 时的份额 | ~~43%~~ | **28%**（2026-09-22 更正） |
| 翻转点 | ~~≈0.45~~ | **(0.20, 0.22)** |
