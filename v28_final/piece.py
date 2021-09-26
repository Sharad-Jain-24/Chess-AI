import exceptions
from configurations import *


def create_piece(piece, color='white'):
    """
    Initialize piece to dictionary from start postion of game
    :param piece: piece to be initialzed
    :param color: piece color
    :return: piece
    """
    if isinstance(piece, str):
        if piece.upper() in SHORT_NAME.keys():
            color = "white" if piece.isupper() else "black"
            piece = SHORT_NAME[piece.upper()]

        piece = piece.capitalize()
        if piece in SHORT_NAME.values():
            return eval("{classname}(color)".format(classname=piece))

    raise exceptions.ChessError("invalid piece name: '{}'".format(piece))


def get_numeric_notation(rowcol):
    """
    Numeric notation from row, column coordinates to calculate possible moves
    :param rowcol: row, column
    :return: y, x
    """
    row, col = rowcol
    return int(col) - 1, X_AXIS_LABELS.index(row)


class Piece:
    def __init__(self, color):
        """
        Initialize piece
        :param color: color of piece
        """
        self.name = self.__class__.__name__.lower()
        if color == "black":
            self.name = self.name.lower()
        elif color == 'white':
            self.name = self.name.upper()

        self.color = color

    def keep_reference(self, model):
        """
        Update model & dictionary of piece creation
        :param model: link to model
        """
        self.model = model

    def moves_available(self, current_position, directions, distance):
        """
        Collection of all moves from all possible pieces
        :param current_position: start position of piece
        :param directions: direction of move
        :param distance: distance to move
        :return: all moves available
        """
        piece = self
        model = self.model
        allowed_moves = []
        next_allowed_moves = []
        start_row, start_column = get_numeric_notation(current_position)
        for x, y in directions:
            collision = False
            for step in range(1, distance + 1):
                # is path blocked
                if collision:
                    break

                destination = start_row + step * x, start_column + step * y
                # allowed move
                if self.possible_position(destination) not in model.all_occupied_positions():
                    allowed_moves.append(destination)
                # capture move
                elif self.possible_position(destination) in model.all_positions_occupied_by_color(piece.color):
                    collision = True
                # normal move
                else:
                    allowed_moves.append(destination)
                    collision = True

        allowed_moves = filter(model.is_on_board, allowed_moves)
        return map(model.get_alphanumeric_position, allowed_moves)

    def possible_position(self, destination):
        """
        Available square section
        :param destination: end square
        :return: alphanumeric notation
        """
        return self.model.get_alphanumeric_position(destination)


