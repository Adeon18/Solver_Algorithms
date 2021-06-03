'''
module containing crossword solving algorithm using backtracking
'''
import pygame
import random
DIRECTIONS = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

class Crossword:
    '''
    class representing crossword
    has methods to read it from file and solve it
    '''
    def __init__(self, file_path, vizual=None):
        '''
        initialise crossword with its field and target words
        '''
        self.field, self.target_words = self.read_from_file(file_path)
        self.boocked_positions = []
        self.completed_words = []
        self.temp_pos = []
        self.vizual = vizual

    def read_from_file(self, file_path):
        '''
        read crossword from file
        first block of file is its field with words
        separated by empty line goes target words, each in new line
        '''

        # read the game field
        field = []
        file = open(file_path, 'r')
        while True:
            line = file.readline().split()
            field.append(line)
            if not line:
                break

        # read targt words
        target_words = []
        line = file.readline().split()
        while True:
            line = file.readline().strip()
            target_words.append(line)
            if not line:
                break

        file.close()
        return (field, target_words)

    def solve(self):
        '''
        solve the crossword
        '''
        def recurse(dirr, letter, pos, word):
            new_pos = [pos[0] + dirr[0], pos[1] + dirr[1]]
            
            try:
                # if letter on field by its direction equals requiered letter
                if self.field[new_pos[0]][new_pos[1]].lower() == word[letter]:
                    # make this letter upper, to show that it's in
                    self.field[new_pos[0]][new_pos[1]] = self.field[new_pos[0]][new_pos[1]].upper()
                    if recurse(dirr, letter + 1, new_pos, word):
                        # if we've got the whole word, start adding useful information
                        self.boocked_positions.append(new_pos)
                        self.temp_pos.append(new_pos)
                        # For visual repesentation
                        if self.vizual:
                            self.vizual.draw(self.vizual.LIGHTRED)
                            self.vizual.events()
                            pygame.time.wait(self.vizual.TIMESTEP)
                        return True
                    else:
                        if new_pos not in self.boocked_positions:
                            # if this word wasn't found on the needed position
                            # backtrack and lower all the letters
                            # if this leter is a part of other word, do not erase it
                            self.field[new_pos[0]][new_pos[1]] = self.field[new_pos[0]][new_pos[1]].lower()
                            # For visual repesentation
                            if self.vizual:
                                self.vizual.draw()
                                self.vizual.events()
                                pygame.time.wait(self.vizual.TIMESTEP)
                        return False
            except IndexError:
                if letter == len(word):
                    return True
            return False

        i = 0
        j = 0
        for row in self.field:
            for letter in row:
                for word in self.target_words:
                    if word and word[0] == letter:
                        # if the first letter of word is our current letter on field
                        # make it upper and go recurse through all directions to find the word
                        # For visual repesentation
                        if self.vizual:
                            self.vizual.draw()
                            self.vizual.events()
                            pygame.time.wait(self.vizual.TIMESTEP)

                        for dirr in DIRECTIONS:
                            self.field[i][j] = self.field[i][j].upper()
                            if recurse(dirr, 1, [i, j], word):

                                self.boocked_positions.append([i, j])
                                self.temp_pos.append([i, j])
                                self.completed_words.append(self.temp_pos)
                                self.temp_pos = []
                            else:
                                if [i, j] not in self.boocked_positions:
                                    self.field[i][j] = self.field[i][j].lower()

                j += 1
            i += 1
            j = 0

        # double check if all found words are ok
        for pos in self.boocked_positions:
            self.field[pos[0]][pos[1]] = self.field[pos[0]][pos[1]].upper()
            # For visual repesentation
            if self.vizual:
                self.vizual.draw(self.vizual.LIGHTRED)
                self.vizual.events()
                pygame.time.wait(self.vizual.TIMESTEP)

    def __str__(self):
        res = ""
        for line in self.field:
            for item in line:
                res += str(item) + " "
            res += "\n"
        res += "\n"
        for word in self.target_words:
            res += str(word) + "\n"
        return res

if __name__ == "__main__":
    crossword = Crossword("test_1.txt")
    crossword.solve()
    print(crossword)