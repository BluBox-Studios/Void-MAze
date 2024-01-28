import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the maze dimensions
width, height = 31, 21
cell_size = 20

# Set up Pygame window
screen = pygame.display.set_mode((width * cell_size, height * cell_size))
pygame.display.set_caption("Void Maze")

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (0, 128, 0)
LIGHT_GREEN = (144, 238, 144)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)  # New color for the player

# Hardcoded maze layout with exit marked by 'E' and starting position by 'S'
maze_layout = [
    "###############################",
    "#SB  #   #         #       E#",
    "# # # # ### ### ### ### ##### #",
    "# # # #     #   #   #   #     #",
    "# # # ### ##### ##### ### #####",
    "#     #   #   #     #   #     #",
    "# # # # ### ### ### ### # ### #",
    "# # # #   S   #   #   #   #   #",
    "# # ### ######### ### ### ### #",
    "# #   #       #   #       #   #",
    "# ### ##### ### ######### #####",
    "#   #     #   #   #     #     #",
    "# ##### ### ##### # ### ##### #",
    "#   #   #     #   # #   #   # #",
    "# # ### ##### ### ### ### ### #",
    "# #   #   #   #     #   #   # #",
    "# ##### ### ######### ##### # #",
    "#     #               #     # #",
    "#S########################### #",
    "###############################"
]

# Find the player's initial position and finish position
for y, row in enumerate(maze_layout):
    for x, cell in enumerate(row):
        if cell == 'S':
            start_x, start_y = x, y
            player_x, player_y = start_x, start_y
        elif cell == 'E':
            finish_x, finish_y = x, y

# Timer
start_time = None

# World Record
world_record_filename = "world_record.txt"

def load_world_record():
    try:
        with open(world_record_filename, "r") as file:
            return float(file.read())
    except FileNotFoundError:
        return float("inf")

def save_world_record(record):
    with open(world_record_filename, "w") as file:
        file.write(str(record))

def draw_maze():
    for y, row in enumerate(maze_layout):
        for x, cell in enumerate(row):
            if cell == ' ':
                green_cell_size = cell_size // 2
                for i in range(2):
                    for j in range(2):
                        color = LIGHT_GREEN if (i + j) % 2 == 0 else DARK_GREEN
                        pygame.draw.rect(screen, color, (x * cell_size + i * green_cell_size, y * cell_size + j * green_cell_size, green_cell_size, green_cell_size))
            elif cell == 'E':
                pygame.draw.rect(screen, RED, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif cell == 'S':
                pygame.draw.rect(screen, BLUE, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw the player on top
    pygame.draw.rect(screen, PURPLE, (player_x * cell_size, player_y * cell_size, cell_size, cell_size))

def display_winning_screen(elapsed_time):
    global world_record

    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    user_time_text = f"Your time: {elapsed_time:.2f} seconds"
    user_time = font.render(user_time_text, True, BLACK)
    user_time_rect = user_time.get_rect(center=(width * cell_size // 2, height * cell_size // 2 - 20))
    screen.blit(user_time, user_time_rect)

    if elapsed_time < world_record:
        world_record = elapsed_time
        save_world_record(world_record)
        world_record_text = f"New World Record: {world_record:.2f} seconds!"
    else:
        world_record_text = f"World Record: {world_record:.2f} seconds."

    world_record_render = font.render(world_record_text, True, BLACK)
    world_record_rect = world_record_render.get_rect(center=(width * cell_size // 2, height * cell_size // 2 + 20))
    screen.blit(world_record_render, world_record_rect)

    retry_text = "Press 'R' to retry"
    retry = font.render(retry_text, True, BLACK)
    retry_rect = retry.get_rect(center=(width * cell_size // 2, height * cell_size // 2 + 60))
    screen.blit(retry, retry_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Return to main menu to retry

def display_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    title_text = "Void Maze"
    title = font.render(title_text, True, BLACK)
    title_rect = title.get_rect(center=(width * cell_size // 2, height * cell_size // 2 - 20))
    screen.blit(title, title_rect)

    start_text = "Press 'S' to start"
    start = font.render(start_text, True, BLACK)
    start_rect = start.get_rect(center=(width * cell_size // 2, height * cell_size // 2 + 20))
    screen.blit(start, start_rect)

    pygame.display.flip()

def main():
    global player_x, player_y, start_time, world_record

    while True:
        display_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_time = time.time()
                    world_record = load_world_record()
                    play_game()

def play_game():
    global player_x, player_y, start_time, world_record

    player_x, player_y = start_x, start_y  # Reset player position
    start_time = time.time()  # Reset timer

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Move the player with arrow keys
                if event.key == pygame.K_LEFT and maze_layout[player_y][player_x - 1] == ' ':
                    player_x -= 1
                elif event.key == pygame.K_RIGHT and maze_layout[player_y][player_x + 1] == ' ':
                    player_x += 1
                elif event.key == pygame.K_UP and maze_layout[player_y - 1][player_x] == ' ':
                    player_y -= 1
                elif event.key == pygame.K_DOWN and maze_layout[player_y + 1][player_x] == ' ':
                    player_y += 1

                # Check if the player is adjacent to the finish
                if (abs(player_x - finish_x) <= 1 and abs(player_y - finish_y) == 0) or \
                   (abs(player_y - finish_y) <= 1 and abs(player_x - finish_x) == 0):
                    elapsed_time = time.time() - start_time
                    display_winning_screen(elapsed_time)
                    return  # Return to main menu to retry

        screen.fill(BLACK)
        draw_maze()
        pygame.display.flip()

if __name__ == "__main__":
    main()
