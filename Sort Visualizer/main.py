import pygame
from pygame.locals import *
from widgets import *
from colors import *
from time import sleep

from pgu import gui

##############################################################################################################

##############################################################################################################

##############################################################################################################

# class ColorDialog(gui.Dialog):
#     def __init__(self, value, **params):
#         self.value = list(gui.parse_color(value))
#
#         title = gui.Label("Color Picker")
#
#         main = gui.Table()
#
#         main.tr()
#
#         self.color = gui.Color(self.value, width=64, height=64)
#         main.td(self.color, rowspan=3, colspan=1)
#
#         ##The sliders CHANGE events are connected to the adjust method.  The
#         ##adjust method updates the proper color component based on the value
#         ##passed to the method.
#         ##::
#         main.td(gui.Label(' Red: '), 1, 0)
#         e = gui.HSlider(value=self.value[0], min=0, max=255, size=32, width=128, height=16)
#         e.connect(gui.CHANGE, self.adjust, (0, e))
#         main.td(e, 2, 0)
#         ##
#
#         main.td(gui.Label(' Green: '), 1, 1)
#         e = gui.HSlider(value=self.value[1], min=0, max=255, size=32, width=128, height=16)
#         e.connect(gui.CHANGE, self.adjust, (1, e))
#         main.td(e, 2, 1)
#
#         main.td(gui.Label(' Blue: '), 1, 2)
#         e = gui.HSlider(value=self.value[2], min=0, max=255, size=32, width=128, height=16)
#         e.connect(gui.CHANGE, self.adjust, (2, e))
#         main.td(e, 2, 2)
#
#         gui.Dialog.__init__(self, title, main)
#
#     ##The custom adjust handler.
#     ##::
#     def adjust(self, value):
#         (num, slider) = value
#         self.value[num] = slider.value
#         self.color.repaint()
#         self.send(gui.CHANGE)
#     ##
#
#
# if __name__ == '__main__':
#     app = gui.Desktop()
#     app.connect(gui.QUIT, app.quit, None)
#
#     c = gui.Table(width=640, height=480)
#
#     dialog = ColorDialog("#00ffff")
#
#     e = gui.Button("Color")
#     e.connect(gui.CLICK, dialog.open, None)
#     c.tr()
#     c.td(e)
#
#     app.run(c)

##############################################################################################################

# class AboutDialog(gui.Dialog):
#     def __init__(self, **params):
#         title = gui.Label("About Cuzco's Paint")
#
#         width = 400
#         height = 200
#         doc = gui.Document(width=width)
#
#         space = title.style.font.size(" ")
#
#         doc.block(align=0)
#         for word in """Cuzco's Paint v1.0 by Phil Hassey""".split(" "):
#             doc.add(gui.Label(word))
#             doc.space(space)
#         doc.br(space[1])
#
#         doc.block(align=-1)
#         doc.add(gui.Image("cuzco.png"), align=1)
#         for word in """Cuzco's Paint is a revolutionary new paint program it has all the awesome features that you need to paint really great pictures.""".split(
#                 " "):
#             doc.add(gui.Label(word))
#             doc.space(space)
#         doc.br(space[1])
#
#         doc.block(align=-1)
#         for word in """Cuzco's Paint will drive you wild!  Cuzco's Paint was made as a demo of Phil's Pygame Gui.  We hope you enjoy it!""".split(
#                 " "):
#             doc.add(gui.Label(word))
#             doc.space(space)
#
#         for i in range(0, 10):
#             doc.block(align=-1)
#             for word in """This text has been added so we can show off our ScrollArea widget.  It is a very nice widget built by Gal Koren!""".split(
#                     " "):
#                 doc.add(gui.Label(word))
#                 doc.space(space)
#             doc.br(space[1])
#
#         gui.Dialog.__init__(self, title, gui.ScrollArea(doc, width, height))
#
#
# ##
#
#
# if __name__ in '__main__':
#     app = gui.Desktop()
#     app.connect(gui.QUIT, app.quit, None)
#
#     c = gui.Table(width=640, height=480)
#
#     ##The button CLICK event is connected to the dialog.open method.
#     ##::
#     dialog = AboutDialog()
#
#     e = gui.Button("About")
#     e.connect(gui.CLICK, dialog.open, None)
#     ##
#     c.tr()
#     c.td(e)
#
#     app.run(c)

##############################################################################################################

