import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top or bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        # Check collision with player paddle
        if self.rect().colliderect(player.rect()):
            self.velocity_x = abs(self.velocity_x)  # Go right
            self.x = player.x + player.width

        # Check collision with AI paddle
        if self.rect().colliderect(ai.rect()):
            self.velocity_x = -abs(self.velocity_x)  # Go left
            self.x = ai.x - self.width

    def reset(self):
        """Reset the ball position and direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        """Return a rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
