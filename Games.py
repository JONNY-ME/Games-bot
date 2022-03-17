import random 
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

