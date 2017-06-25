"""
initial:

    1  3        1     3        1  2  3        1  2  3        1  2  3
 4  2  5   =>   4  2  5   =>   4     5   =>   4  5      =>   4  5  6
 7  8  6        7  8  6        7  8  6        7  8  6        7  8

also can be:

1  2  3
4     5
7  8  6



#########################
#       #       #       #
#   1   #   2   #   3   #
#       #       #       #
#########################
#       #       #       #
#   4   #   5   #   6   #
#       #       #       #
#########################
#       #       #       #
#   7   #   8   #       #
#       #       #       #
#########################

"""

import curses
from running_line import RunningLine

screen = curses.initscr()
curses.beep()
curses.noecho()
curses.cbreak()
curses.start_color()
screen.keypad(1)
curses.curs_set(0)

curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

solved_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
board = None

current_pos = 0
moves = 0


def start_new_game():
    global board, moves, current_pos
    board = generate_board()
    moves = 0
    current_pos = 0


def generate_board():
    # todo: should be randomly generated here
    return [0, 1, 3, 4, 2, 5, 7, 8, 6]


def swap(col1, col2):
    val1 = board[col1]
    board[col1] = board[col2]
    board[col2] = val1

    global current_pos
    current_pos = col2


def draw_board():
    screen.clear()
    screen.border(0)
    key_event = None

    screen.addstr(0, 10, "8 Puzzle", curses.color_pair(3))
    res = "next"
    while key_event != ord('\n'):
        if res == "next":
            col = 0
            screen_row = 1
            screen.addstr(screen_row, 1, "#########################", curses.color_pair(2))
            for row in range(3):
                screen.addstr(1 + screen_row, 1, "#       #       #       #", curses.color_pair(2))
                screen_row += 1
                screen.addstr(1 + screen_row, 1, f"#   {board[col] if board[col] != 0 else ' '}   #"
                                                 f"   {board[col+1] if board[col+1] != 0 else ' '}   # "
                                                 f"  {board[col+2] if board[col+2] != 0 else ' '}   #",
                              curses.color_pair(2))
                screen_row += 1
                screen.addstr(1 + screen_row, 1, "#       #       #       #", curses.color_pair(2))
                screen_row += 1
                screen.addstr(1 + screen_row, 1, "#########################", curses.color_pair(2))
                screen_row += 1

                col += 3

            screen.addstr(screen_row, 1, "#########################", curses.color_pair(2))

        screen.addstr(16, 1, "Use ← → ↑ ↓ to move the square", curses.color_pair(4))
        screen.addstr(18, 1, "Press Enter to go to main menu")

        key_event = screen.getch()
        res = move(key_event)

        if res == "success":
            curses.beep()
            break

    return res


def move(direction):
    move_to = current_pos
    if direction == curses.KEY_UP:
        if current_pos > 2:
            move_to = current_pos-3
    elif direction == curses.KEY_DOWN:
        if current_pos < 6:
            move_to = current_pos+3
    elif direction == curses.KEY_LEFT:
        if current_pos % 3 != 0:
            move_to = current_pos-1
    elif direction == curses.KEY_RIGHT:
        if (current_pos + 1) % 3 != 0:
            move_to = current_pos+1
    else:
        return

    if move_to != current_pos:
        global moves
        moves += 1
        swap(current_pos, move_to)
        if solved_board == board:
            return "success"
        else:
            return "next"


cur_selected_menu_style = curses.color_pair(1)
cur_menu_style = curses.A_NORMAL

rl = RunningLine("Made with ♡", 25)


def draw_about():
    screen.clear()
    screen.border(0)
    key_event = None
    screen.timeout(100)

    screen.addstr(2, 2, "Welcome to 8 Puzzle game :)", curses.A_STANDOUT)
    screen.addstr(6, 2, "Artem Shkolovy 2017", cur_menu_style)
    screen.addstr(7, 2, "https://github.com/shkolovy/8puzzle-terminal", cur_menu_style)

    while key_event != ord('\n'):
        screen.addstr(4, 2, rl.draw(), cur_menu_style)

        key_event = screen.getch()

    return "back"


def draw_end_menu():
    screen.clear()
    screen.border(0)

    key_event = None
    menu_pos_old = None
    menu_pos = 1

    while key_event != ord('\n'):
        if menu_pos != menu_pos_old:
            screen.addstr(2, 2, f"Success in {moves} moves", curses.color_pair(2))
            screen.addstr(4, 4, "Play again!", cur_selected_menu_style if menu_pos == 1 else cur_menu_style)
            screen.addstr(5, 4, "Quit", cur_selected_menu_style if menu_pos == 2 else cur_menu_style)

        key_event = screen.getch()

        if key_event == curses.KEY_UP:
            menu_pos_old = menu_pos
            menu_pos -= 1
            if menu_pos == 0:
                menu_pos = 2
        elif key_event == curses.KEY_DOWN:
            menu_pos_old = menu_pos
            menu_pos += 1
            if menu_pos > 2:
                menu_pos = 1

    return menu_pos if menu_pos != 2 else "exit"


def draw_greeting_menu():
    screen.clear()
    screen.border(0)

    key_event = None
    menu_pos = 1
    menu_pos_old = None

    # ord('\n') - Enter press
    while key_event != ord('\n'):
        if menu_pos != menu_pos_old:
            screen.addstr(2, 2, "Welcome to 8 Puzzle game :)", curses.A_STANDOUT)
            screen.addstr(4, 2, "Select something:", curses.A_BOLD)

            screen.addstr(5, 4, "1 - Start the game", cur_selected_menu_style if menu_pos == 1 else cur_menu_style)
            screen.addstr(6, 4, "2 - About", cur_selected_menu_style if menu_pos == 2 else cur_menu_style)
            screen.addstr(7, 4, "3 - Exit", cur_selected_menu_style if menu_pos == 3 else cur_menu_style)

        key_event = screen.getch()

        if key_event == curses.KEY_UP:
            menu_pos_old = menu_pos
            menu_pos -= 1
            if menu_pos == 0:
                menu_pos = 3
        elif key_event == curses.KEY_DOWN:
            menu_pos_old = menu_pos
            menu_pos += 1
            if menu_pos > 3:
                menu_pos = 1

    return menu_pos if menu_pos != 3 else "exit"

current_screen = "greeting_menu"

if __name__ == '__main__':
    close = False
    while not close:
        if current_screen == "greeting_menu":
            e = draw_greeting_menu()
            if e == 2:
                current_screen = "about_menu"
            elif e == 1:
                start_new_game()
                current_screen = "game"
        elif current_screen == "about_menu":
            e = draw_about()
            current_screen = "greeting_menu"
        elif current_screen == "game":
            e = draw_board()
            if e == "success":
                current_screen = "end_menu"
            else:
                current_screen = "greeting_menu"
        elif current_screen == "end_menu":
            e = draw_end_menu()
            if e == 1:
                start_new_game()
                current_screen = "game"

        if e == "exit":
            close = True

    curses.endwin()
