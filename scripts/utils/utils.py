import numpy as np
from plotly.colors import get_colorscale, colorscale_to_colors


def make_colormap(series, method='minmax', cmap='RdBu', quantile_value=0.05):
    color_list = colorscale_to_colors(get_colorscale(cmap))
    if method == 'minmax':
        vmin, vmax = series.min(), series.max()
    else:
        vmin, vmax = series.quantile(quantile_value), series.quantile(1 - quantile_value)
    if vmin * vmax > 0:
        return color_list, None
    else:
        l_list = len(color_list)
        extent = vmax if np.abs(vmax) >= np.abs(vmin) else vmin
        is_extent_positive = True if np.abs(vmax) >= np.abs(vmin) else False
        mid_index = l_list // 2
        mid_color = color_list[mid_index]
        interval_index = 2 / (l_list - 1)
        if is_extent_positive:
            interval_value = vmax / (l_list // 2 - 1)
            upper_color_list = list(zip(np.linspace(0, vmax, l_list // 2), color_list[mid_index:]))
            lower_index = int(mid_index - (int(np.abs(vmin) / interval_value) + 1))
            lower_value = - interval_value * (int(np.abs(vmin) / interval_value) + 1)
            lower_color_list = list(zip(np.arange(lower_value, 0, interval_value), color_list[lower_index:mid_index]))
            color_list = lower_color_list + upper_color_list
            return colorscale_to_colors(color_list), (color_list[0][0], color_list[-1][0])
        else: 
            interval_value = np.abs(vmin) / (l_list // 2 - 1)
            lower_color_list = list(zip(np.linspace(vmin, 0, l_list // 2 - 1, endpoint=False), color_list[:mid_index + 1]))
            upper_index = int(mid_index + (int(np.abs(vmax) / interval_value) + 2))
            upper_value = interval_value * (int(np.abs(vmax) / interval_value) + 2)
            upper_color_list = list(zip(np.arange(0, upper_value, interval_value), color_list[mid_index:upper_index + 1]))
            color_list = lower_color_list + upper_color_list
            return colorscale_to_colors(color_list), (color_list[0][0], color_list[-1][0])