# Load an alternate theme to show how it is done. You can also
# specify a path (absolute or relative) to your own custom theme:
#
#   app = gui.Desktop(theme=gui.Theme("path/to/theme"))
#
# app = gui.Desktop()
# app.connect(gui.QUIT,app.quit,None)
#
# ##The table code is entered much like HTML.
# ##::
# c = gui.Table()
#
#
# c.tr()
# c.td(gui.Label("Gui Widgets"),colspan=4)
#
# def cb():
#     print("Clicked!")
# btn = gui.Button("Click Me!")
# btn.connect(gui.CLICK, cb)
#
# c.tr()
# c.td(gui.Label("Button"))
# c.td(btn,colspan=3)
# ##
#
# c.tr()
# c.td(gui.Label("Switch"))
# c.td(gui.Switch(False),colspan=3)
#
# c.tr()
# c.td(gui.Label("Checkbox"))
# ##Note how Groups are used for Radio buttons, Checkboxes, and Tools.
# ##::
# g = gui.Group(value=[1,3])
# c.td(gui.Checkbox(g,value=1))
# c.td(gui.Checkbox(g,value=2))
# c.td(gui.Checkbox(g,value=3))
# ##
#
# c.tr()
# c.td(gui.Label("Radio"))
# g = gui.Group()
# c.td(gui.Radio(g,value=1))
# c.td(gui.Radio(g,value=2))
# c.td(gui.Radio(g,value=3))
#
# c.tr()
# c.td(gui.Label("Select"))
# e = gui.Select()
# e.add("Goat",'goat')
# e.add("Horse",'horse')
# e.add("Dog",'dog')
# e.add("Pig",'pig')
# c.td(e,colspan=3)
#
# c.tr()
# c.td(gui.Label("Tool"))
# g = gui.Group(value='b')
# c.td(gui.Tool(g,gui.Label('A'),value='a'))
# c.td(gui.Tool(g,gui.Label('B'),value='b'))
# c.td(gui.Tool(g,gui.Label('C'),value='c'))
#
# c.tr()
# c.td(gui.Label("Input"))
# def cb():
#     print("Input received")
# w = gui.Input(value='Cuzco',size=8)
# w.connect("activate", cb)
# c.td(w,colspan=3)
#
# c.tr()
# c.td(gui.Label("Slider"))
# c.td(gui.HSlider(value=23,min=0,max=100,size=20,width=120),colspan=3)
#
# c.tr()
# c.td(gui.Label("Keysym"))
# c.td(gui.Keysym(),colspan=3)
#
# c.tr()
# c.td(gui.Label("Text Area"), colspan=4, align=-1)
#
# c.tr()
# c.td(gui.TextArea(value="Cuzco the Goat", width=150, height=70), colspan=4)
#
# app.run(c)

##############################################################################################################

# app = gui.Desktop()
# app.connect(gui.QUIT,app.quit,None)
# g = gui.Group(name='colors', value='g')
#
# t = gui.Table()
# t.tr()
# t.td(gui.Label('Red'))
# t.td(gui.Radio(g, 'r'))
# t.tr()
# t.td(gui.Label('Green'))
# t.td(gui.Radio(g, 'g'))
# t.tr()
# t.td(gui.Label('Blue'))
# t.td(gui.Radio(g, 'b'))
#
# app.run(t)

##############################################################################################################

# app = gui.Desktop()
# app.connect(gui.QUIT,app.quit,None)
#
# c = gui.Table(width=200,height=120)
#
# ##::
# class Quit(gui.Button):
#     def __init__(self,**params):
#         params['value'] = 'Quit'
#         gui.Button.__init__(self,**params)
#         self.connect(gui.CLICK,app.quit,None)
# ##
#
# ##Adding the button to the container.  By using the td method to add it, the button
# ##is placed in a sub-container, and it will not have to fill the whole cell.
# ##::
# c.tr()
# e = Quit()
# c.td(e)
# ##
#
# app.run(c)

##############################################################################################################

# ##Using Desktop instead of App provides the GUI with a background.
# ##::
# app = gui.Desktop()
# app.connect(gui.QUIT,app.quit,None)
# ##
#
# ##The container is a table
# ##::
# c = gui.Table(width=200,height=120)
# ##
#
# ##The button CLICK event is connected to the app.close method.  The button will fill the whole table cell.
# ##::
# e = gui.Button("Quit")
# e.connect(gui.CLICK,app.quit,None)
# c.add(e,0,0)
# ##
#
# app.run(c)

##############################################################################################################

# ##::
# app = gui.App()
#
# e = gui.Button("Hello World")
#
# app.connect(gui.QUIT, app.quit)
#
# app.run(e)

##############################################################################################################

#################################################
##				   Game vars				   ##
#################################################

DISPLAY = None
TITLE = "Sort visualizer"
DEFAULT_SIZE = (900, 600)
WIDTH = DEFAULT_SIZE[0]
HEIGHT = DEFAULT_SIZE[1]
BUTTON_TEXT_FONT = None


