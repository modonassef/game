import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 80, 60
PIPE_WIDTH, PIPE_HEIGHT = 50, HEIGHT - 200
GRAVITY = 0.25
FLAP_HEIGHT = -5
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

# Load sound effects
flap_sound = pygame.mixer.Sound('7.wav')  # Replace 'flap_sound.wav' with your sound file
collision_sound = pygame.mixer.Sound('9.wav')  # Replace 'collision_sound.wav' with your sound file
game_over_sound = pygame.mixer.Sound('8.wav')  # Replace 'game_over_sound.wav' with your sound file


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zunjistan")

# Load images
bird_img = pygame.image.load('bird.png')  # Replace 'bird.png' with your image
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
game_over_imgs = [
    pygame.image.load('game_over_1.png'),  # Replace 'game_over_1.png', 'game_over_2.png', etc., with your images
    pygame.image.load('game_over_2.png'),
    pygame.image.load('game_over_3.png')
]

game_over_imgs = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in game_over_imgs]

# Create bird object
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_HEIGHT
        flap_sound.play()  # Play flap sound

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Create pipe objects
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.pipe_gap = 150
        self.top_pipe_height = random.randint(50, PIPE_HEIGHT - self.pipe_gap)
        self.bottom_pipe_height = HEIGHT - self.top_pipe_height - self.pipe_gap
        self.pipe_speed = 3
        self.pipe_width = PIPE_WIDTH

    def update(self):
        self.x -= self.pipe_speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.pipe_width, self.top_pipe_height))
        pygame.draw.rect(screen, GREEN, (self.x, HEIGHT - self.bottom_pipe_height, self.pipe_width, self.bottom_pipe_height))

    def collide(self, bird):
        if bird.y < self.top_pipe_height or bird.y + BIRD_HEIGHT > HEIGHT - self.bottom_pipe_height:
            if self.x < bird.x + BIRD_WIDTH < self.x + self.pipe_width:
                collision_sound.play()  # Play collision sound
                return True
        return False

# Create initial objects
bird = Bird()
pipes = []

# Create a function to display game over screen
def show_game_over():
    game_over_img = random.choice(game_over_imgs)  # Choose a random game over image
    screen.blit(game_over_img, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)

game_over = False  # Flag to track game over state

# Initialize score and timer variables
score = 0
score_font = pygame.font.Font(None, 36)  # Font for displaying the score
score_timer = pygame.time.get_ticks()  # Start time for score calculation

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    bird.flap()
                    game_over = False

    # Bird update and draw
    bird.update()
    bird.draw()

    # Game over logic
    if not game_over:
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw()
            if pipe.collide(bird):
                collision_sound.play()
                game_over = True
                break

            if pipe.x < -pipe.pipe_width:
                pipes.remove(pipe)

        # Score calculation
        current_time = pygame.time.get_ticks()
        if current_time - score_timer >= 1000:  # Increment score every 1000 milliseconds (1 second)
            score += 1
            score_timer = current_time  # Reset the timer for the next score increment

    # Display score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game over handling
    if game_over:
        show_game_over()
        bird = Bird()
        pipes = []
        game_over = False
        score = 0  # Reset score

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
sys.exit()
