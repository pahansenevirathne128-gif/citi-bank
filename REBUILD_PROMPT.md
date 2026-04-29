# Citi Global Markets Challenge 2026 — Notebook Rebuild

## Environment

- Python: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`
- Jupyter kernel: **Python 3.12 (system)** (`sys-python312`)
- Working directory: this folder

Install dependencies first (run once in terminal):
```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/pip3 install \
  yfinance pandas numpy matplotlib scikit-learn scipy \
  PyPortfolioOpt cvxpy --break-system-packages -q
```

---

## What to Build

A single Jupyter notebook: `citi_markets_2026.ipynb`

Generate it by running: `python3 create_notebook.py`

The notebook has 16 cells. Each cell is self-contained. No caches, no fallbacks — just download the data and run.

---

## Rules

- Download all data fresh via `yfinance.Ticker(t).history()` — one ticker at a time with `time.sleep(1)` between calls
- Save each download as a CSV in `data/` immediately after download
- All charts use `matplotlib` only — no plotly, no kaleido
- No cache checks, no `if file.exists()` logic — always download
- Colors: `NAVY='#0A1628'`, `GOLD='#C9A84C'`, `FOREST='#1B4332'`, `OCEAN='#1A5276'`, `CRIMSON='#922B21'`, `GREY='#7F8C8D'`
- Save charts to `charts/` with `plt.savefig(..., dpi=150, bbox_inches='tight')`
- Kernel metadata: `"name": "sys-python312"`, `"display_name": "Python 3.12 (system)"`

---

## Cell 1 — Imports

```python
import warnings; warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import time

NAVY='#0A1628'; GOLD='#C9A84C'; FOREST='#1B4332'
OCEAN='#1A5276'; CRIMSON='#922B21'; GREY='#7F8C8D'
COLORS = [NAVY, GOLD, FOREST, OCEAN, CRIMSON, GREY]

CHARTS = Path('charts'); DATA = Path('data')
CHARTS.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)

