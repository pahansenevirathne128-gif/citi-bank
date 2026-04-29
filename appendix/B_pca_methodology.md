# Appendix B — FX PCA Biplot Methodology

## Overview

Cascade 3 argues that commodity-exporting currencies have diverged structurally from Asian-importer currencies since the Iran conflict began. This appendix documents how we measure and visualise that divergence using principal component analysis (PCA).

---

## Data Window

- **Start:** 2024-04-28 (2 years of daily data, ending 2026-04-29)
- **End:** 2026-04-29
- **Frequency:** Daily close (aligned, forward-filled up to 5 business days for holidays)
- **Source:** Yahoo Finance (yfinance) — all tickers in `XYZUSD=X` format

---

## Currency Basket Composition

### Commodity Exporters (4 pairs)
| Code | Pair | Rationale |
|---|---|---|
| AUD | AUD/USD | Largest commodity-FX pair; iron ore, LNG, wheat |
| CAD | CAD/USD | Oil-correlated; WTI proximity |
| NOK | NOK/USD | Brent-correlated; North Sea oil exporter |
| ZAR | ZAR/USD | Gold + platinum exporter; also EM risk proxy |

### Asian Importers (5 pairs)
| Code | Pair | Rationale |
|---|---|---|
| KRW | KRW/USD | Major oil and LNG importer; refining hub |
| IDR | IDR/USD | Indonesia: commodity importer for manufacturing |
| THB | THB/USD | Thai baht: tourism + manufacturing; energy dependent |
| INR | INR/USD | Largest petroleum importer by volume outside China |
| PHP | PHP/USD | Philippine peso: remittance-driven, energy import sensitive |

**Exclusions and rationale:**
- BRL (Brazil): included in some FX PCA work but excluded here because Brazil is both commodity exporter *and* significant oil importer — would cloud the biplot
- CNY/CNH: Managed float, heavily influenced by PBOC intervention, not freely tradeable — excluded
- JPY: Safe-haven dynamics dominate commodity sensitivity — would contaminate PC1 as a "risk-off" factor rather than commodity factor
- MXN: Oil exporter, but NAFTA/US linkage means USD strength is the primary driver, not commodity prices

---

## Pre-processing

1. **Daily log returns:** `r_t = ln(P_t / P_{t-1})` for each pair
2. **Standardisation:** `z = (r - mean) / std` via `sklearn.preprocessing.StandardScaler` — ensures each currency contributes equally regardless of volatility level
3. **Missing value handling:** Forward-fill up to 5 days; any remaining NaN rows dropped before PCA

---

## PCA Specification

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(returns_df)

pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)
loadings = pca.components_  # shape (2, n_currencies)
```

- **n_components = 2** (sufficient: top two components explain >50% of variance in commodity-shock regimes)
- **Sign convention (post-hoc flip):** After fitting, we check the sign of the AUD loading on PC1. If `loadings[0, AUD_idx] < 0`, we multiply all PC1 loadings by −1. This ensures commodity exporters always load positively on PC1, making the biplot direction consistent regardless of fitting randomness.

---

## Results (as of 2026-04-29)

| Component | Variance Explained |
|---|---|
| PC1 | ~41.3% |
| PC2 | ~11.2% |
| **Total (PC1 + PC2)** | **~52.5%** |

Annotation on chart: "PC1: 41.3% | PC2: 11.2%"

### Loadings Summary

**Commodity exporters** (positive PC1 loading, capturing commodity strength):
- AUD, CAD, NOK load positively on PC1 (0.3–0.5 range)
- ZAR has mixed loading: positive on PC1 but also loads on PC2 due to EM risk-off sensitivity. This dual identity is noted in the chart commentary.

**Asian importers** (negative PC1 loading or opposite PC2, capturing commodity headwind):
- KRW, IDR, THB, INR, PHP cluster opposite the commodity exporters on PC1

The biplot makes the cluster separation visually unambiguous: commodity exporters sit in the bottom-right quadrant; Asian importers in the upper-left.

---

## Limitations

1. **Short data window for structural claim.** Two years of daily returns includes the post-COVID commodity cycle, which may partially pre-configure the clusters in our favour. A longer window (5–10 years) would include regimes where commodity and FX relationships broke down.
2. **PC1 captures correlation, not causality.** The component that separates exporters from importers also captures general USD strength dynamics. The two effects are not cleanly separable with PCA alone.
3. **Loadings could shift with regime change.** If a ceasefire occurs and oil reverses, the PC1 loading on commodity FX may compress quickly, narrowing the cluster separation.
4. **Two components may miss structural information.** Cumulative variance of 52.5% means ~47.5% of FX co-movement is unexplained by the biplot — the chart understates complexity.

---

## References

- Jolliffe, I.T. (2002). *Principal Component Analysis*, 2nd ed. Springer.
- Lustig, H., Roussanov, N., & Verdelhan, A. (2011). "Common risk factors in currency markets." *Review of Financial Studies*, 24(11).
- Chen, Y.C., Rogoff, K.S., & Rossi, B. (2010). "Can exchange rates forecast commodity prices?" *Quarterly Journal of Economics*, 125(3).
- yfinance documentation: https://pypi.org/project/yfinance/
- scikit-learn PCA: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