class King(Piece):
    def moves_available(self, current_position):
        """
        Find all possible moves of king
        :param current_position: current position of king
        :return: all possible king moves
        """
        directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
        dirs = ((0, -1), (0, 1), (0, -2), (0, 2))
        dds = directions + dirs
        max_distance = 1
        model = self.model
        allowed_moves = []
        start_col, start_row = get_numeric_notation(current_position.upper())
        piece = model.get(current_position)
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        WK = config.get('castle_rights', 'wking_moved')
        BK = config.get('castle_rights', 'bking_moved')
        WR1 = config.get('castle_rights', 'wrook1_moved')
        WR2 = config.get('castle_rights', 'wrook2_moved')
        BR1 = config.get('castle_rights', 'brook1_moved')
        BR2 = config.get('castle_rights', 'brook2_moved')
        try:
            if piece.color == "white":
                # king already moved
                if WK == "True":
                    return super().moves_available(current_position, directions, max_distance)

                else:
                    flg = 0
                    # are castling squares empty
                    if ((model.get_piece_at("B1") is None) and (model.get_piece_at("C1") is None) and (
                            model.get_piece_at("D1") is None) and (model.get_piece_at("F1") is None) and (
                            model.get_piece_at("G1") is None)):
                        # is queen side castling is safe
                        if (model.will_move_cause_check("E1", "D1")) or (model.will_move_cause_check("E1", "B1")):
                            # is king side castling is safe
                            if model.will_move_cause_check("E1", "F1"):
                                flg = 0
                            else:
                                flg = 3
                        # is king side castling is safe
                        elif model.will_move_cause_check("E1", "F1"):
                            flg = 2
                        else:
                            flg = 1

                    # are queen side castling squares empty
                    elif ((model.get_piece_at("B1") is None) and (model.get_piece_at("C1") is None) and (
                            model.get_piece_at("D1") is None)):
                        # is queen side castling is safe
                        if (model.will_move_cause_check("E1", "D1")) or (model.will_move_cause_check("E1", "B1")):
                            # are king side castling squares empty
                            if (model.get_piece_at("F1") is None) and (model.get_piece_at("G1") is None):
                                # is king side castling is safe
                                if model.will_move_cause_check("E1", "F1"):
                                    flg = 0
                                else:
                                    flg = 3
                        else:
                            flg = 2

                    # are king side castling squares empty
                    elif (model.get_piece_at("F1") is None) and (model.get_piece_at("G1") is None):
                        # is king side castling is safe
                        if model.will_move_cause_check("E1", "F1"):
                            # are queen side castling squares empty
                            if ((model.get_piece_at("B1") is None) and (model.get_piece_at("C1") is None) and (
                                    model.get_piece_at("D1") is None)):
                                # is queen side castling is safe
                                if ((model.will_move_cause_check("E1", "D1")) or (
                                        model.will_move_cause_check("E1", "B1"))):
                                    flg = 0
                                else:
                                    flg = 2
                        else:
                            flg = 3

                    # rooks already moved
                    if (WR1 == "True") and (WR2 == "True"):
                        flg = 0

                    if flg == 0:
                        return super().moves_available(current_position, directions, max_distance)

                    # both side castling move
                    elif flg == 1:
                        dirs = ((0, -1), (0, 1), (0, -2), (0, 2))
                        dds = directions + dirs
                        for x, y in dds:
                            destination = start_col + x, start_row + y
                            if ((model.get_alphanumeric_position(
                                    destination) not in model.all_positions_occupied_by_color(piece))) and (
                                    model.get_alphanumeric_position(
                                        destination) not in model.all_positions_occupied_by_color(piece.color)):
                                allowed_moves.append(destination)

                    # king side castling move
                    elif flg == 2:
                        dirs = ((0, -1), (0, 1), (0, -2))
                        dds = directions + dirs
                        for x, y in dds:
                            destination = start_col + x, start_row + y
                            if ((model.get_alphanumeric_position(
                                    destination) not in model.all_positions_occupied_by_color(piece))) and (
                                    model.get_alphanumeric_position(
                                        destination) not in model.all_positions_occupied_by_color(piece.color)):
                                allowed_moves.append(destination)

                    # queen side castling move
                    elif flg == 3:
                        dirs = ((0, -1), (0, 1), (0, 2))
                        dds = directions + dirs
                        for x, y in dds:
                            destination = start_col + x, start_row + y
                            if ((model.get_alphanumeric_position(
                                    destination) not in model.all_positions_occupied_by_color(piece))) and (
                                    model.get_alphanumeric_position(
                                        destination) not in model.all_positions_occupied_by_color(piece.color)):
                                allowed_moves.append(destination)

            if piece.color == "black":
                # king already moved
                if BK == "True":
                    return super().moves_available(current_position, directions, max_distance)

                else:
                    flg = 0
                    # are castling squares empty
                    if ((model.get_piece_at("B8") is None) and (model.get_piece_at("C8") is None) and (
                            model.get_piece_at("D8") is None) and (model.get_piece_at("F8") is None) and (
                            model.get_piece_at("G8") is None)):
                        # is queen side castling is safe
                        if (model.will_move_cause_check("E8", "D8")) or (model.will_move_cause_check("E8", "B8")):
                            # is king side castling is safe
                            if model.will_move_cause_check("E8", "F8"):
                                flg = 0
                            else:
                                flg = 3
                        # is king side castling is safe
                        elif model.will_move_cause_check("E8", "F8"):
                            flg = 2
                        else:
                            flg = 1

                    # are queen side castling squares empty
                    elif ((model.get_piece_at("B8") is None) and (model.get_piece_at("C8") is None) and (
                            model.get_piece_at("D8") is None)):
                        # is queen side castling is safe
                        if (model.will_move_cause_check("E8", "D8")) or (model.will_move_cause_check("E8", "B8")):
                            # are king side castling squares empty
                            if (model.get_piece_at("F8") is None) and (model.get_piece_at("G8") is None):
                                # is king side castling is safe
                                if model.will_move_cause_check("E8", "F8"):
                                    flg = 0
                                else:
                                    flg = 3
                        else:
                            flg = 2

                    # are king side castling squares empty
                    elif (model.get_piece_at("F8") is None) and (model.get_piece_at("G8") is None):
                        # is king side castling is safe
                        if model.will_move_cause_check("E8", "F8"):
                            # are queen side castling squares empty
                            if ((model.get_piece_at("B8") is None) and (model.get_piece_at("C8") is None) and (
                                    model.get_piece_at("D8") is None)):
                                # is queen side castling is safe
                                if ((model.will_move_cause_check("E8", "D8")) or (
                                        model.will_move_cause_check("E8", "B8"))):
                                    flg = 0
                                else:
                                    flg = 2
                        else:
                            flg = 3

                    # rooks already moved
                    if (BR1 == "True") and (BR2 == "True"):
                        flg = 0

                    if flg == 0:
                        return super().moves_available(current_position, directions, max_distance)

                    # both side castling move
                    elif flg == 1:
                        dirs = ((0, -1), (0, 1), (0, -2), (0, 2))
                        dds = directions + dirs
                        for x, y in dds:
                            destination = start_col + x, start_row + y
                            if ((model.get_alphanumeric_position(
                                    destination) not in model.all_positions_occupied_by_color(piece))) and (
                                    model.get_alphanumeric_position(
                                        destination) not in model.all_positions_occupied_by_color(piece.color)):
                                allowed_moves.append(destination)

                    # king side castling move
                    elif flg == 2:
                        dirs = ((0, -1), (0, 1), (0, -2))
                        dds = directions + dirs
                        for x, y in dds:
                            destination = start_col + x, start_row + y
                            if ((model.get_alphanumeric_position(
                                    destination) not in model.all_positions_occupied_by_color(piece))) and (
                                    model.get_alphanumeric_position(
                                        destination) not in model.all_positions_occupied_by_color(piece.color)):
                                allowed_moves.append(destination)

                    # queen side castling move
                    elif flg == 3:
                        dirs = ((0, -1), (0, 1), (0, 2))
                        dds = directions + dirs
                        for x, y in dds:
                            destination = start_col + x, start_row + y
                            if ((model.get_alphanumeric_position(
                                    destination) not in model.all_positions_occupied_by_color(piece))) and (
                                    model.get_alphanumeric_position(
                                        destination) not in model.all_positions_occupied_by_color(piece.color)):
                                allowed_moves.append(destination)

        except:
            pass

        if len(allowed_moves) == 0:
            return super().moves_available(current_position, directions, max_distance)

        if model.lboard.is_check():
            return super().moves_available(current_position, directions, max_distance)

        allowed_moves = filter(model.is_on_board, allowed_moves)
        return map(model.get_alphanumeric_position, allowed_moves)


