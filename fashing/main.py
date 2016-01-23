#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import Tkinter as tk
import json
import sys
import tkFileDialog
import ttk

import mod.util as util
import mod.word2vec as w2v

# import subprocess as sub

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

        self.WORD_INPUT = self.make_entry("Search: ", width=20)

    def make_entry(self, caption, width=None, **kwargs):
        tk.Label(self, text=caption, font=FONT_GRAPH).grid(row=0, column=0, sticky="e")
        entry = tk.Entry(self, font=FONT_GRAPH, **kwargs)
        if width:
            entry.config(width=width)

        entry.grid(row=0, column=1, sticky="w")
        return entry


class Application(tk.Frame):
    canvas_padding = 100
    canvas_grid_sections = 5
    canvas_x_headline = ""
    canvas_y_headline = ""
    graph_headline = ""

    def __init__(self, master=None, *args, **kwargs):
        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 600
        self.CANVAS = None

        self.TITLE = "Fashing"

        self.DRAW = None

        self.graph_data = []

        tk.Frame.__init__(self, master, *args, **kwargs)
        self.statusbar = Statusbar(self)
        self.main_area = MainArea(self)

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

        # self.main_area.pack(side="left", fill="both")

        # self.statusbar.pack(side="bottom", fill="x")

    def open_file(self, **kwargs):
        path = tkFileDialog.askopenfilename(**kwargs)
        return util.open_json(path)

    def open_json_with_path(self, path, **kwargs):
        try:
            with open(path, "r") as json_file:
                return json.load(json_file)
        except IOError as e:
            print "File error occurred:", e.message
            return False

    def open_json(self, title):
        file_json_options = {
            'filetypes': [("json files", "*.json")],
            'title': title
        }

        path = tkFileDialog.askopenfilename(**file_json_options)
        return util.open_json(path)

    def save_file(self, path, text):
        try:
            with open(path, "w") as s_file:
                s_file.write(text)
        except IOError as e:
            print "IOError:" + e.message

    def save_graph(self):
        print "TODO"

    def select_dir(self, title):
        file_html_save_options = {
            'filetypes': [("html file", "*.html")],
            'title': title
        }
        return tkFileDialog.asksaveasfilename(**file_html_save_options)

    def export_html(self):
        # data = self.open_json(title='Choose the JSON with the documents')
        # tags = self.open_json(title='Choose the JSON with the tags')

        data = self.open_json_with_path("../data/input_data/example_docs/example_docs.json")
        tags = self.open_json_with_path("../data/output_data/vector_words_tags.json")

        # path = self.select_dir(title="Select where to save the HTML file")  # TODO uncomment
        path = "../data/html/js_test.html"
        self.save_file(path=path, text=util.create_html(data, tags))

    def execute_w2v(self, model):
        w2v.word2vec(model=model)

    def calc_precision_recall(self):
        self.graph_data = util.compare_docs(self.open_json("Select tagged data"), self.open_json("Select mined data"))

    def about(self):
        print "command: about"

    def quit(self):
        sys.exit(0)

    def compare_docs(self):
        gold_document_path = "../data/input_data/example_docs/example_docs_tags_manuell_final.json"
        w2v_document_path = "../data/output_data/vector_words_tags.json"

        gold = self.open_json_with_path(path=gold_document_path)
        word2vec = self.open_json_with_path(path=w2v_document_path)

        self.graph_data = util.compare_docs(gold_document=gold, w2v_document=word2vec)
        self.update_canvas(x_headline="Recall", y_headline="Precision", graph_headline="Precision/Recall Graph",
                           grid_sections=self.canvas_grid_sections)

    def calc_precision(self):
        gold_document_path = "../data/input_data/example_docs/example_docs_tags_manuell_final.json"
        w2v_document_path = "../data/output_data/vector_words_tags.json"

        gold = self.open_json_with_path(path=gold_document_path)
        word2vec = self.open_json_with_path(path=w2v_document_path)

        self.graph_data = util.compare_docs(gold_document=gold, w2v_document=word2vec, mode="precision", steps=0.02)
        self.update_canvas(x_headline="Cosinus", y_headline="Precision", graph_headline="Precision Graph",
                           grid_sections=self.canvas_grid_sections)

    def calc_recall(self):
        gold_document_path = "../data/input_data/example_docs/example_docs_tags_manuell_final.json"
        w2v_document_path = "../data/output_data/vector_words_tags.json"

        gold = self.open_json_with_path(path=gold_document_path)
        word2vec = self.open_json_with_path(path=w2v_document_path)

        self.graph_data = util.compare_docs(gold_document=gold, w2v_document=word2vec, mode="recall", steps=0.02)
        self.update_canvas(x_headline="Cosinus", y_headline="Recall", graph_headline="Recall Graph",
                           grid_sections=self.canvas_grid_sections)

    def calc_f1(self):
        gold_document_path = "../data/input_data/example_docs/example_docs_tags_manuell_final.json"
        w2v_document_path = "../data/output_data/vector_words_tags.json"

        gold = self.open_json_with_path(path=gold_document_path)
        word2vec = self.open_json_with_path(path=w2v_document_path)

        self.graph_data = util.compare_docs(gold_document=gold, w2v_document=word2vec, mode="f1", steps=0.01)
        self.update_canvas(x_headline="Cosinus", y_headline="F1", graph_headline="F1 Score")

    def clear_graph(self):
        self.graph_data = []
        self.update_canvas(x_headline="", y_headline="", graph_headline="")

    def count_existing_words(self):
        gold_document_path = "../data/input_data/example_docs/example_docs_tags_manuell_final.json"
        fashion_dictionary_path = "../data/dictionaries/one_word_entities.txt"

        gold_document = self.open_json_with_path(path=gold_document_path)
        fashion_dictionary = self.open_json_with_path(path=fashion_dictionary_path)

        print util.count_existing_words(gold_document, fashion_dictionary)

    def create_menu_bar(self):
        self.menubar = tk.Menu(self, font=FONT_MENU)

        self.file_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.file_menu.add_command(label="Open", command=lambda: self.open_file())
        self.file_menu.add_command(label="Save", command=lambda: self.save_graph())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Export HTML", command=lambda: self.export_html())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        self.analyse_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.analyse_menu.add_command(label="Execute Word2Vec with self trained model",
                                      command=lambda: self.execute_w2v(model="selftrained"))
        self.analyse_menu.add_command(label="Execute Word2Vec with Glove model",
                                      command=lambda: self.execute_w2v(model="glove"))
        # self.analyse_menu.add_command(label="Execute Word2Vec", command=execute_w2v)
        self.analyse_menu.add_command(label="Calculate Precision/Recall", command=lambda: self.compare_docs())
        self.analyse_menu.add_command(label="Calculate Precision", command=lambda: self.calc_precision())
        self.analyse_menu.add_command(label="Calculate Recall", command=lambda: self.calc_recall())
        self.analyse_menu.add_command(label="Calculate F1 Score", command=lambda: self.calc_f1())
        self.analyse_menu.add_command(label="Count new and existing words from gold standard",
                                      command=lambda: self.count_existing_words())

        self.graph_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.graph_menu.add_command(label="Precision Mode", command=lambda: self.update_canvas(grid_sections=10))
        self.graph_menu.add_command(label="Simple Mode", command=lambda: self.update_canvas(grid_sections=5))
        self.graph_menu.add_separator()
        self.graph_menu.add_command(label="Clear", command=lambda: self.clear_graph())

        self.help_menu = tk.Menu(self.menubar, tearoff=0, font=FONT_MENU)
        self.help_menu.add_command(label="About", command=self.about)

        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Analyse", menu=self.analyse_menu)
        self.menubar.add_cascade(label="Graph", menu=self.graph_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

    def create_canvas(self):
        self.CANVAS = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                background=CANVAS_BACKGROUND_COLOR)
        self.CANVAS.pack(side="right")
        self.draw_canvas()

    def update_canvas(self, padding=canvas_padding, x_headline=canvas_x_headline, y_headline=canvas_y_headline,
                      graph_headline=graph_headline, grid_sections=canvas_grid_sections):
        print self.canvas_grid_sections, grid_sections

        if grid_sections:
            self.canvas_grid_sections = grid_sections
        if padding:
            self.canvas_padding = padding
        if x_headline:
            self.canvas_x_headline = x_headline
        if y_headline:
            self.canvas_y_headline = y_headline
        if graph_headline:
            self.graph_headline = graph_headline

        self.CANVAS.delete("all")
        self.CANVAS.config(width=self.CANVAS_WIDTH,
                           height=self.CANVAS_HEIGHT,
                           background=CANVAS_BACKGROUND_COLOR)

        self.draw_canvas(padding=self.canvas_padding,
                         x_headline=self.canvas_x_headline,
                         y_headline=self.canvas_y_headline,
                         graph_headline=self.graph_headline,
                         grid_sections=self.canvas_grid_sections)

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


if __name__ == "__main__":
    """Execute the main function if this file was executed from the terminal"""
    main()
