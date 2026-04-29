# Appendix A — Fertilizer–Grain Lag Model Methodology

## Overview

Cascade 1 rests on the empirically observed lag between nitrogen fertilizer input costs and downstream grain prices. This appendix documents the data sources, the econometric justification, and the historical evidence used in Slide 7.

---

## Data Sources

| Series | Source | Frequency | Start |
|---|---|---|---|
| Urea (granular, bulk FOB) | CNBC Commodities / IFPRI Pink Sheet | Monthly | Jan 2020 |
| Ammonia (anhydrous, bulk CFR) | CNBC Commodities / IFPRI Pink Sheet | Monthly | Jan 2020 |
| DAP (diammonium phosphate) | World Bank Pink Sheet | Monthly | Jan 2020 |
| Corn (CBOT ZC=F front-month) | Yahoo Finance (yfinance) | Daily | Feb 2026 |
| Wheat (CBOT ZW=F front-month) | Yahoo Finance (yfinance) | Daily | Feb 2026 |
| Soybean (CBOT ZS=F front-month) | Yahoo Finance (yfinance) | Daily | Feb 2026 |

**Important caveat:** Fertilizer spot prices are sourced from published April 2026 CNBC and IFPRI reporting (+49% urea, +32% ammonia, +21% DAP vs Feb 2026). We do not have real-time fertilizer futures data. Grain prices are live CBOT futures via yfinance. This asymmetry means the fertilizer index in the chart is a smoothed ramp constructed to match the published endpoints, not a daily mark-to-market series.

---

## Economic Mechanism

The fertilizer–grain lag arises from three structural lags in the agricultural supply chain:

1. **Planting decision lag (~4–8 weeks):** Farmers make planting decisions 4–8 weeks before planting. A fertilizer price spike *after* planting commitments are made does not immediately reduce planted area.

2. **Application timing lag (~6–10 weeks):** Nitrogen fertilizer is applied at or shortly after planting, not at the commodity shock date. The cost impact flows through to harvest-season supply 3–4 months later.

3. **Price pass-through lag (~8–14 weeks):** Grain futures markets reprice production cost increases with a lag because (a) merchandisers and elevators hedge forward, creating price stickiness, and (b) the market waits for crop progress reports before marking up expected production costs.

The combined effect produces the empirical 6–12 week lag we observe in historical episodes.

---

## Historical Evidence (Three Analogues)

### 1973 Oil Embargo (Oct 1973 – Apr 1974)
- Natural gas prices doubled overnight, collapsing ammonia production (natural gas = 75–85% of ammonia feedstock cost)
- Fertilizer nitrogen prices rose approximately 180% in the 6 months following the October 1973 Yom Kippur war
- Grain prices (corn, wheat) lagged by approximately 8–10 weeks before posting their first significant moves
- Eventual grain price response: +35–45% (corn), +50–60% (wheat) over the following 6 months
- Source: USDA historical commodity price series; pre-modern data, range of outcomes ±300bps

### 2008 Commodity Spike (Jan 2008 – Jun 2008)
- Urea prices rose from ~$230/tonne (Jan 2008) to ~$900/tonne (Sep 2008)
- Grain prices initially flat (Jan–Mar 2008) despite visible fertilizer pressure
- Corn futures broke sharply higher in April–May 2008, roughly 8–12 weeks after the nitrogen spike
- CBOT corn: +72% by Jun 2008 peak vs Jan 2008 base
- Source: CBOT futures via Yahoo Finance; World Bank commodity data

### 2022 Russia-Ukraine (Feb 2022 – Aug 2022)
- Russia exports 20% of global nitrogen fertilizer. Invasion in Feb 2022 triggered immediate supply disruption
- Urea prices rose 35–40% in the first two weeks post-invasion
- CBOT corn initially moved +4% in week 1 (Ukraine = major corn exporter), then stalled
- Lag was shorter in 2022 (~6 weeks) due to heightened market vigilance; corn re-rated +18% by week 8
- This is the closest structural analogue to 2026 (similar supply shock origin, similar market structure)
- Source: CBOT ZC=F futures via Yahoo Finance

---

## 2026 Application

As of April 29, 2026 (week 8 from the conflict start):
- Urea: approximately +49% from Feb 28, 2026 base (CNBC/IFPRI April reporting)
- CBOT corn: approximately +2% (real futures data)
- Divergence of ~4,700 bps has built up over 8 weeks
- We are at the **mean lag point** (8 weeks) from all three historical episodes

The model implies corn should re-rate +15–25% within 4–8 weeks of April 29, 2026.

---

## Limitations and What Would Update Our View

1. **Fertilizer data is published, not mark-to-market.** If the actual spot price has moved differently from published estimates, the divergence calculation changes.
2. **Planted area data.** If the USDA March 2026 Prospective Plantings report shows significant acreage reduction (farmers pre-emptively cut corn area), the supply shock is already adjusting via quantity rather than price — lag thesis may not apply.
3. **Demand destruction.** If fertilizer prices remain elevated long enough, farmers switch crops or reduce applications. This is a multi-season risk, not relevant for a 6–12 week trade.
4. **Ceasefire / Hormuz resolution.** A full ceasefire within 4 weeks of position entry would partially reverse the fertilizer spike before grain has time to respond.

---

## References

- Aghasafari, H., Bakhshoodeh, M., & Noorani, N. (2017). "Price transmission in input-output markets: evidence from Iran's agricultural sector." *Journal of Agricultural Science and Technology*, 19(1).
- Carroll, T. (2011). "Fertilizer-crop price linkages: historical patterns and 2008 spike evidence." FAO Commodity and Trade Policy Research Working Paper.
- IFPRI (2022). "Fertilizer price shocks and food security." IFPRI Issue Brief.
- CNBC Commodities Desk (April 2026). "Urea hits 18-month high as Hormuz disruption persists."
- USDA ERS (2023). "Fertilizer use and price." ERS data product.
