import pygame
import game_mechanics
import random

FRAMERATE = 30

ROWS = 13
COLUMNS = 6

BLACK = pygame.Color(0, 0, 0) # background color
WHITE = pygame.Color(255, 255, 255) # grid color

RED = pygame.Color(255, 0, 0) # block color
ORANGE = pygame.Color(255, 131, 0) # block color
YELLOW = pygame.Color(250, 255, 0) # block color
BLUE = pygame.Color(0, 0, 255) # block color
PURPLE = pygame.Color(174, 0, 255) # block color
PINK = pygame.Color(255, 163, 241) # block color
GRAY = pygame.Color(158, 170, 175) # block color

GREEN = pygame.Color(0, 255, 0) # matching color
TEAL = pygame.Color(66, 244, 223) # landing color

class ColumnsGame:
    def __init__(self):
        self._running = True

    def _redraw(self, board:list) -> None:
        '''This function takes in a board and makes the window with the particular color'''
        self.surface = pygame.display.get_surface()

        self.surface.fill(BLACK) # background color

        self._grid() # grid

        self._change_board(board)

    def _starting_info(self, random_column:int, list_of_three_random_colors:list) -> list:
        '''This function takes in a random column and a list of three random colors and then creates a list that is in the form of ['', column_number, color1, color2, color3]'''
        info = []
        info.append('')
        info.append(random_column)
        info.append(list_of_three_random_colors[0])
        info.append(list_of_three_random_colors[1])
        info.append(list_of_three_random_colors[2])

        return info

    def _three_random_colors_finder(self) -> list:
        '''This function randomly gets three colors and places it in the list and then returns it in the list'''
        full_list_of_colors = [RED, ORANGE, YELLOW, BLUE, PURPLE, PINK, GRAY]
        random_list_of_three_colors = []

        random_list_of_three_colors.append(random.choice(full_list_of_colors))
        random_list_of_three_colors.append(random.choice(full_list_of_colors))
        random_list_of_three_colors.append(random.choice(full_list_of_colors))

        return random_list_of_three_colors

    def _random_column_finder(self) -> int:
        '''This function randomly gets a number from 1 to the number of columns and returns it'''
        column = random.randint(1, COLUMNS)
        return column

    def _grid(self) -> None:
        '''This function adds grids in the window'''
        height, width, self.block_size, space = ROWS, COLUMNS, 40, 3
        self.coords = dict()
        for x in range(width):
            for y in range(2):
                self.coords[(x, y)] = (-999, -999)
        for y in range(height):
            for x in range(width):
                color = WHITE
                drawX, drawY = x*(self.block_size+space) + (self.sizeX - (self.block_size+space)*width)/2, y*(self.block_size+space) + (self.sizeY - (self.block_size+space)*height)/2
                self.coords[(x, y + 2)] = (drawX, drawY)
                rect = pygame.Rect(drawX, drawY, self.block_size, self.block_size) # top, left, width, height
                pygame.draw.rect(self.surface, color, rect)

    def _color_block(self, x:int, y:int, color:pygame.Color) -> None:
        '''This function add a color into jewel'''
        pygame.draw.rect(self.surface, color, pygame.Rect(self.coords[(x, y)][0], self.coords[(x, y)][1], self.block_size, self.block_size))

    def _resize_surface(self, size: (int, int)) -> pygame.Surface:
        '''This function sizes the window'''
        return pygame.display.set_mode(size, pygame.RESIZABLE)

    def _change_board(self, board:list) -> None:
        '''This function adds colors to all of the jewels and places a small green box on the matching jewels in the window'''
        for row in range(ROWS + 2):
            if row >= 2:
                for column in range(COLUMNS):
                    if board[column][row] == None:
                        pass
                    elif type(board[column][row].get_color()) == pygame.Color:
                        if board[column][row].get_state() == 'Falling':
                            self._color_block(column, row, board[column][row].get_color())
                        elif board[column][row].get_state() == 'Landed':
                            pygame.draw.rect(self.surface, TEAL, pygame.Rect(self.coords[(column, row)][0], self.coords[(column, row)][1], self.block_size/2, self.block_size/2)) # recently added
                        elif board[column][row].get_state() == 'Frozen':
                            self._color_block(column, row, board[column][row].get_color())
                        elif board[column][row].get_state() == 'Match':
                            self._color_block(column, row, board[column][row].get_color())


    def run(self) -> None:
        '''This function runs all the necessary functions in order to make the Columns Game run with the graphics'''
        pygame.init()

        self.sizeX, self.sizeY = 650, 700
        self.surface = self._resize_surface((self.sizeX, self.sizeY)) # creates a window

        clock = pygame.time.Clock() # contructs a clock

        new_fall = False

        board = game_mechanics.make_board(COLUMNS, ROWS)
        FRAME = 0
        while self._running:
            clock.tick(FRAMERATE)

            self._redraw(board)
            FRAME += 1
            if not new_fall:
                info = self._starting_info(self._random_column_finder(), self._three_random_colors_finder())
                gs = game_mechanics.GameState(board, info)
                gs.new_faller() # inputs 3 jewels into the board
                if FRAME % FRAMERATE == 0:
                    gs.jewels_move_down_one()
                new_fall = True
            if not gs.jewels_have_landed():
                if FRAME % FRAMERATE == 0:
                    gs.jewels_move_down_one()
            else:
                gs.change_all_three_jewels_to_landed()
                self._change_board(board)
                gs.change_all_three_jewels_to_frozen()
                matched = gs.jewels_match()
                if matched:
                    self.match(gs, ROWS + 2, COLUMNS, board)
                if gs.game_over_checker() == True:
                    exit()
                new_fall = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    pygame.quit()
                    return

                if gs.jewels_have_landed() == False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            gs.move_faller_right()
                            self._change_board(board)
                        elif event.key == pygame.K_LEFT:
                            gs.move_faller_left()
                            self._change_board(board)
                        elif event.key == pygame.K_DOWN:
                            gs.jewels_move_down_one()
                            self._change_board(board)
                        elif event.key == pygame.K_SPACE:
                            gs.rotate_faller()
                            self._change_board(board)
                else:
                    update(gs, ROWS + 2, COLUMNS, board)
                    if gs.game_over_checker() == True:
                        exit()

                    matched = gs.jewels_match()
                    if matched:
                        self.match(gs, ROWS + 2, COLUMNS, board)
                self._redraw(board)

            pygame.display.flip()

    def match(self, gs:game_mechanics.GameState, rows:int, columns:int, board:list) -> None:
        '''This function runs all the match functions from game_mechanics and places a small green box on the matching jewels in the window'''
        matched = gs.jewels_match()
        if matched:
            for column in range(gs.columns):
                for row in range(gs.rows):
                    if gs.board[column][row] != None and type(gs.board[column][row]) == game_mechanics.Jewel:
                        if gs.board[column][row].get_state() == 'Match':
                            pygame.draw.rect(self.surface, GREEN, pygame.Rect(self.coords[(column, row)][0], self.coords[(column, row)][1], self.block_size/2, self.block_size/2))
            gs.remove_matching()
            matched = gs.jewels_match()
            self.match(gs, rows, columns, board)

def update(gs:game_mechanics.GameState, rows:int, columns:int, board:list) -> None:
    '''This function takes in a game_mechanics.GameState, rows, columns, and board in which it then puts the jewels in landed state and then frozen state'''
    gs.change_all_three_jewels_to_landed()
    gs.change_all_three_jewels_to_frozen()
    matched = gs.jewels_match()

if __name__ == '__main__':
    ColumnsGame().run()
