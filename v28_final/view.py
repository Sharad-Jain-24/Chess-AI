import sys
import multiprocessing
import threading
import time
import tkinter as tk
from tkinter import Tk, Menu, Canvas, messagebox, PhotoImage, filedialog

import chess
import pyautogui
from PIL import ImageTk, Image

import aimanager
import clockwindow
import configurations
import controller
import exceptions
import guiconfig
import model
import preferenceswindow
from configurations import *


class MoveTimer:
    try:
        def __init__(self):
            global clkstp
            clkstp = False
            self.stp = False

        def run(self):
            """
            Clock Thread starter
            """
            self.stp = False
            config = ConfigParser()
            config.read('../data/chess_options.ini')
            # gets time in seconds & converts to minutes
            wc = int(config.get('chess_clock', 'white_clock')) * 60
            bc = int(config.get('chess_clock', 'black_clock')) * 60
            self.countdown(wc, bc)

        def countdown(self, wc, bc):
            """
            Decrement Clock timer based on move made by player
            :param wc: white timer at present
            :param bc: black timer at present
            :return: victor based on time
            """
            global pt, clkstp
            while wc and bc:
                if not clkstp:
                    ai_move_made = False
                    if self.stp == True:
                        break

                    # black won on time
                    if wc <= 0:
                        View.time_out_win(vobj, 1)
                        break

                    # white won on time
                    if bc <= 0:
                        View.time_out_win(vobj, 2)
                        break

                    # decrement white timer
                    if pt == "white":
                        wm = int((wc / 60) % 60)
                        ws = int((wc) % 60)
                        wt = int((wc * 10) % 10)
                        wht = '{:02d}:{:02d}:{:0d}'.format(wm, ws, wt)
                        wc -= 0.01
                        c2.config(text=wht)
                        configurations.wctime = wht

                    # decrement black timer
                    if pt == "black":
                        bm = int((bc / 60) % 60)
                        bs = int((bc) % 60)
                        bt = int((bc * 10) % 10)
                        blk = '{:02d}:{:02d}:{:0d}'.format(bm, bs, bt)
                        bc -= 0.01
                        c1.config(text=blk)
                        configurations.bctime = blk

                time.sleep(0.01)

        def pause(self):
            """
            Pause timer for both players
            """
            global clkstp
            clkstp = not clkstp

        def resume(self):
            """
            Resume timer for both players
            """
            global clkstp
            clkstp = not clkstp

        def stop(self):
            """
            Stops timer for both players
            """
            self.stp = True

    except:
        pass