class Queen(Piece):
    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
    max_distance = 8

    def moves_available(self, current_position):
        """
        Get all possible moves of queen
        :param current_position: queens position
        :return: all possible queen moves
        """
        return super().moves_available(current_position, self.directions, self.max_distance)


class Rook(Piece):
    directions = ORTHOGONAL_POSITIONS
    max_distance = 8
    has_rook_moved = False

    def moves_available(self, current_position):
        """
        Get all possible moves of rook
        :param current_position: rook position
        :return: all possible rook moves
        """
        return super().moves_available(current_position, self.directions, self.max_distance)


class Bishop(Piece):
    directions = DIAGONAL_POSITIONS
    max_distance = 8

    def moves_available(self, current_position):
        """
        Get all possible moves of bishop
        :param current_position: bishop position
        :return: all possible bishop moves
        """
        return super().moves_available(current_position, self.directions, self.max_distance)


class Knight(Piece):
    def moves_available(self, current_position):
        """
        Get all possible moves of knight
        :param current_position: knight position
        :return: all possible knight moves
        """
        model = self.model
        allowed_moves = []
        start_col, start_row = get_numeric_notation(current_position.upper())
        piece = model.get(current_position)
        for x, y in KNIGHT_POSITIONS:
            destination = start_col + x, start_row + y
            if ((model.get_alphanumeric_position(destination)) not in model.all_positions_occupied_by_color(
                    piece.color)):
                allowed_moves.append(destination)

        allowed_moves = filter(model.is_on_board, allowed_moves)
        return map(model.get_alphanumeric_position, allowed_moves)


