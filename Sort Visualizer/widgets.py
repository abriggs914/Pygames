# quick widgets from pygame
from colors import *
from queue import Queue
import math
import random

"""
Aug. 30 2020
    -   Added basic button functionality using functions. Allowed for the button to have a function to
        execute when clicked and color changing when mouse hovering.
    -   Started a ButtonBar class for either horizontal or vertical button bars.
    
Aug. 31 2020
    -   Converted button function to a class. Added scroll functionality for the button to work with the
        ScrollBar class.
    -   Started a ScrollBar class for either horizontal or vertical scroll bars. Need to figure out how the
        contents will work using using nested widgets.
    -   Created arrow drawing function.

Sept. 1 2020
    -   Created Table & TableRow classes to offer a tableview widget.
    -   Added toggle functionality to Button class.
    -   Made parent Widget class for all widgets.
    -   Started RadioButton class.
    
Sept. 2 2020
    -   Edited RadioButton class with color and design attributes.
    -   Is it possible to move functions (resize, set_divider_width...) to parent class to save repetitive code?
    -   Created RadioGroups to control RadioButtons. 
    
Sept. 3 2020
    -   Added resize and move functions to all widgets
"""

# # Orientations
# NORTH = 0
# NORTH_EAST = 1
# EAST = 2
# SOUTH_EAST = 3
# SOUTH = 4
# SOUTH_WEST = 5
# WEST = 6
# NORTH_WEST = 7
# orientations
NORTH = 4
NORTH_EAST = 5
EAST = 6
SOUTH_EAST = 7
SOUTH = 0
SOUTH_WEST = 1
WEST = 2
NORTH_WEST = 3


# Create and return text surface and rect for blitting
def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Ensure that a text will fit into a given pygame.Rect object.
# Adjusts the message using new line characters to fit width-wise.
def wrap_text(msg, r, font):
    txt = ""
    for c in msg:
        txt += c
        text = txt.split("\n")
        txt_w, txt_h = font.size(text[-1])
        if txt_w >= r.width * 0.9:
            txt += "\n"
    return txt


# Writes text to the display.
def write_text(game, display, r, msg, font, bg_c=WHITE, tx_c=BLACK, wrap=True):
    if not msg or msg is None:
        msg = "--"
    if wrap:
        msg = wrap_text(msg, r, font)
    lines = msg.split("\n")
    x, y, w, h = r
    to_blit = []
    length = max(2, len(lines))
    for i, line in enumerate(lines):
        text_surf, text_rect = text_objects(line, font, tx_c)
        width, height = font.size(line)
        text_rect.center = ((x + (w / 2)), (((i * height) + y) + (h / length)))
        to_blit.append((text_surf, text_rect))

    if bg_c is not None:
        game.draw.rect(display, bg_c, r)
    display.blits(to_blit)


# return random RGB color
def random_color():
    return (
        random.randint(10, 245),
        random.randint(10, 245),
        random.randint(10, 245)
    )


# Clamp an number between small and large values.
def clamp(s, v, l):
    return max(s, min(v, l))


# Darken an RGB color using a proportion p (0-1)
def darken(c, p):
    r, g, b = c
    r = clamp(0, round(r - (255 * p)), 255)
    g = clamp(0, round(g - (255 * p)), 255)
    b = clamp(0, round(b - (255 * p)), 255)
    return r, g, b


# Brighten an RGB color using a proportion p (0-1)
def brighten(c, p):
    r, g, b = c
    r = clamp(0, round(r + (255 * p)), 255)
    g = clamp(0, round(g + (255 * p)), 255)
    b = clamp(0, round(b + (255 * p)), 255)
    return r, g, b


# display a button and listen for it to be clicked.
# game      -   pygame object
# display   -   display created by pygame
# msg 		- 	button text
# x			-	button x
# y			-	button y
# w			-	button width
# h			-	button height
# ic		-	button color
# ac		-	button color when hovering
# font      -   font style
# action	-	function to be called on click
# args      -   tuple of function arguments
# def button(game, display, msg, x, y, w, h, ic, ac, font, action=None, args=None):
#     # print("game:", self.game, "type:", type(self.game))
#     # print("self:", self, "type:", type(self))
#     if font is None:
#         font = game.font.Font(None, 16)
#     mouse = game.mouse.get_pos()
#     click = game.mouse.get_pressed()
#
#     if x + w > mouse[0] > x and y + h > mouse[1] > y:
#         game.draw.rect(display, ac, (x, y, w, h))
#         if click[0] == 1:
#             if action is not None:
#                 if args is None:
#                     action()
#                 else:
#                     action(*args)
#                 # action(*args) if args is not None else action()
#     else:
#         game.draw.rect(display, ic, (x, y, w, h))
#
#     font.set_bold(True)
#     text_surf, text_rect = text_objects(msg, font)
#     text_rect.center = ((x + (w / 2)), (y + (h / 2)))
#     display.blit(text_surf, text_rect)


# display a button and listen for it to be clicked.
# shorter signature, but requires a pygame.Rect object for sizing.
# game      -   pygame object
# display   -   display created by pygame
# msg 		- 	button text
# r			-	pygame rect shape
# ic		-	button color
# ac		-	button color when hovering
# font      -   font style
# action	-	function to be called on click
def buttonr(game, display, msg, r, ic, ac, font, action=None, args=None):
    return Button(game, display, msg, *r, ic, ac, font, action, args)


# Rotate a 2D point about the origin, a given amount of degrees.
def rotate_on_origin(px, py, theta):
    t = math.radians(theta)
    x = (px * math.cos(t)) - (py * math.sin(t))
    y = (px * math.sin(t)) + (py * math.cos(t))
    return x, y


