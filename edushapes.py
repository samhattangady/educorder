from reshape_extra import ReshapeCirclesParent

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse


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
        # For use in specific init
        self.touch_up = touch_up

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

    def start_move_shape(self, touch):
        self.x_offset = touch.x - self.x
        self.y_offset = touch.y - self.y

    def move_shape(self, touch):
        # Move shape based on where it was dragged from
        self.x = touch.x - self.x_offset
        self.y = touch.y - self.y_offset
        self.reshape_circles = ReshapeCirclesParent(self)

    def reshape(self, touch, circle_index):
        # To reshape the shapes by dragging the circles in corner/side
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
    def __init__(self, touch_down, touch_up, line_colour, fill_colour):
        super(EducorderRectangle,self).__init__(touch_down, touch_up, line_colour, fill_colour)
        self.shape = 'Rectangle'

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

    def __init__(self, touch_down, touch_up, line_colour, fill_colour):
        super(EducorderEllipse,self).__init__(touch_down, touch_up, line_colour, fill_colour)
        self.shape = 'Ellipse'

    def clicked_on(self, x_in, y_in):
        a = self.width/2
        b = self.height/2

        x = x_in - (self.x + self.width/2)
        y = y_in - (self.y + self.height/2)
        return ((x**2/a**2) + (y**2/b**2)) < 1

    def draw_shape(self):
        # Draws ellipse based on line and fill colours
        if self.fill:
            Color(1, 0, 0)
            Ellipse(pos=(self.x, self.y), size=(self.width, self.height))
        if self.line:
            Color(0, 0, 0)
            Line(ellipse=(self.x, self.y, self.width, self.height))
        if self.selected:
            self.reshape_circles.reshape_draw()
