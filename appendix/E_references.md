# Appendix E — References & Data Sources

## Data Sources

### Market Data

| Source | Access Method | Data Used |
|---|---|---|
| Yahoo Finance | yfinance Python library (`pip install yfinance`) | FX pairs, grain futures (ZC=F, ZW=F, ZS=F), equity ETFs (IVV, VGK, EEM, LQD, TIP, PDBC), commodity ETFs (GSG, DBC), index proxies (^GSPC, ^TNX), EUAD ETF |
| Federal Reserve (FRED) | fredapi library / pandas-datareader | Atlanta Fed Sticky CPI (`STICKCPIM157SFRBATL`), T-bill rate (`TB3MS`), 10Y yield (`GS10`), headline CPI (`CPIAUCSL`), TIPS 5Y yield (`DFII5`) |
| World Bank Pink Sheet | worldbank.org/en/research/commodity-markets | Historical commodity prices (urea, DAP, wheat, corn) — used for pre-2000 analogue period calibration |
| CME FedWatch | CME Group website | Implied Fed Funds futures pricing; 2026 cut expectations |
| Polymarket | Gamma Markets API (`gamma-api.polymarket.com/markets`) | Iran conflict resolution probability; fallback values used where live data unavailable |

### Fundamental/Reported Data

| Source | Data Used |
|---|---|
| CNBC Commodities Desk (April 2026) | Urea spot +49%, ammonia +32%, DAP +21% from Feb 28, 2026 base |
| IFPRI (International Food Policy Research Institute) | Fertilizer-food price linkage; quarterly commodity market monitor |
| Rheinmetall AG annual report / investor presentation (2025) | Order backlog €63.8bn (+36% YoY); 2026 sales guidance +40–45% |
| BAE Systems annual report (2025) | Order backlog £83.6bn; revenue guidance +7–9% |
| Leonardo SpA consensus estimates (Bloomberg) | Order backlog €44bn estimate |
| Thales Group consensus estimates (Bloomberg) | Order backlog €52bn estimate |
| Atlanta Fed (Federal Reserve Bank of Atlanta) | Sticky CPI methodology: https://www.atlantafed.org/research/inflationproject/stickyprice |
| BLS (Bureau of Labor Statistics) | Headline CPI data (`CPIAUCSL`) |

---

## Python Libraries

| Library | Version Used | Purpose |
|---|---|---|
| `yfinance` | 1.3.0 | Market data fetching |
| `plotly` | 6.7.0 | All charting |
| `kaleido` | 0.2.1 | PNG export from Plotly (pinned — v1+ breaks write_image) |
| `pandas` | 2.x | Data manipulation |
| `numpy` | 1.x | Numerical computation |
| `scikit-learn` | 1.x | PCA, StandardScaler |
| `scipy` | 1.x | Optimisation fallbacks |
| `PyPortfolioOpt` | 1.5.x | Black-Litterman model, Ledoit-Wolf covariance |
| `cvxpy` | 1.x | Convex optimisation solver (used by PyPortfolioOpt) |
| `fredapi` | 0.5.x | FRED data access |
| `pandas-datareader` | 0.10.x | Alternative FRED/World Bank access |
| `pyarrow` | latest | Parquet file I/O for FX data cache |
| `Pillow` | latest | Contact sheet image composition |
| `requests` | latest | Polymarket API calls |

---

## Academic References

### Portfolio Construction
- Black, F. & Litterman, R. (1992). "Global portfolio optimization." *Financial Analysts Journal*, 48(5), 28–43.
- Idzorek, T. (2005). "A step-by-step guide to the Black-Litterman model." Zephyr Associates working paper.
- Ledoit, O. & Wolf, M. (2004). "A well-conditioned estimator for large-dimensional covariance matrices." *Journal of Multivariate Analysis*, 88(2), 365–411.
- Roncalli, T. (2013). *Introduction to Risk Parity and Budgeting*. CRC Press.

### Fertilizer–Grain Economics
- Aghasafari, H., Bakhshoodeh, M., & Noorani, N. (2017). "Price transmission in input-output markets: evidence from Iran's agricultural sector." *Journal of Agricultural Science and Technology*, 19(1).
- Carroll, T. (2011). "Fertilizer-crop price linkages: historical patterns and 2008 spike evidence." FAO Commodity and Trade Policy Research Working Paper No. 33.
- Gilbert, C.L. (2010). "How to understand high food prices." *Journal of Agricultural Economics*, 61(2), 398–425.
- IFPRI (2022). "Fertilizer and food prices: market outlook 2022." IFPRI Global Food Policy Report.

### FX and Commodity Markets
- Lustig, H., Roussanov, N., & Verdelhan, A. (2011). "Common risk factors in currency markets." *Review of Financial Studies*, 24(11), 3731–3777.
- Chen, Y.C., Rogoff, K.S., & Rossi, B. (2010). "Can exchange rates forecast commodity prices?" *Quarterly Journal of Economics*, 125(3), 1145–1194.
- Jolliffe, I.T. (2002). *Principal Component Analysis*, 2nd ed. Springer.

### Monetary Policy and Inflation
- Coibion, O. & Gorodnichenko, Y. (2015). "Is the Phillips Curve alive and well after all?" *American Economic Journal: Macroeconomics*, 7(1), 197–232.
- Bernanke, B. (2022). "21st century monetary policy: The Federal Reserve from the Great Inflation to COVID-19." W.W. Norton.

---

## News Sources

| Outlet | Usage |
|---|---|
| CNBC Commodities Desk | Fertilizer price reporting (April 2026) |
| Reuters | European defence backlog data; Hormuz strait status |
| Al Jazeera | Iran conflict updates; ceasefire probability context |
| Financial Times | NATO defence spending commitments; European fiscal data |
| Bloomberg | Defence company consensus estimates; ETF data |
| CNN (April 2026) | Polymarket integrity reporting (cited as caveat in Slide 16) |

---

## Tool Acknowledgements

- **Anthropic Claude** — analytical framework, chart code generation, narrative drafting
- **Jupyter Notebook** — single-file deliverable (`citi_markets_2026.ipynb`)
- **Git / GitHub** — version control; repository at https://github.com/pahansenevirathne128-gif/citi-bank
- **VS Code** — development environment

---

## Data Availability Statement

All yfinance data is freely accessible via the Yahoo Finance API with no registration requirement. FRED data is freely accessible with a free API key (FRED_API_KEY). World Bank Pink Sheet data is openly licensed. Polymarket data is publicly accessible. Defence company backlog figures are from public filings (annual reports and investor presentations). Fertilizer price data is from published reporting (CNBC, IFPRI) and is not behind a paywall.

No proprietary Bloomberg terminal data was used in this analysis.
