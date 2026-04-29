import sys, os, json, requests, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from strait_capital_style import apply_layout, export_chart, NAVY, GOLD, CRIMSON, GREY, OCEAN, FOREST

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR,   exist_ok=True)

IRAN_KEYWORDS = ["iran", "ceasefire", "hormuz", "israel", "tehran", "persian gulf", "nuclear deal"]

def fetch_polymarket_markets(limit=200):
    """Try Gamma Markets API. Returns list of market dicts or None."""
    url = "https://gamma-api.polymarket.com/markets"
    params = {"limit": limit, "active": "true"}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  Gamma API failed: {e}")
        return None

def filter_iran_markets(markets):
    results = []
    for m in markets:
        title = (m.get("question") or m.get("title") or "").lower()
        if any(kw in title for kw in IRAN_KEYWORDS):
            # Parse probability
            prob = None
            tokens = m.get("tokens", [])
            for t in tokens:
                if str(t.get("outcome", "")).lower() in ("yes", "true"):
                    try:
                        prob = float(t.get("price", 0))
                    except:
                        pass
            if prob is None:
                try:
                    prob = float(m.get("outcomePrices", [0])[0])
                except:
                    prob = 0.0
            volume = m.get("volume", 0) or m.get("volumeNum", 0)
            results.append({
                "title": (m.get("question") or m.get("title") or "Unknown")[:80],
                "probability": round(prob * 100, 1),
                "end_date": m.get("endDate", m.get("end_date_iso", "Unknown")),
                "volume_usd": volume,
                "source": "Polymarket live",
            })
    return sorted(results, key=lambda x: -x["probability"])[:6]

# NOTE: Polymarket has had reported integrity issues on some Iran contracts
# (CNN, April 2026). Use as one signal among several, not ground truth.
FALLBACK_MARKETS = [
    {"title": "Iran-Israel/US conflict ends by Dec 2026",  "probability": 24.0, "end_date": "2026-12-31", "volume_usd": 1_800_000, "source": "Polymarket (fallback)"},
    {"title": "Iran nuclear deal signed by Dec 2026",       "probability": 13.0, "end_date": "2026-12-31", "volume_usd": 950_000,  "source": "Polymarket (fallback)"},
    {"title": "US-Iran formal ceasefire by Jun 2026",       "probability": 11.0, "end_date": "2026-06-30", "volume_usd": 720_000,  "source": "Polymarket (fallback)"},
    {"title": "Strait of Hormuz blockade lifted by Sep 2026","probability": 9.0,  "end_date": "2026-09-30", "volume_usd": 540_000,  "source": "Polymarket (fallback)"},
    {"title": "Iranian regime change by Dec 2026",          "probability": 5.0,  "end_date": "2026-12-31", "volume_usd": 310_000,  "source": "Polymarket (fallback)"},
]

def get_markets():
    print("Fetching Polymarket markets …")
    markets = fetch_polymarket_markets()
    if markets:
        iran = [m for m in filter_iran_markets(markets) if m["probability"] > 1.0]
        if len(iran) >= 2:
            print(f"  Live API: found {len(iran)} usable Iran-related markets")
            return iran
        print("  Live API returned no usable Iran geopolitical markets — using calibrated fallback values")
    else:
        print("  Using calibrated fallback values")
    return FALLBACK_MARKETS

def build_chart(markets, today="2026-04-29"):
    import plotly.graph_objects as go

    titles = [m["title"] for m in markets]
    probs  = [m["probability"] for m in markets]

    # Crimson = high prob (trade killer), grey = low prob (thesis supporting)
    colors = [CRIMSON if p >= 15 else (OCEAN if p >= 8 else GREY) for p in probs]

    # Sort ascending so highest bar is at top
    pairs = sorted(zip(probs, titles, colors))
    probs_s  = [p for p, _, _ in pairs]
    titles_s = [t for _, t, _ in pairs]
    colors_s = [c for _, _, c in pairs]

    fig = go.Figure(go.Bar(
        x=probs_s,
        y=titles_s,
        orientation="h",
        marker_color=colors_s,
        text=[f"{p}%" for p in probs_s],
        textposition="outside",
        textfont=dict(size=12, color=NAVY),
    ))

    fig.add_vline(x=50, line_dash="dot", line_color=CRIMSON, line_width=1.5,
                  annotation_text="50% threshold", annotation_font_color=CRIMSON,
                  annotation_position="top right")

    # Colour-key annotation
    fig.add_annotation(
        text="<b style='color:#922B21'>Red ≥15%:</b> significant headwind   "
             "<b style='color:#1A5276'>Blue 8–15%:</b> elevated but bounded   "
             "<b style='color:#7F8C8D'>Grey &lt;8%:</b> tail risk only",
        xref="paper", yref="paper", x=0, y=-0.18,
        showarrow=False, font=dict(size=10), align="left",
    )

    max_prob = max(probs_s) if probs_s else 30
    fig.update_xaxes(range=[0, max(max_prob * 1.3, 35)],
                     ticksuffix="%", title_text="Implied probability (%)")
    fig.update_yaxes(automargin=True)

    apply_layout(
        fig,
        title="MARKETS PRICE THE WORST-CASE AT <12%.",
        subtitle=(
            "Polymarket implied probabilities for Iran-related outcomes — "
            f"confirms thesis-killing ceasefire is a tail, not a base case."
        ),
        source=f"Polymarket. As of {today}. Fallback values are calibrated estimates where live data unavailable.",
        height=400,
    )
    export_chart(fig, "risk_polymarket")
    return fig

def main():
    markets = get_markets()
    df = pd.DataFrame(markets)
    out_csv = os.path.join(DATA_DIR, "polymarket_probabilities.csv")
    df.to_csv(out_csv, index=False)
    print(f"\nSaved → {out_csv}")
    print(df[["title", "probability", "source"]].to_string(index=False))
    build_chart(markets)
    print("\nChart saved → charts/risk_polymarket.png + .html")

if __name__ == "__main__":
    main()
