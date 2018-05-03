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
import Server.ServerAPI.serverconn as serverCon
import uuid
import datetime

Builder.load_file('daily.kv')

'''
HoursWidget
This widget serves as the page to display a schedule.
'''


class HoursWidget(Screen):

    def on_enter(self):
        classList = serverCon.select_all('class')
        allClasses = ""
        today = datetime.datetime.today()
        today = str(today).split(" ")
        today = today[0]
        for myClass in classList:
            if 'name' in myClass:
                begin = str(myClass['start']).split(" ")
                if begin[0] == 'None':
                    break
                hour_minutes_start = begin[1].rsplit(":", 1)
                stop = str(myClass['end']).split(" ")
                hour_minutes_end = stop[1].rsplit(":", 1)
                #if begin[0] == today:
                allClasses += str(myClass['name']) + " - " + str(myClass['crn']) + "\n" + hour_minutes_start[
                        0] + " - " + hour_minutes_end[0] + "\n\n"

        now = datetime.datetime.now()
        month_day = now.strftime("%B") + " " + "%d" % now.day
        self.ids.HoursBox.clear_widgets()
        self.ids.HoursBox.add_widget(Button(text=month_day, size_hint=(.1, .1), disabled='true'))
        self.ids.HoursBox.add_widget(Button(text=allClasses, font_size = 14, disabled='true'))
