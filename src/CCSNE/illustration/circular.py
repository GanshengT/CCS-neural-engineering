"""Circular-data plotting utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_phase_rose(
    df: pd.DataFrame,
    phase_col: str,
    condition_col: str = "condition",
    polarity_col: str = "polarity",
    conditions: list[str] | None = None,
    nbins: int = 36,
    palette: dict[str, str] | None = None,
    radial_limit: tuple[float, float] | None = None,
    font_size: int = 14,
    tick_font_size: int = 12,
    axis_line_width: float = 1.8,
    tick_width: float = 1.8,
    tick_len: float = 7.0,
):
    """Create rose (polar histogram) plots for circular phase data.

    Parameters:
        df:
            Input dataframe containing phase, condition, and polarity columns.
        phase_col:
            Phase angle column in radians. Values are wrapped to `[0, 2pi)`.
        condition_col:
            Condition grouping column.
        polarity_col:
            Polarity grouping column.
        conditions:
            Optional explicit condition order.
        nbins:
            Number of angular bins for histogramming.
        palette:
            Optional mapping from polarity labels to colors.
        radial_limit:
            Optional radial axis range as `(min, max)`.
        font_size:
            Title font size.
        tick_font_size:
            Tick label font size.
        axis_line_width:
            Polar spine line width.
        tick_width:
            Tick width.
        tick_len:
            Tick length.

    Returns:
        tuple[matplotlib.figure.Figure, list[matplotlib.axes.Axes]]:
            Matplotlib figure and axes list for further customization.

    Example:
        >>> import numpy as np
        >>> import pandas as pd
        >>> from CCSNE.illustration import plot_phase_rose
        >>> df = pd.DataFrame({
        ...     "condition": ["pre"] * 100 + ["post"] * 100,
        ...     "polarity": ["Positive"] * 50 + ["Negative"] * 50 + ["Positive"] * 50 + ["Negative"] * 50,
        ...     "phase": np.random.vonmises(mu=1.0, kappa=2.0, size=200),
        ... })
        >>> fig, axes = plot_phase_rose(df, phase_col="phase")
    """
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
        if radial_limit is not None:
            ax.set_ylim(*radial_limit)
        else:
            ax.set_ylim(0, max_count if max_count > 0 else 1)
        ax.set_yticks([])
        ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2])
        ax.set_xticklabels(["0", "pi/2", "pi", "3pi/2"])
        ax.spines["polar"].set_linewidth(axis_line_width)
        ax.tick_params(axis="x", width=tick_width, length=tick_len, labelsize=tick_font_size)

    fig.suptitle("Phase rose plots by condition and polarity", y=1.02, fontsize=font_size)
    fig.tight_layout()
    return fig, axes
