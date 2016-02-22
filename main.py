#!/usr/bin/python

from kivy.app import App
from kivy.properties import ListProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line, Ellipse

# Declaring some constant colours. Not working right
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

        self.reallign_shape()

        self.selected = False
        self.line = line_colour  # Colour or False if none
        self.fill = fill_colour  # Colour or False if none

        self.reshape_circles = ReshapeCirclesParent(self)

    def clicked_on(self, x, y):
        # collide_point() doesn't seem to work correctly,
        # so wrote a function specifically
        return (self.x < x < self.x + self.width) \
            and (self.y < y < self.y + self.height)

    def reallign_shape(self):
        # The operations are to make sure that heights and widths
        # are positive, to make further operations simpler
        if self.width < 0:
            self.width = abs(self.width)
            self.x -= self.width
        if self.height < 0:
            self.height = abs(self.height)
            self.y -= self.height

    def move_shape(self, touch):
        # Temporary. Moves shape by center rather than point on which was clicked
        self.x = touch.x - self.width/2
        self.y = touch.y - self.height/2
        self.reshape_circles = ReshapeCirclesParent(self)

    def reshape(self, touch, circle_index):

        def reshape_right():
            self.width = touch.x - self.x

        def reshape_left():
            self.width += self.x - touch.x
            self.x = touch.x

        def reshape_top():
            self.height = touch.y - self.y

        def reshape_bottom():
            self.height += self.y - touch.y
            self.y = touch.y

        if circle_index == 1:       # Bottom Left Corner
            reshape_bottom()
            reshape_left()

        elif circle_index == 2:     # Bottom Right Corner
            reshape_bottom()
            reshape_right()

        elif circle_index == 3:     # Top Right Corner
            reshape_top()
            reshape_right()

        elif circle_index == 4:     # Top Left Corner
            reshape_top()
            reshape_left()

        elif circle_index == 5:     # Bottom Side
            reshape_bottom()

        elif circle_index == 6:     # Right Side
            reshape_right()

        elif circle_index == 7:     # Top Side
            reshape_top()

        elif circle_index == 8:     # Left Side
            reshape_left()

        self.reshape_circles = ReshapeCirclesParent(self)


class EducorderSelectionRectangle(EduShape):
    """
        Selection Box
    """

    def draw_shape(self):
        # Draws rectangle based on line and fill colours
        # Doesn't work right now, so we're just using hardcoded colours for now
            Color(0, 0, 0)
            Line(rectangle=(self.x, self.y, self.width, self.height), dash_offset=2, dash_length=4)


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
            self.reshape_circles.reshape_draw()


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


class ReshapeCirclesParent(Widget):
    """
        The small circles in the corners that you drag
    """
    def __init__(self, eduShape):
        self.dia = 10
        self.width = eduShape.width
        self.height = eduShape.height
        self.shape = eduShape

        # List to hold all the circles
        # 0 - Off Screen, because we will use index of this list as an if condition,
        #  and 0 will be false value
        # 1 - Bottom Left Corner
        # 2 - Bottom Right Corner
        # 3 - Top Right Corner
        # 4 - Top Left Corner
        # 5 - Bottom Side
        # 6 - Right Side
        # 7 - Top Side
        # 8 - Left Side

        self.circles = [ReshapeCircles(-5, -5, 3)]
        # Corners
        self.circles.append(ReshapeCircles(self.shape.x-(self.dia/2), self.shape.y-(self.dia/2), self.dia))
        self.circles.append(ReshapeCircles((self.shape.x + self.shape.width)-(self.dia/2), self.shape.y-(self.dia/2),
                                           self.dia))
        self.circles.append(ReshapeCircles((self.shape.x + self.shape.width)-(self.dia/2),
                                           (self.shape.y + self.shape.height)-(self.dia/2), self.dia))
        self.circles.append(ReshapeCircles(self.shape.x-(self.dia/2), (self.shape.y + self.shape.height)-(self.dia/2),
                                           self.dia))
        # Sides
        self.circles.append(ReshapeCircles(self.shape.x+(self.shape.width/2)-(self.dia/2), self.shape.y-(self.dia/2),
                                           self.dia))
        self.circles.append(ReshapeCircles((self.shape.x+self.shape.width)-(self.dia/2),
                                           self.shape.y+(self.shape.height/2)-(self.dia/2), self.dia))
        self.circles.append(ReshapeCircles(self.shape.x+(self.shape.width/2)-(self.dia/2),
                                           self.shape.y+self.height-(self.dia/2), self.dia))
        self.circles.append(ReshapeCircles(self.shape.x-(self.dia/2), self.shape.y+(self.shape.height/2)-(self.dia/2),
                                           self. dia))

    def reshape_draw(self):
        for circle in self.circles:
            circle.draw_reshape_circle()


