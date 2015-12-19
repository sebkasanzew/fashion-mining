#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import ttk
import sys
# import subprocess as sub
# import fashing.mod.graph as graph
import mod.word2vec as w2v

COLOR_WHITE = '#FFF'
COLOR_GRAY_LIGHT = "#CCC"
COLOR_GRAY_DARK = "#333"
COLOR_LINE_ONE = "#F00"

FONT_MENU = ("Myriad Pro", 14)
FONT_GRAPH = ("Myriad Pro", 24)


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


class Application(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        self.CANVAS = None
        self.CANVAS_WIDTH = 1000
        self.CANVAS_HEIGHT = 1000

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

        # menubar and sub menus
        self.menubar = None
        self.file_menu = None
        self.analyse = None
        self.help_menu = None
        self.create_menu_bar()

        self.master.title(self.TITLE)
        self.master.config(menu=self.menubar)

        # self.statusbar.pack(side="bottom", fill="x")

        # self.create_widgets()
        self.create_canvas()

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
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.open_save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        self.analyse = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.analyse.add_command(label="Calculate Precision/Recall", command=calc_precision_recall)

        self.help_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.help_menu.add_command(label="About", command=self.about)

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Analyse", menu=self.analyse)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

    def create_widgets(self):
        self.DRAW = ttk.Button(self)
        self.DRAW["text"] = "Draw"
        self.DRAW.pack({"side": "bottom"})

    def create_canvas(self):
        self.CANVAS = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background=COLOR_WHITE)
        self.CANVAS.pack()
        self.draw_canvas()

    def draw_canvas(self):
        canvas = self.CANVAS
        padding = 50
        min_y = 0 + padding
        min_x = 0 + padding
        max_y = self.CANVAS_HEIGHT - padding
        max_x = self.CANVAS_WIDTH - padding
        x_range = max_x - min_x
        y_range = max_y - min_y

        grid_sections = 5

        # create a grid
        for i in xrange(min_x, max_x, (x_range / grid_sections)):
            canvas.create_line(i, min_y, i, max_y, dash=(5, 5), fill=COLOR_GRAY_LIGHT)

        for i in xrange(max_y, min_y, -(y_range / grid_sections)):
            canvas.create_line(min_x, i, max_x, i, dash=(5, 5), fill=COLOR_GRAY_LIGHT)

        # create closing grid lines
        canvas.create_line(max_x, min_y, max_x, max_y, dash=(5, 5), fill=COLOR_GRAY_LIGHT)
        canvas.create_line(min_x, min_y, max_x, min_y, dash=(5, 5), fill=COLOR_GRAY_LIGHT)

        # create the graph axes
        canvas.create_line(min_x, max_y, min_x, min_y, fill=COLOR_GRAY_DARK, width=2)  # y axis
        canvas.create_line(min_x, max_y, max_x, max_y, fill=COLOR_GRAY_DARK, width=2)  # x axis
        canvas.create_polygon((10, 20, 30, 40, 20, 30), fill=COLOR_GRAY_DARK)  # triangle not working

        # create the axis texts
        canvas.create_text(min_x - 10, max_y + 10, text="0", font=FONT_GRAPH)

        pre = []  # temp value for the previous iteration
        for val in self.graph_data:
            if pre:
                x_start = pre[0] * x_range + min_x
                y_start = (1 - pre[1]) * y_range + min_y
                x_end = val[0] * x_range + min_x
                y_end = (1 - val[1]) * y_range + min_y
                canvas.create_line(x_start, y_start, x_end, y_end, fill=COLOR_LINE_ONE)

            pre = val


def calc_precision_recall():
    print(w2v.word2vec())


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
