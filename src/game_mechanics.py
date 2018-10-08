# Anmol Singh 95173029 ICS 32 Lab sec 6 Project 5

class GameState:
    def __init__(self, board:list, user_response = None):
        '''Initalizes the class'''
        self.board = board

        self.columns = self.num_of_cols_finder()
        self.rows = self.num_of_rows_finder()

        self.fall_action = user_response

        self.count = 1

        self.current_falling_column = None

        self.direction = None

        self.current_top_row_num = None
        self.current_middle_row_num = None
        self.current_bottom_row_num = None

    def num_of_rows_finder(self) -> int:
        '''Finds the number of rows a single column has from the board'''
        rows = len(self.board[0])
        return rows

    def num_of_cols_finder(self) -> int:
        '''Finds the number of columns a board has'''
        columns = len(self.board)
        return columns

    def game_over_checker(self) -> bool:
        '''This function returns True or False based on whether the game is over.'''
        return all(type(self.board[int(self.current_falling_column) - 1][int(row)]) == Jewel for row in range(1, self.rows))

    def jewels_have_landed(self) -> bool:
        '''This function returns True or False based on whether the jewels have landed/frozen.'''
        try:
            if type(self.board[int(self.current_falling_column) - 1][(self.count + 1) + 1]) != Jewel:
                return False
            else:
                self.top_jewel_icon.change_state_to_landed()
                self.middle_jewel_icon.change_state_to_landed()
                self.bottom_jewel_icon.change_state_to_landed()
                return True
                self.count = 1
        except IndexError:
            self.top_jewel_icon.change_state_to_landed()
            self.middle_jewel_icon.change_state_to_landed()
            self.bottom_jewel_icon.change_state_to_landed()
            return True
            self.count = 1

    def new_faller(self) -> None:
        '''This function creates a new set of jewels'''
        self.current_falling_column = int(self.fall_action[1])

        self.top_jewel_icon = Jewel(self.fall_action[2], 'Falling') # top jewel color/letter
        self.middle_jewel_icon = Jewel(self.fall_action[3], 'Falling') # middle jewel color/letter
        self.bottom_jewel_icon = Jewel(self.fall_action[4], 'Falling') # bottom jewel color/letter

        self.board[int(self.current_falling_column) - 1][0] = self.top_jewel_icon
        self.board[int(self.current_falling_column) - 1][1] = self.middle_jewel_icon
        self.board[int(self.current_falling_column) - 1][2] = self.bottom_jewel_icon

        self.current_top_row_num = 0
        self.current_middle_row_num = 1
        self.current_bottom_row_num = 2

    def jewels_move_down_one(self) -> None:
        '''This function moves all jewels down one space'''

        self.board[int(self.current_falling_column) - 1][(self.count - 1)] = None # somehow removes all previous jewels from the previous column

        self.board[int(self.current_falling_column) - 1][self.count] = self.top_jewel_icon
        self.board[int(self.current_falling_column) - 1][(self.count) + 1] = self.middle_jewel_icon
        self.board[int(self.current_falling_column) - 1][(self.count + 1) + 1] = self.bottom_jewel_icon

        self.current_top_row_num = self.count
        self.current_middle_row_num = (self.count) + 1
        self.current_bottom_row_num = (self.count + 1) + 1

        self.count += 1

    def rotate_faller(self) -> None:
        '''This function rotates the jewel icons bottom to top'''
        three_piece = []
        three_piece.append(self.top_jewel_icon.get_color()) # X
        three_piece.append(self.middle_jewel_icon.get_color()) # Y
        three_piece.append(self.bottom_jewel_icon.get_color()) # Z
        three_piece = rotate_jewels(three_piece, -1) # [X, Y, Z] becomes [Z, X, Y]

        self.top_jewel_icon = Jewel(three_piece[0], 'Falling')
        self.middle_jewel_icon = Jewel(three_piece[1], 'Falling')
        self.bottom_jewel_icon = Jewel(three_piece[2], 'Falling')

        for num in range(3):
            self.board[int(self.current_falling_column) - 1][self.current_top_row_num] = self.top_jewel_icon # Z
            self.board[int(self.current_falling_column) - 1][self.current_middle_row_num] = self.middle_jewel_icon # X
            self.board[int(self.current_falling_column) - 1][self.current_bottom_row_num] = self.bottom_jewel_icon # Y

    def check_if_blocked(self) -> bool:
        '''This function returns True or False by checking whether moving the set of jewels to the left or right is possible'''
        if self.direction == 'left':
            temp_left_current_falling_column = self.current_falling_column - 1
            if (temp_left_current_falling_column - 1) < 0: # this if statement blocks the jewels from teleporting to the otherside
                return True
            elif ((self.board[int(temp_left_current_falling_column) - 1][self.count - 1] == None) and # this if statement blocks the jewels from moving to the left if there are jewels in the way
                (self.board[int(temp_left_current_falling_column) - 1][(self.count)] == None) and
                (self.board[int(temp_left_current_falling_column) - 1][(self.count + 1)] == None)):
                return False
            else:
                return True
        elif self.direction == 'right':
            temp_right_current_falling_column = self.current_falling_column + 1
            if (temp_right_current_falling_column) > self.columns: # this if statement blocks the jewels from teleporting to the otherside
                return True
            elif ((self.board[int(temp_right_current_falling_column) - 1][self.count - 1] == None) and # this if statement blocks the jewels from moving to the right if there are jewels in the way
                (self.board[int(temp_right_current_falling_column) - 1][(self.count)] == None) and
                (self.board[int(temp_right_current_falling_column) - 1][(self.count + 1)] == None)):
                return False
            else:
                return True

    def move_faller_left(self) -> None:
        '''This function moves the set of jewels to the left'''
        self.direction = 'left'

        if self.check_if_blocked() == False:
            self.current_falling_column -= 1 # keeps a global track of the current falling set of jewels

            self.board[int(self.current_falling_column)][self.count] = None # gets rid of bottom
            self.board[int(self.current_falling_column)][(self.count + 1)] = None # gets rid of middle
            self.board[int(self.current_falling_column)][(self.count - 1)] = None # gets rid of top

            self.board[int(self.current_falling_column) - 1][self.count - 1] = self.top_jewel_icon # moves the top jewel to the left
            self.board[int(self.current_falling_column) - 1][(self.count)] = self.middle_jewel_icon # moves the middle jewel to the left
            self.board[int(self.current_falling_column) - 1][(self.count + 1)] = self.bottom_jewel_icon # moves the bottom jewel to the left

            self.current_top_row_num = self.count - 1 # needed to rotate the faller
            self.current_middle_row_num = (self.count) # needed to rotate the faller
            self.current_bottom_row_num = (self.count + 1) # needed to rotate the faller

    def move_faller_right(self) -> None:
        '''This function moves the set of jewels to the right'''
        self.direction = 'right'

        if self.check_if_blocked() == False:
            self.current_falling_column += 1 # keeps a global track of the current falling set of jewels

            self.board[int(self.current_falling_column) - 2][self.count] = None # gets rid of bottom
            self.board[int(self.current_falling_column) - 2][(self.count + 1)] = None # gets rid of middle
            self.board[int(self.current_falling_column) - 2][(self.count - 1)] = None # gets rid of top

            self.board[int(self.current_falling_column) - 1][self.count - 1] = self.top_jewel_icon # moves the top jewel to the right
            self.board[int(self.current_falling_column) - 1][(self.count)] = self.middle_jewel_icon # moves the middle jewel to the right
            self.board[int(self.current_falling_column) - 1][(self.count + 1)] = self.bottom_jewel_icon # moves the bottom jewel to the right

            self.current_top_row_num = self.count - 1 # needed to rotate the faller
            self.current_middle_row_num = (self.count) # needed to rotate the faller
            self.current_bottom_row_num = (self.count + 1) # needed to rotate the faller

    def check_validity_column_number(self) -> bool:
        '''This function returns True or False based on whether the desired column exists'''
        return (1 <= int(self.fall_action[1]) <= int(self.columns))

    def jewels_match(self) -> bool:
        '''This function runs all four matching functions and returns a boolean on whether the functions found a match or not'''
        vert = self.vertical_match()
        hori = self.horizontal_match()
        backdiag = self.backdiag_match()
        forwdiag = self.forwdiag_match()
        return vert or hori or backdiag or forwdiag

    def backdiag_match(self) -> bool:
        '''This function changes all the jewels that have a backward diagonal match into 'Match' state and returns a boolean on whether it found a match or not'''
        return self.match_by_direction('BACKDIAG')

    def forwdiag_match(self) -> bool:
        '''This function changes all the jewels that have a forward diagonal match into 'Match' state and returns a boolean on whether it found a match or not'''
        return self.match_by_direction('FORWDIAG')

    def horizontal_match(self) -> bool:
        '''This function changes all the jewels that have a horizontal match into 'Match' state and returns a boolean on whether it found a match or not'''
        return self.match_by_direction('HORIZONTAL')

    def vertical_match(self) -> bool:
        '''This function changes all the jewels that have a vertical match into 'Match' state and returns a boolean on whether it found a match or not'''
        return self.match_by_direction('VERTICAL')

    def match_by_direction(self, direction) -> bool:
        '''This function checks whether there is a match based on the direction'''
        board = self.board
        if direction == 'VERTICAL':
            board = board
        elif direction == 'HORIZONTAL':
            board = [*zip(*board)]
        elif direction == 'BACKDIAG':
            def get_diag(board:list) -> list:
                '''This function takes in a board and finds all the backward diagonal Jewels in a separate lists and returns that list'''
                b = [None] * (len(board) - 1)
                board = [b[i:] + r + b[:i] for i, r in enumerate(board)]
                return [[c for c in r] for r in zip(*board)]
            board = get_diag(board)
        else:
            def get_diag(board:list) -> list:
                '''This function takes in a board and finds all the forward diagonal Jewels in a separate lists and returns that list'''
                b = [None] * (len(board) - 1)
                board = [b[:i] + r + b[i:] for i, r in enumerate(board)]
                return [[c for c in r] for r in zip(*board)]
            board = get_diag(board)

        return self.check_match(board)

    def check_match(self, board:list) -> bool:
        '''This function checks whether is a match'''
        result = False
        for row in board:
            current_color = None
            for i in range(len(row)):
                count = 0
                flagged = []
                jewel = row[i]
                if jewel:
                    current_color = jewel.get_color()
                    rest = row[i:]
                    j = 1
                    while len(rest) != 0 and rest[0] and rest[0].get_color() == current_color:
                        flagged.append(rest[0])
                        count += 1
                        rest = row[i+j:]
                        j += 1
                    if count >= 3:
                        for jewel in flagged:
                            jewel.change_state_to_match()
                        result = True
        return result

    def remove_matching(self) -> None:
        ''' This function removes all Jewels from the board that have the state 'Match' and lands all floating Jewels if any.'''
        for column in range(self.columns):
            for row in range(self.rows):
                if self.board[column][row] != None and type(self.board[column][row]) == Jewel:
                    if self.board[column][row].get_state() == 'Match':
                        self.board[column][row] = None
                        for _ in range(self.rows):
                            self.jewels_that_have_not_landed()
                            self.force_land_jewels()

    def change_all_three_jewels_to_landed(self) -> None:
        '''This function changes three jewels into the landed state'''
        self.top_jewel_icon.change_state_to_landed()
        self.middle_jewel_icon.change_state_to_landed()
        self.bottom_jewel_icon.change_state_to_landed()

    def change_all_three_jewels_to_frozen(self) -> None:
        '''This function changes three jewels into the frozen state'''
        self.top_jewel_icon.change_state_to_frozen()
        self.middle_jewel_icon.change_state_to_frozen()
        self.bottom_jewel_icon.change_state_to_frozen()

    def jewels_that_have_not_landed(self) -> None:
        '''This function checks and stores jewels that have not landed within the board'''
        self.not_landed_jewels = []
        for column in range(self.columns):
            for row in range(self.rows-1):
                if type(self.board[column][row]) == Jewel and self.board[column][row + 1] == None:
                    self.not_landed_jewels.append([column, row])

    def force_land_jewels(self) -> None:
        '''This function lands all the jewels that are floating'''
        for num in range(len(self.not_landed_jewels)):
            column = self.not_landed_jewels[num][0]
            row = self.not_landed_jewels[num][1]
            orig = self.board[column][row]
            self.board[column][row+1] = self.board[column][row] # move down
            i = 1
            while row-i > 0:
                self.board[column][row] = self.board[column][row-i] # set old spot
                i += 1