#################################################

def click_1():
    print("click 1")


def click_2():
    print("click 2")


def which_click(msg):
    print("click:", msg)


def draw_display():
    DISPLAY.fill((110, 120, 130))

    #################################################################################################################
    # buttons demo
    button1.draw()
    button2.draw()

    # #################################################################################################################
    # # button bar demo
    # bbh = ButtonBar(pygame, DISPLAY, 550, 145, 100, 200, BUTTON_TEXT_FONT, LIGHT_GRAY, 0.95, True)
    # bbv = ButtonBar(pygame, DISPLAY, 450, 145, 100, 200, BUTTON_TEXT_FONT, LIGHT_GRAY, 0.95, False)
    #
    # names = ["start", "stop", "play", "reset"]
    # ics = [BLUE, GREEN, RED, DARK_GRAY]
    # acs = [GREEN, RED, DARK_GRAY, BLUE]
    # actions = [which_click, which_click, which_click, which_click]
    # lst = [names, ics, acs, actions, names]
    # for i in range(len(names)):
    #     bbh.add_button(*[l[i] if j < 4 else tuple([l[i]]) for j, l in enumerate(lst)])
    #     bbv.add_button(*[l[i] if j < 4 else tuple([l[i]]) for j, l in enumerate(lst)])
    #
    # bbh.draw()
    # bbv.draw()

    # #################################################################################################################
    # # scrollbar demo
    # # game, display, x, y, w, h, button_c, background_c, bar_c, is_vertical = True
    # sbv.draw()
    # sbh.draw()

    # ################################################################################################################
    # table demo
    t1.draw()
    # t1.resize(pygame.Rect(random.randint(0, 100), random.randint(0, 100), random.randint(250, 350), random.randint(250, 350)))
    # t2.draw()
    # sleep(1)

    ################################################################################################################
    # radio button demo
    r1.draw()
    r2.draw()
    r3.draw()
    r4.draw()
    r5.draw()

    # ################################################################################################################
    # # radio group demo
    # rg1.draw()

    pygame.display.update()


