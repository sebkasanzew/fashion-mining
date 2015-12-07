#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main():
    print "There is no main function"


def draw(canvas):
    canvas.create_line(10, 10, 10, 490, fill="#333", width=2)
    canvas.create_line(10, 490, 490, 490, fill="#333", width=2)

if __name__ == "__main__":
    # Execute the main function if this file was executed from the terminal
    main()
