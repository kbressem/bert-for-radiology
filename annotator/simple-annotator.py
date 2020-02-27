#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import chdir
import os.path

import pandas as pd
import curses
import numpy as np
from helpers import is_annotated, Finding, RightSideMenu, MasterTable, fish, ProgressBar, User, Confidence

current_annotator = User()


class SimpleAnnotaor(object):
    def __init__(self):
        self.foo = "bar"

    def check_untypical_length(self, text):
        if len(text) < 250 or len(text) > 2000:
            return True
        else:
            return False


simple_annotator = SimpleAnnotaor()


def scroll_reports(key, row, n_row):
    if key == ord('n') or key == curses.KEY_RIGHT:
        if row < (n_row - 1):
            row += 1
    else:
        if row > 0:
            row -= 1
    return row


def finding_update(master_table, FindingCreator=Finding):
    findings = []
    for col in range(1, master_table.n_col):
        findings.append(FindingCreator(master_table.csv_file, col, master_table.row))

    return findings


def main(stdscr):
    curses.resize_term(100, 300)  # prevents crash from resizing if lower right panel border is not active terminal
    # size)

    curses.curs_set(0)
    stdscr.idcok(False)  # might reduce flashing
    stdscr.idlok(False)  # might reduce flashing

    # set color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)  # for non-evaluable findings
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # for NaN values
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)  # low confidence
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # medium confidence
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)  # high confidence


    # create new windows for menu, report, progressbar etc.
    menu_window = curses.newpad(200, 50)
    text_report_window = curses.newpad(400, 400)

    # init variables
    show_annotated = 0
    key_range = []

    # init classes
    # csv file with annotations, need to find a better name
    master_table = MasterTable('data/file_dir.csv')
    master_table.read_file()

    # print report text
    master_table.print_report(text_report_window)

    # Confidence ratings
    confidence = Confidence()

    # Progress Bar on top
    progress_bar = ProgressBar(master_table.n_row, current_annotator.name, master_table.csv_file)
    progress_bar.update(master_table.csv_file.iloc[:, 1].count(), master_table.row)

    # Right side Menu
    right_side_menu = RightSideMenu()
    right_side_menu.show_menu(menu_window, confidence.level)
    findings = finding_update(master_table)

    if len(findings) > 9:  # currently no more than 9 findings are supported (key 1 to 9)
        findings = findings[0:9]
        master_table.n_col = 10

    for item in findings:
        key_range.append(item.key)

    while 1:
        for item in findings:
            item.print_label(menu_window, ") ")

        key = stdscr.getch()

        if key in key_range:
            for finding in findings:
                if finding.key == key:
                    if finding.value != -1:
                        finding.toggle()
        elif key == ord('a'):
            for finding in findings:
                finding.value = 1
        elif key == ord('s'):
            for finding in findings:
                finding.value = 0
        elif key == ord('d'):
            for finding in findings:
                finding.value = np.NaN
        elif key == ord('x'):
            for finding in findings:
                finding.toggle_uninterpretable()

        elif key == ord('n') or key == curses.KEY_RIGHT or key == ord('v') or key == curses.KEY_LEFT:
            while 1:
                master_table.row = scroll_reports(key, master_table.row, master_table.n_row)
                findings = finding_update(master_table)
                confidence.load_existing_level(master_table.csv_file, master_table.row)
                if show_annotated == 1 and is_annotated(findings):
                    break
                elif show_annotated == 2 and not is_annotated(findings):
                    break
                elif show_annotated == 0:
                    break
                elif master_table.row in [0, master_table.n_row-1]:
                    break

        elif key == ord('A'):
            right_side_menu.show_only_annotated_toggle()
            if show_annotated in [0, 1]:
                show_annotated += 1
            else:
                show_annotated = 0
        elif key == ord('S'):
            right_side_menu.toggle_ai()
        elif key == curses.KEY_UP and not np.isnan(findings[1].value):
            confidence.toggle("up")
        elif key == curses.KEY_DOWN and not np.isnan(findings[1].value):
            confidence.toggle("down")
        elif key == ord('q'):
            curses.endwin()
            quit()
        elif key == ord('f'):
            fish()
        elif key == curses.KEY_MOUSE or key == curses.KEY_MOVE:
            curses.resize_term(100, 300)
            curses.flushinp()  # prevents endless flicker after mouse scrolling
        else:
            curses.flushinp()
            curses.resize_term(100, 300)

        if is_annotated(findings):
            for finding in findings:
                finding.NaN_to_0()
        else:
            confidence.toggle("delete")


        master_table.write_findings(findings)
        master_table.read_file()
        master_table.print_report(text_report_window)
        progress_bar.update(master_table.csv_file.iloc[:, 1].count(), master_table.row)
        current_annotator.update_log(master_table.file_name, is_annotated(findings), confidence.level)
        right_side_menu.show_menu(menu_window, confidence.level)


curses.wrapper(main)
