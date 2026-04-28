import matplotlib
matplotlib.use('Agg')

from pathlib import Path
import plotly.graph_objects as go

NAVY    = "#0A1628"
GOLD    = "#C9A84C"
FOREST  = "#1B4332"
OCEAN   = "#1A5276"
CRIMSON = "#922B21"
GREY    = "#7F8C8D"
COLORS  = [NAVY, GOLD, FOREST, OCEAN, CRIMSON, GREY]


def apply_layout(fig, title, subtitle="", source="", width=1050, height=560):
    annotations = []

    annotations.append(dict(
        text=f"<b>{title}</b>",
        xref="paper", yref="paper",
        x=0.0, y=1.13,
        xanchor="left", yanchor="top",
        font=dict(family="Helvetica Neue, Arial, sans-serif", size=18, color=NAVY),
        showarrow=False,
    ))

    if subtitle:
        annotations.append(dict(
            text=f"<i>{subtitle}</i>",
            xref="paper", yref="paper",
            x=0.0, y=1.06,
            xanchor="left", yanchor="top",
            font=dict(family="Helvetica Neue, Arial, sans-serif", size=12, color=GREY),
            showarrow=False,
        ))

    if source:
        annotations.append(dict(
            text=f"<i>{source}</i>",
            xref="paper", yref="paper",
            x=0.0, y=-0.13,
            xanchor="left", yanchor="top",
            font=dict(family="Helvetica Neue, Arial, sans-serif", size=9, color=GREY),
            showarrow=False,
        ))

    fig.update_layout(
        width=width,
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=60, r=40, t=100, b=70),
        font=dict(family="Helvetica Neue, Arial, sans-serif", color=NAVY),
        annotations=annotations,
        xaxis=dict(showgrid=False, linecolor=GREY, linewidth=1, mirror=False, ticks="outside"),
        yaxis=dict(showgrid=False, linecolor=GREY, linewidth=1, mirror=False, ticks="outside"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            font=dict(size=11, color=NAVY),
        ),
    )
    return fig


def export_chart(fig, name, scale=2):
    charts_dir = Path(__file__).parent.parent / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    html_path = charts_dir / f"{name}.html"
    fig.write_html(str(html_path))
    print(f"Saved HTML: {html_path}")

    png_path = charts_dir / f"{name}.png"
    try:
        fig.write_image(str(png_path), scale=scale)
        print(f"Saved PNG:  {png_path}")
    except Exception as e:
        print(f"PNG export failed — is kaleido==0.2.1 installed? Error: {e}")
        print("Run: pip3 install 'kaleido==0.2.1' --force-reinstall")
