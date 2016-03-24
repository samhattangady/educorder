#!/usr/bin/python

from kivy.config import Config as kivy_config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from educanvas import EducorderCanvas

kivy_config.set('input', 'mouse', 'mouse,disable_multitouch')


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

    def change_to_line(self, obj):
        self.main_canvas.selected_mode = 3

    def change_to_text(self, obj):
        self.main_canvas.selected_mode = 4

    def build(self):
        self.main_canvas = EducorderCanvas()

        """
            ALL FOR BUILD TESTING PURPOSES ONLY
        """

        button2 = Button(text='Rectangle')
        button2.bind(on_release=self.change_to_rectangle)

        button1 = Button(text='Ellipse')
        button1.bind(on_release=self.change_to_ellipse)

        button0 = Button(text='Line')
        button0.bind(on_release=self.change_to_line)

        button5 = Button(text='Text')
        button5.bind(on_release=self.change_to_text)

        button3 = Button(text='Fill')
        button3.bind(on_release=self.fill_in_toggle)

        button4 = Button(text='Line')
        button4.bind(on_release=self.out_line_toggle)

        shapes = BoxLayout(orientation='vertical')
        shapes.add_widget(button2)
        shapes.add_widget(button1)
        shapes.add_widget(button0)
        shapes.add_widget(button5)

        buttons = BoxLayout(orientation='horizontal')
        buttons.height = 30
        buttons.add_widget(shapes)
        buttons.add_widget(button3)
        buttons.add_widget(button4)

        root = BoxLayout(orientation='vertical')
        root.add_widget(buttons)
        root.add_widget(self.main_canvas.canvastextinput)
        root.add_widget(self.main_canvas)

        return root

if __name__ == '__main__':
    EducorderApp().run()