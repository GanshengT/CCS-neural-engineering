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
