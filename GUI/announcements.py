"""
addRoom.py
Programmer:     Brandon Campbell
Date:           2/11/2018
Purpose:        Allows the user view announcements
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import mainthread

import uuid

Builder.load_file('announcements.kv')

'''
AnnouncementsWidget
This widget serves as the page to display announcements.
'''


class AnnouncementsWidget(Screen):
    # List 'dummy' announcements.
    def on_enter(self):
        self.ids.announcementsBox.clear_widgets()
        announcements = ('IEEE Meeting - 3/13/2018 @12:00PM', 'PIZZA! - 3/15/2018 @3:00PM', 'Video Game Contest - 3/17/2018 @9:00PM')
        for a in announcements:
            self.ids.announcementsBox.add_widget(Button(text=a, font_size=20, disabled='true'))

