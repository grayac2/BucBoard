from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from Server.ServerAPI.serverconn import insert, select_all
import uuid

Builder.load_file("addUser.kv")


class AddUserWidget(Screen):
    room_list = ['']
    rooms = select_all("room")  # Return room JSON objects
    officeNumber = Spinner()

    def on_enter(self):
        self.room_list = ['']
        self.rooms = select_all("room")  # Return room JSON objects
        for room in self.rooms:  # for each returned room...
            if room['message_type'] != 1:  # Check for message type
                self.room_list.append(room['room_num'])  # add room number to room_list
        self.officeNumber = Spinner(size_hint_y=None, height=35, font_size='20sp', values=self.room_list, id="officeNumber")
        for child in self.ids.form_layout.children:
            if child.id == "officeNumber":
                self.ids.form_layout.remove_widget(child)
        self.ids.form_layout.add_widget(self.officeNumber)

    def submit_new_user(self, *args):
        room_id = ''
        for room in self.rooms:
            if room['message_type'] != 1:
                if room['room_num'] == self.officeNumber.text:
                    room_id = room['id']

        if self.ids['adminTypeToggleButton'].state == 'down':
            user_type = '100'
        if self.ids['professorTypeToggleButton'].state == 'down':
            user_type = '112'

        user_last_name = self.ids['userLastName'].text
        user_first_name = self.ids['userFirstName'].text

        unique_id = uuid.uuid4()

        popup = Popup(content=Label(text='Data to be sent to DB:\n'
                                         'Last Name: ' + user_last_name + '\n'
                                         'First Name: ' + user_first_name + '\n'
                                         'Office ID: ' + room_id + '\n'
                                         'Type: ' + user_type + '\n'
                                         'UID: ' + str(unique_id)), size_hint=(None, None), size=(400, 400))
        # popup.open()

        new_user = {
            "first_name": user_first_name,
            "last_name": user_last_name,
            "office": room_id,
            "prefix": user_type
        }

        insert("user", new_user)

        self.ids['userLastName'].text = ''
        self.ids['userFirstName'].text = ''
