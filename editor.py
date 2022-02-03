import pygame

FIG_SIZE_X = 60
FIG_SIZE_Y = 20

GAME_N_ROWS = 20
GAME_N_COLS = 13

WIN_SIZE_X = FIG_SIZE_X * GAME_N_COLS
WIN_SIZE_Y = 600
WIN_SIZE = (WIN_SIZE_X, WIN_SIZE_Y)

DIR_UP = 2
DIR_LEFT = - 1
DIR_RIGHT = + 1
DIR_DOWN = 0

# Все цвета в игре
COLOR_SCREEN = (0, 0, 0)
COLOR_BORDER = (117, 117, 117)
COLOR_CURSOR = (52, 255, 33)
COLOR_YELLOW = (251, 255, 0)
COLOR_BLUE = (0, 255, 208)
COLOR_RED = (255, 0, 0)
COLOR_PURPULE = (171, 0, 173)

COLOR_MAP = {'X': COLOR_SCREEN,
             '1': COLOR_YELLOW,
             '2': COLOR_CURSOR,
             '3': COLOR_BLUE,
             '4': COLOR_RED,
             '5': COLOR_PURPULE,
             }

# Все классы в игре


class Figure:
    def __init__(self, ftype):
        self.color = COLOR_MAP[ftype]
        self.ftype = ftype

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, self.color, (x, y, FIG_SIZE_X, FIG_SIZE_Y))


class GameField:
    def __init__(self, screen):
        self.pos_i = 0
        self.pos_j = 0
        self.w = FIG_SIZE_X * GAME_N_COLS
        self.h = FIG_SIZE_Y * GAME_N_ROWS
        x_mid = WIN_SIZE_X / 2
        self.xl = x_mid - self.w / 2
        self.xr = x_mid + self.w / 2
        self.yu = 0
        self.yb = self.h
        self.screen = screen
        self.game_field = list()
        self.clear_game_field()

    def save_level(self):
        print("Enter file name:")
        f_name = input()
        f = open(f_name + ".dat", "w")
        for i in range(GAME_N_ROWS):
            for j in range(GAME_N_COLS):
                fig = self.game_field[i][j]
                if fig is None:
                    f.write('X')
                else:
                    f.write(fig.ftype)

    def draw(self):
        y = self.yu
        for i in range(GAME_N_ROWS):
            x = self.xl
            for j in range(GAME_N_COLS):
                f = self.game_field[i][j]
                if f is not None:
                    f.draw(self.screen, x, y)
                if i == self.pos_i and j == self.pos_j:
                    pygame.draw.rect(self.screen, COLOR_CURSOR, (x, y, FIG_SIZE_X, FIG_SIZE_Y), 1)
                else:
                    pygame.draw.rect(self.screen, COLOR_BORDER, (x, y, FIG_SIZE_X, FIG_SIZE_Y), 1)
                x += FIG_SIZE_X
            y += FIG_SIZE_Y

    def new_figure(self, ftype):
        f = Figure(ftype)
        self.game_field[self.pos_i][self.pos_j] = f

    def can_move(self, direction):
        pos_i = self.pos_i
        pos_j = self.pos_j
        can = True
        if direction == DIR_LEFT:
            pos_j -= 1
            if pos_j < 0:
                can = False
        elif direction == DIR_RIGHT:
            pos_j += 1
            if pos_j >= GAME_N_COLS:
                can = False
        elif direction == DIR_DOWN:
            pos_i += 1
            if pos_i >= GAME_N_ROWS:
                can = False
        elif direction == DIR_UP:
            pos_i -= 1
            if pos_i < 0:
                can = False

        return can

    def clear_game_field(self):
        self.pos_i = 0
        self.pos_j = 0
        for i in range(GAME_N_ROWS):
            row = list()
            for j in range(GAME_N_COLS):
                row.append(None)
            self.game_field.append(row)

    def move(self, direction):
        can_move = self.can_move(direction)
        if direction == DIR_LEFT:
            if can_move:
                self.pos_j -= 1
        elif direction == DIR_RIGHT:
            if can_move:
                self.pos_j += 1
        elif direction == DIR_DOWN:
            if can_move:
                self.pos_i += 1
        elif direction == DIR_UP:
            if can_move:
                self.pos_i -= 1

        return can_move


def main():
    # Программа должна начинаться с инициализации pygame

    pygame.init()

    screen = pygame.display.set_mode(WIN_SIZE)

    pygame.display.set_caption("ARCANOID EDITOR")

    clock = pygame.time.Clock()

    # Другие инициализации, специфичные для игры

    do_pygame = True

    game_field = GameField(screen)

    # Главный цикл программы. Каждую итерацию опрашиваются и обрабатываются события,

    # изменяются объекты и перерисовываются на экране

    while do_pygame:

        # оброботка событей

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                do_pygame = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game_field.move(DIR_UP)
                if event.key == pygame.K_s:
                    game_field.move(DIR_DOWN)
                if event.key == pygame.K_a:
                    game_field.move(DIR_LEFT)
                if event.key == pygame.K_d:
                    game_field.move(DIR_RIGHT)
                if event.key == pygame.K_x:
                    game_field.new_figure('X')
                if event.key == pygame.K_1:
                    game_field.new_figure('1')
                if event.key == pygame.K_2:
                    game_field.new_figure('2')
                if event.key == pygame.K_3:
                    game_field.new_figure('3')
                if event.key == pygame.K_4:
                    game_field.new_figure('4')
                if event.key == pygame.K_5:
                    game_field.new_figure('5')
                if event.key == pygame.K_c:
                    game_field.save_level()

        # Здесь перерисовываются все обекты

        screen.fill(COLOR_SCREEN)

        game_field.draw()

        # Каждая итерация заканчивается этими двумя командами

        pygame.display.flip()  # Отображаем перерисованное на экране

        clock.tick(60)  # Каждая итерация занимает 60 миллисекунд

        # Освобождаем память по окончании игры

    pygame.quit()


if __name__ == "__main__":
    main()
