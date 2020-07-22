import easygui


def ask_dimens():
    msg = "Select dimensions"
    title = "Dimensions"
    fieldNames = ["Rows", "columns"]
    fieldValues = easygui.multenterbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None:
            break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        rows, cols = fieldValues
        if str(rows).isdigit() and str(cols).isdigit():
            ROWS, COLS = int(rows), int(cols)
        else:
            errmsg = "Invalid values."
        if errmsg == "":
            break  # no problems found
        fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
    print("Reply was:", fieldValues)
    if fieldValues is None:
        rows, cols = 15, 15
        ROWS, COLS = rows, cols
    return ROWS, COLS


def ask_draw_square():
    msg = "Would you like the grid to be square or rectangular?"
    choices = ["square", "rectangular"]
    reply = easygui.buttonbox(msg, choices=choices)
    print("reply:", reply, ", reply == 0:", reply == choices[0])
    return reply == choices[0]


def ask_draw_block_indexes():
    msg = "Would you like the grid squares to be numbered?"
    choices = ["yes", "no"]
    reply = easygui.buttonbox(msg, choices=choices)
    print("reply:", reply, ", reply == 0:", reply == choices[0])
    return reply == choices[0]


def ask_save():
    msg = "Save current map state?"
    choices = ["yes", "no"]
    reply = easygui.buttonbox(msg, choices=choices)
    print("reply:", reply, ", reply == 0:", reply == choices[0])
    return reply == choices[0]


def get_file_name():
    return easygui.fileopenbox()

