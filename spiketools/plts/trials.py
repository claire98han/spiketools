"""Plots for trials related measures and analyses."""

import numpy as np

from spiketools.utils.base import flatten
from spiketools.utils.options import get_avg_func, get_var_func
from spiketools.plts.settings import DEFAULT_COLORS
from spiketools.plts.annotate import add_vlines, add_vshade, add_significance
from spiketools.plts.utils import check_ax, savefig
from spiketools.plts.style import set_plt_kwargs

###################################################################################################
###################################################################################################

@savefig
@set_plt_kwargs
def plot_rasters(data, vline=None, colors=None, vshade=None,
                 show_axis=False, ax=None, **plt_kwargs):
    """Plot rasters across multiple trials.

    Parameters
    ----------
    data : list of list of float
        Spike times per trial.
        Multiple conditions can also be passed in.
    vline : float or list, optional
        Location(s) to draw a vertical line. If None, no line is drawn.
    colors : str or list of str, optional
        Color(s) to plot the raster ticks.
        If more than one, should be the length of data.
    vshade : list of float, optional
        Vertical region of the plot to shade in.
    show_axis : bool, optional, default: False
        Whether to show the axis around the plot.
    ax : Axes, optional
        Axis object upon which to plot.
    plt_kwargs
        Additional arguments to pass into the plot function.
    """

    ax = check_ax(ax, figsize=plt_kwargs.pop('figsize', None))

    check = False
    for val in data:
        try:
            if isinstance(val, float):
                break
            elif isinstance(val[0], (list, np.ndarray)):
                check = True
                break
        except (IndexError, TypeError):
            continue

    if check:
        lens = [len(el) for el in data]
        colors = DEFAULT_COLORS[0:len(lens)] if not colors else colors
        colors = flatten([[col] * ll for col, ll in zip(colors, lens)])
        data = flatten(data)

    ax.eventplot(data, colors=colors)

    add_vlines(vline, ax, lw=2.5, color=plt_kwargs.pop('line_color', 'green'), alpha=0.5)
    add_vshade(vshade, ax, color=plt_kwargs.pop('shade_color', 'red'), alpha=0.25)

    if not show_axis:
        ax.set_axis_off()


@savefig
@set_plt_kwargs
def plot_rate_by_time(x_vals, y_vals, average=None, shade=None, labels=None,
                      stats=None, sig_level=0.05, ax=None, **plt_kwargs):
    """Plot continuous firing rates across time.

    Parameters
    ----------
    x_vals : 1d array
        Values for the x-axis, for example time values or bin numbers.
    y_vals : list of array
        One or many set of values for the y-axis.
        If each array is 1d values are plotted directly.
        If 2d, is to be averaged before plotting.
    average : {'mean', 'median'}, optional
        Averaging to apply to firing rate activity before plotting.
    shade : {'sem', 'std'} or list of array, optional
        Measure of variance to compute and/or plot as shading.
    labels : list of str, optional
        Labels for each set of y-values.
        If provided, a legend is added to the plot.
    stats : list, optional
        Statistical results, including p-values, to use to annotate the plot.
    sig_level : float, optional, default: 0.05
        Threshold level to consider a result significant.
    ax : Axes, optional
        Axis object upon which to plot.
    plt_kwargs
        Additional arguments to pass into the plot function.
    """

    ax = check_ax(ax, figsize=plt_kwargs.pop('figsize', None))

    if not isinstance(y_vals[0], np.ndarray):
        y_vals = [y_vals]

    if isinstance(shade, str):
        shade = [get_var_func(shade)(arr, 0) for arr in y_vals]

    if isinstance(average, str):
        y_vals = [get_avg_func(average)(arr, 0) for arr in y_vals]

    for ind, ys in enumerate(y_vals):

        ax.plot(x_vals, ys, lw=3, label=labels[ind] if labels else None, **plt_kwargs)

        if shade:
            ax.fill_between(x_vals, ys-shade[ind], ys+shade[ind], alpha=0.25)

    if labels:
        ax.legend(loc='best')

    if stats:
        add_significance(stats, sig_level=sig_level, ax=ax)


def create_raster_title(label, avg_pre, avg_post, t_val=None, p_val=None):
    """Create a standardized title for an event-related raster plot.

    Parameters
    ----------
    label : str
        Label to add to the beginning of the title.
    avg_pre, avg_post : float
        The average firing rates pre and post event.
    t_val, p_val : float, optional
        The t value and p statistic for a t-test comparing pre and post event firing.

    Returns
    -------
    title : str
        Title for the plot.
    """

    if t_val is None:
        title = '{} - Pre: {:1.2f} / Post: {:1.2f}'.format(label, avg_pre, avg_post)
    else:
        title = '{} - Pre: {:1.2f} / Post: {:1.2f} (t:{:1.2f}, p:{:1.2f})'.format(\
            label, avg_pre, avg_post, t_val, p_val)

    return title
