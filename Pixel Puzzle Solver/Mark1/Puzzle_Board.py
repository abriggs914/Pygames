# import importlib
#
# puzzles_list = input('puzzles_list.py')
# importlib.import_module(puzzles_list)
#import get_list_of_puzzles
#import puzzles_list
from puzzle import puzzleify

from puzzles_list import list_of_puzzles
# def define_puzzles_list():
#     return puzzles_list.get_list_of_puzzles()


# list_of_puzzles = get_list_of_puzzles()



list_of_puzzles = puzzleify(list_of_puzzles)


def begin_scoring():
    print('Begin scoring')
    score = 0
    # summary = True
    summary = False
    solved_puzzles = []
    progress_bar = [' ' for i in range(len(list_of_puzzles.keys()))]
    for i in list_of_puzzles.keys():
        if list_of_puzzles[i].solved:  # list_of_puzzles[i].puzzle_board == list_of_puzzles[i].solved_puzzle_board:
            score += 1
            # print('\n\tPuzzle is Solved!\n')
            # print(list_of_puzzles[i])
            solved_puzzles.append(list_of_puzzles[i])
    if summary:
        for puzzle in solved_puzzles:
            id = puzzle.id
            progress_bar[id - 1]
            print('\n\tPuzzle #' + str(id) + ' is Solved!\n')
            print(puzzle)
    print('currently',score,'out of',len(list_of_puzzles),'puzzles are solved.')


begin_scoring()
# end Puzzle_Board
# inp = input('type something')