# Rotate a 2D point around any central point, a given amount of degrees.
def rotate_point(cx, cy, px, py, theta):
    xd = 0 - cx
    yd = 0 - cy
    rx, ry = rotate_on_origin(px + xd, py + yd, theta)
    return rx - xd, ry - yd


class Widget:

    def __init__(self, game, display):
        self.game = game
        self.display = display

    def draw(self):
        print("Nothing to draw")


# class RadioGroup(Widget):
#
#     def __init__(self, game, display, max_selections=None):
#         super().__init__(game, display)
#         self.max_selections = 1 if max_selections is None else max_selections
#         self.radio_buttons = []
#         self.selected = Queue(self.max_selections)
#
#     def __repr__(self):
#         return "<RadioGroup (" + str(len(self.radio_buttons)) + " buttons, " + str(self.selected.qsize()) + " / " + str(self.max_selections) + " selected)>"
#
#     def get_selected_buttons(self):
#         # TODO: this can probably be done more efficiently with a simple list
#         buttons = [self.selected.get() for i in range(self.selected.qsize())]
#         self.selected = Queue(self.max_selections)
#         for b in buttons:
#             self.selected.put(b)
#         return buttons
#
#     def set_max_selections(self, n):
#         self.max_selections = clamp(1, n, len(self.radio_buttons))
#         new_queue = Queue(self.max_selections)
#         buttons = self.get_selected_buttons()
#         for i, b in enumerate(buttons):
#             if i < self.max_selections:
#                 new_queue.put(b)
#             if i < len(buttons) and new_queue.full():
#                 button = new_queue.get()
#                 button.set_selected(False)
#         self.selected = new_queue
#
#     def add_buttons(self, *radio_buttons):
#         for button in radio_buttons:
#             self.radio_buttons.append(button)
#
#             # Button listener
#             buttonr(self.game, self.display, "", button.bounds, None, None, None, self.set_selected, [button])
#
#     def set_selected(self, radio_button):
#         print("click:",self.selected.qsize())
#         if radio_button not in self.get_selected_buttons():
#             if self.selected.full():
#                 b = self.selected.get()
#                 b.set_selected(False)
#             self.selected.put(radio_button)
#             radio_button.set_selected(True)
#
#     def clear_all_selected(self):
#         buttons = self.get_selected_buttons()
#         for b in buttons:
#             b.set_selected(False)
#         self.selected = Queue(self.max_selections)


class RadioGroup(Widget):

    def __init__(self, game, display, max_selections=None):
        super().__init__(game, display)
        self.max_selections = 1 if max_selections is None else max_selections
        self.radio_buttons = []
        self.selected = []
        self.keep_grouped = True

    def __repr__(self):
        return "<RadioGroup (" + str(len(self.radio_buttons)) + " buttons, " + str(len(self.selected)) + " / " + str(
            self.max_selections) + " selected)>"

    def set_max_selections(self, n):
        n = clamp(1, n, len(self.radio_buttons))
        self.max_selections = n
        if n < len(self.selected):
            unselect = self.selected[len(self.selected) - n:]
            for button in unselect:
                button.set_selected(False)

    def add_buttons(self, *radio_buttons):
        for button in radio_buttons:
            self.radio_buttons.append(button)
        # sort list for resizing purposes, don't want any overlap.
        self.sort_buttons()

    # sort the list of buttons by increasing x coordinates
    def sort_buttons(self):
        print("BEFORE radio buttons", self.radio_buttons)
        self.radio_buttons.sort(key=lambda rb: rb.bounds.x)
        print("AFTER radio buttons", self.radio_buttons)

    def set_selected(self, radio_button):
        if radio_button not in self.selected:
            if len(self.selected) == self.max_selections:
                b = self.selected.pop(0)
                b.set_selected(False)
            self.selected.append(radio_button)
            radio_button.set_selected(True)

    def clear_all_selected(self):
        for b in self.selected:
            b.set_selected(False)
        self.selected = []

    def set_keep_grouped(self, g):
        self.keep_grouped = g

    def move(self, r):
        if len(self.radio_buttons) > 0:
            first_bounds = self.radio_buttons[0].bounds
            diff_bounds = r.x - first_bounds.x, r.y - first_bounds.y
            for button in self.radio_buttons:
                new_r = self.game.Rect(diff_bounds[0] + button.bounds.x, diff_bounds[1] + button.bounds.y,
                                       button.bounds.width, button.bounds.height)
                button.move(new_r)

    def resize(self, r, is_horizontal=True):
        if len(self.radio_buttons) > 0:
            first_bounds = self.radio_buttons[0].bounds
            diff_bounds = r.width - first_bounds.width, r.height - first_bounds.height
            # print("first_bounds:", first_bounds)
            # print("first_bounds:", first_bounds)
            # print("r_bounds:", r)
            # print("diff_bounds:", diff_bounds)
            nb = len(self.radio_buttons)
            w = r.width / nb if is_horizontal else r.width
            h = r.height / nb if not is_horizontal else r.height
            for i, button in enumerate(self.radio_buttons):
                # new_r = self.game.Rect(button.bounds.x, button.bounds.y, diff_bounds[0] + button.bounds.width,
                #                        diff_bounds[1] + button.bounds.height)
                new_r = self.game.Rect(button.bounds.x, button.bounds.y, w, h)
                if i < len(self.radio_buttons) - 1:
                    next_bounds = self.radio_buttons[i + 1].bounds
                    x_diff = abs(new_r.right - next_bounds.x) if is_horizontal else 0
                    y_diff = abs(new_r.bottom - next_bounds.y) if not is_horizontal else 0
                    if new_r.colliderect(next_bounds):
                        # x_diff = new_r.right - next_bounds.x if is_horizontal else 0
                        # y_diff = new_r.bottom - next_bounds.y if not is_horizontal else 0
                        next_bounds = self.game.Rect(next_bounds.x + x_diff, next_bounds.y + y_diff, next_bounds.width, next_bounds.height)
                        self.radio_buttons[i + 1].move(next_bounds)
                        print("next_bounds:", next_bounds)
                    elif self.keep_grouped:
                        # x_diff = next_bounds.x - new_r.right if is_horizontal else 0
                        # y_diff = next_bounds.y - new_r.bottom if not is_horizontal else 0
                        next_bounds = self.game.Rect(next_bounds.x - x_diff, next_bounds.y - y_diff, next_bounds.width, next_bounds.height)
                        self.radio_buttons[i + 1].move(next_bounds)
                        print("next_bounds:", next_bounds)

                button.resize(new_r)

    def draw(self):
        for button in self.radio_buttons:
            b = buttonr(self.game, self.display, "", button.bounds, None, None, None, self.set_selected, [button])
            b.draw()
            button.draw()


