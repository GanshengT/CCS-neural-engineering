"""Polarity plotting utilities inspired by Fig4 workflows."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

COLOR_POSITIVE_RGB = "rgb(154,46,55)"
COLOR_NEGATIVE_RGB = "rgb(50,107,156)"
DEFAULT_PALETTE = {"Positive": COLOR_POSITIVE_RGB, "Negative": COLOR_NEGATIVE_RGB, "combined": "lightgrey"}


def plot_rayleigh_by_polarity(
    res: pd.DataFrame,
    value_col: str = "rayleigh_stat",
    p_col: str = "rayleigh_p",
    polarity_col: str = "polarity",
    title: str = "Saccade-angle clustering by Polarity",
) -> go.Figure:
    """Replicate manuscript half-violin + jitter + median±SD style."""
    x_map = {"Positive": 0, "Negative": 1, "combined": 2}
    draw_order = ["Positive", "Negative", "combined"]

    fig = go.Figure()
    for pol in draw_order:
        dfp = res[res[polarity_col] == pol]
        if dfp.empty:
            continue

        color = DEFAULT_PALETTE[pol]
        x0 = x_map[pol]

        fig.add_trace(
            go.Violin(
                x=[x0] * len(dfp),
                y=dfp[value_col],
                legendgroup=pol,
                scalegroup=pol,
                name=f"{pol} violin",
                side="negative",
                width=0.6,
                points=False,
                line=dict(width=0),
                fillcolor=color,
                opacity=0.5,
                spanmode="hard",
                span=[0, 15],
            )
        )

        xs = np.random.normal(loc=x0 + 0.1, scale=0.03, size=len(dfp))
        marker_opacity = 0.02 if pol == "Positive" else 0.2
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=dfp[value_col],
                mode="markers",
                marker=dict(color=color, size=6, opacity=marker_opacity),
                name=f"{pol} points",
                showlegend=False,
            )
        )

        med = dfp[value_col].median()
        sd = dfp[value_col].std(ddof=1)
        fig.add_trace(
            go.Scatter(
                x=[x0 + 0.1],
                y=[med],
                error_y=dict(type="data", array=[sd], visible=True),
                mode="markers",
                marker=dict(color=color, size=14),
                name=f"{pol} median±SD",
                showlegend=False,
            )
        )

    y_min = min(-1.0, float(res[value_col].min()) - 0.1)
    y_max = max(10.0, float(res[value_col].max()) + 0.1)
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1, 2],
            ticktext=["Positive", "Negative", "Combined"],
            title="Polarity",
        ),
        yaxis=dict(title=value_col, range=(y_min, y_max)),
        title=title,
        width=700,
        height=500,
        template="simple_white",
    )
    return fig


def plot_polarity_violin(
    df: pd.DataFrame,
    value_col: str,
    condition_col: str = "condition",
    polarity_col: str = "polarity",
    conditions: list[str] | None = None,
    palette: dict[str, str] | None = None,
) -> go.Figure:
    """Create split violin + mean/std overlays per condition and polarity."""
    palette = palette or {"Positive": COLOR_POSITIVE_RGB, "Negative": COLOR_NEGATIVE_RGB}
    if conditions is None:
        conditions = list(df[condition_col].dropna().unique())

    stats = (
        df.groupby([condition_col, polarity_col])[value_col]
        .agg(["mean", "std"])
        .reset_index()
    )

    fig = go.Figure()
    x_base = 0.0
    for i, cond in enumerate(conditions):
        for pol in ["Positive", "Negative"]:
            yvals = df.loc[(df[condition_col] == cond) & (df[polarity_col] == pol), value_col].dropna()
            if yvals.empty:
                x_base += 1.1
                continue

            fig.add_trace(
                go.Violin(
                    x=[x_base] * len(yvals),
                    y=yvals,
                    name=pol,
                    legendgroup=pol,
                    scalegroup=pol,
                    side="negative",
                    width=0.7,
                    points=False,
                    line=dict(color=palette[pol], width=0),
                    fillcolor=palette[pol],
                    opacity=0.4,
                    showlegend=(i == 0),
                )
            )

            jitter = np.random.uniform(-0.1, 0.1, size=len(yvals))
            fig.add_trace(
                go.Scatter(
                    x=x_base + 0.4 + jitter,
                    y=yvals,
                    mode="markers",
                    marker=dict(size=4, color=palette[pol], opacity=0.15),
                    legendgroup=pol,
                    showlegend=False,
                    hoverinfo="y",
                )
            )

            row = stats[(stats[condition_col] == cond) & (stats[polarity_col] == pol)]
            mean = row["mean"].iloc[0]
            std = row["std"].iloc[0]
            fig.add_trace(
                go.Scatter(
                    x=[x_base + 0.4],
                    y=[mean],
                    mode="markers",
                    marker=dict(symbol="circle", size=12, color=palette[pol], line=dict(width=1, color="black")),
                    error_y=dict(type="data", array=[std], thickness=1.5, width=6, color=palette[pol]),
                    showlegend=False,
                )
            )
            x_base += 1.1
        x_base += 1.5

    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=list(range(len(conditions))), ticktext=conditions, title="Condition"),
        yaxis=dict(title=value_col),
        width=920,
        height=520,
        template="simple_white",
        legend_title="Polarity",
        violingap=0,
        violingroupgap=0.5,
    )
    return fig


def plot_phase_rose(
    df: pd.DataFrame,
    phase_col: str,
    condition_col: str = "condition",
    polarity_col: str = "polarity",
    conditions: list[str] | None = None,
    nbins: int = 36,
    palette: dict[str, str] | None = None,
):
    """Create rose plots for each condition with positive/negative overlays."""
    palette = palette or {"Positive": "#9A2E37", "Negative": "#326B9C"}
    if conditions is None:
        conditions = list(df[condition_col].dropna().unique())

    phases = np.mod(df[phase_col].to_numpy(dtype=float), 2 * np.pi)
    df2 = df.copy()
    df2[phase_col] = phases

    bin_edges = np.linspace(0, 2 * np.pi, nbins + 1)
    bin_centers = bin_edges[:-1] + np.diff(bin_edges) / 2

    hist = {}
    max_count = 0
    for cond in conditions:
        hist[cond] = {}
        for pol in ["Positive", "Negative"]:
            vals = df2.loc[(df2[condition_col] == cond) & (df2[polarity_col] == pol), phase_col].dropna().to_numpy()
            cnt, _ = np.histogram(vals, bins=bin_edges)
            hist[cond][pol] = cnt
            max_count = max(max_count, int(cnt.max()) if cnt.size else 0)

    fig, axes = plt.subplots(1, len(conditions), subplot_kw={"projection": "polar"}, figsize=(3.2 * len(conditions), 3.2))
    if len(conditions) == 1:
        axes = [axes]

    for ax, cond in zip(axes, conditions):
        for pol in ["Positive", "Negative"]:
            ax.bar(
                bin_centers,
                hist[cond][pol],
                width=2 * np.pi / nbins,
                bottom=0,
                color=palette[pol],
                alpha=0.4,
                edgecolor=None,
            )
        ax.set_title(cond, pad=10)
        ax.set_ylim(0, max_count if max_count > 0 else 1)
        ax.set_yticks([])
        ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2])
        ax.set_xticklabels(["0", "pi/2", "pi", "3pi/2"])

    fig.suptitle("Phase rose plots by condition and polarity", y=1.02)
    fig.tight_layout()
    return fig, axes
