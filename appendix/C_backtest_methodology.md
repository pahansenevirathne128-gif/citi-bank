# Appendix C — Backtest Stress Matrix Methodology

## Overview

Slide 13 compares our portfolio construction against Fund X across four historical commodity-geopolitical analogues. This appendix documents the asset proxies, portfolio construction formulae, FX alpha assumptions, and the caveats that judges should hold in mind when interpreting the results.

**Key caveat (must be stated in Q&A if asked):** This is asset-class proxy replication, not security-level historical simulation. The cascade-specific alpha overlays are calibrated assumptions, not historical realisations. Range of outcomes ±300bps.

---

## Analogue Period Definitions

| Period | Dates | Trigger | Why This Analogue |
|---|---|---|---|
| 1973 Oil Embargo | Oct 1, 1973 – Mar 31, 1974 | Yom Kippur war + OPEC embargo | Fertilizer supply shock, energy price spike, Middle East origin |
| 2008 Commodity Spike | Jan 1, 2008 – Jun 30, 2008 | Global commodity supercycle peak | Oil + ag prices, commodity-FX divergence, pre-financial crisis |
| 2011 Arab Spring | Feb 1, 2011 – Jul 31, 2011 | Libyan civil war, regional unrest | Geopolitical disruption, energy + food price pressure |
| 2022 Russia-Ukraine | Feb 1, 2022 – Jul 31, 2022 | Russian invasion of Ukraine | Closest structural analogue: commodity shock + defence rerating + European security crisis |

---

## Asset-Class Proxies

### Equities
- **Post-1980:** `^GSPC` (S&P 500 Total Return, via Yahoo Finance)
- **Pre-1980:** `^GSPC` price-only adjusted for dividend yield (approx. 4% annual yield applied via simple model)
- **1973 data quality note:** Pre-modern index data is sparse. `^GSPC` is available but without reliable total-return adjustment. Range of outcomes for 1973 period is therefore wider (±400–500bps vs ±300bps for later periods).

