import numpy as np
import pandas as pd

from CCSNE.illustration import plot_polarity_violin, plot_phase_rose

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
