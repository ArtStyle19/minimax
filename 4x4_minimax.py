import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen size and colors
# Screen size and colors
WIDTH, HEIGHT = 400, 500  # Increased height to accommodate the menu
LINE_WIDTH = 15
SQUARE_SIZE = WIDTH // 3
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

WIN_COLOR = (255, 0, 255)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
SHADOW_COLOR = (0, 0, 0, 100)  # Semi-transparent shadow color

# Fonts
FONT = pygame.font.Font(None, 40)
MENU_FONT = pygame.font.Font(None, 60)

# Fonts
FONT = pygame.font.Font(None, 40)
MENU_FONT = pygame.font.Font(None, 60)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

def initial_state(rows, cols):
    """Returns the initial state of the board."""
    return [[None for _ in range(cols)] for _ in range(rows)]

def player(state):
    """Returns the player (X or O) whose turn it is."""
    x_count = sum(row.count("X") for row in state)
    o_count = sum(row.count("O") for row in state)
    return "X" if x_count == o_count else "O"

def actions(state):
    """Returns the available legal moves in the current state."""
    return [(i, j) for i in range(len(state)) for j in range(len(state[0])) if state[i][j] is None]

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
    rows, cols = len(state), len(state[0])
    # Check rows
    for row in state:
        if row.count(row[0]) == len(row) and row[0] is not None:
            return row[0]
    # Check columns
    for col in range(cols):
        if all(state[row][col] == state[0][col] for row in range(rows)) and state[0][col] is not None:
            return state[0][col]
    # Check diagonals
    if all(state[i][i] == state[0][0] for i in range(rows)) and state[0][0] is not None:
        return state[0][0]
    if all(state[i][cols - 1 - i] == state[0][cols - 1] for i in range(rows)) and state[0][cols - 1] is not None:
        return state[0][cols - 1]
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

def minimax(state, depth, is_maximizing, alpha, beta):
    if terminal(state):
        return utility(state), None

    if is_maximizing:
        best_value = -math.inf
        best_move = None
        for action in actions(state):
            min_result, _ = minimax(result(state, action), depth + 1, False, alpha, beta)
            if min_result > best_value:
                best_value = min_result
                best_move = action
            alpha = max(alpha, best_value)
            if beta <= alpha:  # Beta cut-off
                break
        return best_value, best_move
    else:
        best_value = math.inf
        best_move = None
        for action in actions(state):
            max_result, _ = minimax(result(state, action), depth + 1, True, alpha, beta)
            if max_result < best_value:
                best_value = max_result
                best_move = action
            beta = min(beta, best_value)
            if beta <= alpha:  # Alpha cut-off
                break
        return best_value, best_move
def draw_lines(rows, cols):
    """Draws the Tic-Tac-Toe board."""
    screen.fill(BG_COLOR)
    # Draw horizontal lines
    for i in range(1, rows):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
    # Draw vertical lines
    for j in range(1, cols):
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * j, 0), (SQUARE_SIZE * j, HEIGHT - 100), LINE_WIDTH)

def draw_figures(state):
    """Draws X's and O's on the board."""
    for row in range(len(state)):
        for col in range(len(state[0])):
            if state[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif state[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def draw_rounded_rect(surface, color, rect, radius):
    """Draws a rounded rectangle on the surface."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def display_turn(turn):
    """Displays the current player's turn at the top of the screen with enhanced styling."""
    # Define new colors
    shadow_color = (0, 0, 50, 100)  # Dark blue shadow
    bg_color = (173, 216, 230)  # Light blue background
    text_color = (255, 255, 255)  # White text

    # Draw shadow
    shadow_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 50)
    draw_rounded_rect(screen, shadow_color, shadow_rect.move(2, 2), 15)  # Shadow with offset

    # Draw background
    bg_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 50)
    draw_rounded_rect(screen, bg_color, bg_rect, 15)  # Rounded rectangle background

    # Render text
    text_surface = FONT.render(f"Turn: {turn}", True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 75))  # Center text

    # Blit text to screen
    screen.blit(text_surface, text_rect)