### Commodities
- **Post-2006:** `GSG` (iShares S&P GSCI Commodity-Indexed Trust ETF, inception 2006-07-21) via Yahoo Finance
- **Pre-2006:** Synthetic blend: `0.5 × CL=F (WTI crude) + 0.5 × GC=F (gold spot)`, both via Yahoo Finance
- **2026 cascade tilt:** Within the commodity sleeve, we apply a 40% ag complex weight (vs GSCI's ~15–20%) to capture the fertilizer–grain trade. This is implemented as an alpha overlay (see below).

### Fixed Income
- **Post-2002:** `TLT` (iShares 20+ Year Treasury Bond ETF) via Yahoo Finance
- **Pre-2002:** Synthetic price return from 10Y yield change: `ΔP ≈ −duration × Δy`, using `^TNX` (10Y UST constant maturity yield) and duration assumption of 7 years
- **TIPS (our portfolio, post-2003):** `TIP` ETF via Yahoo Finance
- **TIPS (pre-2003):** Nominal bond return + 200bps inflation overlay (calibrated to realised CPI during each period)

---

## Portfolio Construction Formulae

### Fund X (Benchmark)
```
Fund X return = 0.50 × equity_return + 0.30 × FI_return + 0.20 × commodity_return
```

### Our Portfolio (Cascade Tilts)
```
Our return = (0.30 × equity_return × beta_adj)
           + (0.28 × tips_return)
           + (0.22 × tilted_commodity_return)
           + (0.17 × fx_overlay_return)
           + (0.03 × cash_return)
```

Where:
- `beta_adj = 0.60` (we are net short broad equity, long theme-specific longs; 0.60 effective beta)
- `tilted_commodity_return` = base commodity return + cascade_ag_alpha (see below)
- `fx_overlay_return` = calibrated assumption (see FX Alpha section)
- `cash_return` = 3-month T-bill rate (from FRED `TB3MS`)

---

## Cascade Alpha Overlays (Calibrated Assumptions)

These overlays are the difference between our portfolio and a mechanical asset-class mix. They represent the "skill" contribution from our cascade views.

| Overlay | Calibration Method | Value Used |
|---|---|---|
| Ag complex tilt (commodity sleeve) | 2022 analogue: wheat/corn outperformed GSCI by +18% in 6 months | +12–18% annualised during commodity shocks |
| EU defence tilt (equity sleeve) | 2022 analogue: EUAD-equivalent outperformed broad EU equities by ~22% | Applied only to post-2006 periods |
| FX alpha (long commodity FX, short importer FX) | Backtested via synthetic pair baskets (AUD/CAD/NOK vs KRW/INR/THB) during each analogue | See FX Alpha section below |

**Critical disclosure (required in Q&A):** The ag and defence tilts were not implementable via ETFs during 1973 and 2008 — the instruments didn't exist. These alpha estimates represent what the strategy *would* have captured if the same instruments had existed. This is counterfactual backtesting, and judges may push on it.

---

## FX Alpha Calibration

**Assumption:** A long-commodity-FX / short-Asian-importer-FX overlay generates a calibrated +500bps annualised (+250bps 6-month) excess return during commodity-geopolitical shocks.

**Calibration evidence:**
- 2022 Russia-Ukraine: AUD (+3.2%), CAD (+2.9%), NOK (+10.1%) vs KRW (−5.4%), INR (−4.8%), PHP (−6.2%) over 6 months — spread ≈ 12–16pp, gross
- 2008 commodity spike: AUD (+11%), NOK (+8%) vs KRW (−14%), THB (−4%) — spread ≈ 15–25pp gross
- Applying haircut for transaction costs, correlation friction, and implementation lag → conservative estimate of +500bps annualised net

**Disclosure:** The FX overlay did not exist in Fund X's investable universe during any of the analogue periods. Its inclusion in the backtest as a separate alpha sleeve is a forward-looking calibration, not a historical realisation.

---

## Survivorship Bias Acknowledgment

The four analogue periods were selected *because* they were commodity-geopolitical shocks — the same regime type as 2026. This creates **selection bias**: we are not showing periods where a similar portfolio construction underperformed. An unbiased backtest would include periods like:

- 2015–2016 commodity bust (when commodity overweight destroyed value)
- 2020 COVID crash (when commodity sleeve fell sharply before recovering)

The four chosen analogues are the *best-case* comparison for our thesis. They are presented as "stress test" analogues for the current regime, not as a random sample of historical performance.

---

## Results Summary

| Period | Fund X 6M Return | Our Portfolio 6M Return | Delta (bps) | Fund X MDD | Our MDD | Fund X Sharpe | Our Sharpe |
|---|---|---|---|---|---|---|---|
| 1973 Oil Embargo | −7.8% | −2.2% | +560 | −9.8% | −5.5% | −1.86 | −0.71 |
| 2008 Commodity Spike | +1.5% | +9.5% | +800 | −5.5% | −4.3% | +0.34 | +1.86 |
| 2011 Arab Spring | +2.6% | +6.5% | +390 | −8.6% | −6.0% | +0.46 | +1.16 |
| 2022 Russia-Ukraine | −9.5% | −2.3% | +714 | −13.7% | −10.5% | −1.00 | −0.18 |

**Range of outcomes:** All figures carry ±300bps uncertainty from proxy construction.

---

## References

- GSPC data: Yahoo Finance (`^GSPC`)
- 10Y UST yield: FRED `GS10`; Yahoo Finance `^TNX`
- Commodity proxies: Yahoo Finance `GSG`, `CL=F`, `GC=F`
- TLT, TIP: Yahoo Finance
- T-bill rate: FRED `TB3MS`
- World Bank Pink Sheet historical commodity prices: https://www.worldbank.org/en/research/commodity-markets
