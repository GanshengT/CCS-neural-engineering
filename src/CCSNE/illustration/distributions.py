"""Distribution plots for categorical or binary grouped data."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

COLOR_POSITIVE_RGB = "rgb(154,46,55)"
COLOR_NEGATIVE_RGB = "rgb(50,107,156)"
DEFAULT_PALETTE = {"Positive": COLOR_POSITIVE_RGB, "Negative": COLOR_NEGATIVE_RGB, "combined": "lightgrey"}
PRESET_COLOR_MAPS = {
    "ccs": ["rgb(154,46,55)", "rgb(50,107,156)", "rgb(120,120,120)", "rgb(204,153,0)", "rgb(68,68,68)"],
    "plotly": ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"],
    "viridis": ["#440154", "#3B528B", "#21918C", "#5EC962", "#FDE725"],
    "plasma": ["#0D0887", "#7E03A8", "#CC4778", "#F89540", "#F0F921"],
}


def _resolve_colors(
    categories: list[str],
    palette: dict[str, str] | None,
    color_sequence: list[str] | None,
    colormap: str,
) -> dict[str, str]:
    if palette is not None:
        missing = [c for c in categories if c not in palette]
        if missing:
            raise ValueError(f"Palette is missing categories: {missing}")
        return {c: palette[c] for c in categories}

    if color_sequence is not None:
        if len(color_sequence) < len(categories):
            raise ValueError("color_sequence must have at least as many colors as categories")
        return {c: color_sequence[i] for i, c in enumerate(categories)}

    cmap = PRESET_COLOR_MAPS.get(colormap.lower())
    if cmap is None:
        raise ValueError(f"Unknown colormap '{colormap}'. Choose from: {list(PRESET_COLOR_MAPS)}")
    return {c: cmap[i % len(cmap)] for i, c in enumerate(categories)}


def plot_distribution_by_category(
    df: pd.DataFrame,
    value_col: str,
    category_col: str,
    categories: list[str] | None = None,
    palette: dict[str, str] | None = None,
    color_sequence: list[str] | None = None,
    colormap: str = "ccs",
    summary: str = "median",
    show_points: bool = True,
    show_annotations: bool = True,
    annotate_format: str = "n={n}, {summary}={center:.2f}, sd={sd:.2f}",
    title: str | None = None,
    x_title: str | None = None,
    y_title: str | None = None,
    jitter: float = 0.03,
    point_opacity: float = 0.15,
    violin_opacity: float = 0.5,
) -> go.Figure:
    """Generic half-violin distribution plot for arbitrary categories."""
    if categories is None:
        categories = [str(c) for c in df[category_col].dropna().unique().tolist()]
    x_map = {cat: i for i, cat in enumerate(categories)}
    colors = _resolve_colors(categories, palette=palette, color_sequence=color_sequence, colormap=colormap)

    if summary not in {"mean", "median"}:
        raise ValueError("summary must be either 'mean' or 'median'")

    fig = go.Figure()
    for cat in categories:
        dcat = df[df[category_col] == cat]
        if dcat.empty:
            continue
        yvals = dcat[value_col].dropna()
        if yvals.empty:
            continue

        x0 = x_map[cat]
        color = colors[cat]
        fig.add_trace(
            go.Violin(
                x=[x0] * len(yvals),
                y=yvals,
                legendgroup=cat,
                scalegroup=cat,
                name=str(cat),
                side="negative",
                width=0.6,
                points=False,
                line=dict(width=0),
                fillcolor=color,
                opacity=violin_opacity,
            )
        )

        if show_points:
            xs = np.random.normal(loc=x0 + 0.1, scale=jitter, size=len(yvals))
            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=yvals,
                    mode="markers",
                    marker=dict(color=color, size=6, opacity=point_opacity),
                    showlegend=False,
                    hoverinfo="y",
                )
            )

        center = float(yvals.median() if summary == "median" else yvals.mean())
        sd = float(yvals.std(ddof=1)) if len(yvals) > 1 else 0.0
        fig.add_trace(
            go.Scatter(
                x=[x0 + 0.1],
                y=[center],
                error_y=dict(type="data", array=[sd], visible=True),
                mode="markers",
                marker=dict(color=color, size=14),
                showlegend=False,
            )
        )

        if show_annotations:
            y_anchor = float(yvals.max())
            txt = annotate_format.format(n=len(yvals), summary=summary, center=center, sd=sd)
            fig.add_annotation(
                x=x0,
                y=y_anchor,
                text=txt,
                showarrow=False,
                yshift=18,
                font=dict(size=10, color=color),
            )

    y = df[value_col].dropna()
    y_min = float(y.min() - 0.1) if not y.empty else -1.0
    y_max = float(y.max() + 0.1) if not y.empty else 1.0
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=list(x_map.values()),
            ticktext=[str(c) for c in categories],
            title=x_title or category_col,
        ),
        yaxis=dict(title=y_title or value_col, range=(y_min, y_max)),
        title=title or f"Distribution of {value_col} by {category_col}",
        width=760,
        height=520,
        template="simple_white",
        legend_title=category_col,
    )
    return fig


def plot_rayleigh_by_polarity(
    res: pd.DataFrame,
    value_col: str = "rayleigh_stat",
    p_col: str = "rayleigh_p",
    polarity_col: str = "polarity",
    title: str = "Saccade-angle clustering by Polarity",
    palette: dict[str, str] | None = None,
    color_sequence: list[str] | None = None,
    colormap: str = "ccs",
    show_annotations: bool = True,
) -> go.Figure:
    """Back-compatible wrapper specialized to Positive/Negative/combined polarity labels."""
    categories = ["Positive", "Negative", "combined"]
    fig = plot_distribution_by_category(
        df=res,
        value_col=value_col,
        category_col=polarity_col,
        categories=categories,
        palette=palette if palette is not None else DEFAULT_PALETTE,
        color_sequence=color_sequence,
        colormap=colormap,
        summary="median",
        show_points=True,
        show_annotations=show_annotations,
        title=title,
        x_title="Polarity",
        y_title=value_col,
        point_opacity=0.12,
        violin_opacity=0.5,
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

            jitter_vals = np.random.uniform(-0.1, 0.1, size=len(yvals))
            fig.add_trace(
                go.Scatter(
                    x=x_base + 0.4 + jitter_vals,
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
