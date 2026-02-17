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

### Example: manuscript-style polarity plot

```python
import pandas as pd
from CCSNE.illustration import plot_rayleigh_by_polarity

res = pd.DataFrame(
    {
        "polarity": ["Positive", "Negative", "combined", "Positive", "Negative", "combined"],
        "rayleigh_stat": [5.2, 3.8, 2.9, 6.1, 4.0, 3.1],
        "rayleigh_p": [0.01, 0.03, 0.08, 0.007, 0.02, 0.07],
    }
)
fig = plot_rayleigh_by_polarity(res)
fig.show()
```

## Documentation

- Project docs: see `docs/` locally
- GitHub Pages deployment is configured via `.github/workflows/docs.yml`

## Dependency safety and compatibility

- `pyproject.toml` defines `requires-python = ">=3.10"` and minimum library versions.
- CI (`.github/workflows/ci.yml`) validates installation and imports across Python 3.10, 3.11, and 3.12.
- Keep dependency ranges in `pyproject.toml` and avoid hard pins unless needed for reproducibility.

This approach is safer than custom install-time checks and prevents breaking user installs.
