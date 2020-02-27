#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time
import numpy as np
import pandas as pd
import os.path

def fish():
    """
    Easter egg, shows bypassing fish
    """
    A1 = "(                                                     \n" \
         " )                                                  ( \n" \
         "(         (                                      ,/.. \n" \
         ")    )    )                                  (<')   `=\n" \
         ".(.....(..(....................................).``\``"
    A2 = "(                                                      \n" \
         " )                                                   ( \n" \
         " (          (                                ,/..     )\n" \
         " )      )   )                             <')   `=<  ( \n" \
         ".(......(..(.......o........................`/````...)."
    A3 = "(                                                 __   \n" \
         "  )                                             <'_>< (\n" \
         " (         (                         ,/..         `   )\n" \
         "  )    )    )       O              <')   `=<    (    ( \n" \
         ".(......(..(.........................``\```......)...)."
    A4 = " (                                         __          \n" \
         " )                                       <'_><     (   \n" \
         "(          )       O           ,/..        `         ) \n" \
         " )      ( (                  <')   `=<         )    (  \n" \
         ".(.....)..)...................`/````.........(.......)."
    A5 = " (                O                    __              \n" \
         "  )                                  <'_><          (  \n" \
         " (         (             ,/..          `             ) \n" \
         "  )    (    )          <')   `=<               )    (  \n" \
         ".)......)..(.............``\```...............(......)."
    A6 = "  )                                __                  \n" \
         " (                               <'_><               ( \n" \
         "  )        )        o ,/..         `                 ) \n" \
         "  )    (  (        <')   `=<                  (     (  \n" \
         ".)......)..).........`/````........o..........)......)."
    A7 = " )                          __                         \n" \
         " )                  O     <'_><                    (   \n" \
         "  )        )      ,/..      `                       )  \n" \
         "  (    (  (    <')   `=<            O         )     (  \n" \
         ".(......)..).....``\```...............o.......(......)."
    A8 = " )               O   __                                \n" \
         ")                   <'_><            O              (  \n" \
         " )        )   ,/..    `                              ) \n" \
         ")       )( <')   `=<                   O      )     (  \n" \
         ".).....(..)..``\```............................(......)."
    A9 = ")           __                        o                \n" \
         "(          <'_><                       O            (  \n" \
         " )     )  ,/..                                       ) \n" \
         " (    )<')   `=<                               )     ( \n" \
         ".)...(..`/````.......................o.......(......).."
    A10 = "   )  __                                              \n" \
          " (  <'_><                              O         (    \n" \
          " )    ,/..                                        )   \n" \
          "(  <')   `=<                        O        )     (  \n" \
          ".).. ``\```.................................(......).."
    A11 = "                                                      \n" \
          "                                                    ( \n" \
          ",/..                               O                ) \n" \
          "   `=<                                       )     (  \n" \
          "``\```.......................................(......)."

    aquarium = curses.newwin(10, 60, 40, 3)
    for i in [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11]:
        aquarium.addstr(0, 0, i)
        curses.resize_term(300, 300)
        aquarium.refresh()
        time.sleep(1)
    del aquarium


def is_annotated(finding_list):
    """
    Checks if any of the findings has been annotated
    :return: bool
    """
    annotated = False

    for item in finding_list:
        if not np.isnan(item.value):
            annotated = True
            break

    return annotated


