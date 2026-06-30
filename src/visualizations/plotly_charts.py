import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

TEMPLATE = "plotly_white"
COLOR_SEQUENCE = ["#0f766e", "#d19a2a", "#2f7fa6", "#cf5f44", "#667a35"]


def _finish_figure(fig: Figure, height: int = 480) -> Figure:
    """Apply a consistent interactive dashboard style to a Plotly figure."""
    fig.update_layout(
        height=height,
        hovermode="x unified",
        margin=dict(l=18, r=22, t=68, b=24),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#16212a", family="Arial, sans-serif", size=13),
        template=TEMPLATE,
        title=dict(font=dict(size=18, color="#16212a"), x=0.02, xanchor="left"),
        hoverlabel=dict(
            bgcolor="#16212a",
            bordercolor="#16212a",
            font=dict(color="#ffffff", size=12),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(96,112,128,0.18)",
        linecolor="rgba(96,112,128,0.25)",
        zeroline=False,
        title=None,
    )
    fig.update_yaxes(
        showgrid=False,
        linecolor="rgba(96,112,128,0.18)",
        zeroline=False,
        title=None,
    )
    return fig


def horizontal_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    *,
    height: int = 500,
) -> Figure:
    """Create a sorted horizontal bar chart with hover and text labels."""
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        title=title,
        text=x,
        template=TEMPLATE,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(
        marker_color=COLOR_SEQUENCE[0],
        marker_line_color="rgba(255,255,255,0.85)",
        marker_line_width=1,
        textposition="outside",
        textfont=dict(color="#607080", size=11),
        cliponaxis=False,
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    return _finish_figure(fig, height=height)


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    *,
    height: int = 440,
) -> Figure:
    """Create an interactive line chart with markers."""
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title,
        template=TEMPLATE,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(
        line=dict(width=3, color=COLOR_SEQUENCE[0]),
        marker=dict(size=9, color=COLOR_SEQUENCE[1], line=dict(width=2, color="#ffffff")),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(96,112,128,0.16)")
    return _finish_figure(fig, height=height)


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    *,
    height: int = 440,
) -> Figure:
    """Create a donut chart for proportional distributions."""
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.45,
        title=title,
        template=TEMPLATE,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(
        marker=dict(line=dict(color="#ffffff", width=2)),
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(color="#ffffff", size=12),
    )
    fig.update_layout(showlegend=True)
    return _finish_figure(fig, height=height)
