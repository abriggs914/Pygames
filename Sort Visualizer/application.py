import pygame
from pygame.locals import *

# Generic bolier-plate code for starting a pygame application
# https://pygame.readthedocs.io/en/latest/5_app/app.html

class Scene:
    """Create a new scene (room, level, view)."""
    id = 0
    bg = Color('gray')

    def __init__(self, *args, **kwargs):
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

    def __str__(self):
        return 'Scene {}'.format(self.id)

class Text:
    """Create a text object."""

    def __init__(self, text, pos, **options):
        self.text = text
        self.pos = pos

        self.fontname = None
        self.fontsize = 72
        self.fontcolor = Color('black')
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()

        w, h = self.rect.size
        w0, h0 = self.text_img.get_size()

        if self.h_align == 0:
            x = 0
        elif self.h_align == 1:
            x = (w - w0) // 2
        else:
            x = w - w0

        if self.v_align == 0:
            y = 0
        elif self.v_align == 1:
            y = (h - h0) // 2
        else:
            y = h - h0

        self.img0.blit(self.text_img, (x, y))
        self.img = self.img0.copy()

        self.rect.topleft = self.pos

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        App.screen = pygame.display.set_mode((640, 240), flags)
        App.t = Text('Pygame App', pos=(20, 20))

        App.running = True
        App.scenes = []
        App.scene = None

    def add_scene(self, scene):
        App.scenes.append(scene)

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

            if App.scene:
                App.scene.draw()
            # App.screen.fill(Color('gray'))
            # App.t.draw()
            pygame.display.update()

        pygame.quit()

# if __name__ == '__main__':
#     App().run()

class Demo(App):
    def __init__(self):
        super().__init__()

        s1 = Scene(caption='Intro')
        s1.add(Text('Scene 0', (0, 0)))
        s1.add(Text('Introduction screen the app', (0, 75)))

        s2 = Scene(bg=Color('yellow'), caption='Options')
        s2.add(Text('Scene 1', (0, 0)))
        s2.add(Text('Option screen of the app', (0, 75)))

        s3 = Scene(bg=Color('green'), caption='Main')
        s3.add(Text('Scene 2', (0, 0)))
        s3.add(Text('Main screen of the app', (0, 75)))

        self.add_scene(s1)
        self.add_scene(s2)
        self.add_scene(s3)
        App.scene = App.scenes[1]


if __name__ == '__main__':
    Demo().run()