class ReshapeCircles(EduShape):
    """
    The individual circles will need to be widgets so its easy to
    detect clicks on them
    """
    def __init__(self, x, y, dia):
        self.x = x
        self.y = y
        self.dia = dia
        self.width = dia
        self.height = dia

    def draw_reshape_circle(self):
        Color(1, 1, 1)
        Ellipse(pos=(self.x, self.y), size=(self.dia, self.dia))
        Color(0, 0, 0)
        Line(ellipse=(self.x, self.y, self.dia, self.dia))


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
        self.modes = {0: 'Standard', 1: 'Rectangle', 2: 'Ellipse'}
        self.selected_mode = 0
        self.reshaping = False

        # Drawing the canvas to start off
        self.draw_canvas()
        self.draw_canvas()

    def on_touch_down(self, touch):
        # We always want to store every click
        # Only draw if it is within the bounds of
        self.touch_down = touch.pos
        self.draw_canvas()
        if self.selected_mode:
            if self.check_touch_in_bounds(touch):
                self.deselect_all()
                self.draw_canvas()

        else:
            if self.check_touch_in_bounds(touch):
                self.select_clicked_on(touch)
                for shape in self.shapes:
                    if shape.selected:
                        for circle in shape.reshape_circles.circles:
                            if circle.clicked_on(touch.x, touch.y):
                                self.reshaping = shape.reshape_circles.circles.index(circle)

    def on_touch_move(self, touch):
        # To draw the shape as it is being drawn
        self.draw_canvas()
        if self.selected_mode:
            if self.check_touch_in_bounds(touch):
                with self.canvas:
                    self.current_shape(touch.pos).draw_shape()

        else:
            # To move/reshape the selected shape
            if self.any_selected():
                if self.reshaping:  # Reshaping code
                    for shape in self.shapes:
                        if shape.selected:
                            shape.reshape(touch, self.reshaping)

                else:  # Moving shape code
                    for shape in self.shapes:
                        if shape.selected:
                            shape.move_shape(touch)

            # To draw selection box
            else:
                if self.check_touch_in_bounds(touch):
                    with self.canvas:
                        self.current_shape(touch.pos).draw_shape()

    def on_touch_up(self, touch):
        # Save the release position of mouse
        # Only draw if both down and up are within bounds
        # Maybe also add functionality so that if shape is dragged out of bounds, it is drawn till the bounds
        self.draw_canvas()
        self.touch_up = touch.pos
        if self.selected_mode:
            if self.check_touch_in_bounds(touch) and not self.click_on_spot():
                self.create_shape()

        else:       # Selection box code
            if not self.any_selected():
                selection_x = self.touch_down[0]
                selection_y = self.touch_down[1]
                selection_width = self.touch_up[0] - self.touch_down[0]
                selection_height = self.touch_up[1] - self.touch_down[1]

                if selection_width < 0:
                    selection_width = abs(selection_width)
                    selection_x -= selection_width
                if selection_height < 0:
                    selection_height = abs(selection_height)
                    selection_y -= selection_height

                for shape in self.shapes:
                    if self.shape_in_selection(shape, selection_x, selection_y, selection_width, selection_height):
                        shape.selected = True
                self.draw_canvas()


        if self.click_on_spot():
            if self.check_touch_in_bounds(touch):
                self.selected_mode = 0
                self.select_clicked_on(touch)

        if self.reshaping:
            self.reshaping = False
            for shape in self.shapes:
                if shape.selected:
                    shape.reallign_shape()
                    shape.reshape_circles = ReshapeCirclesParent(shape)


    def select_clicked_on(self, touch):
        # Meant to select whichever shape was clicked on.
        self.deselect_all()
        for shape in reversed(self.shapes):
            if shape.clicked_on(touch.x, touch.y):
                shape.selected = True
                self.draw_canvas()
                return

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
        if self.modes[self.selected_mode] == 'Rectangle':
            return EducorderRectangle(self.touch_down, touch,
                                      self.line_colour, self.fill_colour)
        elif self.modes[self.selected_mode] == 'Ellipse':
            return EducorderEllipse(self.touch_down, touch,
                                    self.line_colour, self.fill_colour)
        elif self.modes[self.selected_mode] == 'Standard':
            return EducorderSelectionRectangle(self.touch_down, touch, None, None)

    def draw_canvas(self):
        # Draws all the shapes in shapes
        with self.canvas:
            self.canvas.clear()
            Rectangle(size=(self.width, self.height))
            for shape in self.shapes:
                shape.draw_shape()

    def any_selected(self):
        for shape in self.shapes:
            if shape.selected:
                return True
        return False

    def shape_in_selection(self, shape, x, y, width, height):
        return (x < shape.x < shape.x + shape.width < x + width) and \
               (y < shape.y < shape.y + shape.height < y + height)


