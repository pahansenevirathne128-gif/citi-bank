# Day 3 Audit — Slide vs Chart Gap Check
> Generated: 2026-04-29 | Quant lead review before Day 3 build

---

## Slide-by-Slide Status

| # | Slide Title | Required Chart/Visual | File Path | Status | Owner |
|---|---|---|---|---|---|
| 1 | Title & Executive Summary | None (text only) | — | ✅ DONE | Person B |
| 2 | Hero 1: The Divergence Chart | `hero_1_divergence.png` | `charts/hero_1_divergence.png` | ✅ DONE | Quant |
| 3 | The Macro Setup: Why 2026 Is Different | None (narrative text) | — | ✅ DONE | Person B |
| 4 | First-Order Effects: What's Already Priced | None (bullet list) | — | ✅ DONE | Person B |
| 5 | The Opportunity Map: Four Cascades | Table (text) | — | ✅ DONE | Person B |
| 6 | Cascade Framework: How Lags Create Alpha | None (narrative text) | — | ✅ DONE | Person B |
| 7 | Cascade 1: Fertilizer–Grain Lag | `cascade_1_fertilizer_lag.png` | `charts/cascade_1_fertilizer_lag.png` | ✅ DONE | Quant |
| 8 | Cascade 2: Defence Backlog Anomaly | `cascade_2_defence_backlog.png` | `charts/cascade_2_defence_backlog.png` | ✅ DONE | Quant |
| 9 | Cascade 3: FX Dislocation (PCA Biplot) | `hero_2_fx_pca.png` | `charts/hero_2_fx_pca.png` | ✅ DONE | Quant |
| 10 | Cascade 4: Sticky Inflation vs Fed Pricing | `cascade_4_sticky_cpi.png` | `charts/cascade_4_sticky_cpi.png` | ✅ DONE | Quant |
| 11 | Black-Litterman Portfolio: Posterior Weights | `portfolio_risk_donut.png` | `charts/portfolio_risk_donut.png` | ✅ DONE | Quant |
| 12 | Benchmark Deep Dive: Fund X | None (table + text) | — | ✅ DONE | Person B |
| 13 | Hero 3: Backtest Stress Matrix | `hero_3_backtest.png` + `hero_3_stress_table.png` | `charts/hero_3_backtest.png`, `charts/hero_3_stress_table.png` | ✅ DONE | Quant |
| 14 | Portfolio Summary: Returns, Risk, Sizing | Scenario P&L fan chart → `scenario_pl.png` | — | 🔴 MISSING | Quant |
| 15 | Execution Plan: How We Trade This | None (table + text) | — | ✅ DONE | Person B |
| 16 | Risk Panel: Ceasefire Probability | `risk_polymarket.png` | — | 🔴 MISSING | Quant |
| 17 | Appendix: Methodology & Data Sources | 5 methodology `.md` docs | — | 🔴 MISSING | Quant |

---

## Quant Gaps — Top 3 to Fill Today

### Gap 1 (HIGH IMPACT) — Slide 16: Polymarket risk chart
- **File needed:** `charts/risk_polymarket.png`
- **Script to create:** `code/polymarket_scraper.py`
- **Why high impact:** Risk management is explicitly scored in the rubric. Polymarket gives a *quantified* probability for the thesis-killing scenario (ceasefire). This turns "we're monitoring the risk" into "the market prices this at X%."

### Gap 2 (HIGH IMPACT) — Slide 14: Scenario P&L fan chart
- **File needed:** `charts/scenario_pl.png`
- **Script to create:** `code/scenario_chart.py`
- **Why high impact:** Slide 14 currently has a purely textual return/risk scorecard. Judges expect a visual that shows asymmetric upside. Four scenarios, probability-weighted, alpha fan. Essential to the "portfolio construction" scoring criterion.

### Gap 3 (MEDIUM IMPACT) — Slide 17: Methodology appendix docs
- **Files needed:** `appendix/A_fertilizer_methodology.md` through `appendix/E_references.md`
- **Why medium impact:** Appendix content is not judge-facing during the main read, but it is consulted during Q&A and due diligence. Missing appendix = the team cannot defend its numbers.

---

## Non-Quant Slides (Person B owns)

Slides 1, 3, 4, 5, 6, 12, 15 require zero new quant output. Person B should be assembling these in the actual slide deck while quant finishes the three gaps above.

---

## Current File Inventory

### `charts/` (8 PNGs, 8 HTMLs — all produced Day 1–2)
- `hero_1_divergence.png` / `.html` → Slide 2
- `hero_2_fx_pca.png` / `.html` → Slide 9
- `cascade_1_fertilizer_lag.png` / `.html` → Slide 7
- `cascade_2_defence_backlog.png` / `.html` → Slide 8
- `cascade_4_sticky_cpi.png` / `.html` → Slide 10
- `portfolio_risk_donut.png` / `.html` → Slide 11
- `hero_3_backtest.png` / `.html` → Slide 13
- `hero_3_stress_table.png` / `.html` → Slide 13

### `data/`
- `fx_daily.parquet` — 797 rows, 11 FX/commodity tickers
- `portfolio_weights.csv` — 6-asset BL posterior weights
- `backtest_stress_matrix.csv` — 4 analogue periods

### `code/`
- `strait_capital_style.py` — visual system
- `fetch_fx_data.py` — FX data fetcher

---

## Day 3 Build Plan

| Priority | Task | Est. Time | Output |
|---|---|---|---|
| 1 | Polymarket scraper + risk chart | 1 hr | `risk_polymarket.png`, `polymarket_probabilities.csv` |
| 2 | Scenario P&L fan chart | 1 hr | `scenario_pl.png` |
| 3 | Visual consistency pass + contact sheet | 2 hr | all PNGs updated, `_contact_sheet.png` |
| 4 | Methodology appendix docs | 1.5 hr | 5 `.md` files in `appendix/` |
| 5 | DAY_3_REVIEW.md + DAY_3_HANDOFF.md | 1 hr | 2 planning docs |
