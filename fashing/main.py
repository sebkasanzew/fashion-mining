#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Tkinter import *
import fashing.mod.graph as graph


def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()


class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.create_canvas()

    def create_widgets(self):
        print "null"
        # self.QUIT = Button(self)
        # self.QUIT["text"] = "QUIT"
        # self.QUIT["fg"] = "red"
        # self.QUIT["command"] = self.quit

        # self.QUIT.pack({"side": "left"})

        # self.hi_there = Button(self)
        # self.hi_there["text"] = "Hello",
        # self.hi_there["command"] = self.say_hi

        # self.hi_there.pack({"side": "left"})

    def create_canvas(self):
        self.CANVAS = Canvas(self, width=500, height=500, background='white')
        self.CANVAS.pack()

        # self.CANVAS.create_line(10, 10, 10, 490, fill="#333", width=2)
        # self.CANVAS.create_line(10, 490, 490, 490, fill="#333", width=2)

        self.draw_canvas()


    def draw_canvas(self):
        canvas = self.CANVAS

        canvas.create_line(10, 10, 10, 490, fill="#333", width=2)
        canvas.create_line(10, 490, 490, 490, fill="#333", width=2)


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
