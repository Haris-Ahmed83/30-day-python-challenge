
import curses
import random

def setup_game(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100 ms

    sh, sw = stdscr.getmaxyx()  # Screen height and width
    box = [[3, 3], [sh - 3, sw - 3]]  # Game border
    stdscr.border(box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [
        [sh // 2, sw // 2 + 1],  # Head
        [sh // 2, sw // 2],      # Body
        [sh // 2, sw // 2 - 1]   # Tail
    ]
    direction = curses.KEY_RIGHT

    food = create_food(snake, sh, sw, box)
    score = 0

    return snake, direction, food, score, sh, sw, box

def create_food(snake, sh, sw, box):
    while True:
        food = [
            random.randint(box[0][0] + 1, box[1][0] - 1),
            random.randint(box[0][1] + 1, box[1][1] - 1)
        ]
        if food not in snake:
            return food

def display_game(stdscr, snake, food, score, sh, sw, box):
    stdscr.clear()
    stdscr.border(box[0][0], box[0][1], box[1][0], box[1][1])

    # Display snake
    for y, x in snake:
        stdscr.addch(y, x, '#')

    # Display food
    stdscr.addch(food[0], food[1], '*')

    # Display score
    stdscr.addstr(box[0][0] - 1, box[0][1], f' Score: {score} ')
    stdscr.refresh()

def game_over_screen(stdscr, score):
    sh, sw = stdscr.getmaxyx()
    game_over_text = "GAME OVER!"
    score_text = f"Final Score: {score}"
    restart_text = "Press 'r' to restart or 'q' to quit."

    stdscr.clear()
    stdscr.addstr(sh // 2 - 2, sw // 2 - len(game_over_text) // 2, game_over_text)
    stdscr.addstr(sh // 2, sw // 2 - len(score_text) // 2, score_text)
    stdscr.addstr(sh // 2 + 2, sw // 2 - len(restart_text) // 2, restart_text)
    stdscr.nodelay(0)  # Blocking input for game over screen
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('r'):
            return True
        elif key == ord('q'):
            return False

def main(stdscr):
    while True:
        snake, direction, food, score, sh, sw, box = setup_game(stdscr)

        while True:
            next_head = [snake[0][0], snake[0][1]]
            key = stdscr.getch()

            if key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT
            elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT
            elif key == curses.KEY_UP and direction != curses.KEY_DOWN:
                direction = curses.KEY_UP
            elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
                direction = curses.KEY_DOWN

            if direction == curses.KEY_UP:
                next_head[0] -= 1
            elif direction == curses.KEY_DOWN:
                next_head[0] += 1
            elif direction == curses.KEY_LEFT:
                next_head[1] -= 1
            elif direction == curses.KEY_RIGHT:
                next_head[1] += 1

            # Game over conditions
            if (
                next_head[0] <= box[0][0] or
                next_head[0] >= box[1][0] or
                next_head[1] <= box[0][1] or
                next_head[1] >= box[1][1] or
                next_head in snake
            ):
                break

            snake.insert(0, next_head)

            if next_head == food:
                score += 1
                food = create_food(snake, sh, sw, box)
            else:
                snake.pop()

            display_game(stdscr, snake, food, score, sh, sw, box)

        if not game_over_screen(stdscr, score):
            break

if __name__ == '__main__':
    curses.wrapper(main)
