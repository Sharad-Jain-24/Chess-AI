import chess
import chess.polyglot
from collections import OrderedDict
from configurations import ConfigParser

global board, b_has_castled, w_has_castled, infinity, move_count, table, current_depth
current_depth = 0
infinity = 9999
w_has_castled = False
b_has_castled = False

# Piece Square Table
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

kingstable_endgame = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50]

# Piece's value
queen = 900
rook = 500
bishop = 320
night = 300
pawn = 100

# Castling Value
castle = 100


def check_endgame():
    """
    This function checks if game has reached endgame or not.
    :return: (boolean) True - if endgame else False
    """
    endgame_score = 1600
    endgame_score2 = 2000
    # Number of pieces left on board
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    # Material score of white and black
    white_score = night * wn + bishop * wb + rook * wr + queen * wq
    black_score = night * bn + bishop * bb + rook * br + queen * bq

    if white_score < endgame_score and black_score < endgame_score and (wp + bp) < 11:
        # Endgame condition 1
        return True
    elif (wp + bp) < 6 and white_score < endgame_score2 and black_score < endgame_score2:
        # Endgame condition 2
        return True

    return False


def endgame_finder():
    """
    This function checks if game has reached endgame or not if already not in endgame.
    :return: (boolean / None) True - if endgame else None
    """
    global endgame
    if (not endgame) and check_endgame():
        endgame = True


def eval_castle(beval):
    """
    This function updates provided board value with bonus or penalty for castling moves.
    :param beval: Current board value to be updated.
    :return: Adjusted board value.
    """
    global w_has_castled, b_has_castled

    # Castling eval
    if not w_has_castled:
        # For White side
        if not board.has_castling_rights(chess.WHITE):
            # Bonus of Black
            beval = beval - castle

        if board.piece_type_at(chess.E1) == 6:
            # White King is at starting place
            if board.is_pseudo_legal(chess.Move.from_uci("e1c1")) or board.is_pseudo_legal(chess.Move.from_uci("e1g1")):
                beval = beval + 40

    if not b_has_castled:
        # For Black side
        if not board.has_castling_rights(chess.BLACK):
            # Bonus for White
            beval = beval + castle

        if board.piece_type_at(chess.E8) == 6:
            # White King is at starting place
            if board.is_pseudo_legal(chess.Move.from_uci("e8c8")) or board.is_pseudo_legal(chess.Move.from_uci("e8g8")):
                beval = beval - 40

    return beval


