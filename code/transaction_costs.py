"""
transaction_costs.py — Round-trip transaction cost audit for Strait Capital portfolio.

Cost schedule (case brief):
  DM Equities: 20 bps  |  EM Equities: 50 bps
  FI G10: 25 bps       |  FI Other: 60 bps
  FX G10: 5 bps        |  FX Other: 30 bps
  Commodities: 20 bps

Costs charged on entry AND exit (round trip = 2x one-way).
Run standalone: python code/transaction_costs.py
"""
import pandas as pd, sys
from pathlib import Path

NAV = 500  # $M

COST_RATES = {
    'DM_equity': 20, 'EM_equity': 50,
    'FI_G10': 25,    'FI_other': 60,
    'FX_G10': 5,     'FX_other': 30,
    'commodities': 20,
}

POSITIONS = [
    ('Long fertilizer producers (CF/NTR/MOS/ICL)',        55, 'DM_equity'),
    ('Long ag equipment (DE/AGCO/CNHI)',                   18, 'DM_equity'),
    ('Long EU defence primes (RHM/BAE/LDO/HO/SAAB)',      50, 'DM_equity'),
    ('Long defence suppliers (ESLT/KTOS/HII)',             18, 'DM_equity'),
    ('Long US energy majors (XOM/CVX/COP)',                40, 'DM_equity'),
    ('Long gold miners (NEM/AEM/FNV)',                     30, 'DM_equity'),
    ('Long ASX defence (ASB/EOS/DRO)',                      8, 'DM_equity'),
    ('Long Brazil equities (PBR/VALE/ITUB)',               15, 'EM_equity'),
    ('Long Mexico equities (WALMEX/FEMSA)',                 8, 'EM_equity'),
    ('Long EM ex-Asia basket',                              6, 'EM_equity'),
    ('Short packaged food (KHC/GIS/CPB/UN)',               28, 'DM_equity'),
    ('Short EU autos (VOW/STLA/BMW/MBG)',                  22, 'DM_equity'),
    ('Short airlines (LHA/AF/RYA/DAL)',                    20, 'DM_equity'),
    ('Short Asian manufacturers',                          14, 'DM_equity'),
    ('Short US consumer cyclicals',                         6, 'DM_equity'),
    ('Long TIPS 5Y belly',                                 50, 'FI_G10'),
    ('Long 2Y UST (curve steepener)',                      40, 'FI_G10'),
    ('Short 10Y UST (curve steepener)',                    30, 'FI_G10'),
    ('Long Chinese Govt Bonds',                            20, 'FI_other'),
    ('Long Brazilian local-currency debt',                 15, 'FI_other'),
    ('Long AUD/USD',                                       18, 'FX_G10'),
    ('Long CAD/USD',                                       15, 'FX_G10'),
    ('Long NOK/SEK',                                        8, 'FX_G10'),
    ('Long EUR/USD',                                        7, 'FX_G10'),
    ('Long AUD/JPY',                                       12, 'FX_G10'),
    ('Long CHF/JPY',                                        8, 'FX_G10'),
    ('Long BRL/USD',                                       15, 'FX_other'),
    ('Long MXN/USD',                                       12, 'FX_other'),
    ('Short KRW/USD',                                      22, 'FX_other'),
    ('Short TWD/USD',                                      18, 'FX_other'),
    ('Short INR/USD',                                      12, 'FX_other'),
    ('Short CNH/USD',                                       8, 'FX_other'),
    ('Long Brent crude futures',                           30, 'commodities'),
    ('Long Gold',                                          30, 'commodities'),
    ('Long corn futures',                                  12, 'commodities'),
    ('Long wheat futures',                                 10, 'commodities'),
    ('Long soybean futures',                                5, 'commodities'),
    ('Long natural gas',                                   15, 'commodities'),
    ('Long copper',                                         5, 'commodities'),
]


def compute(positions=POSITIONS, nav=NAV):
    df = pd.DataFrame(positions, columns=['Position', 'Notional_USDmm', 'Bucket'])
    df['Cost_bps_1way']   = df['Bucket'].map(COST_RATES)
    df['Cost_USDmm_1way'] = df['Notional_USDmm'] * df['Cost_bps_1way'] / 10000
    df['Cost_USDmm_RT']   = df['Cost_USDmm_1way'] * 2
    df['Cost_bps_of_NAV'] = df['Cost_USDmm_RT'] / nav * 10000
    return df


if __name__ == '__main__':
    df = compute()
    total_rt  = df['Cost_USDmm_RT'].sum()
    total_bps = total_rt / NAV * 10000
    gross     = df['Notional_USDmm'].sum()

    print('=' * 75)
    print('STRAIT CAPITAL — TRANSACTION COST AUDIT')
    print('=' * 75)
    print(f'Portfolio NAV: ${NAV}M  |  Gross notional: ${gross:.0f}M')
    print(f'Round-trip cost: ${total_rt:.2f}M  ({total_bps:.1f} bps of NAV)')
    print()

    summary = df.groupby('Bucket').agg(
        Notional=('Notional_USDmm', 'sum'),
        RT_Cost_USDmm=('Cost_USDmm_RT', 'sum')
    ).round(2)
    summary['bps_of_NAV'] = (summary['RT_Cost_USDmm'] / NAV * 10000).round(1)
    print(summary.to_string())
    print()
    print('Alpha waterfall:')
    print(f'  Gross scenario-weighted alpha:    +574 bps')
    print(f'  Less hedge book cost:              -80 bps')
    print(f'  Less round-trip transaction costs: -{total_bps:.0f} bps')
    print(f'  NET ALPHA:                        +{574 - 80 - total_bps:.0f} bps')

    out = Path('data') / 'transaction_costs.csv'
    df.to_csv(out, index=False)
    print(f'\nSaved {out}')