class Jewel:
    def __init__(self, color, state):
        '''Initalizes the class'''
        self.color = color
        self.state = state
        self.flagged = False

    def get_color(self):
        '''This function returns the color of a jewel'''
        return self.color

    def get_state(self) -> str:
        '''This function returns the state of a jewel which can either be 'Falling', 'Landed', 'Match'.'''
        return self.state

    def change_state_to_landed(self):
        '''This function changes the state of a jewel to Landed'''
        self.state = 'Landed'

    def change_state_to_frozen(self):
        self.state = 'Frozen'

    def change_state_to_match(self):
        '''This function changes the state of a jewel to Match'''
        self.state = 'Match'

    def flag(self) -> None:
        '''This function flags the jewel'''
        self.flagged = True

    def unflag(self) -> None:
        '''This function unflags the jewel'''
        self.flagged = False

def rotate_jewels(jewels:list, number_of_rotations:int) -> list:
    '''This function takes in a list of jewel icons and an integer that determines the direction of the rotation which it then returns the rotated list'''
    return jewels[number_of_rotations:] + jewels[:number_of_rotations]

def make_board(columns:int, rows:int) -> list:
    '''This function takes in the number of columns and the number of rows and makes a list based on the provided numbers'''
    board = []
    rows = rows + 2
    for column in range(columns):
        board.append([])
        for row in range(rows):
            board[column].append(None)
    return board
