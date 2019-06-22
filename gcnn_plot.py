# Imports. 

import io
import os
import sys
import csv
import math
import pprint

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.font_manager as fm
import matplotlib.transforms as transforms

import pandas as pd
import numpy as np

import plot_preproc


def graph(dfs, ylabels, filename, column_counts):
    
    filename_no_extension = filename.split('.')[0]

    # PLOTTING

    #================================================
    # PARAMETERS
    #================================================

    # Size of ENTIRE PLOT. 
    plot_height = 20 # 7.25
    plot_width = 20
    num_empty_ticks = 0

    # x-axis.
    xaxis = 'index'

    # y-axis.
    yaxis = None

    # Text. 
    title_text =  filename
    subtitle_text = "train"
    xlabel = ""
    banner_text = "©craw"

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
    prop = fm.FontProperties(fname='DecimaMonoPro.ttf')
    prop2 = fm.FontProperties(fname='apercu_medium_pro.otf')
    prop3 = fm.FontProperties(fname='Apercu.ttf')
    prop4 = fm.FontProperties(fname='Apercu.ttf', size=legend_size)

    #ticks_font = matplotlib.font_manager.FontProperties(family='DecimaMonoPro', style='normal', size=12, weight='normal', stretch='normal')

    #================================================
    # END OF PARAMETERS
    #================================================
    
    # =========================================================

    # figure initialization
    fig, axlist = plt.subplots(figsize=(plot_width, plot_height),nrows=len(dfs))
    color_index = 0
    column_total = 0
    NUM_COLORS = sum(column_counts)

    for i, df in enumerate(dfs):
        ax = axlist[i]
        plt.sca(ax)
        style.use('fivethirtyeight')
        column_total += column_counts[i]
        graph, color_index = plot_preproc.create_subplot(
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
                                                            xaxis_opacity=xaxis_opacity,
                                                        )



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
    plt.savefig(filename_no_extension + ".svg", dpi=300)
   
def main():
        
    # filename = sys.argv[1]
    filename = 'prelimSkipSlimGrowing.log'
    filename_no_extension = filename.split('.')[0]
    dfs, ylabels, column_counts = plot_preproc.read_log(filename, 'train')
    graph(dfs, ylabels, filename, column_counts)
    print("Graph saved to:", filename_no_extension + ".svg") 

if __name__ == '__main__':
    main()