class EducorderApp(App):

    def out_line_toggle(self, obj):
        if self.main_canvas.any_selected():
            for shape in self.main_canvas.shapes:
                if shape.selected:
                    if shape.line:
                        shape.line = False
                    else:
                        shape.line = True

        else:
            if self.main_canvas.line_colour:
                self.main_canvas.line_colour = False
            else:
                self.main_canvas.line_colour = RED
        self.main_canvas.draw_canvas()

    def fill_in_toggle(self, obj):
        if self.main_canvas.any_selected():
            for shape in self.main_canvas.shapes:
                if shape.selected:
                    if shape.fill:
                        shape.fill = False
                    else:
                        shape.fill = True

        else:
            if self.main_canvas.fill_colour:
                self.main_canvas.fill_colour = False
            else:
                self.main_canvas.fill_colour = RED
        self.main_canvas.draw_canvas()


    def change_to_rectangle(self, obj):
        self.main_canvas.selected_mode = 1

    def change_to_ellipse(self, obj):
        self.main_canvas.selected_mode = 2

    def build(self):
        self.main_canvas = EducorderCanvas()

        """
            ALL FOR BUILD TESTING PURPOSES ONLY
        """

        button2 = Button(text='Rectangle')
        button2.bind(on_release=self.change_to_rectangle)

        button1 = Button(text='Ellipse')
        button1.bind(on_release=self.change_to_ellipse)

        button3 = Button(text='Fill')
        button3.bind(on_release=self.fill_in_toggle)

        button4 = Button(text='Line')
        button4.bind(on_release=self.out_line_toggle)

        shapes = BoxLayout(orientation='vertical')
        shapes.add_widget(button2)
        shapes.add_widget(button1)

        buttons = BoxLayout(orientation='horizontal')
        buttons.height = 30
        buttons.add_widget(shapes)
        buttons.add_widget(button3)
        buttons.add_widget(button4)

        root = BoxLayout(orientation='vertical')
        root.add_widget(buttons)
        root.add_widget(self.main_canvas)

        return root


if __name__ == '__main__':
    EducorderApp().run()
