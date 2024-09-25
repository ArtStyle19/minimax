import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen size and colors
WIDTH, HEIGHT = 300, 400  # Increased height to accommodate the menu
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)

# Fonts
FONT = pygame.font.Font(None, 40)
MENU_FONT = pygame.font.Font(None, 60)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

# Functions based on the description
def initial_state():
    """Returns the initial state of the board."""
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]

def player(state):
    """Returns the player (X or O) whose turn it is."""
    x_count = sum(row.count("X") for row in state)
    o_count = sum(row.count("O") for row in state)
    return "X" if x_count == o_count else "O"

def actions(state):
    """Returns the available legal moves in the current state."""
    return [(i, j) for i in range(BOARD_ROWS) for j in range(BOARD_COLS) if state[i][j] is None]

def result(state, action):
    """Returns the new state after taking action."""
    i, j = action
    if state[i][j] is not None:
        raise ValueError("Invalid action")

    new_state = [row[:] for row in state]  # Copy the state
    new_state[i][j] = player(state)  # Place the current player's mark
    return new_state

def terminal(state):
    """Checks if the game has ended (either a win or a draw)."""
    return check_winner(state) is not None or not any(None in row for row in state)

def check_winner(state):
    """Returns the winner of the game, if any."""
    # Check rows
    for row in state:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    # Check columns
    for col in range(BOARD_COLS):
        if state[0][col] == state[1][col] == state[2][col] and state[0][col] is not None:
            return state[0][col]
    # Check diagonals
    if state[0][0] == state[1][1] == state[2][2] and state[0][0] is not None:
        return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] and state[0][2] is not None:
        return state[0][2]
    return None

def utility(state):
    """Returns the score of the state (1 if X wins, -1 if O wins, 0 if draw)."""
    win = check_winner(state)
    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0

def minimax(state, is_maximizing):
    """Minimax algorithm to choose the best move."""
    if terminal(state):
        return utility(state), None

    if is_maximizing:
        best_value = -math.inf
        best_move = None
        for action in actions(state):
            min_result, _ = minimax(result(state, action), False)
            if min_result > best_value:
                best_value = min_result
                best_move = action
        return best_value, best_move
    else:
        best_value = math.inf
        best_move = None
        for action in actions(state):
            max_result, _ = minimax(result(state, action), True)
            if max_result < best_value:
                best_value = max_result
                best_move = action
        return best_value, best_move

# Pygame-specific functions
def draw_lines():
    """Draws the Tic-Tac-Toe board."""
    screen.fill(BG_COLOR)
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

def draw_figures(state):
    """Draws X's and O's on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if state[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif state[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def display_turn(turn):
    """Displays the current player's turn at the top of the screen."""
    pygame.draw.rect(screen, BG_COLOR, pygame.Rect(0, HEIGHT - 100, WIDTH, 50))  # Clear area
    text_surface = FONT.render(f"Turn: {turn}", True, TEXT_COLOR)
    screen.blit(text_surface, (10, HEIGHT - 90))

def draw_button():
    """Draws the AI Move button."""
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_COLOR

    if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50 and HEIGHT - 40 <= mouse_pos[1] <= HEIGHT - 10:
        button_color = BUTTON_HOVER_COLOR  # Change color if hovering

    pygame.draw.rect(screen, button_color, (WIDTH // 2 - 50, HEIGHT - 40, 100, 30))
    text_surface = FONT.render("AI Move", True, TEXT_COLOR)
    screen.blit(text_surface, (WIDTH // 2 - 35, HEIGHT - 37))

def button_clicked():
    """Checks if the AI Move button is clicked."""
    mouse_pos = pygame.mouse.get_pos()
    if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50 and HEIGHT - 40 <= mouse_pos[1] <= HEIGHT - 10:
        return True
    return False

# Menu functions
def draw_menu():
    """Draws the main menu."""
    screen.fill(BG_COLOR)
    title_surface = MENU_FONT.render("Tic-Tac-Toe", True, TEXT_COLOR)
    screen.blit(title_surface, (WIDTH // 2 - 110, HEIGHT // 4))

    draw_menu_button("Start Game", WIDTH // 2 - 75, HEIGHT // 2 - 30, 150, 50)
    draw_menu_button("Quit", WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50)

def draw_menu_button(text, x, y, width, height):
    """Draws a button in the main menu."""
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_COLOR

    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        button_color = BUTTON_HOVER_COLOR

    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = FONT.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x + 20, y + 10))

def menu_button_clicked(x, y, width, height):
    """Checks if a menu button is clicked."""
    mouse_pos = pygame.mouse.get_pos()
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        return True
    return False

def main_menu():
    """Displays the main menu and handles interaction."""
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_clicked(WIDTH // 2 - 75, HEIGHT // 2 - 30, 150, 50):
                    game_loop()  # Start the game if "Start Game" is clicked
                if menu_button_clicked(WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50):
                    pygame.quit()
                    sys.exit()  # Quit if "Quit" is clicked
        pygame.display.update()

# Main game loop
def game_loop():
    state = initial_state()
    game_over = False

    draw_lines()
    display_turn(player(state))

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if clicked_row < BOARD_ROWS and state[clicked_row][clicked_col] is None:
                    state = result(state, (clicked_row, clicked_col))

                    draw_figures(state)
                    display_turn(player(state))

                    if terminal(state):
                        game_over = True

            # AI Move button
            if event.type == pygame.MOUSEBUTTONDOWN and button_clicked() and not game_over:
                turn = player(state)
                _, best_move = minimax(state, turn == "X")
                state = result(state, best_move)

                draw_figures(state)
                display_turn(player(state))

                if terminal(state):
                    game_over = True

        draw_button()
        pygame.display.update()

# Start the game by launching the main menu
main_menu()
