# API Reference

Module layout:
- Categorical/binary distribution plots: `CCSNE.illustration.distributions`
- Circular plots: `CCSNE.illustration.circular`

## `CCSNE.illustration.plot_distribution_by_category`

Generic half-violin distribution plot for arbitrary categories.

Parameters:
- `df` (`pandas.DataFrame`): input long-format table.
- `value_col` (`str`): numeric value column.
- `category_col` (`str`): category column used for grouping.
- `categories` (`list[str] | None`): explicit plotting order.
- `palette` (`dict[str, str] | None`): explicit mapping `{category: color}`.
- `color_sequence` (`list[str] | None`): list of colors in category order.
- `colormap` (`str`, default: `"ccs"`): preset map name. Options: `ccs`, `plotly`, `viridis`, `plasma`.
- `summary` (`str`, default: `"median"`): summary marker center. Options: `median`, `mean`.
- `show_points` (`bool`, default: `True`): whether to draw jittered points.
- `show_annotations` (`bool`, default: `True`): whether to annotate each category.
- `annotate_format` (`str`): template using `{n}`, `{summary}`, `{center}`, `{sd}`.
- `title`, `x_title`, `y_title` (`str | None`): axis/title overrides.
- `jitter` (`float`): x-axis jitter scale for points.
- `point_opacity` (`float`): point transparency.
- `violin_opacity` (`float`): violin transparency.

Returns:
- `plotly.graph_objects.Figure`

## `CCSNE.illustration.plot_rayleigh_by_polarity`

Compatibility wrapper for polarity/rayleigh workflows. Internally calls `plot_distribution_by_category`.

Parameters:
- `res` (`pandas.DataFrame`): input table containing polarity and statistic columns.
- `value_col` (`str`, default: `"rayleigh_stat"`): numeric column to plot on y-axis.
- `p_col` (`str`, default: `"rayleigh_p"`): p-value column (reserved for future annotation logic).
- `polarity_col` (`str`, default: `"polarity"`): column with group labels.
- `title` (`str`): figure title.
- `palette` (`dict[str, str] | None`)
- `color_sequence` (`list[str] | None`)
- `colormap` (`str`, default: `"ccs"`)
- `show_annotations` (`bool`, default: `True`)

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
