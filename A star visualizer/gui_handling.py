import easygui


# File makes use of the easygui module found at http://easygui.sourceforge.net/tutorial.html to obtain and handle
# user input for save, load, and customization functions.


def ask_dimens():
    msg = "Select dimensions"
    title = "Dimensions"
    field_names = ["Rows", "columns"]
    field_values = easygui.multenterbox(msg, title, field_names)
    ROWS, COLS = None, None

    # make sure that none of the fields were left blank
    while 1:
        if field_values is None:
            break
        errmsg = ""
        for i in range(len(field_names)):
            if field_values[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % field_names[i])
        rows, cols = field_values
        if str(rows).isdigit() and str(cols).isdigit():
            ROWS, COLS = int(rows), int(cols)
        else:
            errmsg = "Invalid values."
        if errmsg == "":
            break  # no problems found
        field_values = easygui.multenterbox(errmsg, title, field_names, field_values)
    print(msg, "-", " - ".join(list(map(str, [ROWS, COLS]))))
    if field_values is None:
        rows, cols = 15, 15
        ROWS, COLS = rows, cols
    return ROWS, COLS


def ask_draw_square():
    msg = "Would you like the grid to be square or rectangular?"
    choices = ["square", "rectangular"]
    reply = easygui.buttonbox(msg, choices=choices)
    print(msg, "-", reply)
    return reply == choices[0]


def ask_draw_block_indexes():
    msg = "Would you like the grid squares to be numbered?"
    choices = ["yes", "no"]
    reply = easygui.buttonbox(msg, choices=choices)
    print(msg, "-", reply)
    return reply == choices[0]


def ask_save():
    msg = "Save current map state?"
    choices = ["yes", "no"]
    reply = easygui.buttonbox(msg, choices=choices)
    print(msg, "-", reply)
    return reply == choices[0]


def get_file_name():
    return easygui.fileopenbox()

def ask_use_full_screen():
    msg = "Use full screen for application?"
    choices = ["yes", "no"]
    reply = easygui.buttonbox(msg, choices=choices)
    print(msg, "-", reply)
    return reply == choices[0]
