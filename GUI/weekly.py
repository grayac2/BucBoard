"""
weekly.py
Programmer:     Ashley Joyner
Date:           4/2/2018
Purpose:        Allows the user view a weekly schedule
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

Builder.load_file('weekly.kv')

'''
WeeklyWidget
This widget serves as the page to display a weekly schedule.
'''


class WeeklyWidget(Screen):

    def on_enter(self):
        self.ids.WeekBox.clear_widgets()
        schedule = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        monday = "10:30 - 12:30 \n CSCI 3200\n\n12:30 - 2:30 \n CSCI 4100"
        tuesday = "11:30 - 1:30\nCSCI 1250\n\n1:30 - 2:30\nCSCI 1100\n\n2:30 - 4:30\nCSCI 5120\n\n5 - 7:30\nCSCI 2200"
        wednesday = "10:30 - 12:30 \n CSCI 3200\n\nCSCI something"
        thursday = "11:30 - 1:30 \n CSCI 1250\n\n1:30 - 2:30 \n CSCI 1100\n\n5:30 - 7:30 \n CSCI 2200"
        friday = ""

        for s in schedule:
            self.ids.WeekBox.add_widget(Button(text=s, size_hint=(.1, .1), disabled='true'))

        self.ids.WeekBox.add_widget(Button(text=monday, disabled='true'))
        self.ids.WeekBox.add_widget(Button(text=tuesday, disabled='true'))
        self.ids.WeekBox.add_widget(Button(text=wednesday, disabled='true'))
        self.ids.WeekBox.add_widget(Button(text=thursday, disabled='true'))
        self.ids.WeekBox.add_widget(Button(text=friday, disabled='true'))
