import os
from sys import platform


# Check for user system
linux = False
bad_os = False
if platform == "linux" or platform == "linux2":
    linux = True
elif platform == "win32":
    bad_os = True

scripts = {
    1: "maze/main.py",
    2: "sudoku/main.py",
    3: "crossword/main.py",
    4: "graph_colorizer/main.py",
}

print("Hello! This is a script launcher. Choose a number of the script you'd like to run.")
print("Before you choose, close down the program and edit the coresponding file in data folder if you want to solve your problem\n")
print("\
    1. Maze solver\n\
    2. Sudoku solver\n\
    3. Crossword solver\n\
    4. Graph Colorer\n")

while True:
    try:
        choice = int(input("Enter a number: "))
        command = scripts[choice]
        break
    except KeyError:
        print("Enter a correct number")
    except ValueError:
        print("Enter a NUMBER")

if bad_os:
    os.system("python -m " + command)
elif linux:
    os.system("python " + command)



