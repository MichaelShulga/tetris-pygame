import pygame


class InfoWindow:
    def __init__(self, width, height, screen, left, top, font1, font2, border, heading):
        self.width = width
        self.height = height
        self.screen = screen
        self.left = left
        self.top = top

        self.font1 = font1
        self.font2 = font2
        self.border = border

        font = pygame.font.Font(None, 20)
        self.heading = font.render(heading, True, self.font1.color)

    def draw(self, text):
        font = pygame.font.Font(None, 40)
        text = font.render(text, True, self.font2.color)

        shift = 5
        self.screen.blit(self.heading, (self.left + shift, self.top + shift))
        self.screen.blit(text, (self.left + shift, self.top + shift * 2 + self.heading.get_height()))
        pygame.draw.rect(self.screen, self.border.color, (self.left, self.top,
                                                          self.width, self.height), 1)
