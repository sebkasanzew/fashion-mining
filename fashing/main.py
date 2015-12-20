#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import Tkinter as tk
import ttk
import sys
# import subprocess as sub
import mod.util as util
import mod.word2vec as w2v

COLOR_WHITE = '#FFF'
COLOR_BLACK = '#000'
COLOR_GRAY_LIGHT = "#AAA"
COLOR_GRAY_DARK = "#333"
COLOR_LINE_ONE = "#ff6900"

WIDTH_LINE_ONE = 5
CANVAS_BACKGROUND_COLOR = COLOR_WHITE
CANVAS_AXIS_COLOR = COLOR_GRAY_DARK
CANVAS_GRID_COLOR = COLOR_GRAY_LIGHT

FONT_MENU = ("Myriad Pro", 14)
FONT_GRAPH = ("Myriad Pro", 24)
FONT_GRAPH_HEADLINE = ("Myriad Pro", 30)


def main():
    # styling properties with ttk
    # style = ttk.Style()
    # style.configure("TButton", padding=6, relief="flat")

    root = tk.Tk()
    Application(master=root).pack(side="top", fill="both", expand=True)
    root.mainloop()


class Statusbar(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        self.CONSOLE_CONTAINER = None
        self.CONSOLE = None
        self.CONSOLE_TEXT = None

        # console output for the GUI
        # p = sub.Popen('mod/word2vec.py', stdout=sub.PIPE, stderr=sub.PIPE)
        # self.output, self.errors = p.communicate()

        tk.Frame.__init__(self, master, *args, **kwargs)
        self.create_console_log()

    def create_console_log(self):
        self.CONSOLE_CONTAINER = ttk.LabelFrame(self, text="This is the container")
        self.CONSOLE_CONTAINER.pack(fill="both", expand="yes")

        self.CONSOLE = ttk.Label(self.CONSOLE_CONTAINER, text="this is the console")
        self.CONSOLE.pack()

        self.CONSOLE_TEXT = tk.Text(self)
        self.CONSOLE_TEXT.pack()
        # self.CONSOLE_TEXT.insert(END, self.output)


class MainArea(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        # self.grid()

        self.WORD_INPUT = self.make_entry("Search", width=10)

    def make_entry(self, caption, width=None, **kwargs):
        tk.Label(self, text=caption, font=FONT_MENU).grid(row=1, column=1, sticky="nesw")
        entry = tk.Entry(self, **kwargs)
        if width:
            entry.config(width=width)
        return entry


class Application(tk.Frame):
    canvas_padding = 100
    canvas_grid_sections = 5
    canvas_x_headline = "Recall"
    canvas_y_headline = "Precision"
    graph_headline = "Precision/Recall Graph"

    def __init__(self, master=None, *args, **kwargs):
        self.CANVAS_WIDTH = 1000
        self.CANVAS_HEIGHT = 1000
        self.CANVAS = None

        self.TITLE = "Fashing"

        self.DRAW = None

        # Test Data
        self.graph_data = [
            [0, 0],
            [.2, .1],
            [.4, .5],
            [.6, .9],
            [1, 1]
        ]

        tk.Frame.__init__(self, master, *args, **kwargs)
        self.statusbar = Statusbar(self)
        self.main_area = MainArea(self)

        # self.create_widgets()
        self.create_canvas()

        # menubar and sub menus
        self.menubar = None
        self.file_menu = None
        self.analyse_menu = None
        self.graph_menu = None
        self.help_menu = None
        self.create_menu_bar()

        self.master.title(self.TITLE)
        self.master.config(menu=self.menubar)

        self.main_area.pack(side="left", fill="y")

        # self.statusbar.pack(side="bottom", fill="x")

    def open_file(self):
        print "command: file open"

    def open_save(self):
        print "command: file save"

    def about(self):
        print "command: about"

    def quit(self):
        sys.exit(0)

    def create_menu_bar(self):
        self.menubar = tk.Menu(self, font=FONT_MENU)

        self.file_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.file_menu.add_command(label="Open", command=lambda: self.open_file())
        self.file_menu.add_command(label="Save", command=lambda: self.open_save())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        self.analyse_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.analyse_menu.add_command(label="Calculate Precision/Recall", command=calc_precision_recall)

        self.graph_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.graph_menu.add_command(label="Precision Mode", command=lambda: self.update_canvas(grid_sections=10))
        self.graph_menu.add_command(label="Simple Mode", command=lambda: self.update_canvas(grid_sections=5))

        self.help_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.help_menu.add_command(label="About", command=self.about)

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Analyse", menu=self.analyse_menu)
        self.menubar.add_cascade(label="Graph", menu=self.graph_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

    def create_widgets(self):
        self.DRAW = ttk.Button(self)
        self.DRAW["text"] = "Draw"
        self.DRAW.pack({"side": "bottom"})

    def create_canvas(self):
        self.CANVAS = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                background=CANVAS_BACKGROUND_COLOR)
        self.CANVAS.pack(side="right")
        self.draw_canvas()

    def update_canvas(self, padding=canvas_padding, x_headline=canvas_x_headline, y_headline=canvas_y_headline,
                      graph_headline=graph_headline, grid_sections=canvas_grid_sections):
        canvas_padding = padding
        canvas_x_headline = x_headline
        canvas_y_headline = y_headline
        canvas_grid_sections = grid_sections
        graph_headline = graph_headline

        self.CANVAS.delete("all")
        self.CANVAS.config(width=self.CANVAS_WIDTH,
                           height=self.CANVAS_HEIGHT,
                           background=CANVAS_BACKGROUND_COLOR)

        self.draw_canvas(padding=canvas_padding,
                         x_headline=canvas_x_headline,
                         y_headline=canvas_y_headline,
                         graph_headline=graph_headline,
                         grid_sections=canvas_grid_sections)

    def update_canvas_dimensions(self):
        self.CANVAS.config(width="", height="")
        self.draw_canvas()

    def draw_canvas(self, padding=canvas_padding, x_headline=canvas_x_headline, y_headline=canvas_y_headline,
                    graph_headline=graph_headline, grid_sections=canvas_grid_sections):
        canvas = self.CANVAS
        min_y = 0 + padding
        min_x = 0 + padding
        max_y = self.CANVAS_HEIGHT - padding
        max_x = self.CANVAS_WIDTH - padding
        x_range = max_x - min_x
        y_range = max_y - min_y
        graph_data = self.graph_data

        # create a grid and the axis labels
        for i in xrange(min_x, max_x, (x_range // grid_sections)):
            axis_label = (i - padding) / x_range
            # print "( {0} - {1} ) / {2} = {3}".format(i, padding, x_range, axis_label)
            axis_label = 1 - axis_label

            if axis_label < 1.:
                axis_label = "{0}".format(axis_label)[1:]
            else:
                axis_label = util.format_number(axis_label)

            canvas.create_line(i, min_y, i, max_y, dash=(5, 5), fill=CANVAS_GRID_COLOR)
            canvas.create_text(min_x - FONT_GRAPH[1], i, text=axis_label, font=FONT_GRAPH)

        for i in xrange(max_y, min_y, -(y_range // grid_sections)):
            axis_label = (i - padding) / y_range
            # print "( {0} - {1} ) / {2} = {3}".format(i, padding, y_range, axis_label)

            if axis_label < 1.:
                axis_label = "{0}".format(axis_label)[1:]
            else:
                axis_label = util.format_number(axis_label)

            canvas.create_line(min_x, i, max_x, i, dash=(5, 5), fill=CANVAS_GRID_COLOR)
            canvas.create_text(i, max_y + FONT_GRAPH[1], text=axis_label, font=FONT_GRAPH)

        # create closing grid lines
        canvas.create_line(max_x, min_y, max_x, max_y, dash=(5, 5), fill=CANVAS_GRID_COLOR)
        canvas.create_line(min_x, min_y, max_x, min_y, dash=(5, 5), fill=CANVAS_GRID_COLOR)

        # create the graph axes
        canvas.create_line(min_x, max_y, min_x, min_y, fill=CANVAS_AXIS_COLOR, width=2)  # y axis
        canvas.create_line(min_x, max_y, max_x, max_y, fill=CANVAS_AXIS_COLOR, width=2)  # x axis
        canvas.create_polygon((10, 20, 30, 40, 20, 30), fill=CANVAS_AXIS_COLOR)  # triangle not working

        # create the axis headlines
        x_headline_horizontal_pos = (max_x + padding) / 2
        x_headline_vertical_pos = max_y + FONT_GRAPH[1] + padding / 2
        y_headline_horizontal_pos = min_x - FONT_GRAPH[1] - padding / 2
        y_headline_vertical_pos = (max_y + padding) / 2

        canvas.create_text(x_headline_horizontal_pos, x_headline_vertical_pos, text=x_headline, font=FONT_GRAPH)
        canvas.create_text(y_headline_horizontal_pos, y_headline_vertical_pos, text=y_headline, font=FONT_GRAPH,
                           angle=90)

        # create graph headline
        canvas.create_text((max_x + padding) / 2, min_y - padding / 2, text=graph_headline,
                           font=FONT_GRAPH_HEADLINE)

        # create the axis texts
        canvas.create_text(min_x - FONT_GRAPH[1], max_y + FONT_GRAPH[1], text="0", font=FONT_GRAPH)

        # draw the line in the graph
        pre = []  # temp value for the previous iteration
        for val in graph_data:
            if pre:
                x_start = pre[0] * x_range + min_x
                y_start = (1 - pre[1]) * y_range + min_y
                x_end = val[0] * x_range + min_x
                y_end = (1 - val[1]) * y_range + min_y
                canvas.create_line(x_start, y_start, x_end, y_end, fill=COLOR_LINE_ONE, width=WIDTH_LINE_ONE)

            pre = val


def calc_precision_recall():
    print(w2v.word2vec())


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