class Finding(object):
    """
    A Finding is everything, that can be found in a report text, like Congestion, Pneumonia....
    Attributes:
        name: a string with the name of the finding, e.g. Pneumothorax
        value: an integer or np.NaN (default). If 1, the finding is present, if 1 it is not. If -1 the report is uninterpretable
    """

    def __init__(self, csv_master, col, row):

        self.name = csv_master.columns[col]
        self.value = csv_master.iloc[row, col]
        self.key = col + 48
        self.uninterpretable = False

    def toggle(self):
        if not self.uninterpretable:
            if self.value == 1:
                self.value = 0
            else:
                self.value = 1

    def reset_nan(self):
        self.value = np.NaN

    def toggle_uninterpretable(self):
        if self.value == -1:
            self.value = 0
            self.uninterpretable = False
        else:
            self.value = -1
            self.uninterpretable = True

    def NaN_to_0(self):
        if np.isnan(self.value):
            self.value = 0

    def print_label(self, pad, prefix):
        y = self.key - 45

        prefix = str(self.key - 48) + prefix  # from ") " to "key )"

        if self.value == -1:
            pad.addstr(y, 3, prefix + self.name, curses.color_pair(1))
        elif self.value == 0:
            pad.addstr(y, 3, prefix + self.name)
        elif self.value == 1:
            pad.addstr(y, 3, prefix + self.name, curses.A_STANDOUT)
        elif np.isnan(self.value):
            pad.addstr(y, 3, prefix + self.name, curses.color_pair(2))
        pad.refresh(0, 0, 0, 0, 45, 45)


class RightSideMenu(object):
    """
    Menu on the right side of the screen, showing the annotations, Controls and the Menu
    """

    def __init__(self):
        self.language = "english"
        self.show_only_annotated = 0
        self.ai_on = 0

    def show_menu(self, pad, confidence_rating):
        # Heading above annotations
        pad.addstr(2, 3, "Annotation", curses.A_BOLD)

        for i in range(4, 13):
            pad.addstr(i, 3, "<empty>", curses.A_DIM)
        pad.addstr(14, 3, "Confidence: ", curses.A_VERTICAL)
        if confidence_rating == "low":
            pad.addstr(14, 15, confidence_rating + "   ", curses.color_pair(3))
        if confidence_rating == "medium":
            pad.addstr(14, 15, confidence_rating + "", curses.color_pair(4))
        if confidence_rating == "high":
            pad.addstr(14, 15, confidence_rating + "  ", curses.color_pair(5))
        if confidence_rating == "NA":
            pad.addstr(14, 15, confidence_rating + "    ", curses.color_pair(1))
        pad.addstr(15, 3, "(Toggle with up/down arrow)")

        # Controls section
        pad.addstr(17, 3, "Controls", curses.A_BOLD)

        pad.addstr(18, 3, "a) All findings present")
        pad.addstr(19, 3, "s) No finding present")
        pad.addstr(20, 3, "d) Delete annotation")
        pad.addstr(21, 3, "q) Close application")
        pad.addstr(22, 3, "n) Show nex report   \n      (right arrow)")
        pad.addstr(23, 3, "v) Show previous report \n      (left arrow)")
        pad.addstr(24, 3, "x) text is no evaluable")

        # Options section
        pad.addstr(27, 3, "Options", curses.A_BOLD)

        if self.show_only_annotated == 0:
            pad.addstr(29, 3, "A) Show only annotated reports  \n "
                              "     currently all reports are showen             ")
        elif self.show_only_annotated == 1:
            pad.addstr(29, 3, "A) Show only unannotated reports   \n "
                              "     currently shows only annotated reports             ")
        elif self.show_only_annotated == 2:
            pad.addstr(29, 3, "A) Show all reports  \n "
                              "     currently shows only unannotated reports             ")

        #       pad.addstr(30, 3, "l) Zur deutschen Bedienoberfläche wechseln") # might be implemented in the future

        if self.ai_on == 0:
            pad.addstr(31, 3, "S) Turn on AI  \n "
                              "     AI is currently turned off             ")
        elif self.ai_on == 1:
            pad.addstr(31, 3, "S) Turn off AI  \n "
                              "     AI is currently on             ")
        pad.refresh(0, 0, 0, 0, 45, 45)

    def show_only_annotated_toggle(self):
        if self.show_only_annotated == 2:
            self.show_only_annotated = 0
        else:
            self.show_only_annotated += 1

    def toggle_ai(self):
        self.ai_on ^= 1


