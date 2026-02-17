# CCS Neural Engineering

Cognitive Computational Systems Neural Engineering (`CCSNE`) is a Python toolkit for scientific analysis and illustration, with an initial focus on neural time-series and polarity/phase visualization workflows.

## Install

```bash
pip install ccs-neural-engineering
```

For development (editable install):

```bash
git clone <your-repo-url>
cd CCS-neural-engineering
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quick usage

```python
import CCSNE.illustration as ill
import CCSNE.analysis as ana
```

### Example: generic category distribution plot

```python
import pandas as pd
from CCSNE.illustration import plot_distribution_by_category

df = pd.DataFrame(
    {
        "group": ["A", "B", "C", "A", "B", "C", "A", "B", "C"],
        "metric": [1.2, 0.9, 0.7, 1.4, 1.0, 0.8, 1.3, 1.1, 0.9],
    }
)
fig = plot_distribution_by_category(
    df=df,
    value_col="metric",
    category_col="group",
    colormap="viridis",
    show_annotations=True,
)
fig.show()
```

### For polarity/rayleigh style workflows

`plot_rayleigh_by_polarity(...)` remains available and now uses the generic distribution engine underneath.

## Documentation

- Project docs: see `docs/` locally
- GitHub Pages deployment is configured via `.github/workflows/docs.yml`

## Dependency safety and compatibility

- `pyproject.toml` defines `requires-python = ">=3.10"` and minimum library versions.
- CI (`.github/workflows/ci.yml`) validates installation and imports across Python 3.10, 3.11, and 3.12.
- Keep dependency ranges in `pyproject.toml` and avoid hard pins unless needed for reproducibility.

This approach is safer than custom install-time checks and prevents breaking user installs.
