import pygame  # Import pygame library for game functions
import random  # Import random library for random food placement

pygame.init()  # Initialize all pygame modules

# Define colors (RGB tuples)
black = (0, 0, 0)           # Background color
white = (255, 255, 255)     # Snake color
red = (255, 0, 0)           # Food color

# Set screen dimensions
width = 600  # Width of the game window
height = 400  # Height of the game window

# Create the game window
screen = pygame.display.set_mode((width, height))  # Initialize game screen
pygame.display.set_caption("Snake Game ")  # Set window title

block_size = 20  # Size of each snake segment (square)
snake_speed = 5  # Initial speed (frames per second)

clock = pygame.time.Clock()  # Clock object to control FPS

font = pygame.font.SysFont("arial", 15)  # Font for displaying text

def draw_snake(snake_list):
    # Draw each segment of the snake on the screen
    for segment in snake_list:
        pygame.draw.rect(screen, white, [segment[0], segment[1], block_size, block_size])

def show_score(score):
    # Render the score text in red
    value = font.render(f"Score: {score}", True, red)
    # Display score at fixed position on screen
    screen.blit(value, [5, 10])

def message(msg, color, y_displace=0):
    # Render a message and display it centered on the screen, optionally displaced vertically
    mesg = font.render(msg, True, color)
    rect = mesg.get_rect(center=(width // 2, height // 2 + y_displace))
    screen.blit(mesg, rect)

def game_loop():
    while True:  # Loop to restart the game after game over
        # Initialize game variables
        x = width // 2  # Start snake's x position (center)
        y = height // 2  # Start snake's y position (center)
        x_change = 0  # Change in x (velocity)
        y_change = 0  # Change in y (velocity)
        snake_list = []  # List to store snake segments' positions
        length = 1  # Initial snake length

        # Randomly position the first food block
        food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
        food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

        speed = snake_speed  # Current game speed
        running = True  # Game running flag
        game_over = False  # Game over flag

        while running:
            while game_over:
                screen.fill(black)  # Clear screen with black background
                message("Game Over! Press C to Play Again or Q to Quit", red, -30)  # Show game over message
                message(f"Your Score: {length - 1}", white, 30)  # Show final score
                pygame.display.update()  # Update display to show messages

                for event in pygame.event.get():  # Event loop during game over
                    if event.type == pygame.QUIT:
                        pygame.quit()  # Quit pygame
                        quit()  # Exit program
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Quit game
                            pygame.quit()
                            quit()
                        if event.key == pygame.K_c:  # Restart game
                            game_over = False  # Reset game over flag
                            running = False  # Exit current game loop to restart

            for event in pygame.event.get():  # Event handling during gameplay
                if event.type == pygame.QUIT:  # Close window event
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:  # Keyboard input to control snake
                    # Prevent snake from reversing on itself
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -block_size  # Move left
                        y_change = 0
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = block_size  # Move right
                        y_change = 0
                    elif event.key == pygame.K_UP and y_change == 0:
                        y_change = -block_size  # Move up
                        x_change = 0
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        y_change = block_size  # Move down
                        x_change = 0

            x += x_change  # Update snake's x position
            y += y_change  # Update snake's y position

            # Check collision with walls (boundaries)
            if x < 0 or x >= width or y < 0 or y >= height:
                game_over = True  # Trigger game over

            screen.fill(black)  # Fill background with black

            # Draw the food block (red)
            pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

            snake_head = [x, y]  # New head position
            snake_list.append(snake_head)  # Add head to snake body list

            # Remove tail if snake is longer than its length
            if len(snake_list) > length:
                del snake_list[0]

            # Check collision of snake head with its body
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over = True  # Trigger game over

            draw_snake(snake_list)  # Draw snake
            show_score(length - 1)  # Display current score

            pygame.display.update()  # Update the full display surface to screen

            # Check if snake has eaten the food
            if x == food_x and y == food_y:
                length += 1  # Increase snake length by 1
                # Reposition food randomly on grid
                food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
                food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
                speed += 0.5  # Increase speed slightly

            clock.tick(speed)  # Control the game speed (FPS)

# Run the game
game_loop()
