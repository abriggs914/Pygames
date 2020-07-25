import json
import os
from pygame import Rect
from a_star_visualizer import SAVE_FILE_HEADER, SAVE_FILE_MESSAGE_SUCCESS, LOAD_FILE_MESSAGE_FAILURE, \
    LOAD_FILE_MESSAGE_NO_FILE, reset, small_pop_up, LOAD_FILE_MESSAGE_SUCCESS
from grid import Node, Map, A_Star, LEGEND
from gui_handling import ask_save, get_file_name


# File is used to handle reading and writing to save files created by this application. All save files follow a unique
# naming convention of: "a_star_save_file_XXX.json". Only files that match this pattern can be loaded into the program.
# Works closely to the a_star_visualizer.py file by updating the main DATA dict on loads.
#
# July 2020


# Using the preset file header "a_star_save_file_XXX.json", count the number of existing files and
# return a new filename which will be numbered one higher than the last file created
def create_save_file():
    files = os.listdir()
    count = sum([1 for f in files if f.startswith(SAVE_FILE_HEADER)])
    if count > 1000:
        count = 0
    return SAVE_FILE_HEADER + str(count + 1).rjust(3, "0") + ".json"


# Serialize Map, Grid, A_Star and pygame.Rect objects for json dumping
def serialize_objects(obj):
    data = {}
    if isinstance(obj, Map):
        map_data = {
            "rows": obj.rows,
            "cols": obj.cols,
            "status": obj.status
        }
        data.update(map_data)
    if isinstance(obj, A_Star):
        a_star_data = {
            "euclidean": obj.EUCLIDEAN,
            "solved": obj.solved,
            "solvable": obj.solvable
        }
        data.update(a_star_data)
    if isinstance(obj, Rect):
        # print("rect:", obj)
        bucket_data = {
            "x": obj.x,
            "y": obj.y,
            "width": obj.width,
            "height": obj.height
        }
        data.update(bucket_data)
    if isinstance(obj, Node):
        node_data = {
            "block_idx": obj.block_idx,
            "f_cost": obj.f_cost,
            "g_cost": obj.g_cost,
            "h_cost": obj.h_cost
        }
        data.update(node_data)
    if len(data) == 0:
        raise TypeError(str(obj) + ' is not JSON serializable')
    else:
        return data


# Ask the user if they meant to save their progress, then create a file and dump current map state to the json file.
# return to draw_button where a call to small_pop_up is made, notifying the user of the success and the
# file that was created
def save(DATA, DISPLAY):
    do_save = ask_save()
    if do_save:
        file_name = create_save_file()
        to_save = ["grid", "buckets"]
        save_dict = {k: v for k, v in DATA.items() if k in to_save}
        for val in to_save:
            if val not in save_dict:
                save_dict[val] = None
        save_dict.update({"legend": LEGEND})

        with open(file_name, "w") as file:
            json.dump(save_dict, file, default=serialize_objects)
            msg = SAVE_FILE_MESSAGE_SUCCESS.format(FN=os.path.basename(file_name))
            return small_pop_up, (DATA, DISPLAY, msg, "save", 3.25)


# Ask user to select a file to reinitialize the grid. File must have been created by this application, and therefore
# follows the naming conventions specified by the file header "a_star_save_file_XXX.json". Any other file will not be
# loaded and will create an error message. If selection is successful, then the DATA parameter will be overwritten with
# the data collected from the json file. Then resets the current display and returns to draw_button with a call to
# small_pop_up to notify the user of the load status, either fail or success.
def load(DATA, DISPLAY):
    file_name = get_file_name()
    if file_name and file_name.endswith(".json") and SAVE_FILE_HEADER in file_name:
        with open(file_name, "r") as file:
            file_dict = json.load(file)
            grid = file_dict["grid"]
            buckets = file_dict["buckets"]
            legend = file_dict["legend"]

            rows = grid["rows"]
            cols = grid["cols"]
            status = grid["status"]

            legend_separated = {}
            for k, v in legend.items():
                legend_separated[k] = [i for i in range(rows * cols) if status[i // cols][i % cols][0] == v]

            grid_map = Map(rows, cols, legend_separated["start"], legend_separated["end"], legend_separated["block"])
            DATA["grid"] = grid_map
            DATA["buckets"] = [[Rect(*c.values()) for c in r] for r in buckets]
            msg = LOAD_FILE_MESSAGE_SUCCESS.format(FN=os.path.basename(file_name))
            show_time = 2
            reset((1, 0, 0), DATA)
    elif not file_name:
        msg = LOAD_FILE_MESSAGE_NO_FILE
        show_time = 3.25
    else:
        show_time = 3.75
        msg = LOAD_FILE_MESSAGE_FAILURE.format(FN=os.path.basename(file_name))

    return small_pop_up, (DATA, DISPLAY, msg, "load", show_time)
