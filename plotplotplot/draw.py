""" General matplotlib utility for drawing line plots from dataframes. """
import os
import math
import json
import argparse
from typing import List, Dict, Any, Optional

import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.style as style  # type: ignore
import matplotlib.font_manager as fm  # type: ignore
import matplotlib.transforms as transforms  # type: ignore

from plotplotplot import preprocessing, subplot

# pylint: disable=bad-continuation, too-many-locals, too-many-statements

GRAPHS_PATH = "graphs/"


def graph(
    dfs: List[pd.DataFrame],
    y_labels: List[str],
    column_counts: List[int],
    save_path: str,
    settings_path: str,
) -> None:
    """ Graph all the dataframes in ``dfs`` in a separate subplot. """

    # Settings.
    print("Reading settings file from '%s'" % settings_path)
    assert os.path.isfile(settings_path)
    with open(settings_path, "r") as settings_file:
        settings: Dict[str, Any] = json.load(settings_file)

    # Validate arguments.
    assert len(dfs) == len(y_labels) == len(column_counts)

    save_path = os.path.abspath(save_path)
    if not os.path.isdir(os.path.dirname(save_path)):
        os.makedirs(save_path)

    # Entire plot size.
    plot_height = settings["plot_height"]
    plot_width = settings["plot_width"]

    # Column to plot.
    x_axis: Optional[str] = settings["x_axis"]
    y_axis: Optional[str] = settings["y_axis"]
    if x_axis == "":
        x_axis = None
    if y_axis == "":
        y_axis = None

    # Text.
    title_text = settings["title_text"]
    subtitle_text = settings["subtitle_text"]
    banner_text = settings["banner_text"]

    # Labels.
    x_label = settings["x_label"]

    # Edges of plot in figure.
    top = settings["top"]
    bottom = settings["bottom"]
    left = settings["left"]
    right = settings["right"]

    # Title sizes.
    title_pad_x = settings["title_pad_x"]
    title_pos_y = settings["title_pos_y"]
    subtitle_pos_y = settings["subtitle_pos_y"]
    title_font_size = settings["title_font_size"]
    subtitle_font_size = settings["subtitle_font_size"]

    # Opacities.
    text_opacity = settings["text_opacity"]
    x_axis_opacity = settings["x_axis_opacity"]

    # Sizes.
    tick_label_size = settings["tick_label_size"]
    legend_size = settings["legend_size"]
    x_axis_label_size = settings["x_axis_label_size"]
    y_axis_label_size = settings["y_axis_label_size"]
    banner_text_size = settings["banner_text_size"]

    # Line markers and styles.
    line_styles = settings["line_styles"]
    markers = settings["markers"]

    # Import font.
    pkg_path = os.path.dirname(os.path.abspath(__file__))
    decima_path = os.path.join(pkg_path, "fonts/DecimaMonoPro.ttf")
    apercu_medium_path = os.path.join(pkg_path, "fonts/apercu_medium_pro.otf")
    apercu_path = os.path.join(pkg_path, "fonts/Apercu.ttf")
    prop = fm.FontProperties(fname=decima_path)
    apercu_medium = fm.FontProperties(fname=apercu_medium_path)
    apercu = fm.FontProperties(fname=apercu_path)
    apercu_legend = fm.FontProperties(fname=apercu_path, size=legend_size)

    ticks_font = fm.FontProperties(
        family="DecimaMonoPro",
        style="normal",
        size=12,
        weight="normal",
        stretch="normal",
    )

    # Figure initialization.
    fig, axlist = plt.subplots(figsize=(plot_width, plot_height), nrows=len(dfs))
    if len(dfs) == 1:
        axlist = [axlist]
    color_index = 0
    column_total = 0
    num_colors = sum(column_counts)

    for i, df in enumerate(dfs):
        axes = axlist[i]
        plt.sca(axes)
        style.use("fivethirtyeight")
        column_total += column_counts[i]
        graphplot, color_index = subplot.create_subplot(
            axes=axes,
            x_axis=x_axis,
            y_axis=y_axis,
            df=df,
            x_label=x_label,
            y_label=y_labels[i],
            column_count=column_counts[i],
            column_total=column_total,
            color_index=color_index,
            num_colors=num_colors,
            y_axis_label_size=y_axis_label_size,
            x_axis_label_size=x_axis_label_size,
            legend_size=legend_size,
            tick_label_size=tick_label_size,
            axis_font=apercu,
            legend_font=apercu_legend,
            text_opacity=text_opacity,
            x_axis_opacity=x_axis_opacity,
            line_styles=line_styles,
            markers=markers,
        )

    # Add axis labels.
    plt.xlabel(
        x_label, fontproperties=apercu, fontsize=x_axis_label_size, alpha=text_opacity
    )

    # Transforms the x axis to figure fractions, and leaves y axis in pixels.
    xfig_trans = transforms.blended_transform_factory(
        fig.transFigure, transforms.IdentityTransform()
    )
    yfig_trans = transforms.blended_transform_factory(
        transforms.IdentityTransform(), fig.transFigure
    )

    # Banner positioning.
    banner_y = math.ceil(banner_text_size * 0.6)

    # Banner text.
    banner = plt.annotate(
        banner_text,
        xy=(0.01, banner_y * 0.8),
        xycoords=xfig_trans,
        fontsize=banner_text_size,
        color="#FFFFFF",
        fontname="DecimaMonoPro",
    )

    # Banner background height parameters.
    pad = 2  # points
    bounding_box = axes.get_window_extent()
    h_pixels = bounding_box.height / fig.dpi
    h_pixels = h_pixels * len(column_counts)
    height = ((banner.get_size() + 2 * pad) / 72.0) / h_pixels
    # height = 0.01

    # Banner background.
    rect = plt.Rectangle(
        (0, 0),
        width=1,
        height=height,
        transform=fig.transFigure,
        zorder=3,
        fill=True,
        facecolor="grey",
        clip_on=False,
    )
    axes.add_patch(rect)

    # Transform coordinate of left.
    display_left_tuple = xfig_trans.transform((left, 0))
    display_left = display_left_tuple[0]

    # Shift title.
    title_shift_x = math.floor(tick_label_size * 2.6)
    title_shift_x += title_pad_x

    # Title.
    graphplot.text(
        x=display_left - title_shift_x,
        y=title_pos_y,
        transform=yfig_trans,
        s=title_text,
        fontproperties=apercu_medium,
        weight="bold",
        fontsize=title_font_size,
        alpha=text_opacity,
    )

    # Subtitle, +1 accounts for font size difference in title and subtitle.
    graphplot.text(
        x=display_left - title_shift_x + 1,
        y=subtitle_pos_y,
        transform=yfig_trans,
        s=subtitle_text,
        fontproperties=apercu,
        fontsize=subtitle_font_size,
        alpha=text_opacity,
    )

    # Adjust position of subplot in figure.
    plt.subplots_adjust(top=top)
    plt.subplots_adjust(bottom=bottom)
    plt.subplots_adjust(left=left)
    plt.subplots_adjust(right=right)

    # Save to ``.svg``.
    plt.savefig(save_path)
    print("Plot saved to '%s'" % save_path)


def main(args):
    """ Graph from file. """
    assert os.path.isdir(GRAPHS_PATH)
    basename = os.path.basename(args.filepath)
    filename = basename.split(".")[0]
    save_path = os.path.join(GRAPHS_PATH, filename + ".svg")
    if args.format == "csv":
        dfs, y_labels, column_counts = preprocessing.read_csv(args.filepath)
    else:
        raise ValueError("Invalid --format format.")
    graph(dfs, y_labels, column_counts, save_path, args.settings_path)
    print("Graph saved to:", save_path)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Matplotlib 538-style plot generator.")
    PARSER.add_argument(
        "--filepath", type=str, help="File to parse and graph.", required=True
    )
    PARSER.add_argument(
        "--settings-path",
        type=str,
        help="Location of valid settings file.",
        required=True,
    )
    PARSER.add_argument("--format", type=str, default="csv", help="`csv` or `json`.")
    ARGS = PARSER.parse_args()
    main(ARGS)
