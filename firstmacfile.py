#!/usr/bin/env python3
"""
Terminal Snake game (single file).
Requirements:
 - Python 3.7+
 - On Windows: `pip install windows-curses`
Controls:
 - Arrow keys to move
 - 'p' to pause / resume
 - 'q' to quit
"""

import curses
import random
import time

# Game settings
INITIAL_SPEED = 120  # milliseconds per step (lower -> faster)
SPEED_INC = 3        # decrease ms every food eaten (speeds up)
MIN_SPEED = 40
HEIGHT = 20
WIDTH = 40
WALLS = True         # if True, hitting border = game over; if False, wraps around

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])


def within_bounds(pos):
    r, c = pos
    return 0 <= r < HEIGHT and 0 <= c < WIDTH


def place_food(snake):
    while True:
        f = (random.randrange(0, HEIGHT), random.randrange(0, WIDTH))
        if f not in snake:
            return f


def draw_board(win, snake, food, score):
    win.clear()
    # Draw border
    for c in range(WIDTH + 2):
        win.addch(0, c, '#')
        win.addch(HEIGHT + 1, c, '#')
    for r in range(1, HEIGHT + 1):
        win.addch(r, 0, '#')
        win.addch(r, WIDTH + 1, '#')

    # Draw food
    fr, fc = food
    win.addch(fr + 1, fc + 1, '@')

    # Draw snake
    for i, (r, c) in enumerate(snake):
        ch = 'O' if i == 0 else 'o'
        win.addch(r + 1, c + 1, ch)

    # Draw score and controls
    win.addstr(HEIGHT + 2, 0, f" Score: {score}  (p)ause (q)uit ")
    win.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(INITIAL_SPEED)

    # Create a new window with room for border and status line
    win = curses.newwin(HEIGHT + 3, WIDTH + 2, 0, 0)
    win.keypad(True)

    # Initial snake: centered, length 4 moving right
    start_r = HEIGHT // 2
    start_c = WIDTH // 2 - 2
    snake = [(start_r, start_c + i) for i in range(4)][::-1]  # head first
    direction = RIGHT
    next_direction = direction

    food = place_food(snake)
    score = 0
    speed = INITIAL_SPEED
    paused = False
    game_over = False

    draw_board(win, snake, food, score)

    while True:
        try:
            key = win.getch()
        except KeyboardInterrupt:
            break

        if key != -1:
            if key in (curses.KEY_UP, ord('w')):
                if direction != DOWN:
                    next_direction = UP
            elif key in (curses.KEY_DOWN, ord('s')):
                if direction != UP:
                    next_direction = DOWN
            elif key in (curses.KEY_LEFT, ord('a')):
                if direction != RIGHT:
                    next_direction = LEFT
            elif key in (curses.KEY_RIGHT, ord('d')):
                if direction != LEFT:
                    next_direction = RIGHT
            elif key in (ord('p'), ord('P')):
                paused = not paused
                if paused:
                    win.addstr(HEIGHT // 2, (WIDTH // 2) - 3, " PAUSED ")
                    win.refresh()
                else:
                    draw_board(win, snake, food, score)
            elif key in (ord('q'), ord('Q')):
                break

        if paused:
            time.sleep(0.05)
            continue

        direction = next_direction
        head = snake[0]
        new_head = add_tuples(head, direction)

        # Wrap or wall collision
        if WALLS:
            if not within_bounds(new_head):
                game_over = True
        else:
            nr, nc = new_head
            nr %= HEIGHT
            nc %= WIDTH
            new_head = (nr, nc)

        # Self collision
        if new_head in snake:
            game_over = True

        if game_over:
            win.clear()
            win.addstr(HEIGHT // 2 - 1, WIDTH // 2 - 5, " GAME OVER ")
            win.addstr(HEIGHT // 2, WIDTH // 2 - 7, f" Final score: {score} ")
            win.addstr(HEIGHT // 2 + 2, WIDTH // 2 - 12, " Press 'r' to restart or 'q' to quit ")
            win.refresh()
            stdscr.nodelay(False)
            while True:
                ch = stdscr.getch()
                if ch in (ord('q'), ord('Q')):
                    return
                if ch in (ord('r'), ord('R')):
                    # Restart by calling main again (simpler than resetting everything)
                    main(stdscr)
                    return

        # Move snake
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            # speed up
            speed = max(MIN_SPEED, speed - SPEED_INC)
            win.timeout(speed)
            food = place_food(snake)
        else:
            snake.pop()

        draw_board(win, snake, food, score)

        # small sleep to make movement smooth if curses timeout not precise
        # time.sleep(speed / 1000.0)  # not necessary because of win.timeout

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print("Error running the game:", e)
        print("On Windows, make sure you installed 'windows-curses' (pip install windows-curses).")
