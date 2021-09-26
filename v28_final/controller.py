import model
import piece


class Controller:
    def __init__(self):
        """
        Initialize controller link to model
        """
        self.init_model()

    def init_model(self):
        """
        Create model object accessible by controller
        """
        self.model = model.Model()

    def get_numeric_notation(self, position):
        """
        Gets numeric notation of piece square
        :param position: location of square clicked
        :return: numeric notation of square
        """
        return piece.get_numeric_notation(position)

    def get_alphanumeric_position(self, rowcolumntuple):
        """
        Gets alphanumeric value of piece square
        :param rowcolumntuple: x, y coordinate
        :return: alphanumeric notation of square
        """
        return self.model.get_alphanumeric_position(rowcolumntuple)

    def get_all_pieces_on_chess_board(self):
        """
        Get pieces currently on board
        :return: alive pieces
        """
        return self.model.items()

    def get_piece_at(self, position_of_click):
        """
        Get piece present at square clicked
        :param position_of_click: click location
        :return: piece name
        """
        return self.model.get_piece_at(position_of_click)

    def reset_game_data(self):
        """
        Reset links and model of game
        """
        self.model.reset_game_data()

    def reset_to_initial_locations(self):
        """
        Resets pieces to initial locations as in start postition
        """
        self.model.reset_to_initial_locations()

    def pre_move_validation(self, start_pos, end_pos):
        """
        Link to model to validate move being made
        :param start_pos: start square of piece
        :param end_pos: end square of piece
        :return: is move valid & legal
        """
        return self.model.pre_move_validation(start_pos, end_pos)

    def player_turn(self):
        """
        Gets whos turn it is to move
        :return: player turn
        """
        return self.model.player_turn

    def moves_available(self, position):
        """
        Gets all possible moves at the time from current position
        :param position: start position
        :return: all possible moves
        """
        return self.model.moves_available(position)

    def get_board(self):
        """
        Gets the bitboard for AI to work on
        :return: Bitboard
        """
        return self.model.lboard

    def get_lastmove(self):
        """
        Gets count of total moves made
        :return: move count
        """
        length = len(self.model.history)
        return length
