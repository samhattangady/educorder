#!/usr/bin/python
from edushapes import *

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Rectangle

# Declaring some constant colours. Not working right
RED = (1, 0, 0)
WHITE = (1, 1, 1)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)


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

        # Keyboard controls
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        # _keyboard_closed and _on_keyboard_down classes have been taken straight from kivy API docs
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # _keyboard_closed and _on_keyboard_down classes have been taken straight from kivy API docs
        if keycode[1] == 'delete':
            self.delete_selected()
        elif keycode[1] == 'escape':
            keyboard.release()

        self.draw_canvas()
        return True

    def on_touch_down(self, touch):
        # We always want to store every click
        # Only draw if it is within the bounds of
        self.touch_down = touch.pos
        if self.selected_mode:  # Drawing
            if self.check_touch_in_bounds(touch):
                self.deselect_all()

        if self.any_selected():  # Reshaping or moving
            # This is because the reshape circles are partly (or wholly) outside the shape
            # So  without this, a click on the reshape would automatically deselect
            for shape in self.shapes:
                    if shape.selected:
                        shape.start_move_shape(touch)
                        for circle in shape.reshape_circles.circles:
                            if circle.clicked_on(touch.x, touch.y):
                                self.reshaping = shape.reshape_circles.circles.index(circle)
            # This is to cover the case where clicking outside doesn't deselect shape.
            if not self.reshaping:
                self.select_clicked_on(touch)

        else:  # Moving or selection box
            if self.check_touch_in_bounds(touch):
                self.select_clicked_on(touch)
                for shape in self.shapes:
                    if shape.selected:
                        shape.start_move_shape(touch)
        self.draw_canvas()

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

    def delete_selected(self):
        shapes_to_delete = []
        for shape in self.shapes:
            if shape.selected:
                shapes_to_delete.append(self.shapes.index(shape))
        for shape in shapes_to_delete:
            self.shapes.pop(shape)



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
