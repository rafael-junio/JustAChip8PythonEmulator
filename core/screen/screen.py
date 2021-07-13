import curses
import numpy as np
import time


class ScreenHandler:
    def __init__(self):
        self.stdscr = curses.initscr()

    def update_window(self, video_display):
        stringfill = f'{chr(9619)}'
        for index, x in np.ndenumerate(video_display):
            if int(x) == 0:
                if index[0] % 2 == 0:
                    self.stdscr.addstr(int(index[1]), int(index[0]), stringfill)
                    self.stdscr.addstr(int(index[1]), int(index[0] + 1), stringfill)
                    self.stdscr.refresh()
            else:
                if index[0] % 2 == 0:
                    self.stdscr.addstr(int(index[1]), int(index[0]), ' ')
                    self.stdscr.addstr(int(index[1]), int(index[0] + 1), ' ')
                    self.stdscr.refresh()