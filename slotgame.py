
# Import pygame and random modules
import pygame
import random

# Initialize pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define some constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
REEL_WIDTH = 200
REEL_HEIGHT = 400
SYMBOL_SIZE = 100
SYMBOLS = ["apple", "banana", "cherry", "grape", "lemon", "orange", "pear", "plum", "watermelon"]
WINNING_LINES = [[1, 1, 1], [0, 0, 0], [2, 2, 2], [0, 1, 2], [2, 1, 0], [0, 1, 1], [1, 0, 0], [1, 2, 2], [2, 1, 1]]

# Load the images of the symbols
images = {}
for symbol in SYMBOLS:
    images[symbol] = pygame.image.load(symbol + ".png")

# Create a screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Slot Game")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Create a font object to render text
font = pygame.font.SysFont("Arial", 32)

# Create a reel class to represent each reel of the slot machine
class Reel:
    def __init__(self, x, y):
        # Set the position of the reel
        self.x = x
        self.y = y

        # Set the initial symbols of the reel
        self.symbols = [random.choice(SYMBOLS) for _ in range(3)]

        # Set the initial offset of the reel
        self.offset = 0

        # Set the initial speed of the reel
        self.speed = 0

        # Set the initial state of the reel
        self.spinning = False

    def update(self):
        # Update the offset of the reel based on the speed
        self.offset += self.speed

        # If the offset is greater than or equal to the symbol size
        if self.offset >= SYMBOL_SIZE:
            # Shift the symbols up by one position
            self.symbols.pop(0)
            self.symbols.append(random.choice(SYMBOLS))

            # Reset the offset to zero
            self.offset = 0

            # If the speed is greater than zero
            if self.speed > 0:
                # Decrease the speed by one unit
                self.speed -= 1

                # If the speed is zero
                if self.speed == 0:
                    # Stop spinning
                    self.spinning = False

    def draw(self):
        # Draw a rectangle around the reel
        pygame.draw.rect(screen, WHITE, (self.x, self.y, REEL_WIDTH, REEL_HEIGHT), 5)

        # Draw the symbols on the reel with respect to the offset
        for i in range(3):
            screen.blit(images[self.symbols[i]], (self.x + REEL_WIDTH // 2 - SYMBOL_SIZE // 2,
                                                  self.y + i * SYMBOL_SIZE + self.offset - SYMBOL_SIZE // 2))

    def spin(self):
        # Start spinning with a random speed between 10 and 20 units
        self.spinning = True
        self.speed = random.randint(10, 20)

# Create three reels for the slot machine
reels = [Reel(100 + i * REEL_WIDTH + i * 50, SCREEN_HEIGHT // 2 - REEL_HEIGHT // 2) for i in range(3)]

# Create a spin button for the slot machine
spin_button = pygame.Rect(SCREEN_WIDTH // 2 - REEL_WIDTH // 4,
                          SCREEN_HEIGHT // 2 + REEL_HEIGHT // 2 + REEL_HEIGHT // 8, REEL_WIDTH // 2,
                          REEL_HEIGHT // 4)

# Create a text object for the spin button
spin_text = font.render("SPIN", True, WHITE)

# Create a text object for the message
message_text = font.render("", True, WHITE)

# Create a variable to store the message
message = ""

# Create a variable to store the score
score = 0

# Create a loop to run the game
running = True
while running:
    # Handle the events
    for event in pygame.event.get():
        # If the user clicks the close button
        if event.type == pygame.QUIT:
            # Stop running the game
            running = False

        # If the user clicks the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse cursor
            x, y = pygame.mouse.get_pos()

            # If the mouse cursor is over the spin button and none of the reels are spinning
            if spin_button.collidepoint(x, y) and not any(reel.spinning for reel in reels):
                # Spin all the reels
                for reel in reels:
                    reel.spin()

                # Reset the message
                message = ""

    # Update the reels
    for reel in reels:
        reel.update()

    # Check if all the reels have stopped spinning
    if not any(reel.spinning for reel in reels):
        # Get the symbols at the center of each reel
        symbols = [reel.symbols[1] for reel in reels]

        # Check if any of the winning lines match with the symbols
        for line in WINNING_LINES:
            # Get the symbols on the line
            line_symbols = [symbols[i] for i in line]

            # If all the symbols on the line are the same
            if len(set(line_symbols)) == 1:
                # Set the message to "You win!"
                message = "You win!"

                # Increase the score by one unit
                score += 1

                # Break out of the loop
                break

        # If no winning line was found
        else:
            # Set the message to "You lose!"
            message = "You lose!"

    # Update the message text object with the message and score
    message_text = font.render(message + " Score: " + str(score), True, WHITE)

    # Fill the screen with black color
    screen.fill(BLACK)

    # Draw the reels on the screen
    for reel in reels:
        reel.draw()

    # Draw the spin button on the screen
    pygame.draw.rect(screen, GREEN, spin_button)
    screen.blit(spin_text, (spin_button.centerx - spin_text.get_width() // 2,
                            spin_button.centery - spin_text.get_height() // 2))

    # Draw the message text on the screen
    screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - REEL_HEIGHT // 2 - REEL_HEIGHT // 8))

    # Update the display
    pygame.display.flip()

    # Control the frame rate to 60 FPS
    clock.tick(60)

# Quit pygame
pygame.quit()
