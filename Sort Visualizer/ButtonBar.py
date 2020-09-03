from widgets import Widget

# def button_bar(self, display, txts, x, y, w, h, i_colors, a_colors, font, is_horizontal=True, actions=()):
#     buttons = dict(zip(txts, zip(i_colors, a_colors, actions)))
#     button_list = []
#     nb = len(buttons)
#     wp = (w * 0.95)
#     hp = (h * 0.95)
#     xd = w - wp
#     yd = h - hp
#     xi = x
#     yi = y
#     wi = wp / nb if is_horizontal else wp
#     hi = hp / nb if not is_horizontal else hp
#     print("num:", nb, "tot w:", wp, "tot h:", hp, "x_left:", xd, "y_left:", yd)
#     print("\txi:", xi, "yi:", yi, "wi:", wi, "hi:", hi)
#     for b, info in buttons.items():
#         if is_horizontal:
#             xi += (xd / nb) + wi
#         else:
#             yi += (yd / nb) + hi
#         r = self.game.Rect(xi, yi, wi, hi)
#         print("Rect:", r)
#         self.button(display, b, xi, yi, wi, hi, *info[:2], font, info[-1])



class button_bar:

    def __init__(self, display, x, y, w, h, is_horizontal=True):
        self.display = display
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_horizontal = is_horizontal

        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self):
        nb = len(self.buttons)
        wp = (w * 0.95)
        hp = (h * 0.95)
        xd = w - wp
        yd = h - hp
        xi = x
        yi = y
        wi = wp / nb if self.is_horizontal else wp
        hi = hp / nb if not self.is_horizontal else hp
        print("num:", nb, "tot w:", wp, "tot h:", hp, "x_left:", xd, "y_left:", yd)
        print("\txi:", xi, "yi:", yi, "wi:", wi, "hi:", hi)
        for b, info in self.buttons.items():
            if is_horizontal:
                xi += (xd / nb) + wi
            else:
                yi += (yd / nb) + hi
            r = self.game.Rect(xi, yi, wi, hi)
            print("Rect:", r)
            self.button(display, b, xi, yi, wi, hi, *info[:2], font, info[-1])


    buttons = dict(zip(txts, zip(i_colors, a_colors, actions)))
    button_list = []