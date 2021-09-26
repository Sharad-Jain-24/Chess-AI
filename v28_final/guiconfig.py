import platform

main_screen = ""
slider_width = ""
timer_width = ""
strength_win = ""
# default app color
main_color = "green"

# getting current OS
oname = platform.system()
if oname == "Windows":
    main_screen = "325x370"
    slider_width = "130"
    timer_width = "19"
    strength_win = "335x380"
    board_screen = "865x570"
    movelog_h = "29"
    movelog_w = "32"

elif oname == "Linux":
    main_screen = "390x380"
    slider_width = "165"
    timer_width = "18"
    strength_win = "425x370"
    board_screen = "925x550"
    movelog_h = "27"
    movelog_w = "40"

else:
    main_screen = "390x380"
    slider_width = "165"
    timer_width = "18"
    strength_win = "425x370"
    board_screen = "925x550"
    movelog_h = "27"
    movelog_w = "40"
