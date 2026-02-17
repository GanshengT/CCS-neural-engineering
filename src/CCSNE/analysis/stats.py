"""Statistical helpers adapted from manuscript workflows."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2, kstest, mannwhitneyu
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def perform_anova_posthoc(df: pd.DataFrame, dependent_var: str) -> tuple[pd.DataFrame, object]:
    """Run 2-way ANOVA and Tukey HSD for polarity x condition."""
    formula = f"{dependent_var} ~ C(polarity) * C(condition)"
    model = ols(formula, data=df).fit()
    anova_results = anova_lm(model, typ=2)

    if len(anova_results.index) > 1:
        err = anova_results.index[-1]
        ss_error = anova_results.loc[err, "sum_sq"]
        anova_results["eta_sq_partial"] = anova_results["sum_sq"] / (anova_results["sum_sq"] + ss_error)

    posthoc = pairwise_tukeyhsd(df[dependent_var], df["polarity"].astype(str) + " " + df["condition"].astype(str))
    return anova_results, posthoc


def circ_mardia_watson_wheeler(data: np.ndarray, group: np.ndarray) -> tuple[float, float, float]:
    """Mardia-Watson-Wheeler test for circular data across >=2 groups."""
    data = np.asarray(data)
    group = np.asarray(group)
    if len(data) != len(group):
        raise ValueError("Data and group must be the same length")

    mask = ~np.isnan(data)
    data = data[mask]
    group = group[mask]

    if len(data) == 0 or len(np.unique(group)) < 2:
        raise ValueError("No observations or less than two groups after removing missing values")

    labels, idx = np.unique(group, return_inverse=True)
    k = len(labels)
    n = len(data)

    rnd = np.random.random(size=n)
    order = np.lexsort((rnd, data))
    ranks = np.empty(n, dtype=int)
    ranks[order] = np.arange(1, n + 1)

    cr = ranks * 2 * np.pi / n
    C = np.zeros(k)
    S = np.zeros(k)
    ns = np.zeros(k)

    for i in range(k):
        m = idx == i
        ns[i] = np.sum(m)
        C[i] = np.sum(np.cos(cr[m]))
        S[i] = np.sum(np.sin(cr[m]))

    if k == 2:
        W = 2 * (n - 1) * (C[0] ** 2 + S[0] ** 2) / (ns[0] * ns[1])
        df = 2
    else:
        W = 2 * np.sum((C**2 + S**2) / ns)
        df = 2 * (k - 1)

    p_value = 1 - chi2.cdf(W, df)
    return float(W), float(p_value), float(df)


def rayleigh_statistic(angles_deg: np.ndarray) -> float:
    """Rayleigh statistic Z = n * R^2 for angles in degrees."""
    theta = np.radians(np.asarray(angles_deg))
    R = np.abs(np.mean(np.exp(1j * theta)))
    return float(len(theta) * R**2)


def rayleigh_p_value(rayleigh_stat: float) -> float:
    """Simple Rayleigh p-value approximation used in notebook."""
    return float(np.exp(-rayleigh_stat))


def uniform_test(angles_deg: np.ndarray) -> tuple[float, float]:
    """Kolmogorov-Smirnov test against Uniform(0,1) after min-max scaling."""
    angles = np.asarray(angles_deg)
    if len(angles) < 2:
        return np.nan, np.nan
    lo, hi = float(np.min(angles)), float(np.max(angles))
    rng = hi - lo
    if rng == 0:
        return np.nan, np.nan
    scaled = (angles - lo) / rng
    d, p = kstest(scaled, "uniform")
    return float(d), float(p)


def cohen_d(x: np.ndarray, y: np.ndarray) -> float:
    """Cohen's d for two independent samples."""
    x = np.asarray(x)
    y = np.asarray(y)
    nx, ny = len(x), len(y)
    pooled_sd = np.sqrt(((nx - 1) * x.std(ddof=1) ** 2 + (ny - 1) * y.std(ddof=1) ** 2) / (nx + ny - 2))
    return float((x.mean() - y.mean()) / pooled_sd)


def cliff_delta(x: np.ndarray, y: np.ndarray) -> float:
    """Cliff's delta effect size for independent samples."""
    x = np.asarray(x)
    y = np.asarray(y)
    n1, n2 = len(x), len(y)
    u, _ = mannwhitneyu(x, y, alternative="two-sided")
    return float((2 * u) / (n1 * n2) - 1)
