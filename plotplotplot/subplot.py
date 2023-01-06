""" Generate a single subplot. """
from typing import List, Tuple, Optional
import pandas as pd
import matplotlib.axes as ax
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# pylint: disable=bad-continuation, too-many-locals, too-many-arguments


def create_subplot(
    axes: ax.Axes,
    x_axis: Optional[str],
    y_axis: Optional[str],
    df: pd.DataFrame,
    x_label: str,
    y_label: str,
    column_count: int,
    column_total: int,
    color_index: int,
    num_colors: int,
    y_axis_label_size: int,
    x_axis_label_size: int,
    legend_size: int,
    tick_label_size: int,
    axis_font: fm.FontProperties,
    legend_font: fm.FontProperties,
    text_opacity: float,
    x_axis_opacity: float,
    line_styles: List[str],
    markers: List[str],
) -> Tuple[ax.Axes, int]:
    """Creates a graph and returns it along with a color index."""

    graph: ax.Axes = df.plot(x=x_axis, y=y_axis, ax=axes, use_index=True)
    plt.legend(loc="best")

    # Hacks to make axes limits visible.
    # axes.set_ylim(top=0.93, bottom=0.4)
    # axes.set_xlim(left=-0.1, right=10.5)

    # Distinct line colors/styles for many lines.
    # e.g. ``line_styles = ['solid', 'dashed', 'dashdot', 'dotted']``.
    use_markers = False
    if use_markers:
        assert len(markers) >= column_count
    color_map = plt.get_cmap("magma")  # "gist_rainbow"

    j = 0
    while color_index < num_colors:
        plt.gca().get_lines()[j].set_color(
            color_map(
                color_index // len(line_styles) * float(len(line_styles)) / num_colors
            )
        )

        if use_markers:
            plt.gca().get_lines()[j].set_marker(markers[j])
            plt.gca().get_lines()[j].set_linestyle(line_styles[j % len(line_styles)])
            plt.gca().get_lines()[j].set_markersize(7.0)

        plt.gca().get_lines()[j].set_linewidth(3.0)
        color_index += 1
        j += 1

    # Add axis labels.
    plt.xlabel(
        x_label,
        fontproperties=axis_font,
        fontsize=x_axis_label_size,
        alpha=text_opacity,
    )
    plt.ylabel(
        y_label,
        fontproperties=axis_font,
        fontsize=y_axis_label_size,
        alpha=text_opacity,
    )

    # Change font of legend.
    legend = graph.legend(prop={"size": legend_size})
    plt.setp(legend.texts, fontproperties=legend_font, alpha=text_opacity)

    # Set size of tick labels.
    graph.tick_params(axis="both", which="major", labelsize=tick_label_size)

    # Set fontname for tick labels.
    for tick in graph.get_xticklabels():
        tick.set_fontname("DecimaMonoPro")
    for tick in graph.get_yticklabels():
        tick.set_fontname("DecimaMonoPro")

    # Set color for tick labels.
    for tick_label in axes.xaxis.get_ticklabels():
        tick_label.set_color("#303030")
    for tick_label in axes.yaxis.get_ticklabels():
        tick_label.set_color("#303030")

    # Create bolded x-axis.
    graph.axhline(y=0, color="black", linewidth=1.3, alpha=x_axis_opacity)

    # Set color of subplots.
    axes.set_facecolor("#F0F0F0")

    return graph, color_index
