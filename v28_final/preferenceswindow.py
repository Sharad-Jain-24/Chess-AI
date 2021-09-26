import sys
import tkinter
import guiconfig
import configurations
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.colorchooser import *
from configparser import ConfigParser


class PreferencesWindow:
    def __init__(self, view):
        """
        Initialize UI Customization window elements
        :param view: parent window
        """
        self.view = view
        self.parent = view.parent
        self.fill_preference_colors()
        self.create_prefereces_window()

    def fill_preference_colors(self):
        """
        Present color scheme
        """
        self.board_color_1 = configurations.BOARD_COLOR_1
        self.board_color_2 = configurations.BOARD_COLOR_2
        self.highlight_color = configurations.HIGHLIGHT_COLOR
        self.last_mclr = configurations.LASTMOVECLR

    def set_color_1(self):
        """
        Select primary color of the board
        """
        self.board_color_1 = askcolor(initialcolor=self.board_color_1)[-1]
        cc1.config(fg=self.board_color_1, bg=self.board_color_1)
        self.pref_window.focus_force()

    def set_color_2(self):
        """
        Select secondary color of the board
        """
        self.board_color_2 = askcolor(initialcolor=self.board_color_2)[-1]
        cc2.config(fg=self.board_color_2, bg=self.board_color_2)
        self.pref_window.focus_force()

    def set_highlight_color(self):
        """
        Select highlight move color of the board
        """
        self.highlight_color = askcolor(initialcolor=self.highlight_color)[-1]
        cc3.config(fg=self.highlight_color, bg=self.highlight_color)
        self.pref_window.focus_force()

    def set_hlm_color(self):
        """
        Select last move highlight color of the board
        """
        self.last_mclr = askcolor(initialcolor=self.last_mclr)[-1]
        cc4.config(fg=self.last_mclr, bg=self.last_mclr)
        self.pref_window.focus_force()

    def set_main_color(self):
        """
        Select main color scheme of the board
        """
        self.main_mclr = askcolor(initialcolor=guiconfig.main_color)[-1]
        guiconfig.main_color = self.main_mclr
        c1lbl.config(bg=self.main_mclr)
        c2lbl.config(bg=self.main_mclr)
        c3lbl.config(bg=self.main_mclr)
        c4lbl.config(bg=self.main_mclr)
        c5lbl.config(bg=self.main_mclr)
        self.pref_window.config(bg=self.main_mclr)
        cc5.config(fg=self.main_mclr, bg=self.main_mclr)
        self.pref_window.focus_force()

    def create_prefereces_window(self):
        """
        Create GUI window UI Customization
        """
        self.pref_window = Toplevel(self.parent)
        self.pref_window.title("Set Chess UI")
        self.pref_window.geometry("+800+800")
        self.pref_window.config(bg=guiconfig.main_color)
        self.pref_window.focus_force()
        self.create_prefereces_list()
        self.pref_window.transient(self.parent)

    def create_prefereces_list(self):
        """
        Confirm Selection of color scheme
        """
        global cc1, cc2, cc3, cc4, cc5, c1lbl, c2lbl, c3lbl, c4lbl, c5lbl
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        c1lbl = tkinter.Label(self.pref_window, text="Board Color 1")
        c1lbl.config(bg=guiconfig.main_color)
        c1lbl.grid(row=1, sticky=W, padx=5, pady=5)
        c2lbl = tkinter.Label(self.pref_window, text="Board Color 2")
        c2lbl.config(bg=guiconfig.main_color)
        c2lbl.grid(row=2, sticky=W, padx=5, pady=5)
        c3lbl = tkinter.Label(self.pref_window, text="Highlight Color")
        c3lbl.config(bg=guiconfig.main_color)
        c3lbl.grid(row=3, sticky=W, padx=5, pady=5)
        c4lbl = tkinter.Label(self.pref_window, text="Last Move Color")
        c4lbl.config(bg=guiconfig.main_color)
        c4lbl.grid(row=4, sticky=W, padx=5, pady=5)
        c5lbl = tkinter.Label(self.pref_window, text="Main Color")
        c5lbl.config(bg=guiconfig.main_color)
        c5lbl.grid(row=5, sticky=W, padx=5, pady=5)
        self.board_color_1_button = Button(self.pref_window, text='Select Board Color 1', command=self.set_color_1)
        self.board_color_1_button.grid(row=1, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        self.board_color_2_button = Button(self.pref_window, text='Select Board Color 2', command=self.set_color_2)
        self.board_color_2_button.grid(row=2, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        self.highlight_color_button = Button(self.pref_window, text='Select Highlight Color',
                                             command=self.set_highlight_color)
        self.highlight_color_button.grid(row=3, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        self.hlastmove_color_button = Button(self.pref_window, text='Select Last Move Color',
                                             command=self.set_hlm_color)
        self.hlastmove_color_button.grid(row=4, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        self.main_mclr_button = Button(self.pref_window, text='Select Main Color', command=self.set_main_color)
        self.main_mclr_button.grid(row=5, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        BOARDCOLOR1 = config.get('chess_colors', 'board_color_1', fallback="#DDB88C")
        cc1 = tkinter.Label(self.pref_window, text="---", bg=BOARDCOLOR1, fg=BOARDCOLOR1)
        cc1.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        BOARDCOLOR2 = config.get('chess_colors', 'board_color_2', fallback="#DDB88C")
        cc2 = tkinter.Label(self.pref_window, text="---", bg=BOARDCOLOR2, fg=BOARDCOLOR2)
        cc2.grid(row=2, column=3, sticky=W, padx=5, pady=5)
        HIGHLIGHT_COLOR = config.get('chess_colors', 'highlight_color', fallback="#2EF70D")
        cc3 = tkinter.Label(self.pref_window, text="---", bg=HIGHLIGHT_COLOR, fg=HIGHLIGHT_COLOR)
        cc3.grid(row=3, column=3, sticky=W, padx=5, pady=5)
        LASTMOVECLR = config.get('chess_colors', 'last_move_clr', fallback="#34e89e")
        cc4 = tkinter.Label(self.pref_window, text="---", bg=LASTMOVECLR, fg=LASTMOVECLR)
        cc4.grid(row=4, column=3, sticky=W, padx=5, pady=5)
        cc5 = tkinter.Label(self.pref_window, text="---", bg=guiconfig.main_color, fg=guiconfig.main_color)
        cc5.config(highlightbackground="black", highlightcolor="black", borderwidth=2, relief="solid")
        cc5.grid(row=5, column=3, sticky=W, padx=5, pady=5)
        Button(self.pref_window, text="Save", command=self.on_save_button_clicked).grid(row=6, column=2, sticky=E,
                                                                                        padx=5, pady=5)
        Button(self.pref_window, text="Cancel", command=self.on_cancel_button_clicked).grid(row=6, column=1, sticky=E,
                                                                                            padx=5, pady=5)

    def on_save_button_clicked(self):
        """
        Save Changes
        """
        self.set_new_values()
        self.pref_window.destroy()
        self.view.reload_colors(self.board_color_1, self.board_color_2, self.highlight_color)

    def set_new_values(self):
        """
        Load Changes
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        config.set('chess_colors', 'board_color_1', self.board_color_1)
        config.set('chess_colors', 'board_color_2', self.board_color_2)
        config.set('chess_colors', 'highlight_color', self.highlight_color)
        config.set('chess_colors', 'last_move_clr', self.last_mclr)
        configurations.BOARD_COLOR_1 = self.board_color_1
        configurations.BOARD_COLOR_2 = self.board_color_2
        configurations.HIGHLIGHT_COLOR = self.highlight_color
        configurations.LASTMOVECLR = self.last_mclr
        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

    def on_cancel_button_clicked(self):
        """
        Destroy window
        """
        self.pref_window.destroy()
