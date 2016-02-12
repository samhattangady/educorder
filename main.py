#!/usr/bin/python

from kivy.app import App
from kivy.properties import ListProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line, Ellipse

RED = (1, 0, 0)
WHITE = (1, 1, 1)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)


class EduShape(Widget):
    """
        All drawable shapes will be of this type. It is assumed that they all
        have bounding boxes and behave in the same way.
        They have x,y positions as well as width,height properties.
        They also have a line and fill colour, though those functions dont
        work right now.
    """

    def __init__(self, touch_down, touch_up, line_colour, fill_colour):
        # Initializing
        super(EduShape, self).__init__()
        self.x = touch_down[0]
        self.y = touch_down[1]
        self.width = touch_up[0] - touch_down[0]
        self.height = touch_up[1] - touch_down[1]
        self.selected = True
        self.line = line_colour  # Colour or False if none
        self.fill = fill_colour  # Colour or False if none

    '''def collide_point(self, x, y):
        # Wasn't sure that the method worked correctly,
        # so just wrote one to make sure
        return (x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height)'''


class EducorderRectangle(EduShape):
    """
        Basic Rectangle Shape
    """

    def draw_shape(self):
        # Draws rectangle based on line and fill colours
        # Doesn't work right now, so we're just using hardcoded colours for now
        if self.fill:
            Color(1, 0, 0)
            Rectangle(pos=(self.x, self.y), size=(self.width, self.height))
        if self.line:
            Color(0, 0, 0)
            Line(rectangle=(self.x, self.y, self.width, self.height))
        if self.selected:
            Color(0, 0, 0)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=5)


class EducorderEllipse(EduShape):
    """
        Basic Ellipse Shape
    """

    def draw_shape(self):
        # Draws ellipse based on line and fill colours
        if self.fill:
            Color(1, 0, 0)
            Ellipse(pos=(self.x, self.y), size=(self.width, self.height))
        if self.line:
            Color(0, 0, 0)
            Line(ellipse=(self.x, self.y, self.width, self.height))
        if self.selected:
            # Maybe put the shape changing circles in here
            pass

class ReshapeShapes(Widget):
    """
        The small circles in the corners that you drag
    """

class EducorderCanvas(Widget):
    """
        Main canvas on which all the shapes are drawn.
        It also handles all the inputs, and mode changes etc.
    """

    def __init__(self, **kwargs):
        super(EducorderCanvas, self).__init__()
        # This list holds all the shapes that are drawn on the canvas
        self.shapes = []

        self.touch_down = None
        self.touch_up = None

        # Default colour values
        self.line_colour = RED
        self.fill_colour = RED

        # All the possible modes will be here
        self.drawing_mode = True

        self.drawing_shape = 'Rectangle'

        # Drawing the canvas to start off
        with self.canvas:
            Rectangle(size=(self.width, self.height))

    def on_touch_down(self, touch):
        # We always want to store every click
        # Only draw if it is within the bounds of
        self.touch_down = touch.pos
        self.drawing_mode = self.check_touch_in_bounds(touch)  # will need to be changed later as more modes are added

    def on_touch_move(self, touch):
        # To draw the shape as it is being drawn
        self.draw_canvas()
        if self.check_touch_in_bounds(touch):
            with self.canvas:
                self.current_shape(touch.pos).draw_shape()


    def on_touch_up(self, touch):
        # Save the release position of mouse
        # Only draw if both down and up are within bounds
        # Maybe also add functionality so that if shape is dragged out of bounds, it is drawn till the bounds
        self.draw_canvas()
        self.touch_up = touch.pos
        if self.drawing_mode:
            self.drawing_mode = self.check_touch_in_bounds(touch)
            if self.drawing_mode and not self.click_on_spot():
                self.create_shape()

        if self.click_on_spot():
            if self.check_touch_in_bounds(touch):
                self.select_clicked_on(touch)

    def select_clicked_on(self, touch):
        # Meant to select whichever shape was clicked on.
        self.deselect_all()
        for shape in reversed(self.shapes):
            if shape.collide_point(touch.x, touch.y):
                shape.selected = True
                break

    def check_touch_in_bounds(self, touch):
        # Returns whether the position was in bounds of the canvas
        return not (touch.x > self.width or touch.x < 0 or touch.y > self.height or touch.y < 0)

    def click_on_spot(self):
        # Can calculate distance by using pythagoras theorem
        # But I think, for this purpose just returning the greater
        # of dx and dy will be sufficient
        def distance(point1, point2):
            return max(abs(point1[0] - point2[0]),
                       abs(point1[1] - point2[1]))

        return distance(self.touch_down, self.touch_up) < 5

    def deselect_all(self):
        # Deselects all the shapes
        for shape in self.shapes:
            shape.selected = False

    def create_shape(self):
        # Adds the shape to shapes[]
        self.shapes.append(self.current_shape(self.touch_up))
        self.deselect_all()
        self.shapes[-1].selected = True
        self.draw_canvas()

    def current_shape(self, touch):
        # Returns the shape being currently drawn
        if self.drawing_shape == 'Rectangle':
            return EducorderRectangle(self.touch_down, touch,
                                      self.line_colour, self.fill_colour)
        elif self.drawing_shape == 'Ellipse':
            return EducorderEllipse(self.touch_down, touch,
                                    self.line_colour, self.fill_colour)


    def draw_canvas(self):
        # Draws all the shapes in shapes
        with self.canvas:
            self.canvas.clear()
            Rectangle(size=(self.width, self.height))
            for shape in self.shapes:
                shape.draw_shape()


class EducorderApp(App):
    def out_line_toggle(self, obj):
        if self.main_canvas.line_colour:
            self.main_canvas.line_colour = False
        else:
            self.main_canvas.line_colour = RED
        self.main_canvas.draw_canvas()

    def fill_in_toggle(self, obj):
        if self.main_canvas.fill_colour:
            self.main_canvas.fill_colour = False
        else:
            self.main_canvas.fill_colour = RED
        self.main_canvas.draw_canvas()

    def move_to_right(self, obj):
        for shape in self.main_canvas.shapes:
            if shape.selected:
                shape.x += 5
        self.main_canvas.draw_canvas()

    def change_shape(self, obj):
        if self.main_canvas.drawing_shape == 'Rectangle':
            self.main_canvas.drawing_shape = 'Ellipse'
        elif self.main_canvas.drawing_shape == 'Ellipse':
            self.main_canvas.drawing_shape = 'Rectangle'

    def build(self):
        self.main_canvas = EducorderCanvas()

        button1 = Button(text='Right')
        button1.bind(on_release=self.move_to_right)

        button2 = Button(text='Shape')
        button2.bind(on_release=self.change_shape)

        button3 = Button(text='Fill')
        button3.bind(on_release=self.fill_in_toggle)

        button4 = Button(text='Line')
        button4.bind(on_release=self.out_line_toggle)

        buttons = BoxLayout(orientation='horizontal')
        buttons.add_widget(button1)
        buttons.add_widget(button2)
        buttons.add_widget(button3)
        buttons.add_widget(button4)

        root = BoxLayout(orientation='vertical')
        root.add_widget(buttons)
        root.add_widget(self.main_canvas)

        return root


if __name__ == '__main__':
    EducorderApp().run()
