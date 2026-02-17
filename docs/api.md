# API Reference

## `CCSNE.illustration.plot_rayleigh_by_polarity`

Create manuscript-style half-violin plots for `Positive`, `Negative`, and `combined` groups.

Parameters:
- `res` (`pandas.DataFrame`): input table containing polarity and statistic columns.
- `value_col` (`str`, default: `"rayleigh_stat"`): numeric column to plot on y-axis.
- `p_col` (`str`, default: `"rayleigh_p"`): p-value column (reserved for future annotation logic).
- `polarity_col` (`str`, default: `"polarity"`): column with group labels.
- `title` (`str`): figure title.

Returns:
- `plotly.graph_objects.Figure`

## `CCSNE.illustration.plot_polarity_violin`

Plot split violins by condition and polarity with point jitter and mean±SD overlays.

Parameters:
- `df` (`pandas.DataFrame`): long-format input data.
- `value_col` (`str`): value column to visualize.
- `condition_col` (`str`, default: `"condition"`)
- `polarity_col` (`str`, default: `"polarity"`)
- `conditions` (`list[str] | None`): optional explicit ordering.
- `palette` (`dict[str, str] | None`): optional color override.

Returns:
- `plotly.graph_objects.Figure`

## `CCSNE.illustration.plot_phase_rose`

Generate rose/polar histograms per condition with polarity overlays.

Parameters:
- `df` (`pandas.DataFrame`)
- `phase_col` (`str`): phase angle column in radians.
- `condition_col` (`str`, default: `"condition"`)
- `polarity_col` (`str`, default: `"polarity"`)
- `conditions` (`list[str] | None`)
- `nbins` (`int`, default: `36`)
- `palette` (`dict[str, str] | None`)

Returns:
- `(matplotlib.figure.Figure, list[matplotlib.axes.Axes])`

## `CCSNE.analysis`

Available helpers:
- `perform_anova_posthoc`
- `circ_mardia_watson_wheeler`
- `rayleigh_statistic`
- `rayleigh_p_value`
- `uniform_test`
- `cohen_d`
- `cliff_delta`
