import random
import re 
from tabulate import tabulate

class NumberGame:

    def __init__(self, seed=None):
        nums = list(range(1, 10))
        random.shuffle(nums)
        self.seed = seed
        self.generated_number = nums[:4]
        self.guesses = []

    def __str__(self):
        return str(self.generated_number)

    def __repr__(self):
        return f'{self.generated_number}'

    def get_guesses(self):
        return self.guesses

    def guess(self, guess:str):
        flag, mess = self.is_valid(guess)
        if flag:
            num, pos = self.parse_guess(guess)
            self.guesses.append([guess, num, pos])
            if num == 4 and pos == 4:
                return 1, None
            elif len(self.guesses) == 8:
                return -1, None
            else:
                return 0, None
        else:
            return 0, mess

    def parse_guess(self, guess:str):
        num = 0 
        pos = 0
        for i, n in enumerate(self.generated_number):
            if n == int(guess[i]):
                pos += 1
            if str(n) in guess:
                num += 1
        
        return num, pos

    def is_valid(self, guess:str):
        try:
            x = int(guess)
            if len(guess) != 4:
                return False, 'Guess must be 4 digits'
            elif len(set(guess)) != 4:
                return False, 'Guess digits must be unique'
            elif '0' in guess:
                return False, 'Guess must not contain 0'
            else:
                return True, None
        except:
            return False, 'Input must be a number, please try again'
    
    def get_generated_number(self):
        return "".join(map(str, self.generated_number))
    
    def get_guesses(self):
        return self.guesses

    def get_formatted_guesses(self):
        msg = ["Guess", "Num", "Correct"]
        guesses = []
        for j in self.get_guesses():
            guesses.append(list(map(str, j)))

        return tabulate(guesses, headers=msg, tablefmt="fancy_grid")



class XOGame:

    def __init__(self, level=0) -> None:
        self.board = [["_" for i in range(3)] for j in range(3)]
        self.level = level

    def __str__(self):
        return "\n".join(map(lambda x:" ".join(x), self.board))

    def next_move(self, move:str):
        try:
            move = int(move)
            if move < 0 or move > 8:
                return -1, "Input must be for 0 to 8"
            else:
                i, j = divmod(move, 3)
                if self.board[i][j] == "_":
                    self.add_move(i, j)
                    if self.is_done():
                        return 1, "you won!"
                    elif self.no_spot():
                        return 1, "Tie!"
                    self.play()
                    if self.is_done():
                        return 1, "You lose!"
                    elif self.no_spot():
                        return 1, "Tie!"
                    else:
                        return 0, None
                else:
                    return -1, "Spot is already occupied"
        except:
            return -1, "Input must be an integer"
    
    def add_move(self, i, j, char="X"):
        self.board[i][j] = char   
    
    def is_done(self):
        diag1 = ""
        diag2 = ""
        for n in range(3):
            diag1 += self.board[n][n]
            diag2 += self.board[n][2-n]
        for row in self.board+[diag1, diag2]:
            if len(set(row))==1 and row[0]!="_":
                return True 
        for col in zip(*map(list, self.board)):
            if len(set(col))==1 and col[0]!="_":
                return True 
        
        return False
    
    def no_spot(self):
        return "_" not in str(self)
    
    def play(self):
        i, j = None, None
        if self.level == 0:
            pos_spots = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "_":
                        pos_spots.append((i, j))
            i, j = random.choice(pos_spots)
        self.add_move(i, j, "O")

    def get_formatted_board(self):
        board = []
        for i in self.board:
            board.append(map(lambda x:[x, ""][x=="_"], i))
        return tabulate(board, tablefmt="fancy_grid")

        