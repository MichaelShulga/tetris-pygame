import ast
import random
import sys

import pygame
from PyQt5.QtWidgets import QApplication
from board import Board
from color import Color
from info_window import InfoWindow
from settings import SettingsWindow

from load_image import load_image
from matrix import transpose, matrix_count, copy


class ButtonsBoard(Board):
    def __init__(self, width, height, screen, left, top, cell_size, background, border):
        super().__init__(width, height, screen, left, top, cell_size, background, border)
        self.game_running = None

        # images init
        self.run_image = load_image("run_button_2.png", -1)
        self.run_active_image = load_image("run_button_active.png", -1)
        self.settings_image = load_image("settings_button.png", -1)
        self.settings_active_image = load_image("settings_button_active.png", -1)
        self.stop_image = load_image("stop_button.png", -1)
        self.stop_active_image = load_image("stop_button_active.png", -1)
        self.rerun_image = load_image("rerun_button.png", -1)
        self.rerun_active_image = load_image("rerun_button_active.png", -1)
        self.stop_disabled_image = load_image("stop_button_disabled.png", -1)
        self.light_mode_image = load_image("light_mode_button.png", -1)
        self.light_mode_active_image = load_image("light_mode_button_active.png", -1)
        self.dark_mode_image = load_image("dark_mode_button.png", -1)
        self.dark_mode_active_image = load_image("dark_mode_button_active.png", -1)

        self.board = [[self.run_button, self.stop_button, self.settings_button, self.mode_button]]

    def render(self):
        pygame.draw.rect(self.screen, self.border.color, (
            self.left, self.top, self.width * (self.cell_size + 1) + 1, self.height * (self.cell_size + 1) + 1))
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x](x * (self.cell_size + 1) + self.left + 1, y * (self.cell_size + 1) + self.top + 1)

    def run_button(self, left, top):
        image = ((self.run_image, self.run_active_image),
                 (self.rerun_image, self.rerun_active_image)
                 )[int(self.game_running)][int(self.get_cell(pygame.mouse.get_pos()) == (0, 0))]
        self.empty(left, top)
        self.screen.blit(image, (left, top))

    def stop_button(self, left, top):
        image = ((self.stop_disabled_image, self.stop_disabled_image),
                 (self.stop_image, self.stop_active_image)
                 )[int(self.game_running)][int(self.get_cell(pygame.mouse.get_pos()) == (1, 0))]
        self.empty(left, top)
        self.screen.blit(image, (left, top))

    def settings_button(self, left, top):
        if self.get_cell(pygame.mouse.get_pos()) == (2, 0):
            image = self.settings_active_image
        else:
            image = self.settings_image
        self.empty(left, top)
        self.screen.blit(image, (left, top))

    def mode_button(self, left, top):
        image = ((self.light_mode_image, self.light_mode_active_image),
                 (self.dark_mode_image, self.dark_mode_active_image)
                 )[int(self.background.color == self.background.colors[1])][
            int(self.get_cell(pygame.mouse.get_pos()) == (3, 0))]
        self.empty(left, top)
        self.screen.blit(image, (left, top))


class MainBoard(Board):
    def __init__(self, width, height, screen, left, top, cell_size, background, border):
        super().__init__(width, height, screen, left, top, cell_size, background, border)
        self.points = 0

        self.figure = None
        self.x, self.y = None, None
        self.shift = 0

        self.background_board = copy(self.board)

    def remove_empty(self):
        for i in range(len(self.board)):
            if self.background not in self.board[i]:
                del self.background_board[i]
                self.background_board = [[self.background] * self.width] + self.background_board
                self.points += 100

    def generate_coords(self):
        self.x, self.y = random.randint(0, self.width - 4), 0

    def update(self):
        self.board = self.set_figure(self.x, self.y, self.background_board)

    def can_move(self, x=0, y=0, figure=None):
        new_board = self.set_figure(self.x + x, self.y + y, self.background_board, figure)
        a = matrix_count(self.background_board, self.background) - 4
        b = matrix_count(new_board, self.background)
        return a == b

    def set_figure(self, x, y, board, figure=None):
        if figure is None:
            figure = self.figure
        result = copy(board)

        for i in range(4):
            for j in range(4):
                cell = figure[i][j]
                if cell != self.background \
                        and 0 <= i + y - self.shift <= self.height - 1 and 0 <= j + x <= self.width - 1:
                    result[i + y - self.shift][j + x] = cell
        return result

    def update_shift(self):
        self.shift = 0
        for i in self.figure:
            if i.count(self.background) == 4:
                self.shift += 1
            else:
                return


class FigureBoard(Board):
    def __init__(self, width, height, screen, left, top, cell_size, background, border, figure_colors):
        super().__init__(width, height, screen, left, top, cell_size, background, border)

        color1, color2, color3, color4, color5, color6 = figure_colors
        figure1 = [[self.background] * 4,
                   [self.background, color1, color1, self.background],
                   [self.background, color1, color1, self.background],
                   [self.background] * 4]

        figure2 = [[self.background] * 4,
                   [self.background, color2, color2, self.background],
                   [color2, color2, self.background, self.background],
                   [self.background] * 4]

        figure3 = [[self.background] * 4,
                   [color3, color3, self.background, self.background],
                   [self.background, color3, color3, self.background],
                   [self.background] * 4]

        figure4 = [[self.background, color4, self.background, self.background],
                   [self.background, color4, self.background, self.background],
                   [self.background, color4, self.background, self.background],
                   [self.background, color4, self.background, self.background]]

        figure5 = [[self.background, self.background, self.background, self.background],
                   [self.background, color5, self.background, self.background],
                   [self.background, color5, self.background, self.background],
                   [self.background, color5, color5, self.background]]

        figure6 = [[self.background, self.background, self.background, self.background],
                   [self.background, self.background, color6, self.background],
                   [self.background, self.background, color6, self.background],
                   [self.background, color6, color6, self.background]]

        self.figures = [figure1, figure2, figure3, figure4, figure5, figure6]

    def generate(self):
        figure = random.choice(self.figures)
        for _ in range(random.randint(0, 3)):
            figure = transpose(figure)
        return figure


