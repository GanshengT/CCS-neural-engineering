"""Statistical helpers adapted from manuscript workflows."""

import pandas as pd
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
