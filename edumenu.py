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

    def clicked_on(self, touch):
        x = touch.x
        y = touch.y

        return (self.x <= x <= self.x + self.width) \
            and (self.y <= y <= self.y + self.height)

    def draw_menu(self):
        Color(1, 1, 0)
        Rectangle(pos=(self.x, self.y), size=(self.width, self.height))
        Color(0,0,0)
        Label(text='Hi')




