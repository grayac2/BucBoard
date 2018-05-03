from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
Builder.load_file('admin.kv')


class Display:
    def change_screen(self):     # function to switch to next screen
        sm.current = sm.next()  # assign 'next' screen to current screen


# Declare screens
class AnnouncementsScreen(Screen):
    pass


class HoursScreen(Screen):
    pass


class AdminScreen(Screen):
    def showrooms(self):
        pass  # hide other areas, show room functions


class Navigation(Widget):
    layout = BoxLayout(spacing=10)
    admin = Button(text='Admin', size=(100, 1))
    announcements = Button(text='Announcements', size=(100, 1))
    hours = Button(text='Hours', size=(100, 1))
    layout.add_widget(admin)
    layout.add_widget(announcements)
    layout.add_widget(hours)


# Create the screen manager, add screens to it
sm = ScreenManager()
sm.transition.duration = 0
sm.add_widget(AnnouncementsScreen(name='announcements'))
sm.add_widget(HoursScreen(name='hours'))
sm.add_widget(AdminScreen(name='admin'))


class AdminApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    AdminApp().run()
