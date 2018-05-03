"""
addBuilding.py
Programmer:     Brandon Campbell
Date:           3/26/2018
Purpose:        Allows the user to add Buildings to the Database.
"""

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from Server.ServerAPI.serverconn import insert, select_all
import uuid

Builder.load_file('addBuilding.kv')

# Create our initial Popup that will show the user what information they input that will be sent to the DB.
popup = Popup(title='Success!',
                    content=Label(text='Hello world'),
                    size_hint=(None, None), size=(200, 200))


'''
AddBuildingWidget
This widget serves as the page to add buildings to the System.
'''


class AddBuildingWidget(Screen):

    campus_list = ['']
    campuses = select_all("campus")  # Return professor JSON objects
    campusNumberTextBox = Spinner()

    def on_enter(self):
        self.campus_list = ['']
        self.campuses = select_all("campus")
        for campus in self.campuses:          # for each returned professor...
            if campus['message_type'] != 1:   # Check for message type
                self.campus_list.append(campus['name'])  # add campus name to list
        self.campusNumberTextBox = Spinner(id='campusNumberTextBox', size_hint_y=None, height=35, font_size='20sp',
                                           values=self.campus_list)
        for child in self.ids.form_layout.children:
            if child.id == "campusNumberTextBox":
                self.ids.form_layout.remove_widget(child)
        self.ids.form_layout.add_widget(self.campusNumberTextBox)

    # submit_new_classroom()
    # This function puts the information the user entered in the forms and displays a popup of what will eventually
    # be put into the database.
    def submit_new_building(self, *args):

        campus_id = ''
        for campus in AddBuildingWidget.campuses:
            if campus['message_type'] != 1:
                if campus['name'] == self.campusNumberTextBox.text:
                    campus_id = campus['id']

        buildingNameTextBox = self.ids['buildingNameTextBox'].text  # store the building name

        # Determine which Type of room the user wants to submit, then record that as Type.
        unique_id = uuid.uuid4()  # Create a unique ID for the Room.

        # Update the popup to contain the information the user input.
        popup = Popup(content=Label(text='Data to be sent to DB:\n'
                                         'Building Name:' + buildingNameTextBox + '\n'
                                         'Campus ID: ' + campus_id + '\n'
                                         'UID: ' + str(unique_id)), size_hint=(None, None), size=(400, 400))
        # popup.open()  # Show the user their information that will be sent to DB.

        new_building = {    # Create new building JSON object
            "name": buildingNameTextBox,
            "campus": campus_id
        }

        insert("building", new_building)

        self.ids['buildingNameTextBox'].text = ''
