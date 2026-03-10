# Day 16: Terminal Snake Game

## Project Description

This project implements the classic Snake game directly in the terminal using Python's `curses` library. Players control a snake that moves around a bounded area, eating food to grow longer. The game ends if the snake hits the walls or itself. The objective is to achieve the highest possible score.

## Features

*   **Terminal-based UI**: Renders the game directly in the command line interface.
*   **Snake Movement**: Control the snake's direction using arrow keys.
*   **Food Generation**: Randomly places food items on the game board.
*   **Score Tracking**: Keeps track of the player's score as the snake eats food.
*   **Game Over Detection**: Detects collisions with walls or the snake's own body.
*   **Restart/Quit Option**: Allows players to restart the game or quit after a game over.

## How to Run

1.  **Prerequisites**:
    *   Python 3.x installed.
    *   `curses` library (usually pre-installed on Unix-like systems; for Windows, you might need `windows-curses`):
        ```bash
        pip install windows-curses # For Windows users
        ```

2.  **Navigate to the project directory**:
    ```bash
    cd Day16_Terminal_Snake_Game
    ```

3.  **Run the game**:
    ```bash
    python snake_game.py
    ```

## Controls

*   **Arrow Keys** (Up, Down, Left, Right): Change the snake's direction.
*   **r**: Restart the game after game over.
*   **q**: Quit the game after game over.

## Game Logic

1.  **Initialization**: Sets up the `curses` screen, hides the cursor, sets non-blocking input, and defines the game board boundaries.
2.  **Snake**: Represented as a list of `[y, x]` coordinates. The head is the first element, and the tail is the last.
3.  **Food**: A single `[y, x]` coordinate, randomly generated within the game boundaries, ensuring it doesn't overlap with the snake.
4.  **Movement**: In each game loop iteration, a new head position is calculated based on the current direction. This new head is added to the front of the snake list.
5.  **Eating Food**: If the new head position matches the food's position, the snake grows (the tail is not removed), and new food is generated. The score increases.
6.  **Collision Detection**: If the new head collides with the game boundaries or any part of the snake's body, the game ends.
7.  **Game Over Screen**: Displays the final score and prompts the user to restart or quit.

## Code Structure

*   `setup_game(stdscr)`: Initializes game variables like snake position, direction, food, and score.
*   `create_food(snake, sh, sw, box)`: Generates random coordinates for new food.
*   `display_game(stdscr, snake, food, score, sh, sw, box)`: Renders the snake, food, and score on the terminal screen.
*   `game_over_screen(stdscr, score)`: Displays the game over message and handles restart/quit input.
*   `main(stdscr)`: The main game loop, handling input, snake movement, collision, and game state.

## Dependencies

*   `curses` (standard library on Unix-like systems, `windows-curses` for Windows).

## Author

Manus AI