class RadioButton(Widget):

    # Create a RadioButton, used to act as a selection switch between multiple options.
    # Must be accompanied by a RadioGroup in order to interact with the widget, otherwise
    # only shows the set selection state of the button.
    def __init__(self, game, display, rect, msg, font=None, c=None, sc=None, txc=None, bgc=None):
        super().__init__(game, display)
        self.bounds = rect
        self.radius = None
        self.set_radius(self.calc_radius())
        self.msg = msg

        self.font = font if font is not None else game.font.Font(None, 16)
        self.c = c
        self.sc = sc if sc is not None else darken(c, 0.6)
        self.txc = txc if txc is not None else BLACK
        self.bgc = bgc  # can be None, will have no background
        self.div_c = BLACK
        self.div_w = 3
        self.draw_border = bgc is not None
        self.is_selected = False
        # normal color
        # selected color
        # 2 circles, outer button, and inner depressed button
        # label text color
        # label background color
        # label font
        # label message

    def __repr__(self):
        return "RadioButton<(" + self.msg + ") " + str(self.bounds) + ">"

    def calc_radius(self):
        bounds = self.bounds
        return (min(bounds.height, bounds.width) * 0.6) / 2

    def move(self, r):
        self.bounds = self.game.Rect(r.x, r.y, self.bounds.width, self.bounds.height)

    def resize(self, r):
        self.bounds = self.game.Rect(self.bounds.x, self.bounds.y, r.width, r.height)
        self.set_radius(self.calc_radius())

    def set_radius(self, r):
        self.radius = round(r)

    def set_label(self, msg):
        self.msg = msg

    def set_font(self, f):
        self.font = f

    def set_button_color(self, c):
        self.c = c

    def set_selected_color(self, c):
        self.sc = c

    def set_text_color(self, c):
        self.txc = c

    def set_background_color(self, c):
        self.bgc = c

    def set_border_color(self, c):
        self.div_c = c

    def set_border_width(self, w):
        self.div_w = w

    def set_draw_border(self, t):
        self.draw_border = t

    def set_selected(self, t):
        self.is_selected = t

    def toggle(self):
        self.is_selected = not self.is_selected

    def draw(self):
        if self.bgc is not None:
            # draw background
            self.game.draw.rect(self.display, self.bgc, self.bounds)

        # draw border lines
        if self.draw_border:
            self.game.draw.line(self.display, self.div_c, self.bounds.topleft, self.bounds.topright, self.div_w)
            self.game.draw.line(self.display, self.div_c, self.bounds.topleft, self.bounds.bottomleft, self.div_w)
            self.game.draw.line(self.display, self.div_c, self.bounds.topright, self.bounds.bottomright, self.div_w)
            self.game.draw.line(self.display, self.div_c, self.bounds.bottomleft, self.bounds.bottomright, self.div_w)

        # draw circle
        c_x, c_y = self.bounds.centerx, self.bounds.bottom - self.radius - self.div_w
        self.game.draw.circle(self.display, self.c, (c_x, c_y), self.radius, self.div_w)

        if self.is_selected:
            self.game.draw.circle(self.display, self.sc, (c_x, c_y), round(self.radius * 0.5))

        # draw label
        title_rect = self.game.Rect(self.bounds.left + self.div_w, self.bounds.top + self.div_w,
                                    self.bounds.width - (2 * self.div_w),
                                    self.bounds.height - (2 * (self.radius + self.div_w)))
        write_text(self.game, self.display, title_rect, self.msg, self.font, self.bgc, wrap=True)


