#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import ttk
# import subprocess as sub
# import fashing.mod.graph as graph
import mod.word2vec as w2v


def main():
    # styling properties with ttk
    # style = ttk.Style()
    # style.configure("TButton", padding=6, relief="flat")

    root = tk.Tk()
    Application(master=root).pack(side="top", fil="both", expand=True)
    root.mainloop()


class Statusbar(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        # console output for the GUI
        # p = sub.Popen('mod/word2vec.py', stdout=sub.PIPE, stderr=sub.PIPE)
        # self.output, self.errors = p.communicate()

        tk.Frame.__init__(self, master, *args, **kwargs)
        # self.create_console_log()

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
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.statusbar = Statusbar(self)

        self.statusbar.pack(side="bottom", fill="x")

        # self.create_widgets()
        self.create_canvas()

    def create_widgets(self):
        self.DRAW = ttk.Button(self)
        self.DRAW["text"] = "Draw"
        self.DRAW["command"] = self.button_draw()
        self.DRAW.pack({"side": "bottom"})

    def button_draw(self):
        return "TODO"

    def create_canvas(self):
        self.CANVAS_WIDTH = 1000
        self.CANVAS_HEIGHT = 1000

        self.CANVAS = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background='white')
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
            canvas.create_line(i, min_y, i, max_y, dash=(5, 5), fill="#ccc")

        for i in xrange(max_y, min_y, -(y_range / grid_sections)):
            canvas.create_line(min_x, i, max_x, i, dash=(5, 5), fill="#ccc")

        # create closing grid lines
        canvas.create_line(max_x, min_y, max_x, max_y, dash=(5, 5), fill="#ccc")
        canvas.create_line(min_x, min_y, max_x, min_y, dash=(5, 5), fill="#ccc")

        # create the graph axes
        canvas.create_line(min_x, max_y, min_x, min_y, fill="#333", width=2)  # y axis
        canvas.create_line(min_x, max_y, max_x, max_y, fill="#333", width=2)  # x axis
        canvas.create_polygon((10, 20, 30, 40, 20, 30), fill="#333")  # triangle not working

        # create the axis texts
        canvas.create_text(min_x - 10, max_y + 10, text="0", font=("Myriad Pro", 24))

        self.graph_data = [
            [0, 0],
            [.2, .1],
            [.4, .5],
            [.6, .9],
            [1, 1]
        ]

        print(w2v.word2vec())

        pre = []  # temp value for the previous iteration
        for val in self.graph_data:
            if pre:
                x_start = pre[0] * x_range + min_x
                y_start = (1 - pre[1]) * y_range + min_y
                x_end = val[0] * x_range + min_x
                y_end = (1 - val[1]) * y_range + min_y
                canvas.create_line(x_start, y_start, x_end, y_end, fill="#F00")

            pre = val


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
