# Installation

## From PyPI

```bash
pip install ccs-neural-engineering
```

## From source

```bash
git clone https://github.com/GanshengT/CCS-neural-engineering.git
cd CCS-neural-engineering
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Development extras

```bash
pip install -e .[dev,docs]
```

## Compatibility policy

- Python: `>=3.10`
- Compatibility is continuously checked in GitHub Actions for Python `3.10`, `3.11`, `3.12`.

## Install directly from GitHub

```bash
pip install "git+https://github.com/GanshengT/CCS-neural-engineering.git"
```

## Optional export dependency

For Plotly static export (`svg`, `pdf`, `eps`, `png`), install:

```bash
pip install kaleido
```
