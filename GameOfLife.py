import pygame
import numpy as np


GRID_WIDTH = int(input("Enter the width of the grid (in cells): "))
GRID_HEIGHT = int(input("Enter the height of the grid (in cells): "))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (255, 255, 0)  
NEON_BLUE = (255, 20, 147)
CELL_SIZE = 70
GRID_SIZE = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
FPS = 5 #Frames per second 


pygame.init()


font_size = int(GRID_SIZE[0] * 0.05) #ensuring that the font size is comparable to width 
font = pygame.font.Font(None, font_size)


def display_text(text, y):
    
    lines = text.splitlines() #splitting text into lines as new line function didnt work as expected
    for line in lines:
        text_surface = font.render(line, True, NEON_GREEN)
        screen.blit(text_surface, (5, y))
        y += font.get_height() #increment y coordinate for the next line

def display_instructions():
    screen.fill(NEON_BLUE)
    text2="Welcome to Conway's Game of Life!\n\nInstructions:\n- Press SPACE to start/pause the simulation.\n- Press R to initialize the grid randomly with live cells.\n- Press D to switch to define mode where you can click cells to toggle their state.\n- Click on cells in define mode to toggle them.\n- Close the window or press ESC to exit the simulation."
    display_text(text2, GRID_HEIGHT/2)#displaying instructions to centre text 
    
    


# Create the game window
screen = pygame.display.set_mode(GRID_SIZE)



rows = GRID_SIZE[1]// CELL_SIZE
cols = GRID_SIZE[0] // CELL_SIZE

# Initialize grid
grid = np.zeros((rows, cols), dtype=int)

# Function to draw grid lines
def draw_grid():
    for x in range(0, GRID_SIZE[0], CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, GRID_SIZE[1]))
    for y in range(0, GRID_SIZE[1], CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (GRID_SIZE[0], y))

# Function to initialize grid randomly
def init_random():
    global grid
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

# Function to handle mouse click events
def handle_click(pos):
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
   
    grid[row, col] = 1 - grid[row, col] 

# Function to update grid based on game rules
def update_grid():
    global grid
    new_grid = grid.copy()
    for row in range(rows):
        for col in range(cols):
            neighbors = count_neighbors(grid, row, col)
            if grid[row, col] == 1:  # If alive
                if neighbors < 2 or neighbors > 3:
                    new_grid[row, col] = 0  # Dies
            else:  # If dead
                if neighbors == 3:
                    new_grid[row, col] = 1  # Alive
    grid = new_grid

# Function to count live neighbors
def count_neighbors(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            n_row, n_col = row + i, col + j
            if 0 <= n_row < rows and 0 <= n_col < cols:
                count += grid[n_row, n_col]
    return count

# Main game loop
def main():
    running = True
    paused = True
    define_mode = False
    while running:
        screen.fill(NEON_BLUE)
        display_instructions()
        draw_grid()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    init_random()
                elif event.key == pygame.K_d:
                    define_mode = not define_mode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if define_mode:
                    handle_click(pygame.mouse.get_pos())

        # Update grid if not paused
        if not paused:
            update_grid()

        # Draw cells
        for row in range(rows):
            for col in range(cols):
                if grid[row, col] == 1:
                    pygame.draw.rect(screen,NEON_GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
