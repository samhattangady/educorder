from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse

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

