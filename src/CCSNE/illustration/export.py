"""Figure export helpers.

Saving is always explicit: no plot function writes files unless you call these helpers.
"""

from __future__ import annotations

from pathlib import Path


def save_plotly_figure(fig, path: str, fmt: str | None = None, width: int | None = None, height: int | None = None, scale: float = 2.0) -> Path:
    """Save a Plotly figure to vector/raster file.

    Requires the `kaleido` package for static image export.

    Parameters:
        fig: Plotly figure object.
        path: Output file path, e.g. `figures/polarity.svg`.
        fmt: Optional format override (`svg`, `pdf`, `eps`, `png`, ...).
        width: Optional output width in pixels.
        height: Optional output height in pixels.
        scale: Export scale multiplier.

    Returns:
        pathlib.Path: Saved file path.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    figure_format = (fmt or out.suffix.lstrip(".") or "svg").lower()
    fig.write_image(str(out), format=figure_format, width=width, height=height, scale=scale)
    return out


def save_matplotlib_figure(fig, path: str, dpi: int = 300, transparent: bool = True) -> Path:
    """Save a Matplotlib figure.

    Vector formats are inferred from extension (e.g. `.pdf`, `.eps`, `.svg`).

    Parameters:
        fig: Matplotlib figure object.
        path: Output file path.
        dpi: DPI used for raster outputs.
        transparent: Whether output background is transparent.

    Returns:
        pathlib.Path: Saved file path.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out), dpi=dpi, transparent=transparent, bbox_inches="tight")
    return out
