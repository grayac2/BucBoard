"""
addRoom.py
Programmer:     Brandon Campbell
Date:           2/11/2018
Purpose:        Allows the user to add Rooms to the Database.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from Server.ServerAPI.serverconn import insert, select_all
import uuid

Builder.load_file('addRoom.kv')

# Create our initial Popup that will show the user what information they input that will be sent to the DB.
popup = Popup(title='Success!',
                    content=Label(text='Hello world'),
                    size_hint=(None, None), size=(200, 200))


'''
AddRoomWidget
This widget serves as the page to add classrooms to the System.
'''


class AddRoomWidget(Screen):
    # List buildings.
    buildingList = ['']
    buildings = select_all("building")  # Return building JSON objects
    buildingsSpinner = Spinner()

    def on_enter(self):
        self.buildingList = ['']
        self.buildings = select_all("building")
        for building in self.buildings:          # for each returned building...
            if building['message_type'] != 1:   # Check for message type
                self.buildingList.append(building['name'])  # add name of building to buildingList
        self.buildingsSpinner = Spinner(id='buildingsSpinner', size_hint_y=None, height=35, values=self.buildingList,
                                        font_size='20sp')
        for child in self.ids.form_layout.children:
            if child.id == "buildingsSpinner":
                self.ids.form_layout.remove_widget(child)
        self.ids.form_layout.add_widget(self.buildingsSpinner)

    # submit_new_classroom()
    # This function puts the information the user entered in the forms and displays a popup of what will eventually
    # be put into the database.
    def submit_new_classroom(self, *args):
        class_name_text_box = self.ids['roomNumberTextBox'].text  # store the room number

        # Determine which Type of room the user wants to submit, then record that as Type.
        # TODO: This checks the same condition twice
        if self.ids['classRoomTypeToggleButton'].state == 'down':
            type = '0'  # Type set to 0 for classrooms
        if self.ids['officeRoomTypeToggleButton'].state == 'down':
            type = '1'  # Type set to 1 for office

        building_id = ''
        for building in AddRoomWidget.buildings:
            if building['message_type'] != 1:
                if building['name'] == self.buildingsSpinner.text:
                    building_id = building['id']

        unique_id = uuid.uuid4()  # Create a unique ID for the Room.

        # Update the popup to contain the information the user input.
        popup = Popup(content=Label(text='Data to be sent to DB:\n'
                                         'Room Number:' + class_name_text_box + '\n'
                                         'Building ID: ' + building_id + '\n'
                                         'Type: ' + type + '\n'
                                         'UID: ' + str(unique_id)), size_hint=(None, None), size=(400, 400))
        # popup.open()  # Show the user their information that will be sent to DB.

        new_room = {
            "type": type,
            "room_num": class_name_text_box,
            "building": building_id
        }

        insert("room", new_room)

        self.ids['roomNumberTextBox'].text = ''