def draw_rounded_rect(surface, color, rect, radius):
    """Draws a rounded rectangle on the surface."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_button():
    """Draws the Minimax button with enhanced styling."""
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_COLOR
    button_rect = (WIDTH // 2 - 75, HEIGHT - 40, 150, 40)  # Increased size

    # Change color if hovering
    if button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]:
        button_color = BUTTON_HOVER_COLOR  # Change color if hovering

    # Draw button with rounded corners
    draw_rounded_rect(screen, button_color, button_rect, 20)  # Increased radius for rounded corners

    # Draw button border
    border_color = (0, 0, 0)  # Black border
    pygame.draw.rect(screen, border_color, button_rect, 2, border_radius=20)  # Draw border

    # Render text
    text_surface = FONT.render("Minimax", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 20))  # Center text

    # Blit text to screen
    screen.blit(text_surface, text_rect)



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
    screen.blit(title_surface, (WIDTH // 2 - 110, HEIGHT // 10))

    # Increased button width from 150 to 200
    draw_menu_button("3x3 Game", WIDTH // 2 - 100, HEIGHT // 3 - 30, 200, 50)
    draw_menu_button("4x4 Game", WIDTH // 2 - 100, HEIGHT // 3 + 40, 200, 50)
    draw_menu_button("5x5 Game", WIDTH // 2 - 100, HEIGHT // 3 + 110, 200, 50)
    draw_menu_button("Quit", WIDTH // 2 - 100, HEIGHT // 3 + 180, 200, 50)

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
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

def main_menu():
    """Displays the main menu and handles navigation."""
    while True:
        draw_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_clicked(WIDTH // 2 - 100, HEIGHT // 3 - 30, 200, 50):
                    run_game(3, 3)  # Start 3x3 game
                elif menu_button_clicked(WIDTH // 2 - 100, HEIGHT // 3 + 40, 200, 50):
                    run_game(4, 4)  # Start 4x4 game
                elif menu_button_clicked(WIDTH // 2 - 100, HEIGHT // 3 + 110, 200, 50):
                    run_game(5, 5)  # Start 5x5 game
                elif menu_button_clicked(WIDTH // 2 - 100, HEIGHT // 3 + 180, 200, 50):
                    pygame.quit()
                    sys.exit()

def draw_winning_line(winner, state):
    """Draws a line for the winning player."""
    rows, cols = len(state), len(state[0])
    
    if winner is None:
        return

    # Check rows
    for row in range(rows):
        if state[row].count(state[row][0]) == cols and state[row][0] is not None:
            start_pos = (0, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            end_pos = (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.line(screen, CROSS_COLOR, start_pos, end_pos, LINE_WIDTH)
            return

    # Check columns
    for col in range(cols):
        if all(state[row][col] == state[0][col] for row in range(rows)) and state[0][col] is not None:
            start_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 0)
            end_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 100)
            pygame.draw.line(screen, WIN_COLOR, start_pos, end_pos, LINE_WIDTH - 10)
            return

    # Check diagonals
    if all(state[i][i] == state[0][0] for i in range(rows)) and state[0][0] is not None:
        start_pos = (0, 0)
        end_pos = (WIDTH, HEIGHT - 100)  # Exclude the button area
        pygame.draw.line(screen, WIN_COLOR, start_pos, end_pos, LINE_WIDTH - 10)
        return

    if all(state[i][cols - 1 - i] == state[0][cols - 1] for i in range(rows)) and state[0][cols - 1] is not None:
        start_pos = (WIDTH, 0)
        end_pos = (0, HEIGHT - 100)  # Exclude the button area
        pygame.draw.line(screen, WIN_COLOR, start_pos, end_pos, LINE_WIDTH - 10)
        return

def run_game(rows, cols):
    """Main loop for the Tic-Tac-Toe game."""
    global SQUARE_SIZE
    SQUARE_SIZE = WIDTH // cols
    state = initial_state(rows, cols)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                clicked_row = mouse_y // SQUARE_SIZE
                clicked_col = mouse_x // SQUARE_SIZE

                # Check if clicked_row and clicked_col are within bounds
                if 0 <= clicked_row < rows and 0 <= clicked_col < cols:
                    if state[clicked_row][clicked_col] is None:
                        state[clicked_row][clicked_col] = player(state)

                        if terminal(state):
                            game_over = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run_game(rows, cols)  # Restart the game

            # Handle AI move when 'a' is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if player(state) == "X":  # Only allow X to trigger AI
                    ai_move = minimax(state, 0, True, -math.inf, math.inf)[1]
                    if ai_move:
                        state = result(state, ai_move)
                        if terminal(state):
                            game_over = True

            # Handle button click for AI Move
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and button_clicked():
                if player(state) == "X":
                    ai_move = minimax(state, 0, True, -math.inf, math.inf)[1]
                    if ai_move:
                        state = result(state, ai_move)
                        if terminal(state):
                            game_over = True
                elif player(state) == "O":  # Allow O to also use the button
                    ai_move = minimax(state, 0, False, -math.inf, math.inf)[1]  # Change to False for O
                    if ai_move:
                        state = result(state, ai_move)
                        if terminal(state):
                            game_over = True

        screen.fill(BG_COLOR)
        draw_lines(rows, cols)
        draw_figures(state)
        if not game_over:
            display_turn(player(state))
            draw_button()
        else:
            winner = check_winner(state)
            text = "Draw!" if winner is None else f"{winner} wins!"
            text_surface = FONT.render(text, True, TEXT_COLOR)
            screen.blit(text_surface, (WIDTH // 2 - 50, HEIGHT // 2 - 30))

            draw_winning_line(winner, state)  # Draw the winning line
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
