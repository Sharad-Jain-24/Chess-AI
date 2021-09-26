import tkinter as tk
from copy import deepcopy

import chess

import configurations
import exceptions
import guiconfig
import piece
from configurations import *


class Model(dict):
    who_player = None
    player_turn = 'white'
    halfmove_clock = 0
    fullmove_number = 1
    lboard = chess.Board()
    move_text = ""
    count = 0
    enpass_possible = 0
    gameOver = False
    checkStatus = False
    enpass_move_made = False
    history = []
    moveType = []
    prev_enpass = []
    enpass_square = []
    tmp_attack_square = []
    enpass_start_square = []

    def __init__(self):
        """
        Initialize model and set pieces at start position
        :return:
        """
        self.reset_to_initial_locations()

    def get_piece_at(self, position):
        """
        Gets piece at a give position
        :param position: coordinate of click
        :return: piece name
        """
        return self.get(position)

    def get_alphanumeric_position(self, rowcol):
        """
        Gives alphanumeric position of board using x, y coordinates
        :param rowcol: x, y coordinates
        :return: alphanumeric notation
        """
        if self.is_on_board(rowcol):
            row, col = rowcol
            return "{}{}".format(X_AXIS_LABELS[col], Y_AXIS_LABELS[row])

    def get_all_available_moves(self, color):
        """
        Gets all available moves of 1 player
        :param color: player by color
        :return: all available moves
        """
        result = []
        for position in self.keys():
            piece = self.get_piece_at(position)
            if piece and piece.color == color:
                moves = piece.moves_available(position)
                if moves:
                    result.extend(moves)

        return result

    def is_on_board(self, rowcol):
        """
        Checks if generated move is within the board
        :param rowcol: x, y coordinates
        :return: is inside board
        """
        row, col = rowcol
        return 0 <= row <= 7 and 0 <= col <= 7

    def reset_game_data(self):
        """
        Resets operational data to initial state
        """
        self.history = []
        self.moveType = []
        self.prev_enpass = []
        self.gameOver = False
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.player_turn = 'white'

    def reset_to_initial_locations(self):
        """
        Reset piece location back to start position
        """
        self.clear()
        for position, value in START_PIECES_POSITION.items():
            self[position] = piece.create_piece(value)
            self[position].keep_reference(self)

        Model.count = 0
        self.gameOver = False
        self.who_player = None
        self.player_turn = 'white'

    def all_positions_occupied_by_color(self, color):
        """
        Get positions already occupied by other player pieces
        :param color: other player color
        :return: positions occupied by other player pieces
        """
        result = []
        # access dictionary to find piece location
        for position in self.keys():
            piece = self.get_piece_at(position)
            if piece.color == color:
                result.append(position)

        return result

    def all_occupied_positions(self):
        """
        Get all occupied square
        :return: occupied squares
        """
        return self.all_positions_occupied_by_color("white") + self.all_positions_occupied_by_color('black')

    def move(self, start_pos, final_pos):
        """
        Makes the move in the board and updates dictionary accordingly
        :param start_pos: start position of piece
        :param final_pos: end position of piece
        """
        # move count
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        mcnt = int(config.get('chess_moves', 'move_count'))
        mcnt += 1
        config.set('chess_moves', 'move_count', str(mcnt))
        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

        # check for enpassant possiblity
        try:
            mt = self.moveType[-1]
            if mt == "Enpassant Move":
                self.enpass_possible = 0
            else:
                pass
        except:
            pass

        # if normal move
        if self.enpass_possible == 0:
            self[final_pos] = self.pop(start_pos, None)

        # if enpassant move
        elif self.enpass_possible > 0:
            try:
                self[final_pos] = self.pop(start_pos, None)
                at = self.enpass_square[-1]
                ta = self.tmp_attack_square[-1]
                sp = self.enpass_start_square[-1]
                if final_pos == at:
                    if mt == "Double Forward Move":
                        self.pop(ta, None)
                        self.enpass_move_made = True
                        self.keep_reference(self)

            except:
                pass

        self.enpass_possible = 0

    def enpass_reset(self):
        """
        Reset enpassant rights if move made is not enpassant
        """
        self.enpass_possible = 0
        self.enpass_move_made = False
        self.enpass_square.clear()
        self.tmp_attack_square.clear()
        self.enpass_start_square.clear()

    def do_promotion(self, col):
        """
        GUI for pawn promotion window
        :param col: color of promoting piece
        :return: promoted piece name
        """
        global pval
        pval = ""

        def confirm_piece():
            """
            Confirms piece to be promoted into
            """
            pval = val.get()

        screen = tk.Toplevel()
        if col == 1:
            screen.title("White Promotion")
        elif col == 2:
            screen.title("Black Promotion")

        screen.geometry("180x100")
        screen.geometry("+400+200")
        screen.config(bg=guiconfig.main_color)
        screen.focus_force()
        tk.Label(screen, text="Promote To:", bg=guiconfig.main_color).grid(row=1, column=1, padx=5, pady=5)
        val = tk.StringVar()
        svar = tk.IntVar()
        piece_choosen = tk.ttk.Combobox(screen, width="10", textvariable=val)
        piece_choosen.grid(row=1, column=2, padx=5, pady=5)
        piece_choosen['values'] = ("Queen", "Rook", "Knight", "Bishop")
        piece_choosen.current(0)
        btn = tk.Button(screen, text="OK", command=lambda: svar.set(1))
        btn.grid(row=2, column=1, padx=5, pady=5)
        btn.wait_variable(svar)
        confirm_piece()
        self.moveType.append("Promotion")
        screen.destroy()
        return val.get()

    def update_promotion(self, pnames, colr):
        """
        Update dictionary of promotion and new piece deployment
        :param pnames: Piece name
        :param colr: piece color
        """
        for position, value in self.items():
            # for white promotion
            if position[1] == "8":
                if str(type(value)) == "<class 'piece.Pawn'>":
                    if colr == 1:
                        if pnames[0] == "K":
                            self[position] = piece.create_piece("N")
                        else:
                            self[position] = piece.create_piece(pnames[0])

                        self[position].keep_reference(self)

            # for black promotion
            if position[1] == "1":
                if str(type(value)) == "<class 'piece.Pawn'>":
                    if colr == 2:
                        if pnames[0] == "K":
                            self[position] = piece.create_piece("n")
                        else:
                            self[position] = piece.create_piece(pnames[0].lower())

                        self[position].keep_reference(self)

    def do_castle(self, val):
        """
        Update Dictionary & operational data that castling move has been made
        and updating the castling rights
        :param val: notation value of move
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        v = val[0] + val[2] + val[3]
        for position, value in self.items():
            # white king side castling
            if position[1] == v[2] == "1":
                if v[1] == "g":
                    if (str(type(value)) == "<class 'piece.Rook'>") and (position == "H1"):
                        pos = 'F1'
                        self.pop(position)
                        self[pos] = piece.create_piece("R")
                        self[pos].keep_reference(self)
                        config.set('castle_rights', 'wking_moved', "True")
                        config.set('castle_rights', 'wrook2_moved', "True")
                        break

            # black king side castling
            if position[1] == v[2] == "8":
                if v[1] == "g":
                    if (str(type(value)) == "<class 'piece.Rook'>") and (position == "H8"):
                        pos = 'F8'
                        self.pop(position)
                        self[pos] = piece.create_piece("r")
                        self[pos].keep_reference(self)
                        config.set('castle_rights', 'bking_moved', "True")
                        config.set('castle_rights', 'brook2_moved', "True")
                        break

            # white queen side castling
            if position[1] == v[2] == "1":
                if v[1] == "c":
                    if (str(type(value)) == "<class 'piece.Rook'>") and (position == "A1"):
                        pos = 'D1'
                        self.pop(position)
                        self[pos] = piece.create_piece("R")
                        self[pos].keep_reference(self)
                        config.set('castle_rights', 'wking_moved', "True")
                        config.set('castle_rights', 'wrook1_moved', "True")
                        break

            # black queen side castling
            if position[1] == v[2] == "8":
                if v[1] == "c":
                    if (str(type(value)) == "<class 'piece.Rook'>") and (position == "A8"):
                        pos = 'D8'
                        self.pop(position)
                        self[pos] = piece.create_piece("r")
                        self[pos].keep_reference(self)
                        config.set('castle_rights', 'bking_moved', "True")
                        config.set('castle_rights', 'brook1_moved', "True")
                        break

        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

    def update_game_statistics(self, piece, dest, start_pos, end_pos):
        """
        Generate move notation for model use, castling, enpassant
        rights updation
        :param piece: piece being moved
        :param dest: free or occupied square
        :param start_pos: start position of piece
        :param end_pos: end position of piece
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        isai = config.get('ai_stats', 'is_ai')
        ispr = config.get('ai_stats', 'promo')
        aicr = config.get('ai_stats', 'ai_color')
        if piece.color == 'black':
            self.fullmove_number += 1

        self.halfmove_clock += 1
        abbr = piece.name
        abr = piece.name[0].upper()
        if (abbr == "KNIGHT") or (abbr == "knight"):
            abr = "N"
            self.moveType.append("Knight Move")
            self.enpass_reset()

        if (abbr == "BISHOP") or (abbr == "bishop"):
            abr = "B"
            self.moveType.append("Bishop Move")
            self.enpass_reset()

        if (abbr == "ROOK") or (abbr == "rook"):
            abr = "R"
            self.moveType.append("Rook Move")
            # updating castling rights if piece moved is rook
            if piece.color == "white":
                if start_pos == "A1":
                    White_Rook1_moved = "True"
                    config.set('castle_rights', 'wrook1_moved', "True")

                if start_pos == "H1":
                    White_Rook2_moved = "True"
                    config.set('castle_rights', 'wrook2_moved', "True")

            if piece.color == "black":
                if start_pos == "A8":
                    Black_Rook1_moved = "True"
                    config.set('castle_rights', 'brook1_moved', "True")

                if start_pos == "H8":
                    Black_Rook2_moved = "True"
                    config.set('castle_rights', 'brook2_moved', "True")

            self.enpass_reset()

        if (abbr == "KING") or (abbr == "king"):
            abr = "K"
            self.moveType.append("King Move")
            # updating castling rights if piece moved is king
            if piece.color == "white":
                White_King_moved = "True"
                config.set('castle_rights', 'wking_moved', "True")

            if piece.color == "black":
                Black_King_moved = "True"
                config.set('castle_rights', 'bking_moved', "True")

            self.enpass_reset()

        if (abbr == "QUEEN") or (abbr == "queen"):
            abr = "Q"
            self.moveType.append("Queen Move")
            self.enpass_reset()

        if (abbr == "pawn") or (abbr == "PAWN"):
            abr = ''
            self.halfmove_clock = 0

        # check if destination square is free
        if dest is None:
            if (abbr == "PAWN") or (abbr == "pawn") or (abr == ''):
                # white pawn promotion notation
                if end_pos[1] == "8":
                    if isai == "True" and aicr == self.player_turn:
                        self.move_text = abr + end_pos.lower() + "=" + ispr
                        self.update_promotion(ispr, 1)
                    else:
                        pval = self.do_promotion(1)
                        piece.name = pval
                        pname = piece.name[0]
                        if (piece.name == "Knight"):
                            pname = "N"
                            self.enpass_reset()

                        self.move_text = abr + end_pos.lower() + "=" + pname
                        self.update_promotion(piece.name, 1)

                # black pawn promotion notation
                if end_pos[1] == "1":
                    if isai == "True" and aicr == self.player_turn:
                        self.move_text = abr + end_pos.lower() + "=" + ispr
                        self.update_promotion(ispr, 2)
                    else:
                        pval = self.do_promotion(2)
                        piece.name = pval
                        pname = piece.name[0]
                        if piece.name == "Knight":
                            pname = "N"
                            self.enpass_reset()

                        self.move_text = abr + end_pos.lower() + "=" + pname
                        self.update_promotion(piece.name, 2)

                if (end_pos[1] != "1") and (end_pos[1] != "8"):
                    d = abs(int(end_pos[1]) - int(start_pos[1]))
                    if self.enpass_move_made == True:
                        self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower()
                        self.moveType.append("Enpassant Move")
                        self.enpass_possible = 0

                    if d == 2:
                        self.move_text = abr + end_pos.lower()
                        self.moveType.append("Double Forward Move")
                    else:
                        # notation for enpassant move
                        if self.enpass_move_made == True:
                            self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower()
                            self.moveType.append("Enpassant Move")
                            self.enpass_possible = 0
                            self.enpass_reset()
                        else:
                            self.move_text = abr + end_pos.lower()

            else:
                self.move_text = abr + start_pos[0].lower() + end_pos.lower()

        # destionation square occupied
        else:
            if (abbr == "PAWN") or (abbr == "pawn") or (abr == ''):
                # white pawn promotion notation
                if end_pos[1] == "8":
                    if isai == "True" and aicr == self.player_turn:
                        self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + ispr
                        self.update_promotion(ispr, 1)
                    else:
                        pval = self.do_promotion(1)
                        piece.name = pval
                        pname = piece.name[0]
                        if piece.name == "Knight":
                            pname = "N"
                            self.enpass_reset()

                        self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + pname
                        self.update_promotion(piece.name, 1)

                # black pawn promotion notation
                if end_pos[1] == "1":
                    if isai == "True" and aicr == self.player_turn:
                        self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + ispr
                        self.update_promotion(ispr, 2)
                    else:
                        pval = self.do_promotion(2)
                        piece.name = pval
                        pname = piece.name[0]
                        if piece.name == "Knight":
                            pname = "N"
                            self.enpass_reset()

                        self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + pname
                        self.update_promotion(piece.name, 2)

                if (end_pos[1] != "1") and (end_pos[1] != "8"):
                    self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower()
                    self.moveType.append("Pawn Move")
                    self.enpass_reset()

            else:
                if (abbr == "PAWN") or (abbr == "pawn") or (abr == ''):
                    # white pawn promotion notation
                    if end_pos[1] == "8":
                        if isai == "True" and aicr == self.player_turn:
                            self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + ispr
                            self.update_promotion(ispr, 1)
                        else:
                            pval = self.do_promotion(1)
                            piece.name = pval
                            pname = piece.name[0]
                            if piece.name == "Knight":
                                pname = "N"
                                self.enpass_reset()

                            self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + pname
                            self.update_promotion(piece.name, 1)

                    # black pawn promotion notation
                    if end_pos[1] == "1":
                        if isai == "True" and aicr == self.player_turn:
                            self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + ispr
                            self.update_promotion(ispr, 2)
                        else:
                            pval = self.do_promotion(2)
                            piece.name = pval
                            pname = piece.name[0]
                            if piece.name == "Knight":
                                pname = "N"
                                self.enpass_reset()

                            self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower() + "=" + pname
                            self.update_promotion(piece.name, 2)

                    if (end_pos[1] != "1") and (end_pos[1] != "8"):
                        self.move_text = start_pos[0].lower() + abr + 'x' + end_pos.lower()
                        self.moveType.append("Pawn Move")

                else:
                    self.move_text = abr + 'x' + end_pos.lower()
                    self.moveType.append("Pawn Move")
                    self.enpass_reset()

            self.halfmove_clock = 0

        Pa1 = self.get_piece_at("A1")
        Ph1 = self.get_piece_at("H1")
        Pa8 = self.get_piece_at("A8")
        Ph8 = self.get_piece_at("H8")
        # updating castling rights if rook is captured
        if (self.move_text[-3:] == "xa1") and (not str(type(Pa1)) == "<class 'piece.Rook'>"):
            White_Rook1_moved = "True"
            config.set('castle_rights', 'wrook1_moved', "True")

        if (self.move_text[-3:] == "xh1") and (not str(type(Ph1)) == "<class 'piece.Rook'>"):
            White_Rook2_moved = "True"
            config.set('castle_rights', 'wrook2_moved', "True")

        if (self.move_text[-3:] == "xa8") and (not str(type(Pa8)) == "<class 'piece.Rook'>"):
            Black_Rook1_moved = "True"
            config.set('castle_rights', 'brook1_moved', "True")

        if (self.move_text[-3:] == "xh8") and (not str(type(Ph8)) == "<class 'piece.Rook'>"):
            Black_Rook2_moved = "True"
            config.set('castle_rights', 'brook2_moved', "True")

        # notation for king side castling
        if (self.move_text == "Keg1") or (self.move_text == "Keg8"):
            v = self.move_text
            self.move_text = "O-O"
            self.moveType.append("Short Castling")
            self.enpass_reset()
            self.do_castle(v)

        # notation for queen side castling
        if (self.move_text == "Kec1") or (self.move_text == "Kec8"):
            v = self.move_text
            self.move_text = "O-O-O"
            self.moveType.append("Long Castling")
            self.enpass_reset()
            self.do_castle(v)

        with open('../data/chess_options.ini', 'w') as config_file:
            config.write(config_file)

        self.history.append(self.move_text)
        self.makePGN(self.move_text, start_pos, end_pos)
        self.game_state()

    def makePGN(self, move_texts, usp="", uep=""):
        """
        Generate PGN for user and move log from move made
        :param move_texts: model move notation
        :param usp: start position
        :param uep: end position
        """
        fsp = ""
        fep = ""
        fsp = usp
        fep = uep
        val = fsp + fep
        val = val.lower()
        if "=" in move_texts:
            val = val + move_texts[-1]

        # updating bitboard
        try:
            try:
                self.lboard.push(chess.Move.from_uci(val))
            except:
                self.lboard.push_san(val)

            mvv = self.lboard.peek()
            self.lboard.pop()
            umv = self.lboard.san(mvv)
            try:
                self.lboard.push(chess.Move.from_uci(val))
            except:
                self.lboard.push_san(val)

        except:
            pass

        # writing PGN to temproary file
        file1 = open("../data/temp_move_list_pgn.txt", "a")
        if len(self.history) == 1:
            file1.write("1.")

        if Model.count < 2:
            move_texts = '\t' + umv
            file1.write(move_texts)
        elif Model.count >= 2:
            move_texts.strip('\t')
            move_texts = '\n' + str(int(len(self.history) / 2) + 1) + '.\t' + umv
            file1.write(move_texts)
            Model.count = 0

        Model.count += 1
        file1.close()
        self.fenmaker()

    def fenmaker(self):
        """
        Generating FEN notation of current board
        """
        lb = self.lboard
        fm = self.lboard.fen()
        fm = fm + "\n"
        file2 = open("../data/temp_move_list_fen.txt", "a")
        file2.write(fm)
        file2.close()

    def get_alphanumeric_position_of_king(self, color):
        """
        Gets position of selected color king from the board
        :param color: color of king
        :return: position of king
        """
        for position in self.keys():
            this_piece = self.get_piece_at(position)
            if ((isinstance(this_piece, piece.King)) and (this_piece.color == color)):
                return position

    def is_insufficient_material_model(self):
        """
        Check for various insufficient piece situation
        :return: is insufficient material
        """
        wp = len(self.lboard.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.lboard.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.lboard.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.lboard.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.lboard.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.lboard.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.lboard.pieces(chess.ROOK, chess.WHITE))
        br = len(self.lboard.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.lboard.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.lboard.pieces(chess.QUEEN, chess.BLACK))
        # no queens in the board
        if wq == 0 and bq == 0:
            # no rooks in the board
            if wr == 0 and br == 0:
                # no pawns in the board
                if wp == 0 and bp == 0:
                    # 1 bishop in the board
                    if wb == 1 and bp == 0 and wn == 0 and bn == 0:
                        return True

                    # 1 knight in the board
                    if wn == 1 and bn == 0 and wb == 0 and bp == 0:
                        return True

                    # 1 bishop in the board
                    if bb == 1 and wp == 0 and bn == 0 and wn == 0:
                        return True

                    # 1 knight in the board
                    if bn == 1 and wn == 0 and bb == 0 and wp == 0:
                        return True

                    # 2 knights in the board
                    if wn == 1 and bn == 1 and wb == 0 and bp == 0:
                        return True

                    # 2 bishops in the board
                    if wb == 1 and bp == 1 and wn == 0 and bn == 0:
                        return True

        return False

    def is_king_under_check(self, color):
        """
        Checks if given color king is in check
        :param color: king color
        :return: is in check
        """
        Model.checkStatus = self.lboard.is_check()
        position_of_king = self.get_alphanumeric_position_of_king(color)
        opponent = 'black' if color == 'white' else 'white'
        return position_of_king in self.get_all_available_moves(opponent)

    def will_move_cause_check(self, start_position, end_position):
        """
        Checks if given move may put the king under check
        :param start_position: start position of move
        :param end_position: end position of move
        :return: will king be in check
        """
        tmp = deepcopy(self)
        tmp.move(start_position, end_position)
        return tmp.is_king_under_check(self[start_position].color)

    def change_player_turn(self, color):
        """
        Change player turn after move is made by the other
        :param color: move made by color
        """
        enemy = ('white' if color == 'black' else 'black')
        self.player_turn = enemy

    def pre_move_validation(self, initial_pos, final_pos):
        """
        Checks if the move about to be made is valid and legal
        so as to determine if it can be made
        :param initial_pos: start location of move
        :param final_pos: end location of move
        :return: can move be made
        """
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        isai = config.get('ai_stats', 'is_ai')
        aidp = config.get('ai_stats', 'ai_strength')
        initial_pos, final_pos = initial_pos.upper(), final_pos.upper()
        piece = self.get_piece_at(initial_pos)
        try:
            piece_at_destination = self.get_piece_at(final_pos)
        except:
            piece_at_destination = None

        if self.player_turn != piece.color:
            raise exceptions.NotYourTurn("Not " + piece.color + "'s turn!")

        enemy = ('white' if piece.color == 'black' else 'black')
        moves_available = piece.moves_available(initial_pos)
        wmc = self.will_move_cause_check(initial_pos, final_pos)
        if final_pos not in moves_available:
            raise exceptions.InvalidMove

        if self.get_all_available_moves(enemy):
            if wmc:
                raise exceptions.InvalidMove

        if wmc and (self.is_king_under_check(piece.color)):
            raise exceptions.InvalidMove

        # is move type enpassant
        if self.enpass_possible > 0:
            self.move(initial_pos, final_pos)
            self.update_game_statistics(piece, piece_at_destination, initial_pos, final_pos)
            self.change_player_turn(piece.color)

        # is move normal
        else:
            self.move(initial_pos, final_pos)
            self.update_game_statistics(piece, piece_at_destination, initial_pos, final_pos)
            self.change_player_turn(piece.color)
            return 1

        return 0

    def file_updater(self, otcome):
        """
        Update file with game state result
        :param otcome: game state
        """
        fileu = open("../data/temp_move_list_pgn.txt", "a")
        if (len(self.history) % 2) != 0:
            fileu.write("\t")
            fileu.write(otcome)
        else:
            fileu.write("\n")
            fileu.write("\t")
            fileu.write(otcome)

        fileu.close()

    def game_state(self):
        """
        Determines current game state to check for ending events
        """
        bd = self.lboard
        otcome = bd.result()
        if self.lboard.is_checkmate():
            configurations.STATE = 2
            self.gameOver = True
            self.file_updater(otcome)

        if self.lboard.is_insufficient_material():
            self.file_updater(otcome)
            configurations.STATE = 1
            self.gameOver = True

        if self.is_insufficient_material_model():
            self.file_updater("1/2-1/2")
            configurations.STATE = 1
            self.gameOver = True

        if self.lboard.is_stalemate():
            self.file_updater(otcome)
            configurations.STATE = 3
            self.gameOver = True

        if self.lboard.is_seventyfive_moves():
            self.file_updater(otcome)
            configurations.STATE = 4
            self.gameOver = True

        if self.lboard.is_fivefold_repetition():
            self.file_updater(otcome)
            configurations.STATE = 5
            self.gameOver = True
