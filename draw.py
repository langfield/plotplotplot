import io
import os
import sys
import csv
import math
import pprint
import argparse

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.font_manager as fm
import matplotlib.transforms as transforms

import pandas as pd
import numpy as np

import preprocessing
import subplot


def graph(dfs, ylabels, filename, column_counts, phase, save_path):
    
    # PLOTTING

    #=================PARAMS=================
    #=================vvvvvv=================

    # Size of ENTIRE PLOT. 
    plot_height = 20 # 7.25
    plot_width = 20
    num_empty_ticks = 0

    # x-axis.
    xaxis = 'index'
    xaxis = None

    # y-axis.
    yaxis = None

    # Text. 
    title_text =  filename
    subtitle_text = phase
    xlabel = ""
    banner_text = "©spred"

    # Set edges of plot in figure (padding). 
    top = 0.90
    bottom = 0.1 #0.18 -- old
    left = 0.08 # 0.1 -- old
    right = 0.96

    # Title sizes. 
    title_pad_x = 0     # + is left, - is right
    title_pos_y = 0.95
    subtitle_pos_y = 0.92
    title_fontsize = 50
    subtitle_fontsize = 30

    # Opacity.
    text_opacity = 0.75
    xaxis_opacity = 0.7

    # Sizing.
    tick_label_size = 14
    legend_size = 14
    y_axis_label_size = 14
    x_axis_label_size = 24
    banner_text_size = 14

    # Import font. 
    prop = fm.FontProperties(fname='fonts/DecimaMonoPro.ttf')
    prop2 = fm.FontProperties(fname='fonts/apercu_medium_pro.otf')
    prop3 = fm.FontProperties(fname='fonts/Apercu.ttf')
    prop4 = fm.FontProperties(fname='fonts/Apercu.ttf', size=legend_size)

    """
    ticks_font = matplotlib.font_manager.FontProperties(family='DecimaMonoPro', 
                                                        style='normal', 
                                                        size=12, 
                                                        weight='normal', 
                                                        stretch='normal')
    """
    #=================^^^^^^=================
    #=================PARAMS=================
    
    # figure initialization
    fig, axlist = plt.subplots(figsize=(plot_width, plot_height),nrows=len(dfs))
    if len(dfs) == 1:
        axlist = [axlist]
    color_index = 0
    column_total = 0
    NUM_COLORS = sum(column_counts)

    for i, df in enumerate(dfs):
        ax = axlist[i]
        plt.sca(ax)
        style.use('fivethirtyeight')
        column_total += column_counts[i]
        graph, color_index = subplot.create_subplot(
                                                    ax=ax, 
                                                    xaxis=xaxis, 
                                                    yaxis=yaxis, 
                                                    df=df, 
                                                    ylabel=ylabels[i], 
                                                    column_total=column_total, 
                                                    color_index=color_index, 
                                                    NUM_COLORS=NUM_COLORS,
                                                    xlabel=xlabel,
                                                    y_axis_label_size=y_axis_label_size,
                                                    x_axis_label_size=x_axis_label_size,
                                                    legend_size=legend_size, 
                                                    tick_label_size=tick_label_size,
                                                    axis_font=prop3,
                                                    legend_font=prop4,
                                                    text_opacity=text_opacity,
                                                    xaxis_opacity=xaxis_opacity)



    xlabel = "Iterations"
    # add axis labels  
    plt.xlabel(xlabel, 
               fontproperties=prop3, 
               fontsize = 24, 
               alpha=text_opacity)

    # =========================================================

    # transforms the x axis to figure fractions, and leaves y axis in pixels
    xfig_trans = transforms.blended_transform_factory(fig.transFigure, transforms.IdentityTransform())
    yfig_trans = transforms.blended_transform_factory(transforms.IdentityTransform(), fig.transFigure)

    # banner positioning
    banner_y = math.ceil(banner_text_size * 0.6)

    # banner text
    banner = plt.annotate(banner_text, 
             xy=(0.02, banner_y*0.8), 
             xycoords=xfig_trans,
             fontsize = banner_text_size, 
             color = '#FFFFFF', 
             fontname='DecimaMonoPro')

    # banner background height parameters
    pad = 2 # points
    bb = ax.get_window_extent()
    h = bb.height/fig.dpi
    h = h * len(column_counts)
    height = ((banner.get_size()+2*pad)/72.)/h
    # height = 0.01

    # banner background
    rect = plt.Rectangle((0,0), 
                         width=1, 
                         height=height,
                         transform=fig.transFigure, 
                         zorder=3,
                         fill=True, 
                         facecolor="grey", 
                         clip_on=False)
    ax.add_patch(rect)

    #transform coordinate of left
    display_left_tuple = xfig_trans.transform((left,0))
    display_left = display_left_tuple[0]

    # shift title
    title_shift_x = math.floor(tick_label_size * 2.6)
    title_shift_x += title_pad_x

    # title
    graph.text(x = display_left - title_shift_x, y = title_pos_y, 
               transform = yfig_trans,
               s = title_text,
               fontproperties = prop2,
               weight = 'bold', 
               fontsize = title_fontsize,
               alpha = text_opacity)

    # subtitle, +1 accounts for font size difference in title and subtitle
    graph.text(x = display_left - title_shift_x + 1, y = subtitle_pos_y, 
               transform = yfig_trans,
               s = subtitle_text,
               fontproperties=prop3,
               fontsize = subtitle_fontsize, 
               alpha = text_opacity)


    # adjust position of subplot in figure
    plt.subplots_adjust(top=top)
    plt.subplots_adjust(bottom=bottom)
    plt.subplots_adjust(left=left)
    plt.subplots_adjust(right=right)

    # save to .svg
    plt.savefig(save_path)
   
def main(args):
    GRAPHS_PATH = 'graphs/'
    assert os.path.isdir(GRAPHS_PATH)
    filename = os.path.basename(args.filepath)
    filename_no_ext = filename.split('.')[0]
    if args.phase != "":
        save_path = os.path.join(GRAPHS_PATH, filename_no_ext + "_" + args.phase + ".svg")
    else:
        save_path = os.path.join(GRAPHS_PATH, filename_no_ext + ".svg")
    if args.format == 'csv':
        dfs, ylabels, column_counts = preprocessing.read_csv(args.filepath)
    elif args.format == 'json':
        dfs, ylabels, column_counts = preprocessing.read_json(args.filepath, args.phase)
    else:
        raise ValueError("Invalid --format format.")
    graph(dfs, ylabels, filename_no_ext, column_counts, args.phase, save_path)
    print("Graph saved to:", save_path) 

if __name__ == '__main__':
    # TODO: Add an `overwrite` argument which defaults to `True`.
    parser = argparse.ArgumentParser(description='Matplotlib 538-style plot generator.')
    parser.add_argument('--filepath', type=str, help='File to parse and graph.', required=True)
    parser.add_argument('--format', type=str, default='csv', help='`csv` or `json`.')
    parser.add_argument('--phase', type=str, default='', help='The section to graph. One of \'train\', \'validate\', \'test\'.') 
    args = parser.parse_args()
    main(args)
