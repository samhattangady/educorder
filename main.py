from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line


class EducorderRectangle(Widget):

    def __init__(self, touch_down, touch_up):
        self.x = touch_down[0]
        self.y = touch_down[1]
        self.rect_width = touch_up[0] - touch_down[0]
        self.rect_height = touch_up[1] - touch_down[1]

    def draw_shape(self):
        Color(0, 1, 0)
        Line(rectangle=(self.x, self.y, self.rect_width, self.rect_height))


class EducorderCanvas(Widget):
    shapes = ListProperty()

    def on_touch_down(self, touch):
        self.touch_down = touch.pos

    def on_touch_up(self, touch):
        self.touch_up = touch.pos
        self.shapes.append(EducorderRectangle(self.touch_down, self.touch_up))
        if len(self.shapes) > 3:
            self.shapes.pop(0)
        self.prepare_canvas()

    def prepare_canvas(self):
        with self.canvas:
            self.clear_widgets()  # Does not work. Figure out how to clear canvas
            for shape in self.shapes:
                shape.draw_shape()


class EducorderBase(Widget):

    def create_canvas(self):
        EducorderCanvas()



class EducorderApp(App):
    def build(self):
        base = EducorderCanvas()
        #base.create_canvas()
        return base


if __name__ == '__main__':
    EducorderApp().run()