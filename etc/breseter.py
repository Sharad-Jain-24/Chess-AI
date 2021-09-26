from configparser import ConfigParser

config = ConfigParser()
config.read('../data/chess_options.ini')
config.set('chess_clock', 'white_clock', '10')
config.set('chess_clock', 'black_clock', '10')
config.set('chess_colors', 'board_color_1', '#804040')
config.set('chess_colors', 'board_color_2', '#ffffff')
config.set('chess_colors', 'last_move_clr', '#808040')
config.set('chess_colors', 'highlight_color', '#808040')
with open('../data/chess_options.ini', 'w') as config_file:
    config.write(config_file)
