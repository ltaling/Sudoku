# Sudoku Generator

This python program generates sudoku puzzles along with a corresponding solution. It does run fairly slow so I wouldn't recommend having fewer than 25 clues in the puzzle. However, it is guaranteed to have exactly 1 solution so you can be certain there will be no issues with solving it (although the difficulty is completely random). I have also attached an example puzzle, with 25 clues, along with the corresponding solution as a proof it works. 

There is also a sudoku solver (sudo_solver.py) which has an interactive UI in which you can type the sudoku in yourself and it will solve it for you. It's currently very basic as it doesn't detect if your sudoku is possible to solve or not and some sudoku puzzles can take a while to solve. Also, the UI is incredibly basic. Perhaps I shall make improvements in the future (such as implementing knuth's algorithm X) but I currently do not have the time :(
