import pygame


class Board:
    def __init__(self, width, height, screen, left, top, cell_size, background, border):
        self.width = width
        self.height = height
        self.screen = screen
        self.background, self.border = background, border

        self.board = [[background] * width for _ in range(height)]

        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        pygame.draw.rect(self.screen, self.border.color, (
            self.left - 1, self.top - 1, self.width * (self.cell_size + 1) + 1 + 2,
            self.height * (self.cell_size + 1) + 1 + 2), 1)
        for y in range(self.height):
            for x in range(self.width):
                self.empty(x * (self.cell_size + 1) + self.left + 1, y * (self.cell_size + 1) + self.top + 1,
                           self.board[y][x].color)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left - 1) // (self.cell_size + 1)
        cell_y = (mouse_pos[1] - self.top - 1) // (self.cell_size + 1)
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def empty(self, left, top, color=None):
        if not color:
            color = self.background.color
        pygame.draw.rect(self.screen, color, (left, top, self.cell_size, self.cell_size))

    def clear(self):
        self.board = [[self.background] * self.width for _ in range(self.height)]
