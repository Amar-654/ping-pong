import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        """Move paddle up or down while staying within the screen."""
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        """Return the paddle as a pygame.Rect for drawing and collision."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """Automatically move AI paddle to follow the ball."""
        if ball.y < self.y:
            self.move(-self.speed, screen_height)
        elif ball.y > self.y + self.height:
            self.move(self.speed, screen_height)
