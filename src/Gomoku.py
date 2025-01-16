import pygame


# цвета
Black = (0, 0, 0)
White = (245, 245, 245)
Red = (242, 20, 20)
Blue = (83, 243, 238)
Green = (50, 205, 50)

# размерность в пикселях
width = 50
wide = 2
step = 50
board = (width + wide) * 14 + wide
gameWidth = board + step * 2
gameHight = gameWidth + 100
PLAYER = False

class Gomoku:
    def __init__(self): # инициализационный блок
        self.grid = [[0 for x in range(15)] for y in range(15)]
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode((gameWidth, gameHight), pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption('Гомоку')
        pygame.display.set_icon(pygame.image.load('images/avatar.png'))

        self._running = True
        self._playing = False
        self._win = False
        self._draw = False

    def on_event(self, event): # события
        if event.type == pygame.QUIT: # выход из игры
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP: # нажатие мыши
            pos = pygame.mouse.get_pos()
            global PLAYER
            if self.mouse_in_botton(pos):
                if not self._playing:
                    self.start()
                    if PLAYER:
                        PLAYER = not PLAYER
                else:
                    if self.on_draw(): # ничья
                        self._draw=True
                    self.surrender()
                    PLAYER = not PLAYER

            elif self._playing: # процесс игры
                r = (pos[0] - step + width // 2) // (width + wide)
                c = (pos[1] - step + width // 2) // (width + wide)
                if 0 <= r < 15 and 0 <= c < 15:
                    if self.grid[r][c] == 0:
                        self.grid[r][c] = 1 if PLAYER else 2

                        # победа
                        if self.check_win([r,c],PLAYER):
                            self._win = True
                            self._playing = False
                        else:
                            PLAYER = not PLAYER



    def on_render(self): # обработка переменных
        self.render_gomoku_piece()
        self.render_game_info()
        self.render_button()
        pygame.display.update()


    def on_cleanup(self): # выход
        pygame.quit()


    def on_draw(self): # ничья
        for i in range(15):
            for g in range(15):
                if self.grid[i][g] == 0:
                    return False
        return True

    def on_execute(self): # основной бесконечный цикл
        while( self._running ):
            self.gomoku_board_init()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        self.on_cleanup()


    def start(self): # начать
        self._playing = True
        self.grid = [[0 for x in range(15)] for y in range(15)]
        self._win = False
        self._draw = False


    def surrender(self): # реванш
        self._playing = False
        self._win = True


    def gomoku_board_init(self):
        # задний фон
        background = pygame.image.load('images/background.jpg')
        self._display_surf.blit(background, (0, 0))

        # прорисовка игровой сетки
        pygame.draw.rect(self._display_surf, Black, [step, step, board, board])
        for row in range(14):
            for column in range(14):
                pygame.draw.rect(self._display_surf, White, [(wide + width) * column + wide + step,
                                  (wide + width) * row + wide + step, width, width])

    def mouse_in_botton(self,pos): # нажатие на кнопку начать/реванш
        if gameWidth // 2 - 50 <= pos[0] <= gameWidth // 2 + 50 and gameHight - 50 <= pos[1] <= gameHight - 20:
           return True
        return False


    def render_button(self): # обновление кнопки начать/реванш
        color = Green if not self._playing else Red
        info = "Начать!" if not self._playing else "Реванш"
        pygame.draw.rect(self._display_surf, color, (gameWidth // 2 - 50, gameHight - 50, 100, 30))
        info_font = pygame.font.SysFont('Colibri', 22)
        text = info_font.render(info, True, White)
        textRect = text.get_rect()
        textRect.centerx = gameWidth // 2
        textRect.centery = gameHight - 35
        self._display_surf.blit(text, textRect)


    def render_game_info(self):
        # индикатор цвета ходящего игрока
        color = Black if not PLAYER else Blue
        center = (gameWidth // 2 - 60, board + 100)
        radius = 12
        pygame.draw.circle(self._display_surf, color, center, radius, 0)

        # иноформирующая надпись
        if self._draw:
            info = "Ничья"
        elif self._win:
            info = "Победа!"
        else:
            info = "Ходят сейчас"
        info_font = pygame.font.SysFont('Colibri', 24)
        text = info_font.render(info, True, Black)
        textRect = text.get_rect()
        textRect.centerx = self._display_surf.get_rect().centerx + 20
        textRect.centery = center[1]
        self._display_surf.blit(text, textRect)


    def render_gomoku_piece(self): # прорисовка камней на поле
        for r in range(15):
            for c in range(15):
                center = ((wide + width) * r + wide + step, (wide + width) * c + wide + step)
                if self.grid[r][c] > 0:
                    color = Black if self.grid[r][c] == 2 else Blue
                    pygame.draw.circle(self._display_surf, color, center, width // 2 - wide, 0)



    def check_win(self,position,player): # проверка на победу
        target = 1 if player else 2
        if self.grid[position[0]][position[1]] != target:
            return False
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            continue_chess = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < 15 and 0 <= p[1] < 15:
                    if self.grid[p[0]][p[1]] == target:
                        continue_chess += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if continue_chess >= 6:
                return True
        return False


if __name__ == "__main__" :
    gomoku = Gomoku()
    gomoku.on_execute()