class View:
    images = {}
    vboard = chess.Board()
    board_color_1 = BOARD_COLOR_1
    board_color_2 = BOARD_COLOR_2
    selected_piece_position = None
    highlight_color = HIGHLIGHT_COLOR
    all_squares_to_be_highlighted = []

    def __init__(self, parent, controller):
        """
        Initialize GUI of board
        :param parent: root window to build upon for GUI
        :param controller: link to controller & model
        """
        global pt, CAI, click_button
        self.parent = parent
        self.controller = controller
        self.create_chess_base()
        pt = self.controller.player_turn()
        click_button = self.canvas.bind("<Button-1>", self.on_square_clicked)
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        isai = config.get('ai_stats', 'is_ai')
        if isai == "True":
            global send_to_ai
            send_to_ai.send([0, 0, 0, "new"])

        self.start_new_game()

    def last_move_highlight(self, sp, fp):
        """
        Highlights last move made by AI
        :param sp: Start position of piece moved
        :param fp: End position of piece moved
        """
        global last_start, last_end, flipflg
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        lmc = config.get('chess_colors', 'last_move_clr')
        if flipflg == 0:
            yy = (int(fp[1]) - 1)
            if fp[0] == "a":
                y = 0
            elif fp[0] == "b":
                y = 1
            elif fp[0] == "c":
                y = 2
            elif fp[0] == "d":
                y = 3
            elif fp[0] == "e":
                y = 4
            elif fp[0] == "f":
                y = 5
            elif fp[0] == "g":
                y = 6
            elif fp[0] == "h":
                y = 7

            x1, y1 = self.get_x_y_coordinate(yy, y)
            x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
            last_end = self.canvas.create_rectangle(x1, y1, x2, y2, outline=lmc, width=5, stipple="gray50")
            yy = (int(sp[1]) - 1)
            if sp[0] == "a":
                y = 0
            elif sp[0] == "b":
                y = 1
            elif sp[0] == "c":
                y = 2
            elif sp[0] == "d":
                y = 3
            elif sp[0] == "e":
                y = 4
            elif sp[0] == "f":
                y = 5
            elif sp[0] == "g":
                y = 6
            elif sp[0] == "h":
                y = 7

            x1, y1 = self.get_x_y_coordinate(yy, y)
            x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
            last_start = self.canvas.create_rectangle(x1, y1, x2, y2, outline=lmc, width=5, stipple="gray50")
        else:
            yy = 7 - (int(fp[1]) - 1)
            if fp[0] == "a":
                y = 7
            elif fp[0] == "b":
                y = 6
            elif fp[0] == "c":
                y = 5
            elif fp[0] == "d":
                y = 4
            elif fp[0] == "e":
                y = 3
            elif fp[0] == "f":
                y = 2
            elif fp[0] == "g":
                y = 1
            elif fp[0] == "h":
                y = 0

            x1, y1 = self.get_x_y_coordinate(yy, y)
            x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
            last_end = self.canvas.create_rectangle(x1, y1, x2, y2, outline=lmc, width=5, stipple="gray50")
            yy = 7 - (int(sp[1]) - 1)
            if sp[0] == "a":
                y = 7
            elif sp[0] == "b":
                y = 6
            elif sp[0] == "c":
                y = 5
            elif sp[0] == "d":
                y = 4
            elif sp[0] == "e":
                y = 3
            elif sp[0] == "f":
                y = 2
            elif sp[0] == "g":
                y = 1
            elif sp[0] == "h":
                y = 0

            x1, y1 = self.get_x_y_coordinate(yy, y)
            x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE - 2, y1 + DIMENSION_OF_EACH_SQUARE - 2
            last_start = self.canvas.create_rectangle(x1, y1, x2, y2, outline=lmc, width=5, stipple="gray50")

    def update_highlight_list(self, position):
        """
        Updates record of squares to be Highlighted when piece is clicked
        :param position: position of click
        """
        global pt
        mvs = []
        tmvs = []
        vmv = self.controller.get_board().legal_moves
        pt = self.controller.player_turn()
        self.all_squares_to_be_highlighted = None
        try:
            piece = self.controller.get_piece_at(position)
        except:
            piece = None

        if piece and (piece.color == self.controller.player_turn()):
            self.selected_piece_position = position
            self.all_squares_piece_position = position
            self.all_squares_to_be_highlighted = list(map(self.controller.get_numeric_notation,
                                                          self.controller.get_piece_at(position).moves_available(
                                                              position)))

            # recording square to be highlighted
            for i in vmv:
                i = str(i)
                curps = i[0] + i[1]
                if curps.upper() == position.upper():
                    reqmv = i[2] + i[3]
                    mvs.append(reqmv.upper())

            # updating squares to be highlighted
            for mv in self.all_squares_to_be_highlighted:
                mov = self.controller.get_alphanumeric_position(mv)
                if mov in mvs:
                    tmvs.append(mv)

            self.all_squares_to_be_highlighted = tmvs

    def shift(self, start_pos, end_pos):
        """
        Prepares board for change if move is made
        :param start_pos: Start position of piece moved
        :param end_pos: End position of piece moved
        """
        selected_piece = self.controller.get_piece_at(start_pos)
        piece_at_destination = self.controller.get_piece_at(end_pos)
        if not piece_at_destination or piece_at_destination.color != selected_piece.color:
            try:
                pmv = self.controller.pre_move_validation(start_pos, end_pos)
                if pmv == 1:
                    self.auto_flip_board()

            except exceptions.ChessError as error:
                pass
        else:
            pass

    def lead_pts_calc(self):
        """
        Calculate lead score and update label
        """
        global wpts, bpts
        bd = self.controller.get_board()
        wp = len(bd.pieces(chess.PAWN, chess.WHITE))
        bp = len(bd.pieces(chess.PAWN, chess.BLACK))
        wn = len(bd.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(bd.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(bd.pieces(chess.BISHOP, chess.WHITE))
        bb = len(bd.pieces(chess.BISHOP, chess.BLACK))
        wr = len(bd.pieces(chess.ROOK, chess.WHITE))
        br = len(bd.pieces(chess.ROOK, chess.BLACK))
        wq = len(bd.pieces(chess.QUEEN, chess.WHITE))
        bq = len(bd.pieces(chess.QUEEN, chess.BLACK))
        material = 1 * (wp - bp) + 3 * (wn - bn) + 3 * (wb - bb) + 5 * (wr - br) + 9 * (wq - bq)
        if material > 0:
            tpts = "+" + str(material)
            wpts.config(text=tpts)
            bpts.config(text="---")
        elif material < 0:
            material = -material
            tpts = "+" + str(material)
            bpts.config(text=tpts)
            wpts.config(text="---")
        else:
            wpts.config(text="---")
            bpts.config(text="---")

    def ai_update(self):
        """
        Call AI & recieve AI's move
        """
        global rec_form_ai
        mv = rec_form_ai.recv()
        if mv == "00":
            pass
        else:
            # for AI move of pawn promotion
            if len(mv) == 5:
                sp = mv[0] + mv[1]
                fp = mv[2] + mv[3]
                up = mv[4]
                if mv[3] == "8":
                    up = mv[4]
                    up = up.upper()
                else:
                    up = mv[4]

                config.set('ai_stats', 'promo', up)
                with open('../data/chess_options.ini', 'w') as config_file:
                    config.write(config_file)

                pmv = self.controller.pre_move_validation(sp, fp)

            # if AI move is normal
            else:
                sp = mv[0] + mv[1]
                fp = mv[2] + mv[3]
                pmv = self.controller.pre_move_validation(sp, fp)

            root.after(100, self.board_view_check)
            root.after(100, self.can_state_log)
            root.after(100, root.update())
            self.last_move_highlight(sp, fp)

        root.config(cursor='')
        global click_button
        click_button = self.canvas.bind("<Button-1>", self.on_square_clicked)

    def on_square_clicked(self, event):
        """
        Registers mouse clicks and determines piece on square
        :param event: mouse click event
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        mclr = guiconfig.main_color
        root.config(bg=mclr)
        clicked_row, clicked_column = self.get_clicked_row_column(event)
        global flipflg
        if flipflg == 1:
            clicked_row, clicked_column = self.flip_loc(clicked_row, clicked_column)

        position_of_click = self.controller.get_alphanumeric_position((clicked_row, clicked_column))
        # on second click
        if self.selected_piece_position:
            try:
                pmv = self.controller.pre_move_validation(self.selected_piece_position, position_of_click)
                if pmv == 1:
                    self.auto_flip_board()

            except:
                self.shift(self.selected_piece_position, position_of_click)
            finally:
                self.selected_piece_position = None

        self.update_highlight_list(position_of_click)
        self.board_view_check()
        self.can_state_log()
        pt = self.controller.player_turn()
        isai = config.get('ai_stats', 'is_ai')
        ai_color = config.get('ai_stats', 'ai_color')
        # if match against AI
        if isai == "True" and pt == ai_color and not model.Model.gameOver:
            global click_button, send_to_ai, rec_form_ai
            root.update()
            click_button = self.canvas.unbind("<Button-1>", click_button)
            bd = self.controller.get_board()
            mc = self.controller.get_lastmove()
            try:
                lm = bd.peek()
            except:
                lm = 0

            # start thread for AI
            Tai = threading.Thread(target=self.ai_update)
            Tai.setDaemon(True)
            Tai.start()
            root.configure(cursor="exchange #0000FF")
            send_to_ai.send([bd, mc, lm, False])

    def board_view_check(self):
        """
        Draws & updates board based on move made and orientation of board
        """
        global flipflg
        # normal orientation
        if flipflg == 0:
            self.draw_board()
            self.draw_all_pieces()

        # flipped orientation
        else:
            self.re_draw_board()
            self.re_draw_all_pieces()

        self.ai_checker_for_button()
        self.lead_pts_calc()

    def can_state_log(self):
        """
        Game Status Notification Caller
        """
        bd = self.controller.get_board()
        ll = len(list(bd.legal_moves))
        if ll == 0:
            global cntr
            if cntr == 0:
                self.state_log()

            cntr += 1
        else:
            self.state_log()

    def state_log(self):
        """
        Displays currents status of game
        """
        txtar.config(state="normal")
        txtar.delete(1.0, tk.END)
        moves = open('../data/temp_move_list_pgn.txt', 'r')
        lines = moves.readlines()
        count = 0
        # update GUI move log
        for line in lines:
            count += 1
            txtar.insert(tk.INSERT, line)

        moves.close()
        txtar.config(state="disabled")
        txtar.see("end")
        global click_button
        if configurations.STATE == 1:
            messg = "Draw by Insufficient Material"
            self.messg_del(messg)

        elif configurations.STATE == 2:
            messg = "CheckMate"
            self.messg_del(messg)

        elif configurations.STATE == 3:
            messg = "StaleMate"
            self.messg_del(messg)

        elif configurations.STATE == 4:
            messg = "Draw by 75 Move Rule"
            self.messg_del(messg)

        elif configurations.STATE == 5:
            messg = "Draw by Repetition"
            self.messg_del(messg)

    def not_saver(self):
        """
        Notification for PGN & FEN saving
        """
        val = messagebox.askyesno(title="Info", message="Save PGN ?")
        if val == True:
            self.on_save_pgn_menu_clicked()

        val = messagebox.askyesno(title="Info", message="Save FEN ?")
        if val == True:
            self.on_save_fen_menu_clicked()

    def messg_del(self, messg):
        """
        Notifies game over state & reason
        :param messg: content of notification
        """
        self.game_end()
        global click_button
        messagebox.showinfo(title="Info", message=messg)
        self.not_saver()
        val = messagebox.askyesno(title="Info", message="Game Over\n Play Again ?")
        if (val == True):
            self.on_new_game_menu_clicked()
        else:
            click_button = self.canvas.unbind("<Button-1>", click_button)

    def ai_checker_for_button(self):
        """
        Disables buttons of AI to ensure fairplay
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        isai = config.get('ai_stats', 'is_ai')
        if isai == "True":
            ai_color = config.get('ai_stats', 'ai_color')
            global wdb, wrb, bdb, brd
            if ai_color == "white":
                bdb.config(state="disabled")
                brb.config(state="disabled")
                wdb.config(state="disabled")
            else:
                wdb.config(state="disabled")
                wrb.config(state="disabled")
                bdb.config(state="disabled")

    def on_new_game_menu_clicked(self):
        """
        Start sequence for new game
        """
        global flipflg, txtar
        flipflg = 0
        configurations.STATE = 0
        txtar.config(state="normal")
        txtar.delete(1.0, tk.END)
        txtar.config(state="disabled")
        model.Model.lboard = chess.Board()
        self.start_new_game()

    def on_save_pgn_menu_clicked(self):
        """
        Save PGN with user desired name & in user selected directory
        """
        types = [('Text Document', '*.txt'), ('Post Game Notation', '*.pgn')]
        fd = filedialog.asksaveasfilename(filetype=types, defaultextension=types)
        if fd:
            f = open(fd, 'w')
            with open('../data/temp_move_list_pgn.txt', 'r') as firstfile, open(fd, 'a') as secondfile:
                for line in firstfile:
                    secondfile.write(line)

                messagebox.showinfo(title="Info", message="File Saved")

    def on_save_fen_menu_clicked(self):
        """
        Save FEN with user desired name & in user selected directory
        """
        types = [('Text Document', '*.txt'), ('Forsyth Edwardse Notation', '*.fen')]
        fd = filedialog.asksaveasfilename(filetype=types, defaultextension=types)
        if fd:
            f = open(fd, 'w')
            with open('../data/temp_move_list_fen.txt', 'r') as firstfile, open(fd, 'a') as secondfile:
                for line in firstfile:
                    secondfile.write(line)

                messagebox.showinfo(title="Info", message="File Saved")

    def auto_flip_board(self):
        """
        Flips board after every move
        """
        global autoflip
        if autoflip:
            time.sleep(0.25)
            global flipflg
            ptrn = self.controller.player_turn()
            if ptrn == "white" and flipflg == 1:
                self.on_flip_board_clicked()

            elif ptrn == "black" and flipflg == 0:
                self.on_flip_board_clicked()

    def on_auto_flip_board_clicked(self):
        """
        Auto flip toggler
        """
        global autoflip
        autoflip = not autoflip

    def on_flip_board_clicked(self):
        """
        Flip board
        """
        global flipflg
        if flipflg == 0:
            self.re_draw_board()
            self.re_draw_all_pieces()
            self.re_reposition_ent()
        else:
            self.draw_board()
            self.draw_all_pieces()
            self.reposition_ent()

        self.ai_checker_for_button()
        flipflg = int(not flipflg)

    def on_clock_off_menu_clicked(self):
        """
        Pause or Resume the game clock
        """
        global MT, clkstp
        if clkstp:
            MT.resume()
        else:
            MT.pause()

    def on_preference_menu_clicked(self):
        """
        GUI Customization window caller
        """
        self.show_preferences_window()

    def on_clock_menu_clicked(self):
        """
        Clock for next game setting window caller
        """
        clockwindow.Clockwindow(self)

    def on_exit_menu_clicked(self):
        """
        App Close sequence
        """
        val = messagebox.askyesno(title="Info", message="Are you Sure you want to exit ?")
        if val == True:
            self.game_end()
            self.not_saver()
            self.canvas.delete('all')
            root.destroy()
            import gc
            gc.collect()
            send_to_ai.send([0, 0, 0, True])
            sys.exit()

    def show_preferences_window(self):
        """
        GUI Customization window caller
        """
        preferenceswindow.PreferencesWindow(self)

    def on_instr_menu_clicked(self):
        """
        Display Game instructions
        """
        filei = open("../data/instructions.txt", "r")
        txt = filei.read()
        messagebox.showinfo(title="Instructions", message=txt)
        filei.close()

    def get_clicked_row_column(self, event):
        """
        Obtain Rank & File of square clicked
        :param event: mouse click event
        :return: x & y coordinates for board
        """
        col_size = row_size = DIMENSION_OF_EACH_SQUARE
        clicked_column = event.x // col_size
        clicked_row = 7 - (event.y // row_size)
        return (clicked_row, clicked_column)

    def get_x_y_coordinate(self, row, col):
        """
        Obtain x & y coordinates of square clicked
        :param row: x coordinate
        :param col: y coordinate
        :return: Rank & File coordinates for board
        """
        x = (col * DIMENSION_OF_EACH_SQUARE)
        y = ((7 - row) * DIMENSION_OF_EACH_SQUARE)
        return (x, y)

    def get_alternate_color(self, current_color):
        """
        Board color scheme loader
        :param current_color: color in use
        :return: color not in use
        """
        if current_color == self.board_color_2:
            next_color = self.board_color_1
        else:
            next_color = self.board_color_2

        return next_color

    def calculate_piece_coordinate(self, row, col):
        """
        Obtain Rank & File of piece clicked
        :param row: Rank
        :param col: File
        :return: x & y coordinates of piece
        """
        x0 = (col * DIMENSION_OF_EACH_SQUARE) + int(DIMENSION_OF_EACH_SQUARE / 2)
        y0 = ((7 - row) * DIMENSION_OF_EACH_SQUARE + int(DIMENSION_OF_EACH_SQUARE / 2))
        return (x0, y0)

    def create_chess_base(self):
        """
        Creates widgets for chess GUI
        """
        self.create_top_menu()
        self.create_canvas()
        self.draw_board()

    def create_top_menu(self):
        """
        Creates menu bar of chess GUI
        """
        self.menu_bar = Menu(self.parent)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_about_menu()

    def create_canvas(self):
        """
        Creates Board & move log widgets of chess
        """
        global txtar, c1, c2, wpts, bpts, wdb, wrb, bdb, brb, p1i, p2i
        canvas_width = (NUMBER_OF_COLUMNS * DIMENSION_OF_EACH_SQUARE)
        canvas_height = (NUMBER_OF_ROWS * DIMENSION_OF_EACH_SQUARE)
        self.parent.config(background=guiconfig.main_color)
        self.canvas = Canvas(self.parent, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0, padx=5, pady=(17, 5), sticky="NW")
        txtar = tk.Text(self.parent, height=guiconfig.movelog_h, width=guiconfig.movelog_w)
        txtar.grid(row=0, column=1, padx=5, pady=40, columnspan=5, sticky="NS")
        self.reposition_ent()
        self.ai_checker_for_button()

    def create_file_menu(self):
        """
        Creates menu bar elements of modification
        """
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Game", command=self.on_new_game_menu_clicked)
        self.file_menu.add_command(label="Save PGN", command=self.on_save_pgn_menu_clicked)
        self.file_menu.add_command(label="Save FEN", command=self.on_save_fen_menu_clicked)
        self.file_menu.add_command(label="Exit", command=self.on_exit_menu_clicked)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.parent.config(menu=self.menu_bar)

    def create_edit_menu(self):
        """
        Creates menu bar elements of settings
        """
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Auto Flip", command=self.on_auto_flip_board_clicked)
        self.edit_menu.add_command(label="Flip Board", command=self.on_flip_board_clicked)
        self.edit_menu.add_command(label="UI Settings", command=self.on_preference_menu_clicked)
        self.edit_menu.add_command(label="Clock ON-OFF", command=self.on_clock_off_menu_clicked)
        self.edit_menu.add_command(label="Clock Settings", command=self.on_clock_menu_clicked)
        self.menu_bar.add_cascade(label="Settings", menu=self.edit_menu)
        self.parent.config(menu=self.menu_bar)

    def create_about_menu(self):
        """
        Creates menu bar elements of instructions
        """
        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="Instructions", command=self.on_instr_menu_clicked)
        self.menu_bar.add_cascade(label="Help", menu=self.about_menu)
        self.parent.config(menu=self.menu_bar)

    def draw_board(self):
        """
        Draws board and labels edge square coordinates in normal orientation
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        current_color = config.get('chess_colors', 'board_color_2', fallback="#A66D4F")
        hcl = config.get('chess_colors', 'highlight_color')
        # for creating squares
        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
                # create highlight squares
                if self.all_squares_to_be_highlighted and (row, col) in self.all_squares_to_be_highlighted:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=hcl)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=current_color)

                current_color = self.get_alternate_color(current_color)

        # label edge square coordinates
        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                ft = "Times 10"
                rxy = x1 + 6, y1 + 58
                cxy = x1 + 6, y1 + 10
                if col == 0:
                    if row == 0:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="1", font=ft, fill=current_color)
                    elif row == 1:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="2", font=ft, fill=current_color)
                    elif row == 2:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="3", font=ft, fill=current_color)
                    elif row == 3:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="4", font=ft, fill=current_color)
                    elif row == 4:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="5", font=ft, fill=current_color)
                    elif row == 5:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="6", font=ft, fill=current_color)
                    elif row == 6:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="7", font=ft, fill=current_color)
                    elif row == 7:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="8", font=ft, fill=current_color)

                current_color = self.get_alternate_color(current_color)
                if row == 0:
                    if col == 0:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="A", font=ft, fill=current_color)
                    elif col == 1:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="B", font=ft, fill=self.get_alternate_color(current_color))
                    elif col == 2:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="C", font=ft, fill=current_color)
                    elif col == 3:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="D", font=ft, fill=self.get_alternate_color(current_color))
                    elif col == 4:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="E", font=ft, fill=current_color)
                    elif col == 5:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="F", font=ft, fill=self.get_alternate_color(current_color))
                    elif col == 6:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="G", font=ft, fill=current_color)
                    elif col == 7:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="H", font=ft, fill=self.get_alternate_color(current_color))

            current_color = self.get_alternate_color(current_color)

    def draw_single_piece(self, position, piece):
        """
        Loads 1 piece into the board in normal orientation
        :param position: position to place piece
        :param piece: piece to be placed
        """
        x, y = self.controller.get_numeric_notation(position)
        if piece:
            filename = "../pieces_image/{}_{}.png".format(piece.name.lower(), piece.color)
            if filename not in self.images:
                self.images[filename] = PhotoImage(file=filename)

            x0, y0 = self.calculate_piece_coordinate(x, y)
            try:
                self.canvas.create_image(x0, y0, image=self.images[filename], tags=("occupied"), anchor="c")
            except:
                self.canvas.create_image(x0, y0, image=self.images[filename])

    def draw_all_pieces(self):
        """
        Loads pieces into the board in normal orientation
        """
        self.canvas.delete("occupied")
        for position, piece in self.controller.get_all_pieces_on_chess_board():
            self.draw_single_piece(position, piece)

    def re_draw_board(self):
        """
        Draws board and labels edge square coordinates in flipped orientation
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        current_color = config.get('chess_colors', 'board_color_2', fallback="#A66D4F")
        hcl = config.get('chess_colors', 'highlight_color')
        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                r, c = self.flip_loc(row, col)
                x1, y1 = self.get_x_y_coordinate(r, c)
                x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
                if self.all_squares_to_be_highlighted and (row, col) in self.all_squares_to_be_highlighted:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=hcl)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=current_color)

                current_color = self.get_alternate_color(current_color)

        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                ft = "Times 10"
                rxy = x1 + 6, y1 + 58
                cxy = x1 + 6, y1 + 10
                if col == 0:
                    if row == 0:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="8", font=ft, fill=current_color)
                    elif row == 1:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="7", font=ft, fill=current_color)
                    elif row == 2:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="6", font=ft, fill=current_color)
                    elif row == 3:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="5", font=ft, fill=current_color)
                    elif row == 4:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="4", font=ft, fill=current_color)
                    elif row == 5:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="3", font=ft, fill=current_color)
                    elif row == 6:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="2", font=ft, fill=current_color)
                    elif row == 7:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(cxy, text="1", font=ft, fill=current_color)

                current_color = self.get_alternate_color(current_color)
                if row == 0:
                    if col == 0:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="H", font=ft, fill=current_color)
                    elif col == 1:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="G", font=ft, fill=self.get_alternate_color(current_color))
                    elif col == 2:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="F", font=ft, fill=current_color)
                    elif col == 3:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="E", font=ft, fill=self.get_alternate_color(current_color))
                    elif col == 4:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="D", font=ft, fill=current_color)
                    elif col == 5:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="C", font=ft, fill=self.get_alternate_color(current_color))
                    elif col == 6:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="B", font=ft, fill=current_color)
                    elif col == 7:
                        current_color = self.get_alternate_color(current_color)
                        self.canvas.create_text(rxy, text="A", font=ft, fill=self.get_alternate_color(current_color))

            current_color = self.get_alternate_color(current_color)

    def re_draw_single_piece(self, position, piece):
        """
        Loads 1 piece into the board in flipped orientation
        :param position: position to place piece
        :param piece: piece to be placed
        """
        x, y = self.controller.get_numeric_notation(position)
        x, y = self.flip_loc(x, y)
        if piece:
            filename = "../pieces_image/{}_{}.png".format(piece.name.lower(), piece.color)
            if filename not in self.images:
                self.images[filename] = PhotoImage(file=filename)

            x0, y0 = self.calculate_piece_coordinate(x, y)
            try:
                self.canvas.create_image(x0, y0, image=self.images[filename], tags=("occupied"), anchor="c")
            except:
                self.canvas.create_image(x0, y0, image=self.images[filename])

    def re_draw_all_pieces(self):
        """
        Loads pieces into the board in flipped orientation
        """
        self.canvas.delete("occupied")
        for position, piece in self.controller.get_all_pieces_on_chess_board():
            self.re_draw_single_piece(position, piece)

    def reposition_ent(self):
        """
        Loads player color based based in normal orientation
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        isai = config.get('ai_stats', 'is_ai')
        ai_color = config.get('ai_stats', 'ai_color')
        ai_strength = int(config.get('ai_stats', 'ai_strength'))
        global c1, c2, wpts, bpts, wdb, wrb, bdb, brb, p1i, p2i
        c1 = tk.Label(self.parent, text="0:00", width=10, bg="black", fg="white")
        c1.grid(row=0, column=2, padx=5, pady=9, sticky="NW")
        c1.config(text=configurations.bctime)
        brb = tk.Button(self.parent, text="Resign", width=10, command=self.black_won, bg="white", fg="black")
        brb.grid(row=0, column=3, padx=5, pady=5, sticky="S")
        bdb = tk.Button(self.parent, text="Draw", width=10, command=self.white_draw, bg="white", fg="black")
        bdb.grid(row=0, column=4, padx=5, pady=5, sticky="SE")
        wpts = tk.Label(self.parent, text="---", width=3, bg="white", fg="black")
        wpts.grid(row=0, column=5, padx=5, pady=(5, 9), sticky="SE")
        c2 = tk.Label(self.parent, text="0:00", width=10, bg="white", fg="black")
        c2.grid(row=0, column=2, padx=5, pady=(5, 9), sticky="SW")
        c2.config(text=configurations.wctime)
        wrb = tk.Button(self.parent, text="Resign", width=10, command=self.white_won, bg="black", fg="white")
        wrb.grid(row=0, column=3, padx=5, pady=5, sticky="N")
        wdb = tk.Button(self.parent, text="Draw", width=10, command=self.black_draw, bg="black", fg="white")
        wdb.grid(row=0, column=4, padx=5, pady=5, sticky="NE")
        bpts = tk.Label(self.parent, text="---", width=3, bg="black", fg="white")
        bpts.grid(row=0, column=5, padx=5, pady=8, sticky="NE")
        image2 = Image.open("../resc/human_icon1.png")
        image2 = image2.resize((20, 20), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image2)
        image1 = Image.open("../resc/human_icon2.png")
        image1 = image1.resize((20, 20), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)
        self.ai_checker_for_button()
        if isai == "True":
            if ai_strength == 1:
                image1 = Image.open("../resc/ai_icon2.png")
            elif ai_strength == 2:
                image1 = Image.open("../resc/ai_icon4.png")
            elif ai_strength == 3:
                image1 = Image.open("../resc/ai_icon6.png")
            elif ai_strength == 4:
                image1 = Image.open("../resc/ai_icon3.png")
            elif ai_strength == 5:
                image1 = Image.open("../resc/ai_icon1.png")
            elif ai_strength == 6:
                image1 = Image.open("../resc/ai_icon5.png")

            image1 = image1.resize((20, 20), Image.ANTIALIAS)
            image1 = ImageTk.PhotoImage(image1)
            if ai_color == "white":
                p1i = tk.Label(self.parent, image=image2)
                p1i.grid(row=0, column=1, padx=5, pady=10, sticky="NW")
                p1i.image = image2
                p2i = tk.Label(self.parent, image=image1)
                p2i.grid(row=0, column=1, padx=5, pady=(10, 9), sticky="SW")
                p2i.image = image1
            else:
                p1i = tk.Label(self.parent, image=image1)
                p1i.grid(row=0, column=1, padx=5, pady=10, sticky="NW")
                p1i.image = image1
                p2i = tk.Label(self.parent, image=image2)
                p2i.grid(row=0, column=1, padx=5, pady=(10, 9), sticky="SW")
                p2i.image = image2
        else:
            p1i = tk.Label(self.parent, image=image1)
            p1i.grid(row=0, column=1, padx=5, pady=10, sticky="NW")
            p1i.image = image1
            p2i = tk.Label(self.parent, image=image2)
            p2i.grid(row=0, column=1, padx=5, pady=(10, 9), sticky="SW")
            p2i.image = image2

    def re_reposition_ent(self):
        """
        Loads player color based based in flipped orientation
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        isai = config.get('ai_stats', 'is_ai')
        ai_color = config.get('ai_stats', 'ai_color')
        ai_strength = int(config.get('ai_stats', 'ai_strength'))
        global c1, c2, wpts, bpts, wdb, wrb, bdb, brb, p1i, p2i
        c1 = tk.Label(self.parent, text="0:00", width=10, bg="black", fg="white")
        c1.grid(row=0, column=2, padx=5, pady=9, sticky="SW")
        c1.config(text=configurations.bctime)
        brb = tk.Button(self.parent, text="Resign", width=10, command=self.black_won, bg="white", fg="black")
        brb.grid(row=0, column=3, padx=5, pady=5, sticky="N")
        bdb = tk.Button(self.parent, text="Draw", width=10, command=self.white_draw, bg="white", fg="black")
        bdb.grid(row=0, column=4, padx=5, pady=5, sticky="NE")
        wpts = tk.Label(self.parent, text="---", width=3, bg="white", fg="black")
        wpts.grid(row=0, column=5, padx=5, pady=8, sticky="NE")
        c2 = tk.Label(self.parent, text="0:00", width=10, bg="white", fg="black")
        c2.grid(row=0, column=2, padx=5, pady=9, sticky="NW")
        c2.config(text=configurations.wctime)
        wrb = tk.Button(self.parent, text="Resign", width=10, command=self.white_won, bg="black", fg="white")
        wrb.grid(row=0, column=3, padx=5, pady=5, sticky="S")
        wdb = tk.Button(self.parent, text="Draw", width=10, command=self.black_draw, bg="black", fg="white")
        wdb.grid(row=0, column=4, padx=5, pady=5, sticky="SE")
        bpts = tk.Label(self.parent, text="---", width=3, bg="black", fg="white")
        bpts.grid(row=0, column=5, padx=5, pady=9, sticky="SE")
        image2 = Image.open("../resc/human_icon1.png")
        image2 = image2.resize((20, 20), Image.ANTIALIAS)
        image2 = ImageTk.PhotoImage(image2)
        image1 = Image.open("../resc/human_icon2.png")
        image1 = image1.resize((20, 20), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)
        self.ai_checker_for_button()
        if isai == "True":
            if ai_strength == 1:
                image1 = Image.open("../resc/ai_icon2.png")
            elif ai_strength == 2:
                image1 = Image.open("../resc/ai_icon4.png")
            elif ai_strength == 3:
                image1 = Image.open("../resc/ai_icon6.png")
            elif ai_strength == 4:
                image1 = Image.open("../resc/ai_icon3.png")
            elif ai_strength == 5:
                image1 = Image.open("../resc/ai_icon1.png")
            elif ai_strength == 6:
                image1 = Image.open("../resc/ai_icon5.png")

            image1 = image1.resize((20, 20), Image.ANTIALIAS)
            image1 = ImageTk.PhotoImage(image1)
            if ai_color == "white":
                p1i = tk.Label(self.parent, image=image2)
                p1i.grid(row=0, column=1, padx=5, pady=10, sticky="SW")
                p1i.image = image2
                p2i = tk.Label(self.parent, image=image1)
                p2i.grid(row=0, column=1, padx=5, pady=(10, 9), sticky="NW")
                p2i.image = image1
            else:
                p1i = tk.Label(self.parent, image=image1)
                p1i.grid(row=0, column=1, padx=5, pady=10, sticky="SW")
                p1i.image = image1
                p2i = tk.Label(self.parent, image=image2)
                p2i.grid(row=0, column=1, padx=5, pady=(10, 9), sticky="NW")
                p2i.image = image2
        else:
            p1i = tk.Label(self.parent, image=image1)
            p1i.grid(row=0, column=1, padx=5, pady=10, sticky="SW")
            p1i.image = image1
            p2i = tk.Label(self.parent, image=image2)
            p2i.grid(row=0, column=1, padx=5, pady=(10, 9), sticky="NW")
            p2i.image = image2

    def flip_loc(self, x, y):
        """
        Flip values of x & y to be used for flipping
        :param x: x coordinate
        :param y: y coordinate
        :return: flipped values of x & y
        """
        x = 7 - x
        y = 7 - y
        return x, y

    def game_end(self):
        """
        Stoppping timer thread
        """
        global MT
        MT.stop()

    def file_reseter(self):
        """
        Reset game data related to castling
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        config.set('chess_moves', 'move_count', "0")
        config.set('castle_rights', 'wking_moved', "False")
        config.set('castle_rights', 'wrook1_moved', "False")
        config.set('castle_rights', 'wrook2_moved', "False")
        config.set('castle_rights', 'bking_moved', "False")
        config.set('castle_rights', 'brook1_moved', "False")
        config.set('castle_rights', 'brook2_moved', "False")
        config.set('draw_status', 'white_draw_offer', "False")
        config.set('draw_status', 'black_draw_offer', "False")
        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

    def start_new_game(self):
        """
        Creates all GUI elements and related functionality for new game
        """
        global T, MT, pt, txtar, wpts, bpts
        pt = self.controller.player_turn()
        pt = 'white'
        txtar.delete(1.0, tk.END)
        c1.config(text=White_Clock)
        c2.config(text=Black_Clock)
        self.file_reseter()
        open('../data/temp_move_list_pgn.txt', 'w').close()
        open('../data/temp_move_list_fen.txt', 'w').close()
        try:
            self.game_end()
        except:
            pass

        MT = MoveTimer()
        T = threading.Thread(target=MT.run)
        T.setDaemon(True)
        T.start()
        isai = config.get('ai_stats', 'is_ai')
        ai_color = config.get('ai_stats', 'ai_color')
        if isai == "True":
            MT.pause()
            global send_to_ai
            send_to_ai.send([0, 0, 0, "new"])
            self.ai_checker_for_button()

        if isai == "True" and ai_color == "white":
            self.on_flip_board_clicked()
            self.re_reposition_ent()
            pyautogui.click(500, 400)

        self.controller.reset_game_data()
        self.controller.reset_to_initial_locations()
        wpts.config(text="---")
        bpts.config(text="---")
        self.draw_all_pieces()

    def reload_colors(self, color_1, color_2, highlight_color):
        """
        Board color loader if color scheme is changed
        :param color_1: primary color
        :param color_2: secondary color
        :param highlight_color: highlight color
        """
        self.board_color_1 = color_1
        self.board_color_2 = color_2
        self.highlight_color = highlight_color
        self.draw_board()
        self.draw_all_pieces()

    def reload_clock(self, clock_1, clock_2):
        """
        Board clock loader if time is changed
        :param clock_1: white timer
        :param clock_2: black timer
        """
        self.clock_1 = clock_1
        self.clock_2 = clock_2

    def file_updater(self, messg):
        """
        Updates file if game state is changed
        :param messg: game state message to be inserted in file
        """
        fileu = open("../data/temp_move_list_pgn.txt", "a")
        histlen = self.controller.get_lastmove()
        # game state change related to white
        if histlen % 2 != 0:
            st = "\t" + messg
            fileu.write("\t")
            fileu.write(messg)
            txtar.config(state="normal")
            txtar.insert(tk.END, st)
            txtar.config(state="disabled")
        # game state change related to black
        else:
            st = "\n\t" + messg
            fileu.write("\n")
            fileu.write("\t")
            fileu.write(messg)
            txtar.config(state="normal")
            txtar.insert(tk.END, st)
            txtar.config(state="disabled")

        fileu.close()

    def adraw(self):
        """
        Draw by agreement monitor
        """
        messg = "1/2-1/2"
        self.file_updater(messg)
        messg = "Draw by Agreement"
        self.messg_del(messg)

    def white_draw(self):
        """
        Display Draw offer from white
        """
        val = messagebox.askyesno(title="Info", message="White Offered Draw, Accept ?")
        if val == True:
            self.adraw()

    def black_draw(self):
        """
        Display Draw offer from black
        """
        val = messagebox.askyesno(title="Info", message="Black Offered Draw, Accept ?")
        if val == True:
            self.adraw()

    def awin(self):
        """
        Display Victory message & cause
        """
        bd = self.controller.get_board()
        otcome = bd.result()
        self.file_updater(otcome)

    def white_won(self):
        """
        Black clickes Resign button
        """
        self.awin()
        messg = "White Won by Resignation"
        self.messg_del(messg)

    def black_won(self):
        """
        White clickes Resign button
        """
        self.awin()
        messg = "Black Won by Resignation"
        self.messg_del(messg)

    def time_out_win(self, ply):
        """
        Monitor for time out vicotry
        :param ply: winner color code
        """
        global txtar, click_button
        histlen = self.controller.get_lastmove()
        fileu = open("../data/temp_move_list_pgn.txt", "a")
        if ply == 1:
            to = "0-1"
            pcolor = "Black"

        elif ply == 2:
            to = "1-0"
            pcolor = "White"

        self.file_updater(to)
        messg = pcolor + " Won on Time"
        self.messg_del(messg)


def main(model):
    """
    Starts chess GUI
    :param model: link to controller
    """
    global send_to_ai, child_conn, ai_send_conn, rec_form_ai
    send_to_ai, child_conn = multiprocessing.Pipe()
    ai_send_conn, rec_form_ai = multiprocessing.Pipe()
    Thai = multiprocessing.Process(target=aimanager.start_process, args=(child_conn, ai_send_conn,))
    Thai.start()
    global root, vobj
    root = Tk()
    root.title("Chess")
    # root.geometry(guiconfig.board_screen)
    root.geometry("+400+200")
    # root.resizable(False, False)
    p1 = PhotoImage(file='../resc/chess_icon1.png')
    root.iconphoto(False, p1)
    root.focus_force()
    vobj = View(root, model)
    def on_closing():
        """
        Monitor for window close event
        """
        vobj.not_saver()
        vobj.file_reseter()
        root.destroy()
        send_to_ai.send([0, 0, 0, True])
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


def init_new_game():
    """
    Establish link with controller
    """
    initial_game_data = controller.Controller()
    main(initial_game_data)


global send_to_ai, child_conn, ai_send_conn, rec_form_ai
global root, pt, T, MT, flipflg, autoflip, clkstp, CAI, click_button, cntr
cntr = 0
flipflg = 0
clkstp = False
autoflip = False
if __name__ == "__main__":
    init_new_game()