class Button(Widget):

    def __init__(self, game, display, msg, x, y, w, h, ic, ac, font, action=None, args=None):
        super().__init__(game, display)
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac
        self.font = font if font is not None else game.font.Font(None, 16)
        self.action = action
        self.args = args
        self.bounds = None
        self.resize(game.Rect(x, y, w, h))

        self.draw_rect = ic is not None  # if ic is None, no background square is drawn
        self.draw_hover = ac is not None  # if ac is None, no hover square is drawn

        self.scrollable = False
        self.scroll_up_func = None
        self.scroll_up_args = None
        self.scroll_down_func = None
        self.scroll_down_args = None

        self.toggleable = False
        self.toggle_val = False

    def move(self, r):
        self.x = r.x
        self.y = r.y
        self.bounds = self.game.Rect(self.x, self.y, self.w, self.h)

    def resize(self, r):
        self.w = r.width
        self.h = r.height
        self.bounds = self.game.Rect(self.x, self.y, self.w, self.h)

    def enable_toggle(self):
        self.toggleable = True

    def disable_toggle(self):
        self.toggleable = False

    def toggle(self):
        self.toggle_val = not self.toggle_val

    # add scrolling functionality to a button.
    # up_func       -   function to execute on scroll up
    # up_args       -   arguments to pass to scroll up function
    # down_func     -   function to execute on scroll down
    # down_args     -   arguments to pass to scroll down function
    def enable_scrollable(self, up_func, up_args, down_func, down_args):
        self.scrollable = True
        self.scroll_up_func = up_func
        self.scroll_up_args = up_args
        self.scroll_down_func = down_func
        self.scroll_down_args = down_args

    def disable_scrollable(self):
        self.scrollable = False
        self.scroll_up_func = None
        self.scroll_up_args = None
        self.scroll_down_func = None
        self.scroll_down_args = None

    def draw(self):
        mouse = self.game.mouse.get_pos()
        click = self.game.mouse.get_pressed()

        # mouse in button bounds
        if self.bounds.collidepoint(mouse):
            if self.draw_rect:
                self.game.draw.rect(self.display, self.ac, self.bounds)
            # left click
            if click[0] == 1:
                if self.action is not None:
                    if self.args is None:
                        self.action()
                    else:
                        self.action(*self.args)
                # check toggling
                if self.toggleable:
                    self.toggle()
                    self.game.event.wait()
            # check scrolling
            elif self.scrollable:
                event = self.game.event.poll()
                if event.type == self.game.locals.MOUSEBUTTONDOWN or event.type == self.game.locals.MOUSEBUTTONUP:
                    # scroll up
                    if event.button == 4:
                        self.scroll_up_func(*self.scroll_up_args)
                    # scroll down
                    elif event.button == 5:
                        self.scroll_down_func(*self.scroll_down_args)

        elif self.toggleable and self.toggle_val:
            if self.draw_hover:
                self.game.draw.rect(self.display, self.ac, self.bounds)
        elif self.draw_rect:
            self.game.draw.rect(self.display, self.ic, self.bounds)

        # print("toggleable:", self.toggleable, "toggle_val:", self.toggle_val)

        # draw button label
        self.font.set_bold(True)
        text_surf, text_rect = text_objects(self.msg, self.font)
        text_rect.center = ((self.bounds.x + (self.bounds.width / 2)), (self.bounds.y + (self.bounds.height / 2)))
        self.display.blit(text_surf, text_rect)


class ButtonBar(Widget):

    # display a bar of buttons and listen for them to be clicked.
    # game          -   pygame object
    # display       -   display created by pygame
    # x			    -	bar x
    # y			    -	bar y
    # w			    -	bar width
    # h			    -	bar height
    # font          -   button font style
    # bg            -   bar background color
    # proportion    -   proportion of the total bar to consume
    # is_horizontal -   whether the bar is horizontal or vertical
    def __init__(self, game, display, x, y, w, h, font, bg, proportion, is_horizontal=True):
        super().__init__(game, display)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = font if font is not None else game.font.Font(None, 16)
        self.bg = bg
        self.proportion = proportion
        self.is_horizontal = is_horizontal

        self.buttons = {}

    # No need to move buttons within bar, since their placement is calculated in the draw function.
    def move(self, r):
        self.x = r.x
        self.y = r.y

    # No need to resize buttons within bar, since their placement is calculated in the draw function.
    def resize(self, r):
        self.w = r.w
        self.h = r.h

    # Using information, add a button to the bar.
    # msg       -   button name
    # ic        -   button color
    # ac        -   button color when hovering
    # action    -   function to be executed on click
    # args      -   tuple of function args
    def add_button(self, msg, ic, ac, action=None, args=None):
        button = {msg: (ic, ac, action, args)}
        self.buttons.update(button)

    def draw(self):
        nb = len(self.buttons)  # number buttons
        wp = (self.w * self.proportion)  # width proportional
        hp = (self.h * self.proportion)  # height proportional
        xd = self.w - wp  # difference between total width and proportional width
        yd = self.h - hp  # difference between total height and proportional height
        xi = self.x + (xd / 2)  # starting x
        yi = self.y + (yd / 2)  # starting y
        wi = wp / nb if self.is_horizontal else wp  # single button width
        hi = hp / nb if not self.is_horizontal else hp  # single button height

        # draw background
        self.game.draw.rect(self.display, self.bg, (self.x, self.y, self.w, self.h))

        # create and draw buttons
        for b, info in self.buttons.items():
            button = Button(self.game, self.display, b, xi, yi, wi, hi, *info[:2], self.font, *info[2:])
            button.draw()
            if self.is_horizontal:
                xi += (xd / (nb + 1)) + wi
            else:
                yi += (yd / (nb + 1)) + hi


