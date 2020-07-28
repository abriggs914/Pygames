
TITLE = "A* Pathfinding"
SAVE_FILE_HEADER = "a_star_save_file_"
SAVE_FILE_MESSAGE_SUCCESS = "{FN}\nsaved successfully!"
LOAD_FILE_MESSAGE_SUCCESS = "{FN}\nloadad successfully!"
LOAD_FILE_MESSAGE_NO_FILE = "Please select a file."
LOAD_FILE_MESSAGE_FAILURE = "Unable to load file:\n{FN}\nPlease ensure that the file contains the file header:\n\"" + SAVE_FILE_HEADER + "XXX\"\nand has the \".json\" extenstion."
ABOUT_MESSAGE = """A* Pathfinding visualizer

Find a path between a start and end Node using the A* algorithm.

- Draw obstacles on the grid to make the path more complex.
- Save maps and return to them later using the save and load features.
- Search by Euclidean distance, which allows for diagonal movement,
or Manhattan distance which only allows for linear movement.\n
- Reset button features:
Clear search path by left-clicking reset.
Clear drawn obstacles by left-clicking and middle-clicking simultaneously.
Clear entire grid by left-clicking and right-clicking simultaneously.
Click all mouse buttons simultaneously to clear entire grid and reset all
    customization options. Then perform a complete program re-initialization
"""
