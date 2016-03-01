from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
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
        return (self.x <= x <= self.x + self.width) \
            and (self.y <= y <= self.y + self.height)

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


class EducorderLine(EduShape):
    """
        Basic line shape
    """

    def __init__(self, touch_down, touch_up, line_colour, fill_colour):
        super(EducorderLine,self).__init__(touch_down, touch_up, line_colour, fill_colour)
        self.shape = 'Line'

    def draw_shape(self):
        if self.line:
            Color(0, 0, 0)
            Line(points=[self.x, self.y, self.x+self.width, self.y+self.height])
        if self.selected:
            self.reshape_circles.reshape_draw()

    def reallign_shape(self):
        # Left blank because lines are not based on just bounding box
        # So they may need to have negative widths and heights
        pass

    def clicked_on(self, x_in, y_in):
        x = x_in - self.x
        y = y_in - self.y

        return (abs((y / x) - (self.height / self.width)) < .1) and \
            min(self.x, self.x+self.width) < x_in < max(self.x, self.x+self.width) and \
            min(self.y, self.y+self.height) < y_in < max(self.y, self.y+self.height)


class EducorderText(EduShape):
    """
        Text
    """
    def __init__(self, touch_down, touch_up, line_colour, fill_colour):
        super(EducorderText, self).__init__(touch_down, touch_up, line_colour, fill_colour)
        self.shape = 'Text'

    def draw_shape(self):
        pass

    def print_text(self):
        Color(0, 0, 0)
        self.label = CoreLabel()
        self.label.text = 'HEllo WoRld'
        self.label.refresh()


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
        if self.shape.shape == 'Line':
            for circle in [self.circles[1], self.circles[3]]:
                circle.draw_reshape_circle()
        else:
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