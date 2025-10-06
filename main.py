import pygame
from game.game_engine import GameEngine

# Initialize pygame / mixer
pygame.init()
pygame.mixer.init()

# Load sounds
paddle_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game engine
engine = GameEngine(WIDTH, HEIGHT, paddle_sound, wall_sound, score_sound)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        if engine.check_game_over(SCREEN):
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
