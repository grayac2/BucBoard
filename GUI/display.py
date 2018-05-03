from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from GUI.announcements import AnnouncementsWidget
from GUI.daily import HoursWidget
from GUI.weekly import WeeklyWidget


Builder.load_file('display.kv')


class Display:
    def changescreen(self):     # function to switch to next screen
        sm.current = sm.next()  # assign 'next' screen to current screen


class Banner(BoxLayout):
    pass


banner = Banner()       # Banner class initialized instead of box layout for use in kv file

className = Label(text='CSCI 1710-001 — Web Design', halign='left')
room = Label(text='490', halign='left')
classTime = Label(text='10:00 - 12:00', halign='left')

className.size_hint = (None, None)                      # Necessary to left-align labels
className.bind(texture_size=className.setter('size'))
room.size_hint = (None, None)
room.bind(texture_size=room.setter('size'))
classTime.size_hint = (None, None)
classTime.bind(texture_size=classTime.setter('size'))

room_info = BoxLayout()
room_info.orientation = 'horizontal'
room_info.add_widget(room)
room_info.add_widget(classTime)

labels = BoxLayout()            # Place labels in box layout
labels.orientation = 'vertical'
labels.add_widget(className)
labels.add_widget(room_info)
labels.padding = 10

image = AsyncImage(source='https://etsu.edu/cbat/computing/pictures/facstaff/hendrix.jpg')
image.allow_stretch = True
image.size_hint = (None, 1)

banner.add_widget(image)
banner.add_widget(labels)   # add label layout to overall banner layout

banner.orientation = 'horizontal'
banner.size = (100, 75)
banner.size_hint = (1, None)
className.font_size = '30sp'
classTime.font_size = '20sp'
room.font_size = '20sp'
classTime.padding_x = 10


# Declare both screens
class AnnouncementsScreen(Screen):
    pass


class HoursScreen(Screen):
    pass


class WeekScreen(Screen):
    pass


# Create the screen manager, add screens to it
sm = ScreenManager()
sm.add_widget(AnnouncementsWidget(name='announcements'))
sm.add_widget(HoursWidget(name='hours'))
sm.add_widget(WeeklyWidget(name='week'))


# Create main layout
main = BoxLayout()
main.orientation = 'vertical'
main.add_widget(banner)       # add banner to main layout
main.add_widget(sm)        # add screen manager to main layout


class DisplayApp(App):
    def build(self):
        display = Display   # creates local display object
        Clock.schedule_interval(display.changescreen, 10.0)  # set screen to change every 10 seconds
        return main


if __name__ == '__main__':
    DisplayApp().run()

