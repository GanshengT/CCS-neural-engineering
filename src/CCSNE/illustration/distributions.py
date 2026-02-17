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
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
    font_size: int = 16,
    tick_font_size: int = 13,
    axis_line_width: float = 2.0,
    tick_width: float = 2.0,
    tick_len: float = 8.0,
    jitter: float = 0.03,
    point_opacity: float = 0.15,
    violin_opacity: float = 0.5,
) -> go.Figure:
    """Plot category-wise distributions using half-violin, points, and summary markers.

    Parameters:
        df:
            Long-format dataframe containing at least `value_col` and `category_col`.
        value_col:
            Numeric column to visualize on the y-axis.
        category_col:
            Column defining groups (binary or multi-category).
        categories:
            Optional explicit category order. If `None`, order follows dataframe appearance.
        palette:
            Optional explicit color mapping, e.g. `{"A": "#1f77b4", "B": "#ff7f0e"}`.
        color_sequence:
            Optional list of colors aligned with `categories`.
        colormap:
            Preset color map when `palette` and `color_sequence` are not provided.
            Available: `ccs`, `plotly`, `viridis`, `plasma`.
        summary:
            Summary marker center. One of: `median`, `mean`.
        show_points:
            Whether to draw jittered raw points.
        show_annotations:
            Whether to add text annotation per category.
        annotate_format:
            Annotation template. Supports fields: `{n}`, `{summary}`, `{center}`, `{sd}`.
        title:
            Optional figure title override.
        x_title:
            Optional x-axis title override.
        y_title:
            Optional y-axis title override.
        x_range:
            Optional x-axis numeric range as `(min, max)`.
        y_range:
            Optional y-axis numeric range as `(min, max)`.
        font_size:
            Base font size for labels and title.
        tick_font_size:
            Tick label font size.
        axis_line_width:
            X/Y axis line width.
        tick_width:
            X/Y tick width.
        tick_len:
            X/Y tick length.
        jitter:
            Horizontal jitter scale for points.
        point_opacity:
            Opacity for point layer.
        violin_opacity:
            Opacity for violin layer.

    Returns:
        plotly.graph_objects.Figure:
            Configured interactive Plotly figure.

    Example:
        >>> import pandas as pd
        >>> from CCSNE.illustration import plot_distribution_by_category
        >>> df = pd.DataFrame({"group": ["A", "A", "B", "B"], "value": [1.2, 1.5, 0.9, 1.0]})
        >>> fig = plot_distribution_by_category(df, value_col="value", category_col="group", colormap="viridis")
        >>> fig.show()
    """
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
        font=dict(size=font_size),
        xaxis=dict(
            tickmode="array",
            tickvals=list(x_map.values()),
            ticktext=[str(c) for c in categories],
            title=x_title or category_col,
            range=x_range,
            showline=True,
            linewidth=axis_line_width,
            ticks="outside",
            tickwidth=tick_width,
            ticklen=tick_len,
            tickfont=dict(size=tick_font_size),
        ),
        yaxis=dict(
            title=y_title or value_col,
            range=y_range if y_range is not None else (y_min, y_max),
            showline=True,
            linewidth=axis_line_width,
            ticks="outside",
            tickwidth=tick_width,
            ticklen=tick_len,
            tickfont=dict(size=tick_font_size),
        ),
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
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
    font_size: int = 16,
    tick_font_size: int = 13,
    axis_line_width: float = 2.0,
    tick_width: float = 2.0,
    tick_len: float = 8.0,
) -> go.Figure:
    """Wrapper for manuscript-style polarity distributions.

    Parameters:
        res:
            Input dataframe with polarity labels and a Rayleigh-like statistic column.
        value_col:
            Numeric statistic column to display.
        p_col:
            Reserved for compatibility with previous code paths.
        polarity_col:
            Column containing labels such as `Positive`, `Negative`, `combined`.
        title:
            Plot title.
        palette:
            Optional explicit category-color mapping.
        color_sequence:
            Optional explicit ordered list of colors.
        colormap:
            Preset colormap name when explicit colors are not provided.
        show_annotations:
            Whether to annotate each category with summary text.
        x_range:
            Optional x-axis range override.
        y_range:
            Optional y-axis range override.
        font_size:
            Base font size for labels and title.
        tick_font_size:
            Tick label font size.
        axis_line_width:
            X/Y axis line width.
        tick_width:
            X/Y tick width.
        tick_len:
            X/Y tick length.

    Returns:
        plotly.graph_objects.Figure:
            Interactive figure.

    Example:
        >>> import pandas as pd
        >>> from CCSNE.illustration import plot_rayleigh_by_polarity
        >>> res = pd.DataFrame({
        ...     "polarity": ["Positive", "Negative", "combined"] * 3,
        ...     "rayleigh_stat": [5.2, 3.7, 2.9, 4.8, 3.5, 2.7, 5.1, 3.8, 3.0],
        ... })
        >>> fig = plot_rayleigh_by_polarity(res)
        >>> fig.show()
    """
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
        x_range=x_range,
        y_range=y_range,
        font_size=font_size,
        tick_font_size=tick_font_size,
        axis_line_width=axis_line_width,
        tick_width=tick_width,
        tick_len=tick_len,
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
    x_range: tuple[float, float] | None = None,
    y_range: tuple[float, float] | None = None,
    font_size: int = 16,
    tick_font_size: int = 13,
    axis_line_width: float = 2.0,
    tick_width: float = 2.0,
    tick_len: float = 8.0,
) -> go.Figure:
    """Plot condition-wise polarity violins with mean and SD overlays.

    Parameters:
        df:
            Long-format dataframe containing condition, polarity, and value columns.
        value_col:
            Numeric value column.
        condition_col:
            Condition grouping column.
        polarity_col:
            Polarity grouping column.
        conditions:
            Optional explicit condition order.
        palette:
            Optional mapping from polarity labels to colors.
        x_range:
            Optional x-axis numeric range as `(min, max)`.
        y_range:
            Optional y-axis numeric range as `(min, max)`.
        font_size:
            Base font size for labels and title.
        tick_font_size:
            Tick label font size.
        axis_line_width:
            X/Y axis line width.
        tick_width:
            X/Y tick width.
        tick_len:
            X/Y tick length.

    Returns:
        plotly.graph_objects.Figure:
            Interactive figure.

    Example:
        >>> import pandas as pd
        >>> from CCSNE.illustration import plot_polarity_violin
        >>> df = pd.DataFrame({
        ...     "condition": ["pre", "pre", "post", "post"],
        ...     "polarity": ["Positive", "Negative", "Positive", "Negative"],
        ...     "PLV_norm": [0.2, 0.1, 0.3, 0.15],
        ... })
        >>> fig = plot_polarity_violin(df, value_col="PLV_norm")
        >>> fig.show()
    """
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
        font=dict(size=font_size),
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(conditions))),
            ticktext=conditions,
            title="Condition",
            range=x_range,
            showline=True,
            linewidth=axis_line_width,
            ticks="outside",
            tickwidth=tick_width,
            ticklen=tick_len,
            tickfont=dict(size=tick_font_size),
        ),
        yaxis=dict(
            title=value_col,
            range=y_range,
            showline=True,
            linewidth=axis_line_width,
            ticks="outside",
            tickwidth=tick_width,
            ticklen=tick_len,
            tickfont=dict(size=tick_font_size),
        ),
        width=920,
        height=520,
        template="simple_white",
        legend_title="Polarity",
        violingap=0,
        violingroupgap=0.5,
    )
    return fig