class MasterTable(object):
    """
    1. Reads the fileaddress from the csv-file
    2. Imports the text from the file at the fileaddress
    """

    def __init__(self, path_to_csv_file):
        self.path = path_to_csv_file
        self.csv_file = pd.read_csv(self.path)
        self.row = 0
        self.col = 0
        self.n_col = self.csv_file.shape[1]
        self.n_row = self.csv_file.shape[0]

    def read_file(self):
        """
        Read the report-text File
        :param MasterTable: csv with names of all files and annotations
            strcture of the csv file

            fileadress  | Stauung       | Infiltrate    | Dystelektase  | Pneumothorax  | Erguss
            -------------------------------------------------------------------------------------
            13764005.txt| NA            | NA            | NA            | NA            | NA

            :param col: integer for current used column
            :param row: integer for current used row
            """

        self.file_name = self.csv_file.iloc[self.row, self.col]

        file = open("data/txt/" + self.file_name, 'r')
        self.text = file.read()
        file.close()

        # reformat the text
        # 1. insert linebreaks after 100 characters

        x = len(self.text) // 50
        for i in range(0, x):
            pos = i*50
            if "\n" not in self.text[(pos-50):(pos+50)]:
                str_to_replace = self.text[(pos + 25):(pos+50)]
                str_to_replace = str_to_replace.replace(" ", " \n", 1)
                self.text = self.text[:(pos + 25)] + str_to_replace + self.text[(pos+50):]

    def write_findings(self, findings):
        for item in findings:
            col = item.key - 48
            self.csv_file.at[self.row, item.name] = item.value

        self.csv_file.to_csv(self.path, index=False)

    def print_report(self, window):
        """
        Read and display the report in a new window
        :param stdscr: standard curses screen
        Filename can be printed for debugging
        """

        window.clear()
        window.addstr(0, 0, self.text)
        window.refresh(0, 0, 10, 49, 45, 200)


class ProgressBar(object):
    """
    Progress bar for annotation. Shows progress bar on top of screen.
    """

    def __init__(self, n_row, current_annotator, csv_file, pad=None, log="data/log.txt"):

        if pad is None:
            pad = [0, 1, 0, 0, 9, 200]
        self.pad = pad
        self.progress_pad = curses.newpad(pad[4], pad[5])
        self.n_row = n_row
        self.current_annotator = current_annotator
        self.file_names = csv_file.iloc[:, 0]

    def update(self, n_annotated, current_row, log="data/log.txt"):
        self.todo = self.n_row - n_annotated
        self.percent_done = int(100 * n_annotated / self.n_row)

        # get confidence ratings
        no_confidence_rating = []
        annotated_files = []
        with open(log, "r") as file:
            for line in file:
                if "NA" in line:
                    no_confidence_rating.append(line.split(", ")[0])
                elif "low" in line:
                    annotated_files.append(line.split(", ")[0] + "low")
                elif "medium" in line:
                    annotated_files.append(line.split(", ")[0] + "medium")
                elif "high" in line:
                    annotated_files.append(line.split(", ")[0] + "high")

                # does not load annotations form previous session. Maybe it's a problem with the refreshing of chars?

        self.progress_pad.addstr(2, 48, "Progress", curses.A_BOLD)
        self.progress_pad.addstr(4, 48, "|")
        self.progress_pad.addstr(4, 148, "| " + str(self.percent_done) + "%  ")

        index_used = -1
        for i in range(self.n_row):
            index = int(100 * i / self.n_row)
            if self.file_names[i] in no_confidence_rating:
                self.progress_pad.addstr(4, 49 + index, "x", curses.color_pair(1))
                index_used = index
            elif self.file_names[i] + "low" in annotated_files:
                self.progress_pad.addstr(4, 49 + index, "X", curses.color_pair(3))
                index_used = index

            elif self.file_names[i] + "medium" in annotated_files:
                self.progress_pad.addstr(4, 49 + index, "X", curses.color_pair(4))
                index_used = index

            elif self.file_names[i] + "high" in annotated_files:
                self.progress_pad.addstr(4, 49 + index, "X", curses.color_pair(5))
                index_used = index
            else:
                if index_used != index:
                    self.progress_pad.addch(4, 49 + index, "-")

        self.progress_pad.addch(4, 49 + int(current_row / self.n_row * 100), "#", curses.A_BLINK)
        self.progress_pad.addstr(6, 48, str(n_annotated) + " of " + str(self.n_row) + " text reports annotated.")
        self.progress_pad.addstr(6, 90, "Current User: ", curses.A_BOLD)
        self.progress_pad.addstr(6, 104, self.current_annotator)
        self.progress_pad.addstr(8, 48, "Report Text", curses.A_BOLD)
        self.progress_pad.refresh(self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])