def eval_pos(material):
    """
    This function evaluates board according to positions of pieces on board (Positional Evaluation).
    :param material: Current board score to be updated.
    :return: Adjusted board score.
    """
    global endgame, board
    # Individual score of each piece (with position) relative to opponent's pieces
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])

    if endgame:
        kingsq = sum([kingstable_endgame[i] for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum(
            [-kingstable_endgame[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])
    else:
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    # Evaluation of Board
    beval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    return beval


# Evaluate Score of Board
def eval_scores(pos=True, cas=True):
    """
    This function evaluates board score.
    If both parameters are false this function will only do material evaluation.
    :param pos: True if need to do positional evaluation, default = True.
    :param cas: True if need to do castling evaluation, default = True.
    :return: Score of board based on whose turn it is.
    """
    global endgame, infinity, board
    # Check for End Of Game
    if board.is_checkmate():
        return -infinity
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0
    elif board.is_fivefold_repetition():
        return 0

    # Count total number of each type of pieces of each player
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    # Material score
    beval = pawn * (wp - bp) + night * (wn - bn) + bishop * (wb - bb) + rook * (wr - br) + queen * (wq - bq)
    # Piece Position
    if pos:
        beval = eval_pos(beval)

    # Castling Evaluation
    if cas:
        beval = eval_castle(beval)

    if board.turn:
        # If Turn is of White side
        return beval
    else:
        # If Turn is of Black side
        return -beval


def castling_check(move):
    """
    This function will check if current move is castling move if that side has not castled yet.
    :param move: Current move.
    :return: White, black -> True for which has castled in this move and False for other.
    """
    global w_has_castled, b_has_castled
    bc_flag = False
    wc_flag = False
    if board.turn and (not w_has_castled) and board.is_castling(move):
        w_has_castled = True
        wc_flag = True
    elif (not board.turn) and (not b_has_castled) and board.is_castling(move):
        b_has_castled = True
        bc_flag = True

    return wc_flag, bc_flag


def castling_check_undo(wc_flag, bc_flag):
    """
    This function will undo effects of castling_check function.
    :param wc_flag: True if last move caused castling for white.
    :param bc_flag: True if last move caused castling for black.
    """
    global w_has_castled, b_has_castled
    if wc_flag:
        w_has_castled = False
    elif bc_flag:
        b_has_castled = False


class Tree:
    def __init__(self, val):
        """
        Initialize a new node for tree with val.
        :param val:  Default value of new node.
        """
        global infinity
        # Value of node
        self.val = val
        # Child nodes stored in form of ordered dictionary with their value and last move as key.
        self.nodes = OrderedDict()
        # Default alpha and beta value
        self.alpha = -infinity
        self.beta = infinity

    def add_node(self, keyMove, nextNode, score):
        """
        This function attaches a node as child node of current node of tree.
        :param keyMove: A move from current possible moves of board.
        :param nextNode: Address of next node.
        :param score: Value of that child node.
        """
        self.nodes[keyMove] = [nextNode, score]


def sort(subtree):
    """
    This function sorts child nodes of current nodes according to their value in descending order.
    :param subtree: Current node whose children are to be sorted.
    :return: (OrderedDict) of child nodes of current node.
    """
    return OrderedDict(sorted(subtree.nodes.items(), key=lambda item: item[1][1], reverse=True))


class ChessAI:
    def __init__(self):
        """
        Initialize new chess board and tree.
        """
        global board, table, endgame
        board = chess.Board()
        table = Tree(0)
        endgame = False

    def new_board(self):
        """
        This function creates a new chess board and tree for a new game.
        """
        global board, table, endgame
        board = chess.Board()
        table = Tree(0)
        endgame = False

    # Quiescence Search Algorithm
    def quiesce(self, alpha, beta):
        """
        This function implements Quiescence Search.
        The purpose of this search is to only evaluate "quiet" positions, or positions where there are no winning
        tactical moves to be made.
        This search is needed to avoid the horizon effect.
        :param alpha: Alpha for alpha-beta pruning.
        :param beta: Beta for alpha-beta pruning.
        :return: Board score evaluated at end of current Quiescence Search.
        """
        global board
        stand_pat = eval_scores()

        if stand_pat >= beta:
            return beta

        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                # Check castling move
                wc_flag, bc_flag = castling_check(move)
                board.push(move)
                score = -self.quiesce(-beta, -alpha)
                board.pop()
                # Undoing effects of castling check
                castling_check_undo(wc_flag, bc_flag)
                if score >= beta:
                    return beta

                if score > alpha:
                    alpha = score

        return alpha

    def pvSearch(self, alpha, beta, depthleft, subtree, do_null, check_ext):
        """
        Principal Variation Search (PVS), an enhancement to Alpha-Beta, based on null- or zero window searches of
        none PV-nodes, to prove a move is worse or not than an already safe score from the principal variation.

        Pruning Applied:
            Alpha-Beta Pruning
            Extended Null Move Pruning

        Extensions Applied:
            Check Extension
            Singular Reply Extension

        Other Algorithms:
            Negated Minimax Search
            Principal Variation Search (PVS) with Aspiration
            Quiescence Search
            Move Ordering

        :param alpha: Alpha for alpha-beta pruning.
        :param beta: Beta for alpha-beta pruning.
        :param depthleft: Depth that is left to be searched.
        :param subtree: Current active node that needs to be searched.
        :param do_null: True if Extended Null-move pruning is to be performed else False.
        :param check_ext: Number of times check extension has been performed.
        :return: Score of current subtree.
        """
        global board, infinity, endgame
        if board.is_checkmate():
            subtree.val = -infinity
            return -infinity
        elif board.is_stalemate() or board.is_insufficient_material():
            subtree.val = 0
            return 0
        elif board.is_fivefold_repetition():
            subtree.val = 0
            return 0

        lMoves = board.legal_moves
        subtree.alpha = alpha
        subtree.beta = beta

        # Check extension
        if board.is_check() and depthleft <= 3 and check_ext < 4:
            depthleft = depthleft + 1
            check_ext = check_ext + 1
        # Singular Reply Extension
        elif len(list(lMoves)) == 1 and depthleft <= 3:
            depthleft = depthleft + 1

        # Board Evaluation
        if depthleft <= 0:
            result = self.quiesce(alpha, beta)
            subtree.val = result
            return result

        TTNeeded = len(subtree.nodes) == 0
        # Dont make new TT if already exists
        if TTNeeded:
            # Make custom move tree
            for move in lMoves:
                newNode = Tree(-infinity)
                subtree.add_node(move, newNode, -infinity)

        # Extended Null Move Pruning
        # conduct a null-move search if it is legal and desired
        if (not board.is_check()) and do_null:
            move = chess.Move.null()
            board.push(move)
            newNode = Tree(-infinity)
            subtree.add_node(move, newNode, -infinity)
            # null-move search with minimal window around beta
            R = 4 if depthleft >= 6 else 3
            score = self.pvSearch(-subtree.beta, -subtree.beta + 1, depthleft - R - 1, subtree.nodes[move][0], False,
                                  check_ext)
            board.pop()
            score = -score
            subtree.nodes[move][0].val = score
            # cutoff in case of fail-high
            if score >= beta:
                depthleft = depthleft - 4
                if depthleft <= 0:
                    return eval_scores()

        move = list(subtree.nodes.keys())[0]
        # Check castling move
        wc_flag, bc_flag = castling_check(move)

        board.push(move)
        bestscore = self.pvSearch(-subtree.beta, -subtree.alpha, depthleft - 1, subtree.nodes[move][0], True, check_ext)
        board.pop()

        # Undoing effects of castling check
        castling_check_undo(wc_flag, bc_flag)

        bestscore = -bestscore
        subtree.nodes[move][1] = bestscore
        if bestscore >= subtree.beta:
            subtree.val = bestscore
            return bestscore

        if bestscore > subtree.alpha:
            subtree.alpha = bestscore

        # Rest of the moves for every depth
        for move in list(subtree.nodes.keys())[1:]:
            # Check castling move
            wc_flag, bc_flag = castling_check(move)
            # if not endgame:
            board.push(move)
            score = self.pvSearch(-subtree.alpha - 1, -subtree.alpha, depthleft - 1, subtree.nodes[move][0], True,
                                  check_ext)
            board.pop()
            # Undoing effects of castling check
            castling_check_undo(wc_flag, bc_flag)
            score = -score
            # if endgame or (subtree.alpha < score < subtree.beta):
            if subtree.alpha < score < subtree.beta:
                # if it failed high, do a full re-search
                # re-search with window
                # Check castling move
                wc_flag, bc_flag = castling_check(move)
                board.push(move)
                score = self.pvSearch(-subtree.beta, -subtree.alpha, depthleft - 1, subtree.nodes[move][0], True,
                                      check_ext)
                board.pop()
                # Undoing effects of castling check
                castling_check_undo(wc_flag, bc_flag)
                score = -score

            subtree.nodes[move][1] = score
            if score >= subtree.beta:
                subtree.val = score
                return score

            if score > bestscore:
                subtree.val = score
                bestscore = score

            if score > subtree.alpha:
                subtree.alpha = score

        # SORTING / Move Ordering
        subtree.nodes = sort(subtree)
        return bestscore

    # Negated Minimax (Negamax) Algorithm
    def pvnegamax(self, depth, table):
        """
        This function is similar to pvSearch function.
        It first searches for move in book (i.e. pre-calculated moves).
        This function uses pvSearch function to find best move.

        Algorithms:
            Negated Minimax Search
            Principal Variation Search (PVS) with Aspiration
            Move Ordering
            Alpha-Beta Pruning
            Singular Reply Extension

        :param depth: Depth to which search is to be performed.
        :param table: Tree / Transposition table to use during search.
        :return: Move, Table (if move is from book move than table = "book move").
        """
        global board, infinity, move_count
        try:
            if move_count <= 15:
                # Book Move
                path = "../books/human.bin"
                book_move = chess.polyglot.MemoryMappedReader(path).weighted_choice(board).move
                return book_move, "book move"
            else:
                raise Exception("No more book move")

        except:
            # Negamax if not in book

            # aplha - Current best score
            # beta - Best possible score

            lMoves = list(board.legal_moves)
            table.alpha = -infinity
            table.beta = infinity

            # Singular Reply Extension
            if len(list(lMoves)) == 1:
                depth = depth + 1

            TTNeeded = len(table.nodes) == 0
            # Dont make new TT if already exists
            if TTNeeded:
                # make custom move tree
                for move in lMoves:
                    newNode = Tree(-infinity)
                    table.add_node(move, newNode, -infinity)

            # using fail-soft with negamax
            # For first move of every depth
            move = list(table.nodes.keys())[0]

            # Check castling move
            wc_flag, bc_flag = castling_check(move)
            board.push(move)
            bValue = self.pvSearch(-table.beta, -table.alpha, depth - 1, table.nodes[move][0], True, 0)
            board.pop()
            # Undoing effects of castling check
            castling_check_undo(wc_flag, bc_flag)
            bValue = -bValue

            table.nodes[move][1] = bValue
            table.val = bValue
            # bMove = move
            if bValue < table.beta:
                if bValue > table.alpha:
                    table.alpha = bValue

                # First depth is handled here
                for move in list(table.nodes.keys())[1:]:
                    # Check castling move
                    wc_flag, bc_flag = castling_check(move)
                    board.push(move)
                    # alphaBeta or zwSearch
                    boardValue = self.pvSearch(-table.alpha - 1, -table.alpha, depth - 1, table.nodes[move][0], True, 0)
                    board.pop()
                    # Undoing effects of castling check
                    castling_check_undo(wc_flag, bc_flag)
                    boardValue = -boardValue

                    if table.alpha < boardValue < table.beta:
                        # if it failed high, do a full re-search
                        # Check castling move
                        wc_flag, bc_flag = castling_check(move)
                        board.push(move)
                        boardValue = self.pvSearch(-table.beta, -table.alpha, depth - 1, table.nodes[move][0], True, 0)
                        # re-search with window [alfa;beta]
                        board.pop()
                        # Undoing effects of castling check
                        castling_check_undo(wc_flag, bc_flag)
                        boardValue = -boardValue

                    table.nodes[move][1] = boardValue
                    if boardValue >= table.beta:
                        table.val = boardValue
                        break

                    if boardValue > bValue:
                        table.val = boardValue
                        bValue = boardValue
                        # bMove = move

                    if boardValue > table.alpha:
                        table.alpha = boardValue

            # Move Ordering
            table.nodes = sort(table)

            # Selecting best move
            bMove = list(table.nodes.keys())[0]
            if bMove == chess.Move.null():
                # If best move is null move
                bMove = list(table.nodes.keys())[1]

            return bMove, table

    def start_ai(self, human_move, req_depth):
        """
        This function uses Iterative Deepening with pvnegamax function method to calculate best move.

        :param human_move: Last move made by opponent of AI.
        :param req_depth: Depth till which search is to be conducted.
        :return: Calculated best move in string type.
        """
        global endgame, board, move_count, table, current_depth
        if human_move != 0:
            # traverse TT to HUMAN_MOVE (IF cant -> discard TT & CURRENT_DEPTH=0)
            if human_move in table.nodes.keys():
                table = table.nodes[human_move][0]
                # CURRENT_DEPTH-1
                current_depth = current_depth - 1 if current_depth > 0 else 0
            else:
                table = Tree(0)
                current_depth = 0
        else:
            table = Tree(0)
            current_depth = 0

        # Search till REQUIRED_DEPTH
        endgame_finder()
        if endgame:
            req_depth = 3 if req_depth <= 2 else (5 if req_depth < 5 else req_depth + 2)

        book_flag = False
        best_move = chess.Move.null()

        for depth in range(current_depth + 1, req_depth + 1):
            temp_move, table = self.pvnegamax(depth, table)
            if table == "book move":
                book_flag = True
                best_move = temp_move
                table = Tree(0)
                current_depth = 0
                break

            if temp_move:
                best_move = temp_move
                current_depth = depth

        if best_move == chess.Move.null():
            best_move = list(table.nodes.keys())[0]
            if best_move == chess.Move.null():
                best_move = list(table.nodes.keys())[1]

        if not book_flag:
            # current_depth = req_depth
            # Traverse to BEST_MOVE in TT
            table = table.nodes[best_move][0]
            # CURRENT_DEPTH-1
            current_depth = current_depth - 1 if current_depth > 0 else 0

        board.push(best_move)
        return str(best_move)

    def send_bd(self, brd, mov_count, human_move):
        """
        This function process the information received from frontend before passing it to AI.

        :param brd: Board on which opponent of AI is working on.
        :param mov_count: Number of moves performed since start of game.
        :param human_move: Last move made by AI's opponent.
        :return: "00" if some inconsistency occurs else best move calculated by AI in string format.
        """
        global endgame, board, move_count, table, current_depth
        move_count = int(mov_count)
        config = ConfigParser()
        config.read('../data/chess_options.ini')
        ai_color = config.get('ai_stats', 'ai_color')
        req_depth = int(config.get('ai_stats', 'ai_strength'))
        if human_move != 0:
            try:
                # Push last move i.e. human move
                board.push(human_move)
            except Exception as e:
                return "00"

        if len(list(board.legal_moves)) == 0:
            # Check if game is finished
            return "00"
        elif board.fen() == brd.fen():
            if ((not board.turn) and ai_color == "white") or (board.turn and ai_color == "black"):
                print("Wrong Color Passed - ", ai_color, " - ", board.turn)
            else:
                return self.start_ai(human_move, req_depth)
        else:
            print("Boards don't match - ", board.fen(), " - NOT - ", brd.fen())
            board.pop()
            return "00"