def init_display():
    global DISPLAY, sbv, sbh, button2, button1, t1, t2, r1, r2, r3, r4, r5, rg1
    w, h = DEFAULT_SIZE
    DISPLAY = pygame.display.set_mode((w, h), RESIZABLE)
    pygame.display.set_caption(TITLE)

    # toggle buttons
    button2 = buttonr(pygame, DISPLAY, "button2", pygame.Rect(150, 241, 400, 300), RED, BLUE, BUTTON_TEXT_FONT, click_2)
    button1 = Button(pygame, DISPLAY, "button1", 0, 0, 100, 100, GREEN, BLUE, BUTTON_TEXT_FONT, click_1)
    button2.enable_toggle()
    button1.enable_toggle()

    # scroll bars
    # self, game, display, x, y, w, h, bar_proportion, button_c, bar_background_c, bar_c, contents, content_c, is_vertical=True
    sbv = ScrollBar(game=pygame, display=DISPLAY, x=10, y=10, w=300, h=300, bar_proportion=0.08, button_c=DARK_GRAY,
                    bar_background_c=LIGHT_GRAY, bar_c=BLUE, contents=None, content_c=RED, is_vertical=True)
    sbh = ScrollBar(game=pygame, display=DISPLAY, x=350, y=10, w=300, h=300, bar_proportion=0.08, button_c=DARK_GRAY,
                    bar_background_c=LIGHT_GRAY, bar_c=BLUE, contents=None, content_c=GREEN, is_vertical=False)

    # tables
    # self, game, display, x, y, w, h, c, font, title, header
    t1 = Table(game=pygame, display=DISPLAY, x=220, y=230, w=450, h=150, c=WHITE, font=None, title="table 1",
               header=["first name", "last name", "telephone", "address"])
    t1.set_title_color(BLUE)
    t1r1 = TableRow(game=pygame, display=DISPLAY)
    t1r2 = TableRow(game=pygame, display=DISPLAY)
    t1r3 = TableRow(game=pygame, display=DISPLAY)
    t1r4 = TableRow(game=pygame, display=DISPLAY)
    t1r1.set_row_color(random_color())
    t1r2.set_row_color(random_color())
    t1r3.set_row_color(random_color())
    t1r4.set_row_color(random_color())
    t1r1.add_content(["Avery", "Briggs", "506 323 8472", "239 Moose Mountain Road"])
    t1r2.add_content(["Daffy", "Duck", "500 555 1234", "1500 Lake Road"])
    t1r3.add_content(["Donald", "Duck", "1501 Lake Road"])
    t1r4.add_content(["Bugs", "Bunny", "800 500 9876", "12 Albuquerque"])
    t1.add_rows(t1r1, t1r2, t1r3, t1r4)
    t1.add_row(["Goofy", "Dog", "800 555 4567", "Mickey Mouse's club house"])
    t1.add_rows([["Chewbacca", "", 18005551234, "Millennium Falcon"],
                 ["Darth", "Vader", 18005555555, "Death Star"]])

    t2_dict = {
        "first name": ["Avery", "Daffy", "Donald", "Bugs", "Goofy", "Chewbacca", "Darth"],
        "last name": ["Briggs", "Duck", "Duck", "Bunny", "Dog", "", "Vader"],
        "telephone": ["506 323 8472", "500 555 1234", "", "800 500 9876", "800 555 4567", 18005551234, 18005555555],
        "address": ["239 Moose Mountain Road", "1500 Lake Road", "1501 Lake Road", "12 Albuquerque",
                    "Mickey Mouse's club house", "Millennium Falcon", "Death Star"]
    }

    t2 = Table(game=pygame, display=DISPLAY, x=20, y=250, w=450, h=150, c=WHITE, font=None, title="table 1", header=[])
    t2.add_rows(t2_dict)

    print("first names:", t1.get_col_data("first name"))
    print("row 2 col 3", t1r2.get_data(3))
    print("row 2 col 3", t1.get_data(2, 3))

    # Testing brighten / darken
    # print("BLACK:\t", DARK_GRAY)
    # for i in range(0, 100, 5):
    #     print("darker:\t", darken(DARK_GRAY, i/100))
    #     print("brighter:\t", brighten(DARK_GRAY, i/100))

    # radio buttons
    rg1 = RadioGroup(pygame, DISPLAY, 2)
    r1 = RadioButton(game=pygame, display=DISPLAY, rect=pygame.Rect(60, 460, 40, 40), msg="radio button 1",
                     font=None, c=GREEN, sc=None, txc=RED, bgc=None)
    r2 = RadioButton(game=pygame, display=DISPLAY, rect=pygame.Rect(100, 500, 100, 100), msg="radio button 2",
                     font=None, c=GREEN, sc=DARK_GRAY, txc=RED, bgc=WHITE)
    r3 = RadioButton(game=pygame, display=DISPLAY, rect=pygame.Rect(210, 460, 100, 100), msg="radio button 3",
                     font=None, c=RED, sc=DARK_GRAY, txc=RED, bgc=WHITE)
    r4 = RadioButton(game=pygame, display=DISPLAY, rect=pygame.Rect(320, 460, 100, 100), msg="radio button 4",
                     font=None, c=RED, sc=DARK_GRAY, txc=RED, bgc=WHITE)
    r5 = RadioButton(game=pygame, display=DISPLAY, rect=pygame.Rect(430, 460, 100, 100), msg="radio button 5",
                     font=None, c=RED, sc=DARK_GRAY, txc=RED, bgc=WHITE)
    rg1.add_buttons(r1, r2, r3, r4, r5)
    print(rg1)
    rg1.set_selected(r1)
    print(rg1)
    rg1.set_selected(r2)
    print(rg1)
    rg1.set_selected(r3)
    print(rg1)
    rg1.set_selected(r4)
    print(rg1)
    rg1.set_selected(r5)
    print(rg1)



def init_pygame():
    global BUTTON_TEXT_FONT
    print("\n\nINIT PYGAME\n\n")
    pygame.init()
    BUTTON_TEXT_FONT = pygame.font.SysFont("arial", 16)


def check_quit(loop=True):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            loop = False
    return loop


def play():
    loop = True

    # app = gui.App()
    # e = gui.Button("Hello World")
    # print("e\t",e,"type(e):\t", type(e))
    # print("Display\t",DISPLAY,"type(DISPLAY):\t", type(DISPLAY))
    # # e.paint(DISPLAY)
    # app.init(e, DISPLAY, DISPLAY.get_rect())
    # app.connect(gui.QUIT, app.quit)

    # prev = None
    while loop:
        # app.paint(DISPLAY)
        # if DATA["mode"] != prev:
        #     prev = DATA["mode"]
        #     print("mode:", prev)
        #
        draw_display()
        # handle_mode()
        # update_mode()
        # CLOCK.tick(20)
        loop = check_quit()

    quit()


def init():
    if pygame.get_init():
        print("\n\nnQUIT PYGAME\n\n")
        pygame.display.quit()
    init_pygame()
    init_display()
    play()


if __name__ == "__main__":
    init()
