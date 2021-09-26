import sys
import tkinter
import guiconfig
import configurations
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from configparser import ConfigParser


class Clockwindow:
    def __init__(self, view):
        """
        Initialize Clock Customization window elements
        :param view: parent window
        """
        self.view = view
        self.parent = view.parent
        self.set_prefered_clock()
        self.create_clock_window()

    def set_prefered_clock(self):
        """
        Load Default clock Values
        """
        self.clock_1 = configurations.White_Clock
        self.clock_2 = configurations.Black_Clock

    def set_clock_1(self, c1):
        """
        Select clock 1 values
        :param c1: clock 1 value
        """
        self.clock_1 = c1
        self.clock_window.focus_force()

    def set_clock_2(self, c2):
        """
        Select clock 2 values
        :param c2: clock 2 value
        """
        self.clock_2 = c2
        self.clock_window.focus_force()

    def create_clock_window(self):
        """
        Create GUI window of timer selection
        """
        self.clock_window = Toplevel(self.parent)
        self.clock_window.title("Set Chess Clock")
        self.clock_window.geometry("+400+800")
        self.clock_window.config(bg=guiconfig.main_color)
        self.clock_window.focus_force()
        self.create_prefereces_list()
        self.clock_window.transient(self.parent)

    def create_prefereces_list(self):
        """
        Confirm selected values in clock timers
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        WCl = config.get('chess_clock', 'white_clock')
        BCl = config.get('chess_clock', 'black_clock')
        c1 = IntVar()
        c2 = IntVar()
        clbl1 = tkinter.Label(self.clock_window, text="White Timmer", bg=guiconfig.main_color)
        clbl1.grid(row=1, sticky=W, padx=5, pady=5)
        clbl2 = tkinter.Label(self.clock_window, text="Black Timmer", bg=guiconfig.main_color)
        clbl2.grid(row=2, sticky=W, padx=5, pady=5)
        c1 = Spinbox(self.clock_window, from_=0, to=100, width=5)
        c1.grid(row=1, column=3, padx=5, pady=5, sticky=E)
        c1.set(config.get('chess_clock', 'white_clock'))
        c2 = Spinbox(self.clock_window, from_=0, to=100, width=5)
        c2.grid(row=2, column=3, padx=5, pady=5, sticky=E)
        c2.set(config.get('chess_clock', 'black_clock'))
        self.board_clock_1_button = Button(self.clock_window, text='Select White Timmer',
                                           command=lambda: self.set_clock_1(c1.get()))
        self.board_clock_1_button.grid(row=1, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        self.board_clock_2_button = Button(self.clock_window, text='Select Black Timmer',
                                           command=lambda: self.set_clock_2(c2.get()))
        self.board_clock_2_button.grid(row=2, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        Button(self.clock_window, text="Save", command=self.on_save_button_clicked).grid(row=4, column=2, sticky=E,
                                                                                         padx=5, pady=5)
        Button(self.clock_window, text="Cancel", command=self.on_cancel_button_clicked).grid(row=4, column=1, sticky=E,
                                                                                             padx=5, pady=5)

    def on_save_button_clicked(self):
        """
        Save Changes
        """
        self.set_new_values()
        self.clock_window.destroy()
        self.view.reload_clock(self.clock_1, self.clock_2)

    def set_new_values(self):
        """
        Load Changes
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        config.set('chess_clock', 'white_clock', self.clock_1)
        config.set('chess_clock', 'black_clock', self.clock_2)
        configurations.White_Clock = self.clock_1
        configurations.Black_Clock = self.clock_2
        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

    def on_cancel_button_clicked(self):
        """
        Destroy window
        """
        self.clock_window.destroy()
