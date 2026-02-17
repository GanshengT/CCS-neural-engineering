import numpy as np
import pandas as pd

from CCSNE.illustration import plot_phase_rose, plot_polarity_violin, plot_rayleigh_by_polarity

rng = np.random.default_rng(7)
conditions = ["pre_pre_pre_pre", "pre_pre_pre", "pre_pre", "pre", "during", "post"]
rows = []
for c in conditions:
    for p in ["Positive", "Negative"]:
        vals = rng.normal(loc=0.1 if p == "Positive" else 0.05, scale=0.08, size=80)
        phases = rng.vonmises(mu=0.8 if p == "Positive" else 2.0, kappa=2.5, size=80)
        for v, ph in zip(vals, phases):
            rows.append({"condition": c, "polarity": p, "PLV_norm": v, "phase": ph})

df = pd.DataFrame(rows)
fig = plot_polarity_violin(df=df, value_col="PLV_norm", conditions=conditions)
fig.show()

plot_phase_rose(df=df, phase_col="phase", conditions=conditions)

rayleigh_df = pd.DataFrame({
    "polarity": ["Positive"] * 60 + ["Negative"] * 60 + ["combined"] * 60,
    "rayleigh_stat": np.concatenate([
        rng.gamma(shape=2.5, scale=1.2, size=60),
        rng.gamma(shape=2.1, scale=1.0, size=60),
        rng.gamma(shape=1.9, scale=0.9, size=60),
    ]),
})
rayleigh_df["rayleigh_p"] = np.exp(-rayleigh_df["rayleigh_stat"])
plot_rayleigh_by_polarity(rayleigh_df).show()
