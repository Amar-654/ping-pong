import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, paddle_sound, wall_sound, score_sound):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, paddle_sound, wall_sound)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.target_score = 5  # default to 5 points

        self.score_sound = score_sound

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Score check
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            self.score_sound.play()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            self.score_sound.play()

        # Move AI paddle
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        if self.player_score == self.target_score or self.ai_score == self.target_score:
            winner = "Player Wins!" if self.player_score == self.target_score else "AI Wins!"
            text = self.font.render(winner, True, WHITE)
            screen.blit(text, (self.width // 2 - text.get_width() // 2,
                               self.height // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)

            result = self.show_replay_menu(screen)
            if result is not None:
                self.reset_game(result)
                return False
            else:
                return True
        return False

    def show_replay_menu(self, screen):
        menu_font = pygame.font.SysFont("Arial", 25)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        while True:
            screen.fill((0, 0, 0))
            y = self.height // 2 - 100
            for line in options:
                text = menu_font.render(line, True, (255, 255, 255))
                screen.blit(text, (self.width // 2 - text.get_width() // 2, y))
                y += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        return 2
                    elif event.key == pygame.K_5:
                        return 3
                    elif event.key == pygame.K_7:
                        return 4
                    elif event.key == pygame.K_ESCAPE:
                        return None

    def reset_game(self, new_target):
        self.player_score = 0
        self.ai_score = 0
        self.target_score = new_target
        self.ball = Ball(self.width // 2, self.height // 2, 7, 7, self.width, self.height,
                         self.ball.paddle_sound, self.ball.wall_sound)