class ScrollBar(Widget):

    def __init__(self, game, display, x, y, w, h, bar_proportion, button_c, bar_background_c, bar_c, contents,
                 content_c, is_vertical=True):
        super().__init__(game, display)
        self.y = y
        self.x = x
        self.w = w
        self.h = h
        self.bar_proportion = bar_proportion
        self.button_c = button_c
        self.bar_background_c = bar_background_c
        self.bar_c = bar_c
        self.contents = [contents] if not isinstance(contents, list) else contents
        self.content_c = content_c
        self.is_vertical = is_vertical

        self.bar_bounds = None
        self.content_bounds = None
        self.widget_bounds = None
        self.set_bounds(x, y, w, h)
        self.bar_val = 0  # 0-100 based on the position of the scroll bar

    def set_bounds(self, x, y, w, h):
        # TODO: adjust content sizes somehow
        if self.is_vertical:
            self.bar_bounds = self.game.Rect(x, y, w * self.bar_proportion, h)
            self.content_bounds = self.game.Rect(x + self.bar_bounds.width, y, w - self.bar_bounds.width, h)
        else:
            self.bar_bounds = self.game.Rect(x, y, w, h * self.bar_proportion)
            self.content_bounds = self.game.Rect(x, y + self.bar_bounds.height, w, h - self.bar_bounds.height)

        self.widget_bounds = self.content_bounds.union(self.bar_bounds)

    def move(self, r):
        self.x = r.x
        self.y = r.y
        self.set_bounds(self.x, self.y, self.w, self.h)

    def resize(self, r):
        self.w = r.width
        self.h = r.height
        self.set_bounds(self.x, self.y, self.w, self.h)

    # Draw an arrow in 1 of 8 directions, denoted by the orientations above.
    # r     -   pygame.Rect object for sizing
    # p     -   float between 0 and 1 for border size around the arrow within the square (0 - 1)
    # o     -   orientation of the arrow using one of the orientations above (0 - 8)
    # c     -   line color of the arrow
    # w     -   line width of the arrow (w >= 1)
    def draw_arrow(self, r, p, o, c, w):
        # p1 - tip
        # p2 - first wing
        # p3 - second wing
        p1x = r.center[0]
        p1y = r.center[1] + (r.height * p)
        p2x = r.center[0] - (r.width * p)
        p2y = r.center[1] - (r.height * p)
        p3x = r.center[0] + (r.width * p)
        p3y = r.center[1] - (r.height * p)
        points = [rotate_point(*r.center, *pt, o * 45) for pt in [(p2x, p2y), (p1x, p1y), (p3x, p3y)]]

        self.game.draw.lines(self.display, c, False, points, w)
        return points

    def get_scroll_pos(self):
        return self.bar_val

    def set_scroll_pos(self, val):
        self.bar_val = val

    def increment_bar_pos(self, n=1):
        if n > 0:
            if self.bar_val < 100:
                self.bar_val += 1
                self.increment_bar_pos(n - 1)

    def decrement_bar_pos(self, n=1):
        if n > 0:
            if self.bar_val > 0:
                self.bar_val -= 1
                self.decrement_bar_pos(n - 1)

    # Using the bar_val attribute, determine where the scroll bar should be positioned on the background.
    def decode_bar_pos(self):
        # TODO: width and height attributes are hardcoded, need to represent the height and width of the contents
        bounds = self.bar_bounds
        if self.is_vertical:
            width = bounds.width * 0.8
            height = 75
            x = bounds.x + (bounds.width * 0.1)
            y = bounds.y + (bounds.height * 0.1) + ((self.bar_val / 100) * ((bounds.height * 0.8) - height))
        else:
            width = 10
            height = bounds.height * 0.8
            y = bounds.y + (bounds.height * 0.1)
            x = bounds.x + (bounds.width * 0.1) + ((self.bar_val / 100) * ((bounds.width * 0.8) - width))

        # print("bar_pos:", self.game.Rect(x, y, width, height))
        return x, y, width, height

    # Using either x or y mouse coordinates, return the position of the top of the scroll bar.
    # Ensures the bar will be encapsulated within the bounds of the scroll area.
    def encode_bar_pos(self, pos):
        bounds = self.bar_bounds
        if self.is_vertical:
            val = min(1, (max(0, pos - bounds.top)) / ((bounds.bottom - bounds.top) * 0.8)) * 100
        else:
            val = min(1, (max(0, pos - bounds.left)) / ((bounds.right - bounds.left) * 0.8)) * 100
        return val

    # Called when the bar is clicked and dragged.
    # Updates the scroll bar's bar_val attribute.
    def move_bar(self):
        mouse_pos = self.game.mouse.get_pos()
        bounds = self.bar_bounds  # self.game.Rect(self.x, self.y, self.w, self.h)
        if bounds.collidepoint(mouse_pos):
            if self.is_vertical:
                button_space = bounds.height * 0.1
                y = mouse_pos[1] - button_space
                val = self.encode_bar_pos(y)
            else:
                button_space = bounds.width * 0.1
                x = mouse_pos[0] - button_space
                val = self.encode_bar_pos(x)
            self.set_scroll_pos(val)

    # content can be nested widgets, strings, pictures..
    def add_contents(self, content):
        self.contents.append(content)
        # TODO needs work, will be nested widgets or generic texts

    def draw(self):
        background = self.bar_bounds  # self.game.Rect(self.x, self.y, self.w, self.h)
        if self.is_vertical:
            space = background.height * 0.1
            bar_background = self.game.Rect(background.x, (background.y + space), background.width,
                                            (background.height - (2 * space)))
            scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
                                    self.bar_background_c, font=None, action=self.move_bar)
            scroll_percent = round((background.height - (2 * space)) * 0.02)
            increment_button_rect = self.game.Rect(background.left, background.top, background.width, space)
            decrement_button_rect = self.game.Rect(background.left, background.bottom - space, background.width, space)
            increment_button_arrow = NORTH
            decrement_button_arrow = SOUTH

            bar_rect = self.game.Rect(*self.decode_bar_pos())
        else:
            space = background.width * 0.1
            bar_background = self.game.Rect(background.x + space, background.y, (background.width - (2 * space)),
                                            background.height)
            scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
                                    self.bar_background_c, font=None, action=self.move_bar)
            scroll_percent = round((background.width - (2 * space)) * 0.02)
            increment_button_rect = self.game.Rect(background.left, background.top, space, background.height)
            decrement_button_rect = self.game.Rect(background.right - space, background.top, space, background.height)
            increment_button_arrow = WEST
            decrement_button_arrow = EAST
            bar_rect = self.game.Rect(*self.decode_bar_pos())

        # enable mouse scrolling for entire widget
        widget_button = buttonr(self.game, self.display, "", self.widget_bounds, self.bar_background_c,
                                self.bar_background_c, font=None, action=None)
        widget_button.enable_scrollable(self.decrement_bar_pos, [scroll_percent], self.increment_bar_pos,
                                        [scroll_percent])
        widget_button.draw()

        # draw scroll background
        scroll_button.draw()

        # draw increment, decrement buttons
        increment_button = Button(self.game, self.display, "", *increment_button_rect, self.button_c, self.button_c,
                                  font=None,
                                  action=self.decrement_bar_pos)
        decrement_button = Button(self.game, self.display, "", *decrement_button_rect, self.button_c, self.button_c,
                                  font=None, action=self.increment_bar_pos)
        increment_button.draw()
        decrement_button.draw()

        # draw increment, decrement arrows
        self.draw_arrow(increment_button_rect, 0.2, increment_button_arrow, BLACK, 3)
        self.draw_arrow(decrement_button_rect, 0.2, decrement_button_arrow, BLACK, 3)

        # draw bar
        self.game.draw.rect(self.display, self.bar_c, bar_rect)

        # draw content background
        self.game.draw.rect(self.display, self.content_c, self.content_bounds)

    # def draw(self):
    #     background = self.game.Rect(self.x, self.y, self.w, self.h)
    #     if self.is_vertical:
    #         space = background.height * 0.1
    #         bar_background = self.game.Rect(self.x, (self.y + space), self.w, (self.h - (2 * space)))
    #         scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
    #                                 self.bar_background_c, font=None, action=self.move_bar)
    #         scroll_percent = round((self.h - (2 * space)) * 0.02)
    #         scroll_button.enable_scrollable(self.decrement_bar_pos, [scroll_percent], self.increment_bar_pos, [scroll_percent])
    #         scroll_button.draw()
    #         top_button_rect = self.game.Rect(background.left, background.top, background.width, space)
    #         bottom_button_rect = self.game.Rect(background.left, background.bottom - space, background.width, space)
    #         top_button = Button(self.game, self.display, "", *top_button_rect, self.button_c, self.button_c, font=None,
    #                             action=self.decrement_bar_pos)
    #         bottom_button = Button(self.game, self.display, "", *bottom_button_rect, self.button_c, self.button_c,
    #                                font=None, action=self.increment_bar_pos)
    #         top_button.draw()
    #         bottom_button.draw()
    #         # self.game.draw.rect(self.display, self.button_c, top_button_rect)
    #         # self.game.draw.rect(self.display, self.button_c, bottom_button_rect)
    #         # down arrow - left side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (bottom_button_rect.left + (bottom_button_rect.width * 0.2)),
    #                                 (bottom_button_rect.top + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 bottom_button_rect.center[0],
    #                                 (bottom_button_rect.center[1] + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # down arrow - right side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (bottom_button_rect.right - (bottom_button_rect.width * 0.2)),
    #                                 (bottom_button_rect.top + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 bottom_button_rect.center[0],
    #                                 (bottom_button_rect.center[1] + (bottom_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # up arrow - left side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (top_button_rect.left + (top_button_rect.width * 0.2)),
    #                                 (top_button_rect.bottom - (top_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 top_button_rect.center[0],
    #                                 (top_button_rect.center[1] - (top_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # up arrow - right side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (top_button_rect.right - (top_button_rect.width * 0.2)),
    #                                 (top_button_rect.bottom - (top_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 top_button_rect.center[0],
    #                                 (top_button_rect.center[1] - (top_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         bar_rect = self.game.Rect(*self.decode_bar_pos())
    #     else:
    #         space = background.width * 0.1
    #         bar_background = self.game.Rect(self.x + space, self.y, (self.w - (2 * space)), self.h)
    #         scroll_button = buttonr(self.game, self.display, "", bar_background, self.bar_background_c,
    #                                 self.bar_background_c, font=None, action=self.move_bar)
    #         scroll_percent = round((self.w - (2 * space)) * 0.02)
    #         scroll_button.enable_scrollable(self.decrement_bar_pos, [scroll_percent], self.increment_bar_pos, [scroll_percent])
    #         scroll_button.draw()
    #         left_button_rect = self.game.Rect(background.left, background.top, space, background.height)
    #         right_button_rect = self.game.Rect(background.right - space, background.top, space, background.height)
    #         left_button = Button(self.game, self.display, "", *left_button_rect, self.button_c, self.button_c,
    #                              font=None,
    #                              action=self.decrement_bar_pos)
    #         right_button = Button(self.game, self.display, "", *right_button_rect, self.button_c, self.button_c,
    #                               font=None,
    #                               action=self.increment_bar_pos)
    #         left_button.draw()
    #         right_button.draw()
    #
    #         # self.game.draw.rect(self.display, self.button_c, left_button_rect)
    #         # self.game.draw.rect(self.display, self.button_c, right_button_rect)
    #         # right arrow - top side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (right_button_rect.left + (right_button_rect.width * 0.2)),
    #                                 (right_button_rect.top + (right_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 (right_button_rect.center[0] + (right_button_rect.width * 0.2)),
    #                                 right_button_rect.center[1]
    #                             ),
    #                             3)
    #         # right arrow - bottom side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (right_button_rect.center[0] + (right_button_rect.width * 0.2)),
    #                                 right_button_rect.center[1]
    #                             ),
    #                             (
    #                                 (right_button_rect.left + (right_button_rect.width * 0.2)),
    #                                 (right_button_rect.bottom - (right_button_rect.height * 0.2))
    #                             ),
    #                             3)
    #         # left arrow - top side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (left_button_rect.right - (left_button_rect.width * 0.2)),
    #                                 (left_button_rect.top + (left_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 (left_button_rect.center[0] - (left_button_rect.width * 0.2)),
    #                                 left_button_rect.center[1]
    #                             ),
    #                             3)
    #         # left arrow - bottom side
    #         self.game.draw.line(self.display, BLACK,
    #                             (
    #                                 (left_button_rect.right - (left_button_rect.width * 0.2)),
    #                                 (left_button_rect.bottom - (left_button_rect.height * 0.2))
    #                             ),
    #                             (
    #                                 (left_button_rect.center[0] - (left_button_rect.width * 0.2)),
    #                                 left_button_rect.center[1]
    #                             ),
    #                             3)
    #         bar_rect = self.game.Rect(*self.decode_bar_pos())
    #     self.game.draw.rect(self.display, self.bar_c, bar_rect)