class Pawn(Piece):
    def moves_available(self, current_position):
        """
        Get all possible moves of pawn
        :param current_position: pawn position
        :return: all possible pawn moves
        """
        model = self.model
        piece = self
        if self.color == 'white':
            initial_position, direction, enemy = 1, 1, 'black'
        else:
            initial_position, direction, enemy = 6, -1, 'white'

        allowed_moves = []
        double_forward_moves = []
        double_forward_status = False
        prohibited = model.all_occupied_positions()
        start_position = get_numeric_notation(current_position.upper())
        forward = start_position[0] + direction, start_position[1]
        # enpass move
        for a in range(-1, 2, 2):
            attack = start_position[0] + direction, start_position[1] + a
            tmp_attack = start_position[0], start_position[1] + a
            at = model.get_alphanumeric_position(attack)
            ta = model.get_alphanumeric_position(tmp_attack)
            if len(model.moveType) != 0:
                lm = model.moveType[-1]
                mb = model.player_turn
            else:
                lm = 0
                mb = 0

            if len(model.history) != 0:
                if lm == "Double Forward Move":
                    lmt = model.history[-1].upper()
                else:
                    lmt = 0

            # enpassant column check
            if ta in model.all_positions_occupied_by_color(enemy):
                if ((ta[1] == "5") and (self.color == 'white') and (lm == "Double Forward Move") and (
                        mb == "white") and (ta == lmt)):
                    sp = model.get_alphanumeric_position(start_position)
                    allowed_moves.append(attack)
                    model.enpass_possible += 1
                    model.prev_enpass.append(attack)
                    model.enpass_square.append(at)
                    model.tmp_attack_square.append(ta)
                    model.enpass_start_square.append(sp)

                if ((ta[1] == "4") and (self.color == 'black') and (lm == "Double Forward Move") and (
                        mb == "black") and (ta == lmt)):
                    sp = model.get_alphanumeric_position(start_position)
                    allowed_moves.append(attack)
                    model.enpass_possible += 1
                    model.prev_enpass.append(attack)
                    model.enpass_square.append(at)
                    model.tmp_attack_square.append(ta)
                    model.enpass_start_square.append(sp)

        # first double pawn move
        if model.get_alphanumeric_position(forward) not in prohibited:
            allowed_moves.append(forward)
            if start_position[0] == initial_position:
                double_forward = (forward[0] + direction, forward[1])
                double_forward_status = False
                if model.get_alphanumeric_position(double_forward) not in prohibited:
                    allowed_moves.append(double_forward)
                    double_forward_status = True

        # Attacking move
        for a in range(-1, 2, 2):
            attack = start_position[0] + direction, start_position[1] + a
            if model.get_alphanumeric_position(attack) in model.all_positions_occupied_by_color(enemy):
                allowed_moves.append(attack)

        allowed_moves = filter(model.is_on_board, allowed_moves)
        return map(model.get_alphanumeric_position, allowed_moves)
