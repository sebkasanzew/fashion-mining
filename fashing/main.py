#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Tkinter import *


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
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def create_canvas(self):
        self.CANVAS = Canvas(self, width=500, height=500, background='white')
        self.CANVAS.pack()


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
