import sys
import PIL
import tkinter
import guiconfig
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter.colorchooser import *
from configparser import ConfigParser


def start_game_ai():
    """
    GUI window for AI strength and color
    """
    screen = Tk()
    screen.title("AI Manager")
    screen.geometry(guiconfig.strength_win)
    screen.geometry("+600+250")
    screen.resizable(False, False)
    screen.config(background=guiconfig.main_color)
    p1 = PhotoImage(file='../resc/chess_icon2.png')
    screen.iconphoto(False, p1)
    screen.focus_force()
    pval = IntVar()
    cval = IntVar()
    config = ConfigParser()
    config.read('../data/chess_options.ini')
    mainlbl = tkinter.Label(screen, text="Select AI Variant", bg=guiconfig.main_color, fg="white", anchor='center',
                            font=("Times New Roman", 18, "bold"), width=20)
    mainlbl.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

    def ai_config_game(event=""):
        """
        start game with selected values
        :param event: key press event bind
        """
        if int(pval.get()) != 0 and int(cval.get()) != 0:
            strn = reslbl.cget("text")
            clra = resclrlbl.cget("text")
            clra = "black" if clra == "White" else "white"
            config.set('ai_stats', 'ai_color', clra)
            config.set('ai_stats', 'ai_strength', strn)
            with open('../data/chess_options.ini', 'w') as config_file:
                config.write(config_file)

            screen.destroy()
            import view
            view.init_new_game()
        else:
            messagebox.showerror(title="Alert", message="Field Incomplete")
            screen.focus_force()

    def selclra():
        """
        Select color of AI by selecting your own color
        """
        clai = int(str(cval.get()))
        if clai == 1:
            clra = "White"
        elif clai == 2:
            clra = "Black"

        resclrlbl.config(text=clra)
        if clai == 1:
            clra = "black"
        elif clai == 2:
            clra = "white"

        config.set('ai_stats', 'ai_color', clra)
        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

    def selstrength():
        """
        Select variant of AI
        """
        strn = int(str(pval.get()))
        reslbl.config(text=str(pval.get()))
        config.set('ai_stats', 'ai_strength', str(strn))
        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

    image1 = Image.open("../resc/ai_icon2.png")
    image1 = image1.resize((35, 35), Image.ANTIALIAS)
    image1 = ImageTk.PhotoImage(image1)
    image2 = Image.open("../resc/ai_icon4.png")
    image2 = image2.resize((35, 35), Image.ANTIALIAS)
    image2 = ImageTk.PhotoImage(image2)
    image3 = Image.open("../resc/ai_icon6.png")
    image3 = image3.resize((35, 35), Image.ANTIALIAS)
    image3 = ImageTk.PhotoImage(image3)
    image4 = Image.open("../resc/ai_icon3.png")
    image4 = image4.resize((35, 35), Image.ANTIALIAS)
    image4 = ImageTk.PhotoImage(image4)
    image5 = Image.open("../resc/ai_icon1.png")
    image5 = image5.resize((35, 35), Image.ANTIALIAS)
    image5 = ImageTk.PhotoImage(image5)
    image6 = Image.open("../resc/ai_icon5.png")
    image6 = image6.resize((35, 35), Image.ANTIALIAS)
    image6 = ImageTk.PhotoImage(image6)
    mess1 = "\t" + "1 (1310)" + "\t"
    mess2 = "\t" + "2 (1500)" + "\t"
    mess3 = "\t" + "3 (1600)" + "\t"
    mess4 = "\t" + "4 (1710)" + "\t"
    mess5 = "\t" + "5 (1850)" + "\t"
    mess6 = "\t" + "6 (2020)" + "\t"
    PR1 = tkinter.Radiobutton(screen, text=mess1, image=image1, compound=RIGHT, highlightthickness=0, variable=pval,
                              value=1, bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT,
                              command=selstrength)
    PR1.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    PR2 = tkinter.Radiobutton(screen, text=mess2, image=image2, compound=RIGHT, highlightthickness=0, variable=pval,
                              value=2, bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT,
                              command=selstrength)
    PR2.grid(row=2, column=2, padx=5, pady=5, sticky='w')
    PR3 = tkinter.Radiobutton(screen, text=mess3, image=image3, compound=RIGHT, highlightthickness=0, variable=pval,
                              value=3, bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT,
                              command=selstrength)
    PR3.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    PR4 = tkinter.Radiobutton(screen, text=mess4, image=image4, compound=RIGHT, highlightthickness=0, variable=pval,
                              value=4, bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT,
                              command=selstrength)
    PR4.grid(row=3, column=2, padx=5, pady=5, sticky='w')
    PR5 = tkinter.Radiobutton(screen, text=mess5, image=image5, compound=RIGHT, highlightthickness=0, variable=pval,
                              value=5, bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT,
                              command=selstrength)
    PR5.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    PR6 = tkinter.Radiobutton(screen, text=mess6, image=image6, compound=RIGHT, highlightthickness=0, variable=pval,
                              value=6, bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT,
                              command=selstrength)
    PR6.grid(row=4, column=2, padx=5, pady=5, sticky='w')
    pval.set(2)
    reslbl = tkinter.Label(screen, text="---", width=5, bg="black", fg="white")
    reslbl.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
    reslbl.config(text=str(pval.get()))
    mclrlbl = tkinter.Label(screen, text="Play as", bg=guiconfig.main_color, fg="white", anchor='center',
                            font=("Times New Roman", 18, "bold"), width=20)
    mclrlbl.grid(row=8, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
    CR1 = tkinter.Radiobutton(screen, text="White", bg=guiconfig.main_color, fg="white", variable=cval, value=1,
                              command=selclra, highlightthickness=0)
    CR1.grid(row=9, column=1, padx=5, pady=5, sticky='e')
    CR2 = tkinter.Radiobutton(screen, text="Black", bg=guiconfig.main_color, fg="white", variable=cval, value=2,
                              command=selclra, highlightthickness=0)
    CR2.grid(row=9, column=2, padx=5, pady=5, sticky='w')
    cval.set(1)
    resclrlbl = tkinter.Label(screen, text="White", width=5, bg="black", fg="white")
    resclrlbl.grid(row=10, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
    sub = Button(screen, text="Go (↵)", width=10, command=ai_config_game)
    sub.grid(row=12, column=1, columnspan=2, padx=5, pady=5)
    config.set('ai_stats', 'ai_strength', str(pval.get()))
    with open('../data/chess_options.ini', 'w') as config_file:
        config.write(config_file)

    # bind enter key as shortcut to proceed
    screen.bind("<Return>", ai_config_game)
    screen.mainloop()


def start_game_human():
    """
    Start game with configuration selected for PvP
    """
    import view
    view.init_new_game()


def main():
    """
    GUI window for match configuration
    """
    screen = Tk()
    screen.title("Welcome")
    screen.geometry(guiconfig.main_screen)
    screen.geometry("+600+250")
    screen.resizable(False, False)
    screen.config(background=guiconfig.main_color)
    p1 = PhotoImage(file='../resc/chess_icon2.png')
    screen.iconphoto(False, p1)
    screen.focus_force()
    pval = IntVar()
    cval = IntVar()
    config = ConfigParser()
    config.read('../data/chess_options.ini')
    mainlbl = tkinter.Label(screen, text="Chess", bg=guiconfig.main_color, fg="white", anchor='center',
                            font=("Times New Roman", 18, "bold"))
    mainlbl.grid(row=1, column=2, padx=5, pady=5, sticky='EW')

    def selplayer():
        """
        Select opponent
        """
        ply = int(str(pval.get()))
        if ply == 1:
            resPR.config(text="Human")
            wtim.config(from_=1)
            btim.config(from_=1)
            wtim.set(config.get('chess_clock', 'white_clock'))
            btim.set(config.get('chess_clock', 'black_clock'))
            reswtim.config(text=wtim.get())
            resbtim.config(text=btim.get())
        elif ply == 2:
            resPR.config(text="Computer")
            cval.set(1)
            wtim.set(10)
            btim.set(10)
            wtim.config(from_=10)
            btim.config(from_=10)
            reswtim.config(text=wtim.get())
            resbtim.config(text=btim.get())

    def selwtim():
        """
        Select time on clock for white
        """
        wtt = wtim.get()
        reswtim.config(text=wtt)

    def selbtim():
        """
        Select time on clock for black
        """
        btt = btim.get()
        resbtim.config(text=btt)

    def set_color_1():
        """
        Select primary color of the board
        """
        boardcolor1 = askcolor()[-1]
        reswclr.config(bg=boardcolor1, fg=boardcolor1)

    def set_color_2():
        """
        Select secondary color of the board
        """
        boardcolor2 = askcolor()[-1]
        resbclr.config(bg=boardcolor2, fg=boardcolor2)

    def set_color_3():
        """
        Select highlight color for move in the board
        """
        boardcolor3 = askcolor()[-1]
        reshclr.config(bg=boardcolor3, fg=boardcolor3)

    def set_color_4():
        """
        Select last move highlight color for move in the board
        """
        boardcolor4 = askcolor()[-1]
        reshlmclr.config(bg=boardcolor4, fg=boardcolor4)

    def set_color_5():
        """
        Select main color scheme for the app
        """
        guiconfig.main_color = askcolor()[-1]
        screen.config(background=guiconfig.main_color)
        mainlbl.config(bg=guiconfig.main_color)
        playerlbl.config(bg=guiconfig.main_color)
        PR1.config(bg=guiconfig.main_color)
        PR2.config(bg=guiconfig.main_color)
        wtimelbl.config(bg=guiconfig.main_color)
        btimelbl.config(bg=guiconfig.main_color)
        wclrlbl.config(bg=guiconfig.main_color)
        bclrlbl.config(bg=guiconfig.main_color)
        hclrlbl.config(bg=guiconfig.main_color)
        hlmclrlbl.config(bg=guiconfig.main_color)
        mainclrlbl.config(bg=guiconfig.main_color)
        resmainclr.config(bg=guiconfig.main_color, fg=guiconfig.main_color)

    def config_game(event=""):
        """
        Configure match settings with the selected options
        :return: key press event bind
        """
        wc1 = reswclr.cget("bg")
        bc1 = resbclr.cget("bg")
        hc1 = reshclr.cget("bg")
        lmc = reshlmclr.cget("bg")
        wt1 = reswtim.cget("text")
        bt1 = resbtim.cget("text")
        if pval.get() != 0:
            if int(pval.get()) == 1:
                config.set('chess_colors', 'board_color_1', wc1)
                config.set('chess_colors', 'board_color_2', bc1)
                config.set('chess_colors', 'highlight_color', hc1)
                config.set('chess_colors', 'last_move_clr', lmc)
                config.set('chess_clock', 'white_clock', wt1)
                config.set('chess_clock', 'black_clock', bt1)
                config.set('ai_stats', 'is_ai', "False")
                with open('../data/chess_options.ini', 'w') as config_file:
                    config.write(config_file)

                screen.destroy()
                start_game_human()
            else:
                screen.destroy()
                config.set('ai_stats', 'is_ai', "True")
                with open('../data/chess_options.ini', 'w') as config_file:
                    config.write(config_file)

                start_game_ai()
        else:
            messagebox.showerror(title="Alert", message="Fields Incomplete")
            screen.focus_force()
            return

    playerlbl = tkinter.Label(screen, text="Play Against:", bg=guiconfig.main_color, fg="white", anchor='w',
                              justify=LEFT)
    playerlbl.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    PR1 = tkinter.Radiobutton(screen, text="Human", highlightthickness=0, variable=pval, value=1,
                              bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT, command=selplayer)
    PR1.grid(row=2, column=2, padx=5, pady=5, sticky='w')
    PR2 = tkinter.Radiobutton(screen, text="AI", highlightthickness=0, variable=pval, value=2, bg=guiconfig.main_color,
                              fg="white", justify=LEFT, anchor='w', command=selplayer)
    PR2.grid(row=2, column=3, padx=5, pady=5, sticky='w')
    resPR = tkinter.Label(screen, text="---", bg="black", fg="white", width=8)
    resPR.grid(row=2, column=4, padx=5, pady=5, sticky=W)
    resPR.config(text="Human")
    pval.set(1)
    wtimelbl = tkinter.Label(screen, text="White's Time(M):", bg=guiconfig.main_color, fg="white", anchor='w',
                             justify=LEFT)
    wtimelbl.grid(row=5, column=1, padx=5, pady=5, sticky='w')
    wtim = Spinbox(screen, from_=0, to=100, width=guiconfig.timer_width, command=selwtim)
    wtim.grid(row=5, column=2, padx=5, pady=5, columnspan=2, sticky='w')
    wtim.set(config.get('chess_clock', 'white_clock'))
    reswtim = tkinter.Label(screen, text="---", bg="black", fg="white", width=8)
    reswtim.grid(row=5, column=4, padx=5, pady=5, sticky=W)
    reswtim.config(text=wtim.get())
    btimelbl = tkinter.Label(screen, text="Black's Time(M):", bg=guiconfig.main_color, fg="white", anchor='w',
                             justify=LEFT)
    btimelbl.grid(row=6, column=1, padx=5, pady=5, sticky='w')
    btim = Spinbox(screen, from_=0, to=100, width=guiconfig.timer_width, command=selbtim)
    btim.grid(row=6, column=2, padx=5, pady=5, columnspan=2, sticky='w')
    btim.set(config.get('chess_clock', 'black_clock'))
    resbtim = tkinter.Label(screen, text="---", bg="black", fg="white", width=8)
    resbtim.grid(row=6, column=4, padx=5, pady=5, sticky=W)
    resbtim.config(text=btim.get())
    wclrlbl = tkinter.Label(screen, text="Primary Color:", bg=guiconfig.main_color, fg="white", anchor='w',
                            justify=LEFT)
    wclrlbl.grid(row=7, column=1, padx=5, pady=5, sticky='w')
    wclr = Button(screen, text='Color 1', width=20, command=set_color_1)
    wclr.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky='w')
    BOARDCOLOR1 = config.get('chess_colors', 'board_color_1', fallback="#DDB88C")
    reswclr = tkinter.Label(screen, text="---", bg=BOARDCOLOR1, fg=BOARDCOLOR1, width=8)
    reswclr.grid(row=7, column=4, padx=5, pady=5, sticky=W)
    bclrlbl = tkinter.Label(screen, text="Second Color:", bg=guiconfig.main_color, fg="white", anchor='w', justify=LEFT)
    bclrlbl.grid(row=8, column=1, padx=5, pady=5, sticky='w')
    bclr = Button(screen, text='Color 2', width=20, command=set_color_2)
    bclr.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky='w')
    BOARDCOLOR2 = config.get('chess_colors', 'board_color_2', fallback="#A66D4F")
    resbclr = tkinter.Label(screen, text="---", bg=BOARDCOLOR2, fg=BOARDCOLOR2, width=8)
    resbclr.grid(row=8, column=4, padx=5, pady=5, sticky=W)
    hclrlbl = tkinter.Label(screen, text="Highlight Color:", bg=guiconfig.main_color, fg="white", anchor='w',
                            justify=LEFT)
    hclrlbl.grid(row=9, column=1, padx=5, pady=5, sticky='w')
    hclr = Button(screen, text='Highlight Color', width=20, command=set_color_3)
    hclr.grid(row=9, column=2, columnspan=2, padx=5, pady=5, sticky='w')
    BOARDCOLORH = config.get('chess_colors', 'highlight_color', fallback="#2EF70D")
    reshclr = tkinter.Label(screen, text="---", bg=BOARDCOLORH, fg=BOARDCOLORH, width=8)
    reshclr.grid(row=9, column=4, padx=5, pady=5, sticky=W)
    hlmclrlbl = tkinter.Label(screen, text="Last Move Color:", bg=guiconfig.main_color, fg="white", anchor='w',
                              justify=LEFT)
    hlmclrlbl.grid(row=10, column=1, padx=5, pady=5, sticky='w')
    hlmclr = Button(screen, text='Last Move Color', width=20, command=set_color_4)
    hlmclr.grid(row=10, column=2, columnspan=2, padx=5, pady=5, sticky='w')
    BOARDCOLORHLM = config.get('chess_colors', 'last_move_clr', fallback="#34e89e")
    reshlmclr = tkinter.Label(screen, text="---", bg=BOARDCOLORHLM, fg=BOARDCOLORHLM, width=8)
    reshlmclr.grid(row=10, column=4, padx=5, pady=5, sticky=W)
    mainclrlbl = tkinter.Label(screen, text="Main Color:", bg=guiconfig.main_color, fg="white", anchor='w',
                               justify=LEFT)
    mainclrlbl.grid(row=11, column=1, columnspan=2, padx=5, pady=5, sticky='w')
    mainclr = Button(screen, text='Main Color', width=20, command=set_color_5)
    mainclr.grid(row=11, column=2, columnspan=2, padx=5, pady=5, sticky='w')
    resmainclr = tkinter.Label(screen, text="---", bg=guiconfig.main_color, fg=guiconfig.main_color, width=8)
    resmainclr.grid(row=11, column=4, padx=5, pady=5, sticky=W)
    resmainclr.config(highlightbackground="black", highlightcolor="black", borderwidth=2, relief="solid")
    sub = Button(screen, text="Start (↵)", width=20, command=config_game)
    sub.grid(row=12, column=2, columnspan=2, padx=5, pady=15, sticky='w')
    screen.bind("<Return>", config_game)

    def on_closing():
        """
        Monitor App close event
        """
        screen.destroy()

    # bind enter key as shortcut to proceed
    screen.protocol("WM_DELETE_WINDOW", on_closing)
    screen.mainloop()


if __name__ == "__main__":
    main()
