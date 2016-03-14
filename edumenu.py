from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle



class Canvas_Menu(Widget):
    """
        Menu that opens on right click in canvas area.
        It will have all the cut, copy, change color, order etc. options
    """

    def __init__(self, touch, shapes):
        self.x = touch.x
        self.y = touch.y
        self.shapes = shapes
        self.width = 200
        self.height = 300
        self.label = Label(text='foo')

    def clicked_on(self, touch):
        x = touch.x
        y = touch.y

        return (self.x <= x <= self.x + self.width) \
            and (self.y <= y <= self.y + self.height)

    def draw_menu(self):
        Color(0, 0, 0, .2)
        Rectangle(pos=(self.x-3, self.y-3), size=(self.width+6, self.height+6))
        Color(1, 1, 1)
        Rectangle(pos=(self.x, self.y), size=(self.width, self.height))
        self.label = Label(text='foo', pos=(self.x, self.y), color=(0, 0, 0))