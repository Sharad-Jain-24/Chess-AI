import aimodel


def start_process(ai_child_conn, ui_parent_conn):
    """
    This function initializes the chess board for AI.
    :param ai_child_conn: AI will receive message through this connection.
    :param ui_parent_conn: AI will send response through this connection.
    """
    ai_rec_conn = ai_child_conn
    ai_send_conn = ui_parent_conn
    # Creating object of ChessAI class in aimodel
    cai = aimodel.ChessAI()
    ai_manager(cai, ai_rec_conn, ai_send_conn)


def ai_manager(cai, ai_rec_conn, ai_send_conn):
    """
    This function keeps AI active during the course of the application
    :param cai: Object of ChessAI class of aimodel.
    :param ai_rec_conn: Connection object to receive message from.
    :param ai_send_conn: Connection object to send message to.
    """
    while True:
        # Waiting for a message from Frontend.
        brd, mov_count, human_move, stop_ai = ai_rec_conn.recv()
        if stop_ai == "new":
            # Start a new game
            cai.new_board()
            continue
        if stop_ai:
            # Application closed
            break

        # Start AI processing
        move = cai.send_bd(brd, mov_count, human_move)

        # Send response back to frontend
        ai_send_conn.send(str(move))

    # Closing connection
    ai_send_conn.close()