class TableRow(Widget):

    def __init__(self, game, display):
        super().__init__(game, display)

        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.bounds = None
        self.contents = []
        self.cols = len(self.contents)
        self.div_c = BLACK
        self.div_w = 3
        self.c = WHITE
        self.tx_c = BLACK
        self.font = game.font.Font(None, 16)

    def set_row_font(self, f):
        self.font = f

    def set_row_color(self, c):
        self.c = c

    def set_divider_color(self, c):
        self.div_c = c

    def set_divider_width(self, w):
        self.div_w = w

    def set_text_color(self, c):
        self.tx_c = c

    def update_bounds(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.bounds = self.game.Rect(x, y, w, h)

    # Insert either a single cell of data to the row, or a list of data points for the row of cells.
    def add_content(self, content):
        if isinstance(content, list):
            for c in content:
                self.contents.append(c)
        else:
            self.contents.append(content)
        self.cols = len(self.contents)

    # Get the cell data from row's contents at index col.
    def get_data(self, col):
        data = None
        if -1 < col < self.cols:
            data = self.contents[col]
        return data

    def move(self, r):
        self.update_bounds(r.x, r.y, self.width, self.height)

    def resize(self, r):
        self.update_bounds(self.x, self.y, r.width, r.height)

    def draw(self):
        bounds = self.bounds
        n_dividers = max(1, self.cols)
        divider_space = (bounds.width / n_dividers)
        xi = bounds.left
        for i in range(n_dividers + 1):
            if i < self.cols:
                cell_bounds = self.game.Rect(xi, bounds.y, divider_space, bounds.h)
                # cell_surface, cell_rect = text_objects(self.contents[i], self.font)
                write_text(self.game, self.display, cell_bounds, self.contents[i], self.font, self.c, self.tx_c)
                # center text within cell TODO : add option for gravity and orientation
                # cell_rect.center = (
                #     (cell_bounds.x + (cell_bounds.width / 2)), (cell_bounds.y + (cell_bounds.height / 2))
                # )
                # self.game.draw.rect(self.display, self.c, cell_bounds)
                # self.display.blit(cell_surface, cell_rect)

            self.game.draw.line(self.display, self.div_c, (xi, bounds.top), (xi, bounds.bottom), self.div_w)
            xi += divider_space


class Table(Widget):

    # Create a generic table with a title and header.
    def __init__(self, game, display, x, y, w, h, c, font, title, header):
        super().__init__(game, display)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.c = c
        self.font = font if font is not None else game.font.Font(None, 16)
        self.title = title.title()
        self.header = header

        self.title_color = BLACK
        self.div_c = BLACK
        self.div_w = 3

        self.bounds = self.game.Rect(x, y, w, h)
        self.table_rows = []

        self.set_header(header)

    # Return a TableRow object from index r.
    def get_row(self, r):
        row = None
        if -1 < r < len(self.table_rows):
            row = self.table_rows[r]
        return row

    # Return a list of all column data using a header value.
    def get_col_data(self, c_name):
        h = list(map(str.lower, self.header))
        if c_name.lower() in h:
            idx = self.header.index(c_name)
            return self.get_col(idx)
        return []

    def get_col(self, c_index):
        return [row.contents[c_index] for row in self.table_rows if c_index < row.cols][1:]

    # Get the cell data from row r and col c.
    def get_data(self, r, c):
        row = self.get_row(r)
        if row is not None:
            return row.get_data(c)

    def set_title_color(self, c):
        self.title_color = c
        header_row = self.table_rows[0]
        header_row.set_row_color(self.c)
        header_row.set_text_color(self.title_color)

    def set_table_color(self, c):
        self.c = c

    def set_divider_color(self, c):
        self.div_c = c

    def set_divider_width(self, w):
        self.div_w = w

    def set_title(self, t):
        self.title = t

    def set_header(self, h):
        self.header = h
        header_row = TableRow(self.game, self.display)
        header_row.add_content(list(map(str.title, map(str, h))))
        if len(self.table_rows) > 0:
            self.table_rows = self.table_rows[1:]
        self.add_row(header_row, 0)

    def set_font(self, f):
        self.font = f

    def move(self, r):
        self.x = r.x
        self.y = r.y
        self.bounds = self.game.Rect(self.x, self.y, self.width, self.height)
        for row in self.table_rows:
            row.move(r)
        self.update_row_sizes()

    def resize(self, r):
        # def resize(self, r):
        #     self.width = r.width
        #     self.height = r.height
        #     self.bounds = self.game.Rect(self.x, self.y, self.width, self.height)
        #     self.update_row_sizes()
        #     th = r.height
        #     nr = len(self.table_rows)
        #     rh = round((th / nr) + self.div_w)
        #     y = 0
        #     for row in self.table_rows:
        #         row_r = self.game.Rect(self.x, y, self.width, rh)
        #         row.resize(row_r)
        #         y += rh
        self.width = r.width
        self.height = r.height
        self.bounds = self.game.Rect(self.x, self.y, self.width, self.height)
        for row in self.table_rows:
            row.resize(r)
        self.update_row_sizes()

    # Append a TableRow object to the end of the list, or insert it at given index.
    def add_row(self, table_row, index=None):
        if not isinstance(table_row, TableRow):
            tr = TableRow(self.game, self.display)
            tr.add_content(list(map(str, table_row)))
            tr.set_divider_color(self.div_c)
            table_row = tr
        if index:
            self.table_rows.insert(index, table_row)
        else:
            self.table_rows.append(table_row)
        self.update_row_sizes()

    # When the table is re-sized or a row is added, need to update the sizes of all rows.
    def update_row_sizes(self):
        rows = len(self.table_rows)
        title_height = self.bounds.height * 0.1
        space_left = self.bounds.height - title_height
        row_height = space_left / rows
        for i, row in enumerate(self.table_rows):
            x = self.bounds.x
            y = self.bounds.top + title_height + (row_height * i) + round((row.div_w * i) / 2)
            w = self.bounds.width
            h = row_height
            new_bounds = self.game.Rect(x, y, w, h)
            row.update_bounds(*new_bounds)

    # Add a single TableRow, a list of TableRows, a dict of data, or a list of contents to make TableRows.
    # Using a dict, each key becomes a column, and their values become rows
    def add_rows(self, *table_rows):
        for row in table_rows:
            if isinstance(row, list):
                for el in row:
                    self.add_row(el)
            elif isinstance(row, dict):
                self.set_header(list(row.keys()))
                m = max([len(v) for v in row.values()])
                for i in range(m):
                    data = []
                    for k in row:
                        if len(row[k]) > i:
                            data.append(row[k][i])
                        else:
                            data.append("")
                    self.add_row(data)
            else:
                self.add_row(row)

    def draw(self):
        # draw background
        self.game.draw.rect(self.display, self.c, self.bounds)
        # draw border lines
        self.game.draw.line(self.display, self.div_c, self.bounds.topleft, self.bounds.topright, self.div_w)
        self.game.draw.line(self.display, self.div_c, self.bounds.topleft, self.bounds.bottomleft, self.div_w)
        self.game.draw.line(self.display, self.div_c, self.bounds.topright, self.bounds.bottomright, self.div_w)
        self.game.draw.line(self.display, self.div_c, self.bounds.bottomleft, self.bounds.bottomright, self.div_w)

        # draw title
        title_surface, title_rect = text_objects(self.title, self.font, self.title_color)
        title_rect.center = ((self.x + (self.width / 2)), (self.y + (self.height * 0.05)))
        self.display.blit(title_surface, title_rect)

        # draw each row
        for i, row in enumerate(self.table_rows):
            row.draw()
            bounds = row.bounds
            # draw top border
            if i == 0:
                self.game.draw.line(self.display, row.div_c, bounds.topleft, bounds.topright, row.div_w)
            # draw bottom border
            self.game.draw.line(self.display, row.div_c, bounds.bottomleft, bounds.bottomright, row.div_w)


class Box(Widget):

    def __init__(self, game, display, contents, r, p, bgc, is_horizontal=True):
        super().__init__(game, display)
        self.bounds = r
        self.contents = [] if contents is None else contents
        self.proportion = p
        self.bgc = bgc
        self.is_horizontal = is_horizontal

    def add_contents(self, *contents):
        for content in contents:
            self.contents.append(content)

    def move(self, r):
        self.bounds.x = r.x
        self.bounds.y = r.y

    def resize(self, r):
        self.bounds.width = r.width
        self.bounds.height = r.height

    def draw(self):
        nw = len(self.contents)  # number widgets
        wp = (self.bounds.width * self.proportion)  # width proportional
        hp = (self.bounds.height * self.proportion)  # height proportional
        xd = self.bounds.width - wp  # difference between total width and proportional width
        yd = self.bounds.height - hp  # difference between total height and proportional height
        xi = self.bounds.x + (xd / 2)  # starting x
        yi = self.bounds.y + (yd / 2)  # starting y
        wi = wp / max(1, nw) if self.is_horizontal else wp  # single widget width
        hi = hp / max(1, nw) if not self.is_horizontal else hp  # single widget height

        # draw background
        if self.bgc is not None:
            self.game.draw.rect(self.display, self.bgc, self.bounds)

        # update bounds and draw widgets
        for i, widget in enumerate(self.contents):
            new_bounds = self.game.Rect(xi, yi, wi, hi)
            widget.move(new_bounds)
            if isinstance(RadioGroup, widget):
                widget.resize(new_bounds, self.is_horizontal)
            else:
                widget.resize(new_bounds)
            widget.draw()
            # button = Button(self.game, self.display, b, xi, yi, wi, hi, *info[:2], self.font, *info[2:])
            # button.draw()
            if self.is_horizontal:
                xi += (xd / (nw + 1)) + wi
            else:
                yi += (yd / (nw + 1)) + hi


class VBox(Box):

    # Create a vertical content box, which contains widgets.
    # All widget contents are sized to fit inside box bounds.
    def __init__(self, game, display, contents, r, p, bgc):
        super().__init__(game, display, contents, r, p, bgc, is_horizontal=False)


class HBox(Box):

    # Create a horizontal content box, which contains widgets.
    # All widget contents are sized to fit inside box bounds.
    def __init__(self, game, display, contents, r, p, bgc):
        super().__init__(game, display, contents, r, p, bgc, is_horizontal=True)

# buttons & toggle buttons
# button bar
# scrollable bar TODO: allow a scroll bar on both the vertical and horizontal axes.
# Table rows & cols
# Radio Buttons and groups

# VBox & HBox
# clock
# text area
# text input
# image button
# hyperlink
# combobox
