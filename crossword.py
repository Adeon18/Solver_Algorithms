'''
module containing crossword solving algorithm using backtracking
'''

DIRECTIONS = [[-1, 0], [-1, -1], [0, -1], [1, 0], [0, 1], [1, 1], [-1, 1], [1, -1]]

class Crossword:
    '''
    class representing crossword
    has methods to read it from file and solve it
    '''
    def __init__(self, file_path):
        '''
        initialise crossword with its field and target words
        '''
        self.field, self.target_words = self.read_from_file(file_path)
        self.boocked_positions = []

    def read_from_file(self, file_path):
        '''
        read crossword from file
        first block of file is its field with words
        separated by empty line goes target words, each in new line
        '''
        field = []
        file = open(file_path, 'r')
        while True:
            line = file.readline().split()
            field.append(line)
            if not line:
                break

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
                # print(new_pos, word, letter, self.field[new_pos[0]][new_pos[1]])
                if self.field[new_pos[0]][new_pos[1]].lower() == word[letter]:
                    self.field[new_pos[0]][new_pos[1]].upper()
                    if recurse(dirr, letter + 1, new_pos, word):
                        self.boocked_positions.append(new_pos)
                        return True
                    else:
                        self.field[new_pos[0]][new_pos[1]].lower()
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
                        self.field[i][j].upper()
                        for dirr in DIRECTIONS:
                            if recurse(dirr, 1, (i, j), word):
                                self.boocked_positions.append((i, j))
                j += 1
            i += 1
            j = 0

        for pos in self.boocked_positions:
            self.field[pos[0]][pos[1]] = self.field[pos[0]][pos[1]].upper()

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