def restart(main_board, figure_board):
    main_board.clear()
    figure_board.clear()

    main_board.points = 0
    main_board.figure = None
    main_board.x, y = None, None
    figure_board.board = figure_board.generate()


def next_figure(main_board, figure_board):
    main_board.background_board = copy(main_board.board)
    main_board.remove_empty()
    main_board.points += 10
    main_board.figure = figure_board.board
    main_board.generate_coords()
    main_board.update_shift()

    figure_board.board = figure_board.generate()


def main():
    with open('ClientSettings.txt') as f:
        data = ast.literal_eval(f.read())

    colors = data['Colors']

    figure_colors = [Color([color]) for color in colors['FigureColors']]
    background = Color([colors['FontColors'][0], colors['FontColors'][1]])
    border = Color([colors['BorderColors'][0], colors['BorderColors'][1]])

    cell_size = 43

    x, y = data['Resolution']
    left, top = 10, 10

    size = 2 * left + x * (cell_size + 1) + 1, 2 * top + y * (cell_size + 1) + 1

    figure_x, figure_y = 4, 4
    figure_left, figure_top = size[0], top

    size = size[0] + left + figure_x * (cell_size + 1) + 1, size[1]

    buttons_x, buttons_y = 4, 1
    buttons_left, buttons_top = figure_left, figure_top + top + figure_y * (cell_size + 1)

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('TETRIS')

    main_board = MainBoard(x, y, screen, left, top, cell_size, background, border)
    figure_board = FigureBoard(figure_x, figure_y, screen, figure_left, figure_top, cell_size,
                               background, border, figure_colors)
    buttons_board = ButtonsBoard(buttons_x, buttons_y, screen, buttons_left, buttons_top, cell_size, background, border)

    points_x, points_y = figure_x * (cell_size + 1) + 1, 55
    points_left, points_top = figure_left, figure_top + top + figure_y * (cell_size + 1) + top + buttons_y * (
                cell_size + 1)

    timer_x, timer_y = points_x, 55
    timer_left, timer_top = figure_left, figure_top + top + figure_y * (cell_size + 1) + top + buttons_y * (
            cell_size + 1) + points_y + top

    status_x, status_y = points_x, 55
    status_left, status_top = figure_left, figure_top + top + figure_y * (cell_size + 1) + top + buttons_y * (
            cell_size + 1) + points_y + top + timer_y + top

    points_info = InfoWindow(points_x, points_y, screen, points_left, points_top, border, border, border, 'points:')
    timer = InfoWindow(timer_x, timer_y, screen, timer_left, timer_top, border, border, border, 'timer:')
    status_bar = InfoWindow(status_x, status_y, screen, status_left, status_top, border, border, border, 'status:')

    running = True
    buttons_board.game_running = False

    clock = pygame.time.Clock()
    delta_t = 0
    lock = data['Speed']
    timer_t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = buttons_board.get_cell(event.pos)
                if cell is None:
                    pass
                else:
                    cell = cell[0]
                    if cell == 0:
                        if not buttons_board.game_running:
                            buttons_board.game_running = True
                        restart(main_board, figure_board)
                        timer_t = 0
                    elif cell == 1:
                        if buttons_board.game_running:
                            buttons_board.game_running = False
                    elif cell == 2:
                        ex = SettingsWindow()
                        ex.show()
                    elif cell == 3:
                        background.switch_color()
                        border.switch_color()
            if event.type == pygame.KEYDOWN and main_board.figure and buttons_board.game_running:
                if event.key == pygame.K_LEFT and main_board.can_move(x=-1):
                    main_board.x -= 1
                if event.key == pygame.K_RIGHT and main_board.can_move(x=1):
                    main_board.x += 1
                if event.key == pygame.K_UP:
                    figure = transpose(main_board.figure)
                    if main_board.can_move(figure=figure):
                        main_board.figure = figure
                if event.key == pygame.K_DOWN:
                    if main_board.can_move(y=1):
                        main_board.y += 1
                main_board.update()

        t = clock.tick()
        if buttons_board.game_running:
            delta_t += t
            timer_t += t
            if delta_t > lock:
                delta_t = 0
                if main_board.figure and main_board.can_move(y=1):
                    main_board.y += 1
                    main_board.update()
                else:
                    next_figure(main_board, figure_board)
                    if main_board.can_move():
                        main_board.update()
                    else:
                        buttons_board.game_running = False

        screen.fill(background.color)
        main_board.render()
        figure_board.render()
        buttons_board.render()

        points_info.draw(str(main_board.points))
        timer.draw(str(timer_t // 1000))
        status_bar.draw({True: 'on', False: 'off'}[buttons_board.game_running])
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
