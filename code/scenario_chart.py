import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from strait_capital_style import apply_layout, export_chart, NAVY, GOLD, FOREST, OCEAN, CRIMSON, GREY

import plotly.graph_objects as go
from plotly.subplots import make_subplots

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

# ── Scenario definitions ────────────────────────────────────────────────────
# Four macro scenarios with probability and 6-month alpha vs Fund X (bps)
SCENARIOS = [
    {
        "name": "Base Case",
        "desc": "Conflict persists. Cascades converge\nas priced. No ceasefire.",
        "prob": 0.55,
        "alpha_mid": 574,
        "alpha_lo":  280,
        "alpha_hi":  870,
        "color": OCEAN,
    },
    {
        "name": "Bull Case",
        "desc": "Fertilizer–grain lag closes fast.\nDefence re-rates >20%.",
        "prob": 0.20,
        "alpha_mid": 1_150,
        "alpha_lo":  800,
        "alpha_hi":  1_600,
        "color": FOREST,
    },
    {
        "name": "Bear Case",
        "desc": "Partial ceasefire. Oil reverses.\nCommodity sleeve takes loss.",
        "prob": 0.15,
        "alpha_mid": -320,
        "alpha_lo":  -700,
        "alpha_hi":  100,
        "color": CRIMSON,
    },
    {
        "name": "Stagflation",
        "desc": "CPI entrenches. Fed stays hawkish.\nEquity drawdown hurts benchmark.",
        "prob": 0.10,
        "alpha_mid": 420,
        "alpha_lo":  150,
        "alpha_hi":  690,
        "color": GOLD,
    },
]

# Probability-weighted expected alpha
EXP_ALPHA = sum(s["prob"] * s["alpha_mid"] for s in SCENARIOS)  # ≈ 574 bps

def build_option_b_fan():
    """Fan chart: horizontal bars showing each scenario's alpha range, ordered by probability."""
    fig = go.Figure()

    sorted_s = sorted(SCENARIOS, key=lambda s: s["prob"], reverse=True)

    for i, s in enumerate(sorted_s):
        label = f"<b>{s['name']}</b> ({int(s['prob']*100)}%)"

        # Range bar (lo → hi)
        fig.add_trace(go.Bar(
            y=[label],
            x=[s["alpha_hi"] - s["alpha_lo"]],
            base=[s["alpha_lo"]],
            orientation="h",
            marker_color=s["color"],
            marker_opacity=0.25,
            showlegend=False,
            hovertemplate=f"{s['name']}<br>Range: {s['alpha_lo']:+,} to {s['alpha_hi']:+,} bps<extra></extra>",
        ))

        # Mid-point marker
        fig.add_trace(go.Scatter(
            x=[s["alpha_mid"]],
            y=[label],
            mode="markers+text",
            marker=dict(color=s["color"], size=14, symbol="diamond"),
            text=[f"{s['alpha_mid']:+,}"],
            textposition="middle right",
            textfont=dict(size=12, color=s["color"]),
            showlegend=False,
            hovertemplate=f"{s['name']}: {s['alpha_mid']:+,} bps (mid)<extra></extra>",
        ))

        # Description annotation
        fig.add_annotation(
            x=s["alpha_lo"] - 80,
            y=label,
            text=s["desc"],
            showarrow=False,
            font=dict(size=9, color=GREY),
            xanchor="right",
            align="right",
        )

    # Expected alpha vertical line
    fig.add_vline(
        x=EXP_ALPHA,
        line_dash="dash",
        line_color=NAVY,
        line_width=2,
        annotation_text=f"<b>E[α] = {EXP_ALPHA:+,.0f} bps</b>",
        annotation_font=dict(color=NAVY, size=12),
        annotation_position="top",
    )

    # Zero line
    fig.add_vline(x=0, line_dash="dot", line_color=GREY, line_width=1)

    fig.update_xaxes(
        title_text="Portfolio alpha vs Fund X (bps, 6-month horizon)",
        tickformat="+,",
        range=[-950, 1_900],
        zeroline=False,
    )
    fig.update_yaxes(automargin=True)

    apply_layout(
        fig,
        title="ASYMMETRIC UPSIDE. CAPPED DOWNSIDE.",
        subtitle=f"Probability-weighted alpha vs Fund X = {EXP_ALPHA:+,.0f} bps. "
                 "Bear case is bounded by tail hedges.",
        source=(
            "Internal scenario analysis. Alpha estimates based on BL posterior + cascade convergence assumptions. "
            "Range = ±1σ across analogue periods."
        ),
        height=380,
    )
    export_chart(fig, "scenario_pl")
    return fig

def main():
    print("Building scenario P&L fan chart …")
    build_option_b_fan()
    print(f"\nExpected alpha (probability-weighted): {EXP_ALPHA:+,.0f} bps")
    print("Saved → charts/scenario_pl.png + .html")

if __name__ == "__main__":
    main()
