from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# import created widgets
from GUI.addRoom import AddRoomWidget
from GUI.addClass import AddClassWidget
from GUI.addUser import AddUserWidget
from GUI.addAnnouncement import AddAnnouncementWidget
from GUI.addBuilding import AddBuildingWidget
from GUI.editUser import EditUserWidget
from GUI.editRoom import EditRoomWidget
from GUI.editBuilding import EditBuildingWidget
from GUI.editClass import EditClassWidget

Builder.load_file('admin.kv')
Builder.load_file('login.kv')


class Nav(BoxLayout):
    def callback(self):
        if sm.current == self.id:       # if current screen's nav button is selected..
            sm.current = 'home'         # switch back to home screen
            self.background_color = 0.635, 0.667, 0.678, 1.0    # set previous screen's nav button color to 'default'
            self.color = 0, 0, 0, 1     # set previous screen's nav button text color to black
        else:
            sm.current = self.id        # switch to screen with name == clicked button's id
            for button in Nav.buttons:
                button.background_color = 0.635, 0.667, 0.678, 1.0  # change each button to 'default' color
                button.color = 0, 0, 0, 1                           # change each button's text color to black
            self.background_color = 0.016, 0.118, 0.259, 1.0        # change selected button to 'active' color
            self.color = 1, 1, 1, 1                                 # change selected button text color to white

    users = Button(text='Users')    # create button
    users.id = 'editUser'            # define id for button for callback use
    users.bind(on_press=callback)   # set on_press action
    users.background_normal = ''    # set background image to white

    rooms = Button(text='Rooms')
    rooms.id = 'editRoom'
    rooms.bind(on_press=callback)
    rooms.background_normal = ''

    buildings = Button(text='Buildings')
    buildings.id = 'editBuilding'
    buildings.bind(on_press=callback)
    buildings.background_normal = ''

    classes = Button(text='Classes')
    classes.id = 'editClass'
    classes.bind(on_press=callback)
    classes.background_normal = ''

    announcements = Button(text="Announcements")
    announcements.id = 'addAnnouncement'
    announcements.bind(on_press=callback)
    announcements.background_normal = ''

    buttons = [users, rooms, buildings, classes, announcements]     # add each button to 'buttons'
    for button in buttons:
        button.background_color = 0.635, 0.667, 0.678, 1.0  # change each button to 'default' color
        button.color = 0, 0, 0, 1


nav = Nav()

nav.add_widget(Nav.users)       # add buttons to nav widget
nav.add_widget(Nav.rooms)
nav.add_widget(Nav.buildings)
nav.add_widget(Nav.classes)
nav.add_widget(nav.announcements)

nav.orientation = 'vertical'    # set attributes for nav
nav.size = (130, 300)
nav.size_hint = (None, 1)
nav.spacing = 2
nav.rows = 3
nav.cols = 1


class HomeScreen(Screen):
    pass


# Create the screen manager, add screens to it
sm = ScreenManager(transition=NoTransition())
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(AddUserWidget(name='addUser'))
sm.add_widget(AddClassWidget(name='addClass'))
sm.add_widget(AddRoomWidget(name='addRoom'))
sm.add_widget(AddAnnouncementWidget(name='addAnnouncement'))
sm.add_widget(EditBuildingWidget(name='editBuilding'))
sm.add_widget(EditUserWidget(name='editUser'))
sm.add_widget(EditRoomWidget(name='editRoom'))
sm.add_widget(AddBuildingWidget(name="addBuilding"))
sm.add_widget(EditClassWidget(name="editClass"))


class MainWidget(Screen):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        admin = BoxLayout()     # Create layout for screen
        admin.orientation = 'horizontal'
        admin.add_widget(nav)   # add nav to layout
        admin.add_widget(sm)    # add screen manager to layout
        self.add_widget(admin)  # add layout to screen


class LoginWidget(Screen):
    def change_screen(self):
        main_sm.current = 'main_screen' # Change to main screen on function call


main_sm = ScreenManager(transition=NoTransition())  # define screen manager
main_sm.add_widget(LoginWidget(name='login'))       # add login screen to manager
main_sm.add_widget(MainWidget(name='main_screen'))  # add main screen to manager


class AdminApp(App):
    def build(self):
        return main_sm


if __name__ == '__main__':
    AdminApp().run()