class User(object):
    def __init__(self):
        """
        Asks for the user name before the main program is started. For now, default is Keno.
        """
        print("\n"
              "\n"
              "          +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              "          +                                                                           +\n"
              "          +               Welcome to the Radiology Report Annotator                   +\n"
              "          +                                                                           +\n"
              "          +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
              "\n"
              "          To track your individual annotations, please enter your name below: \n")

        self.name = input("          ")
        if self.name == "":
            self.name = "Annotator Anonymous"
        else:
            correct = "n"
            while correct != "y":
                print("\n"
                      "          Your name is: " + self.name + " Is that correct? \n")
                correct = input("          [y] (starts the Radiology Report Annotator) \n"
                                "          [n] (allows to reenter your name) \n"
                                "          [q] (quits the program)"
                                "\n \n"
                                "          ")
                if correct == "n":
                    self.name = input("          Please re-enter your name: \n "
                                      "\n"
                                      "          ")
                elif correct == "q":
                    exit()
        self.name = self.name.lower()

        self.file_name = "data/log.txt"

        if not os.path.isfile("data/log.txt"):
            with open(self.file_name, "w+") as file:
                file.write("Filename, annotator, confidence\n")

    def update_log(self, name_annotated_file, annotated, confidence):

        """

        Writes a log.txt (actually it's a csv file) about the annotation. First line are the headings (were already
        created on __init__). Then each annotated file is a row. First row-entry is the file name or path (depends on
        the master csv), Second entry is the name of the annotator. Third entry is the confidence in the annotation (
        high, medium, low).

        I'm not satisfied with the handling of the files. But after many (desperate) tries and failures to find more
        elegant ways, it will probably have to stay that way (for now, until I get better in file handling).

        :param name_annotated_file: A string name if the file, as written in the first column of the master csv file
        :param annotated: A bool. If True, a new line can be written or a current line replaced with updated
        information (like new annotator, new confidence rating). If False no new line will be written but if the line
        aready exists (aka the file has previously been annotated but the annotation is now deleted) the line will
        be deleted.

        :param confidence: A string (low, medium, high) giving the confidence of the rater in the finding.

        :return: nothing, writes a file to disk.

        """

        lines = []
        self.confidence = confidence

        with open("data/log.txt", "r+") as file:
            for line in file:
                lines.append(line)

        for i in range(len(lines)):
            if name_annotated_file in lines[i]:
                if not annotated:
                    lines[i] = ""
                else:
                    lines[i] = name_annotated_file + ", " + self.name + ", " + self.confidence + "\n"
                    break
            else:
                if i == (len(lines) - 1) and annotated:
                    lines.append(name_annotated_file + ", " + self.name + ", " + self.confidence + "\n")

        with open("data/log.txt", "w+") as file:
            for line in lines:
                file.writelines(line)


class Confidence(object):
    def __init__(self):
        self.level = "NA"

    def load_existing_level(self, csv_file, row, log="data/log.txt"):
        file_name = csv_file.iloc[row, 0]
        with open(log, "r") as file:
            for line in file:
                if line.startswith(file_name):
                    if "low" in line:
                        self.level = "low"
                    elif "medium" in line:
                        self.level = "medium"
                    elif "high" in line:
                        self.level = "high"
                    elif "NA" in line:
                        self.level = "NA"
                    break

    def toggle(self, up_or_down):
        if up_or_down == "up":
            if self.level == "low":
                self.level = "medium"
            elif self.level == "medium":
                self.level = "high"
            else:
                self.level = "low"
        elif up_or_down == "down":
            if self.level == "low":
                self.level = "high"
            elif self.level == "medium":
                self.level = "low"
            else:
                self.level = "medium"
        else:
            self.level = "NA"