print(f'numpy {np.__version__}  pandas {pd.__version__}')
```

---

## Cell 2 — Download All Data

Download the following tickers via `yfinance.Ticker(t).history(start='2020-01-01')`.
Sleep 1 second between each. Save the combined Close prices to `data/prices.csv`.

Tickers:
- FX: `AUDUSD=X`, `CADUSD=X`, `NOKUSD=X`, `ZARUSD=X`, `KRWUSD=X`, `IDRUSD=X`, `THBUSD=X`, `INRUSD=X`, `PHPUSD=X`
- Grains: `ZC=F`, `ZW=F`, `ZS=F`
- Commodities: `BZ=F`, `GC=F`, `CL=F`
- ETFs: `IVV`, `VGK`, `EEM`, `LQD`, `TIP`, `PDBC`, `EUAD`, `GSG`, `TLT`, `GLD`, `EWZ`, `EWW`
- Equities: `CF`, `NTR`, `MOS`, `ICL`, `DE`, `AGCO`, `CNHI`, `KHC`, `GIS`, `CPB`
- Index: `^GSPC`, `^TNX`

Print how many rows downloaded per ticker. Print final shape of `prices`.

---

## Cell 3 — Hero 1: Fertilizer vs Grain Divergence (Slide 2)

**Chart:** `charts/hero_1_divergence.png`

- Pull `ZC=F` (corn), `ZW=F` (wheat), `ZS=F` (soy) from `prices`
- Normalise each to 100 at first trading day of 2025 (`prices.loc['2025-01-01':]`)
- Fertilizer series is hand-coded: urea ramps from 100 to 149 over Jan–Apr 2025 (published CNBC/IFPRI data — construct a smooth logistic curve)
- Plot all four lines. Annotate urea with `+49%`, corn with actual YTD change
- Title: `"FERTILIZER IS UP 49%. CORN IS UP 0.5%."`
- Source line: `"yfinance (CBOT futures); CNBC Commodities Desk; IFPRI April 2026"`

---

## Cell 4 — Hero 2: FX PCA Biplot (Slide 9)

**Chart:** `charts/hero_2_fx_pca.png`

- Use FX columns from `prices`: `AUDUSD=X`, `CADUSD=X`, `NOKUSD=X`, `ZARUSD=X` (commodity exporters) and `KRWUSD=X`, `IDRUSD=X`, `THBUSD=X`, `INRUSD=X`, `PHPUSD=X` (Asian importers)
- Compute daily log returns. Drop NaNs. StandardScale. Run PCA(n_components=2)
- Plot loading arrows: commodity exporters in GOLD, importers in CRIMSON
- Sign-correct so AUD has positive PC1 loading
- Label each arrow with short name (AUD, CAD, etc.)
- Print: PC1 variance %, PC2 variance %, loading table
- Title: `"COMMODITY FX DIVERGING FROM ASIAN IMPORTERS"`
- Annotation: `"PC1: XX.X% | PC2: XX.X%"`
- Source: `"yfinance 2Y daily returns"`

---

## Cell 5 — Cascade 1: Fertilizer Lag (Slide 7)

**Chart:** `charts/cascade_1_fertilizer_lag.png`

- Three historical analogues (hand-coded index, weeks 0–24): 1973, 2008, 2022 — plot in GREY dashed
- 2026 live line: fertilizer (GOLD), corn (CRIMSON), anchored at week 0 = Feb 2026
- Vertical line at week 8 with annotation `"We are at week 8"`
- Shaded zone weeks 6–12 labelled `"Historical lag range"`
- Title: `"THREE CRISES. SAME LAG. SAME TRADE."`

---

## Cell 6 — Cascade 2: Defence Backlog (Slide 8)

**Chart:** `charts/cascade_2_defence_backlog.png`

Two-panel figure (side by side):

**Left panel:** Horizontal bar chart of order backlogs
- Rheinmetall €63.8bn, BAE £83.6bn, Leonardo €44bn, Thales €52bn, Saab SEK 7.4bn
- Rheinmetall bar in GOLD, rest in NAVY
- Label each bar with value

**Right panel:** EUAD ETF YTD performance
- Pull `EUAD` from `prices`, slice from `2026-01-01`, normalise to 100
- If EUAD unavailable, draw synthetic line ending at 91.3 (−8.7% YTD)
- Annotate final value with `+X.X%` or `−X.X%`

Suptitle: `"BACKLOGS +36%. STOCKS −8.7% YTD. SOMETHING HAS TO GIVE."`
Source: `"Rheinmetall/BAE/Leonardo/Thales annual reports 2025; yfinance EUAD"`

---

## Cell 7 — Cascade 4: Sticky CPI (Slide 10)

**Chart:** `charts/cascade_4_sticky_cpi.png`

Dual-axis chart:

- Left axis (GOLD): Atlanta Fed Sticky CPI monthly Jan 2022–Apr 2026
  Hand-coded values: `[4.2,4.5,4.7,5.1,5.4,5.6,5.8,6.0,6.2,6.3,6.2,6.0,5.7,5.4,5.1,4.8,4.5,4.3,4.2,4.0,3.9,3.8,3.9,3.9,3.9,3.9,3.9,3.9]`
- Right axis (CRIMSON dashed): Implied 2026 Fed cuts in bps from CME FedWatch
  Hand-coded: `[75, 37.5, 25, 12.5]` for Jan–Apr 2026
- Shade region above 3.5% CPI in light gold
- Title: `"CPI IS STICKY. MARKETS PRICE 12.5 BPS OF CUTS. GAP = TRADE."`
- Source: `"Atlanta Fed Sticky CPI; CME FedWatch April 2026"`

---

## Cell 8 — Black-Litterman Portfolio (Slide 11)

**Chart:** `charts/portfolio_risk_donut.png`
**Data:** `data/portfolio_weights.csv`

Asset universe: `IVV` (US_EQ), `VGK` (EU_EQ), `EEM` (EM_EQ), `LQD` (IG), `TIP` (TIPS), `PDBC` (CMDTY)

- Pull from `prices`, slice from `2022-01-01`, rename columns to asset names
- Compute CAPM returns and Ledoit-Wolf covariance via PyPortfolioOpt
- Four BL views (absolute):
  - CMDTY: +12% (confidence 0.70)
  - EU_EQ: +8%  (confidence 0.65)
  - TIPS:  +3%  (confidence 0.75)
  - US_EQ: −4%  (confidence 0.60)
- Run BlackLittermanModel with omega='idzorek'
- Optimise max Sharpe via EfficientFrontier
- Save weights table (Equal / Fund X / BL Posterior) to `data/portfolio_weights.csv`
- Print weights table
- Plot donut chart of marginal risk contribution (not capital weight)
- Title: `"BL PORTFOLIO — MARGINAL RISK CONTRIBUTION"`
- Note below chart: `"Risk budget, not dollar weight"`

---

## Cell 9 — Backtest (Slide 13)

**Chart:** `charts/hero_3_backtest.png`
**Data:** `data/backtest_stress_matrix.csv`

Three analogue periods: 2008 (Jan–Jun), 2011 (Feb–Aug), 2022 (Feb–Aug)

For each period:
- Equity proxy: `^GSPC`; Fixed income: `TLT`; Commodity: average of `BZ=F` and `GC=F`
- Normalise each series to 1.0 at start of period
- Fund X weights: 50% equity / 30% FI / 20% commodity
- Our portfolio weights: 20% equity / 30% FI / 35% commodity / 15% FX alpha
- FX alpha: linear ramp of +5% annualised over the period
- Plot Fund X (NAVY dashed) vs Our Portfolio (GOLD) for each period
- Shade gap GOLD where we outperform, CRIMSON where we underperform
- Compute 6-month return and delta in bps for each period

Three-panel figure (1 row × 3 cols)
Suptitle: `"IN EVERY COMMODITY-GEOPOLITICAL ANALOGUE, OUR PORTFOLIO OUTPERFORMS"`
Footer: `"Asset-class proxies. FX alpha calibrated. ±300bps range."`
Save stress matrix CSV with columns: Period, Fund_X_6m, Ours_6m, Delta_bps

---

## Cell 10 — Scenario P&L Fan (Slide 14)

**Chart:** `charts/scenario_pl.png`

Four scenarios with net alpha after costs:
- Bull (20%): gross +1450bps → net after 71bps costs + 80bps hedges
- Base (55%): gross +575bps → net
- Stagflation (10%): gross +300bps → net
- Bear (15%): gross −400bps → net

Plot cumulative alpha path over 3 months for each scenario (x-axis = months 0–3).
Horizontal dotted line at probability-weighted expected alpha.
Annotate E[α] value.
Title: `"SCENARIO P&L — EXPECTED ALPHA [X] BPS NET OF ALL COSTS"`
Footer: `"Net of 71bps transaction costs + 80bps hedge book. Scenario weights: Bull 20% / Base 55% / Stag 10% / Bear 15%."`

---

## Cell 11 — Transaction Costs

No chart. Print only.

Portfolio positions and notionals exactly as in `code/transaction_costs.py`.
Compute round-trip costs per bucket and total.
Print alpha waterfall:
```
Gross scenario-weighted alpha:    +574 bps
Less hedge book:                   -80 bps
Less round-trip transaction costs: -71 bps
NET ALPHA:                        +423 bps
```
Save to `data/transaction_costs.csv`.

---

## Cell 12 — Concentration Audit: Factor Decomposition

**Chart:** `charts/concentration_heatmap.png`
**Data:** `data/concentration_corr_matrix.csv`

Tickers: `CF`, `NTR`, `MOS`, `ICL` (fertilizer), `DE`, `AGCO`, `CNHI` (ag equipment),
`ZC=F`, `ZW=F`, `ZS=F` (grains), `KHC`, `GIS`, `CPB` (food shorts), `TIP`, `EWZ`, `EWW`

- Pull from `prices`, compute daily log returns, slice from 2021-01-01
- Compute correlation matrix → save as CSV
- Compute eigenvalues and participation ratio:
  ```python
  eigvals = np.linalg.eigvalsh(corr.values)[::-1]
  eigvals = np.maximum(eigvals, 0)
  participation_ratio = eigvals.sum()**2 / (eigvals**2).sum()
  ```
- Run PCA(n_components=3), print loadings ranked by |PC2|
- Plot correlation heatmap with cell annotations (diverging: CRIMSON–white–OCEAN)
- Print verdict: effective bets, % variance in PC1, diversification quality (GOOD ≥3 / MODERATE ≥2 / POOR)

---

## Cell 13 — Alpha Per Cost Ranking

**Chart:** `charts/alpha_per_cost_ranking.png`

Load `data/transaction_costs.csv`.

Assign expected 3-month alpha % to each position (use the table in Cell 11 of the previous notebook — fertilizer producers +12%, corn +12%, wheat +6%, EU defence +9%, etc.).

Compute: `alpha_per_cost = (notional × alpha%) / round_trip_cost_USD`

Rank all positions. Plot horizontal bar chart of top 15, coloured by cascade:
- GOLD = cascade 1, FOREST = cascade 2, OCEAN = cascade 3, CRIMSON = cascade 4, GREY = non-cascade

Print:
- Top 5 and bottom 5 by alpha-per-cost
- Average for cascade-1 vs non-cascade positions
- Verdict: is cascade-1 concentration cost-efficient?

---

## Cell 14 — Concentration Scenarios

**Chart:** `charts/concentration_tornado.png`
**Data:** `data/concentration_scenarios.csv`

Simulate four portfolios with different cascade-1 weightings:
- A: Status Quo (C1 = 26% of NAV)
- B: Trimmed (C1 = 20%)
- C: Diversified (C1 = 18%)
- D: Overweight (C1 = 32%)

For each, compute:
- Round-trip cost in bps of NAV: `C1_notional × 20 × 2 / NAV + other_notional × 15 × 2 / NAV`
- Gross expected alpha bps: `C1_notional × 0.12 / NAV × 10000 + other × 0.05 / NAV × 10000`
- Scenario net alpha (gross × scenario_mux − costs − 80bps hedges):
  - Base ×1.0, Bull ×2.5, Bear ×−0.7, Stagflation ×0.52
- Probability-weighted net alpha (55% / 20% / 15% / 10%)
- Approx Sharpe = PW_net / portfolio_vol where vol = `800 + (C1_pct − 20) × 15` bps

Save CSV. Plot bar chart coloured by portfolio. Annotate each bar with PW alpha and Sharpe.
Print recommendation: STAY / TRIM / OVERWEIGHT with numbers.

---

## Cell 15 — Cascade-1 Stress Tests

**Chart:** `charts/cascade1_stress_tests.png`

Three failure modes, each plotted as a 3-month return path:

- FM1 — Cascade fizzles: C1 sleeve −15%, other +1%, FX alpha unchanged, Fund X −2%
- FM2 — Cascade delayed: C1 sleeve 0%, other +4%, FX alpha unchanged, Fund X +3%
- FM3 — Substitution wins: C1 sleeve +2%, other +4%, FX alpha unchanged, Fund X +3%

For each:
- Plot Our Portfolio (CRIMSON), Our Portfolio + hedge (GOLD dotted), Fund X (NAVY dashed) over months 0–3
- Brent put hedge covers +50bps in FM1 only

Three-panel figure. Print delta vs Fund X (unhedged and hedged) for each mode.
Print: worst-case unhedged, worst-case hedged, hedge coverage in bps.

---

## Cell 16 — Write CONCENTRATION_AUDIT.md

No chart. Write `CONCENTRATION_AUDIT.md` to project root.

Sections:
1. Executive Summary (3 bullets)
2. Factor decomposition findings (participation ratio, PC1%, diversification quality)
3. Alpha-per-cost findings (cascade-1 vs rest, verdict)
4. Scenario comparison table (A/B/C/D with PW alpha and Sharpe)
5. Stress test results (FM1/FM2/FM3, worst-case bps)
6. Recommendation: STAY / TRIM / RESTRUCTURE with specific position changes if any
7. Deck impact: which slides need updating, which Q&A answers to sharpen

Use the numbers computed in Cells 12–15. Do not hardcode — read from the variables in scope.

---

## Output Checklist

```
charts/hero_1_divergence.png
charts/hero_2_fx_pca.png
charts/cascade_1_fertilizer_lag.png
charts/cascade_2_defence_backlog.png
charts/cascade_4_sticky_cpi.png
charts/portfolio_risk_donut.png
charts/hero_3_backtest.png
charts/scenario_pl.png
charts/concentration_heatmap.png
charts/alpha_per_cost_ranking.png
charts/concentration_tornado.png
charts/cascade1_stress_tests.png

data/prices.csv
data/portfolio_weights.csv
data/backtest_stress_matrix.csv
data/transaction_costs.csv
data/concentration_corr_matrix.csv
data/concentration_scenarios.csv

CONCENTRATION_AUDIT.md
```
