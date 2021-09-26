from configparser import ConfigParser

config = ConfigParser()
config.read('../data/chess_options.ini')
STATE = 0
wtime = 0
btime = 0
wctime = 0
bctime = 0
CHANCE = "WHITE"
King_moved = False
Rook_moved = False
NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
DIMENSION_OF_EACH_SQUARE = 64
White_Clock = config.get('chess_clock', 'white_clock')
Black_Clock = config.get('chess_clock', 'black_clock')
White_Offer_Draw = config.get('draw_status', 'white_draw_offer')
Black_Offer_Draw = config.get('draw_status', 'black_draw_offer')
White_King_moved = config.get('castle_rights', 'wking_moved')
Black_King_moved = config.get('castle_rights', 'bking_moved')
White_Rook1_moved = config.get('castle_rights', 'wrook1_moved')
White_Rook2_moved = config.get('castle_rights', 'wrook2_moved')
Black_Rook1_moved = config.get('castle_rights', 'brook1_moved')
Black_Rook2_moved = config.get('castle_rights', 'brook2_moved')
BOARD_COLOR_1 = config.get('chess_colors', 'board_color_1', fallback="#DDB88C")
BOARD_COLOR_2 = config.get('chess_colors', 'board_color_2', fallback="#A66D4F")
HIGHLIGHT_COLOR = config.get('chess_colors', 'highlight_color', fallback="#2EF70D")
LASTMOVECLR = config.get('chess_colors', 'last_move_clr', fallback="#808000")
# Rank & File data for game
X_AXIS_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
Y_AXIS_LABELS = (1, 2, 3, 4, 5, 6, 7, 8)
# piece name abbreviation
SHORT_NAME = {
    'R': 'Rook', 'N': 'Knight', 'B': 'Bishop',
    'Q': 'Queen', 'K': 'King', 'P': 'Pawn'
    }

# initial piece locations
START_PIECES_POSITION = {
    "A8": "r", "B8": "n", "C8": "b", "D8": "q", "E8": "k", "F8": "b", "G8": "n", "H8": "r",
    "A7": "p", "B7": "p", "C7": "p", "D7": "p", "E7": "p", "F7": "p", "G7": "p", "H7": "p",

    "A1": "R", "B1": "N", "C1": "B", "D1": "Q", "E1": "K", "F1": "B", "G1": "N", "H1": "R",
    "A2": "P", "B2": "P", "C2": "P", "D2": "P", "E2": "P", "F2": "P", "G2": "P", "H2": "P"
    }

# move directions
ORTHOGONAL_POSITIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
DIAGONAL_POSITIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
KNIGHT_POSITIONS = ((-2, -1),(-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
