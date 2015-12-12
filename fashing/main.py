#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Tkinter import *
import ttk
# import subprocess as sub
# import fashing.mod.graph as graph
import mod.word2vec as w2v


def main():
    # styling properties with ttk
    # style = ttk.Style()
    # style.configure("TButton", padding=6, relief="flat")

    root = Tk()
    app = Application(master=root)
    app.mainloop()

    print(w2v.word2vec())


class Application(Frame):

    def __init__(self, master=None):
        # console output for the GUI
        # p = sub.Popen('mod/word2vec.py', stdout=sub.PIPE, stderr=sub.PIPE)
        # self.output, self.errors = p.communicate()

        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.create_canvas()
        self.create_console_log()

    def create_widgets(self):
        self.DRAW = ttk.Button(self)
        self.DRAW["text"] = "Draw"
        self.DRAW["command"] = self.button_draw()
        self.DRAW.pack({"side": "bottom"})

    def button_draw(self):
        return "TODO"

    def create_canvas(self):
        self.CANVAS_WIDTH = 500
        self.CANVAS_HEIGHT = 300

        self.CANVAS = Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background='white')
        self.CANVAS.pack()
        self.draw_canvas()

    def create_console_log(self):
        self.CONSOLE_CONTAINER = ttk.LabelFrame(self, text="This is the container")
        self.CONSOLE_CONTAINER.pack(fill="both", expand="yes")

        self.CONSOLE = ttk.Label(self.CONSOLE_CONTAINER, text="this is the console")
        self.CONSOLE.pack()

        self.CONSOLE_TEXT = Text(self)
        self.CONSOLE_TEXT.pack()
        # self.CONSOLE_TEXT.insert(END, self.output)

    def draw_canvas(self):
        canvas = self.CANVAS
        padding = 10
        min_y = 0 + padding
        min_x = 0 + padding
        max_y = self.CANVAS_HEIGHT - padding
        max_x = self.CANVAS_WIDTH - padding

        # create the graph axes
        canvas.create_line(min_x, max_y, min_x, min_y, fill="#333", width=2)  # y axis
        canvas.create_line(min_x, max_y, max_x, max_y, fill="#333", width=2)  # x axis
        # canvas.create_polygon(10, 20, 30, fill="#333")


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
