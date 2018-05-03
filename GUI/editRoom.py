"""
editRoom.py
Programmer:     Brandon Campbell
Date:           3/26/2018
Purpose:        Allows the user to edit Rooms in the Database.
"""

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import Server.ServerAPI.serverconn as serverCon

Builder.load_file('editRoom.kv')

# Create our initial Popup that will show the user what information they input that will be sent to the DB.
popup = Popup(title='Success!',
                    content=Label(text='Hello world'),
                    size_hint=(None, None), size=(200, 200))



'''
AddBuildingWidget
This widget serves as the page to add buildings to the System.
'''


class EditRoomWidget(Screen):
    roomToSave = {'room_num': '', 'message_type': '', 'type': '', 'id': '', 'building': ''}
    bldg = {'name': '', 'campus': '', 'message_type': '', 'id': ''}
    roomList = serverCon.select_all('room')
    roomTypes = {'0': "Office", '1': "Classroom", '2': "Lab"}
    roomTypesReversed = {"Office": "0", "Classroom": "1", "Lab": '2'}
    bldgList = serverCon.select_all('building')
    bldgNames = {}
    bldgNamesReversed = {}
    for bldg in bldgList:
        if 'name' in bldg:
            bldgNames[bldg['id']] = bldg['name']
            bldgNamesReversed[bldg['name']] = bldg['id']

    def change_screen(self, instance):
        self.parent.current = 'addRoom'

    '''
    save_mode(button)
    Parameters: button: the button that needs to be altered. 
    Purpose:    Change the text of the button to "Save"
    '''
    def save_mode(self, button):
        button.text = "Save"

    '''
    edit_mode(button)
    Parameters: button: the button that needs to be altered. 
    Purpose:    Change the text of the button to "Edit"
    '''
    def edit_mode(self, button):
        button.text = "Edit"

    '''
    delete_button_click(instance)
    Parameters: instance: the delete button that was clicked. 
    Purpose:    Deletes the record and removes the associated widgets.
    '''
    def delete_button_click(self, instance):
        idToDelete = (instance.id).replace("deleteButton", "")
        for room in self.roomList:
            if 'room_num' in room:
                if room['id'] == idToDelete:
                    self.roomList.remove(room)
        for child in self.ids.RoomGrid.children:
            if child.id == "type" + (instance.id).replace("deleteButton", ""):
                self.ids.RoomGrid.remove_widget(child)
        for child in self.ids.RoomGrid.children:
            if child.id == "number" + (instance.id).replace("deleteButton", ""):
                self.ids.RoomGrid.remove_widget(child)
        for child in self.ids.RoomGrid.children:
            if child.id == "bldgName" + (instance.id).replace("deleteButton", ""):
                self.ids.RoomGrid.remove_widget(child)
        for child in self.ids.RoomGrid.children:
            if child.id == (instance.id).replace("deleteButton", "editButton"):
                self.ids.RoomGrid.remove_widget(child)
        for child in self.ids.RoomGrid.children:
            if child.id == (instance.id).replace("deleteButton", "cancelButton"):
                self.ids.RoomGrid.remove_widget(child)
        for child in self.ids.RoomGrid.children:
            if child.id == instance.id:
                self.ids.RoomGrid.remove_widget(child)

    '''
    edit_button_click(instance)
    Parameters: instance: the edit/save button that was clicked. 
    Purpose:    Unlocks the editable fields and the delete button. Changes the edit button's text to "Save"
    '''
    def edit_button_click(self, instance):
        for child in self.ids.RoomGrid.children:
            if child.id == "type" + (instance.id).replace("editButton", ""):
                self.roomToSave['type'] = self.roomTypesReversed[child.text]
                self.roomToSave["id"] = (instance.id).replace("editButton", "")
                child.disabled = False
            elif child.id == "number" + (instance.id).replace("editButton", ""):
                self.roomToSave["room_num"] = child.text
                child.disabled = False
            elif child.id == "bldgName" + (instance.id).replace("editButton", ""):
                self.roomToSave["building"] = self.bldgNamesReversed[child.text]
                child.disabled = False
            elif child.id == instance.id:
                self.save_mode(child)
                child.unbind(on_press=self.edit_button_click)
                child.bind(on_press=self.save_changes)
            elif child.id == (instance.id).replace("editButton", "deleteButton"):
                child.disabled = False
            elif child.id == (instance.id).replace("editButton", "cancelButton"):
                child.disabled = False

    '''
    cancel_button_click
    Parameters:
        self
        instance:   The button itself is passed in through this argument automatically.
    Purpose:        This function handles what happens when you click the Cancel button. 
                    The button is disabled and the editable fields are disabled. The fields values are replaced
                    by the pre-edited values.
    '''
    def cancel_button_click(self, instance):
        for child in self.ids.RoomGrid.children:
            if child.id == "type" + (instance.id).replace("cancelButton", ""):
                child.text = self.roomTypes[self.roomToSave["type"]]
                child.disabled = True
            elif child.id == "number" + (instance.id).replace("cancelButton", ""):
                child.text = self.roomToSave["room_num"]
                child.disabled = True
            elif child.id == "bldgName" + (instance.id).replace("cancelButton", ""):
                child.text = self.bldgNames[self.roomToSave["building"]]
                child.disabled = True
            elif child.id == (instance.id).replace("cancelButton", "editButton"):
                self.edit_mode(child)
                child.unbind(on_press=self.save_changes)
                child.bind(on_press=self.edit_button_click)
            elif child.id == (instance.id).replace("cancelButton", "deleteButton"):
                child.disabled = True
            elif child.id == instance.id:
                child.disabled = True

    '''
    save_changes
    Parameters:
        self
        instance:   The button itself is passed in through this argument automatically.
    Purpose:        This function handles what happens when you click the Save button. 
                    The button is changed back to an edit button, and the forms are disabled once again.
                    The list of rooms is updated.
    '''
    def save_changes(self, instance):
        roomToSend = {'room_num':'', 'message_type': '', 'type': '', 'id': '', 'building': ''};
        for child in self.ids.RoomGrid.children:
            if child.id == "type" + (instance.id).replace("editButton", ""):
                roomToSend["type"] = child.text
                self.roomToSave["type"] = self.roomTypesReversed[child.text]
                child.disabled = True
            elif child.id == "number" + (instance.id).replace("editButton", ""):
                roomToSend["room_num"] = child.text
                self.roomToSave["room_num"] = child.text
                child.disabled = True
            elif child.id == "bldgName" + (instance.id).replace("editButton", ""):
                roomToSend["building"] = child.text
                self.roomToSave["building"] = self.bldgNamesReversed[child.text]
                child.disabled = True
            elif child.id == instance.id:
                self.edit_mode(child)
                child.unbind(on_press=self.save_changes)
                child.bind(on_press=self.edit_button_click)
            elif child.id == (instance.id).replace("editButton", "deleteButton"):
                child.disabled = True
            elif child.id == (instance.id).replace("editButton", "cancelButton"):
                child.disabled = True

        for room in self.roomList:
            if 'room_num' in room:
                if room["id"] == self.roomToSave["id"]:
                    room["building"] = int(self.roomToSave["building"])
                    room["room_num"] = int(self.roomToSave["room_num"])
                    room["type"] = int(self.roomToSave["type"])
        serverCon.update('room', self.roomToSave)

        # popup = Popup(content=Label(text='Data to be sent to DB:\n'
        #                                  'Type: ' + self.roomToSave["type"] + '\n'
        #                                  'Number: ' + self.roomToSave["room_num"] + '\n'
        #                                 'Building Name: ' + self.roomToSave["building"] + '\n'
        #                             ), size_hint=(None, None), size=(400, 400))
        # popup.open()


    def on_enter(self):
        self.ids.RoomGrid.clear_widgets()
        self.ids.EditRoomBox.clear_widgets()
        self.roomList = serverCon.select_all('room')
        self.bldgList = serverCon.select_all('building')

        for bldg in self.bldgList:
            if 'name' in bldg:
                self.bldgNames[bldg['id']] = bldg['name']
                self.bldgNamesReversed[bldg['name']] = bldg['id']

        for room in self.roomList:
            if 'room_num' in room:
                typeSpinner = Spinner(id="type" + room['id'], disabled='true', size_hint_y=None, height=35, font_size=15, size_hint_max_x=270, text=self.roomTypes[room['type']])

                typeSpinner.values = self.roomTypes.values()

                self.ids.RoomGrid.add_widget(typeSpinner)

                self.ids.RoomGrid.add_widget(TextInput(text=room['room_num'], disabled='true', id="number" + room['id'], height=35, font_size=15, size_hint_y=None, size_hint_max_x=250))

                bldgSpinner = Spinner(id="bldgName" + room['id'], disabled='true', height=35, font_size=15, size_hint_y=None, size_hint_max_x=270, text=self.bldgNames[room['building']])

                bldgSpinner.values = self.bldgNames.values()

                self.ids.RoomGrid.add_widget(bldgSpinner)

                editButton = Button(text="Edit", id="editButton" + room['id'], height=35, font_size=15, size_hint_y=None, size_hint_max_x=220)

                editButton.bind(on_press=self.edit_button_click)

                self.ids.RoomGrid.add_widget(editButton)

                cancelButton = Button(text="Cancel", id="cancelButton" + room['id'], disabled="true", height=35, font_size=15, size_hint_y=None, size_hint_max_x=220)

                cancelButton.bind(on_press=self.cancel_button_click)

                self.ids.RoomGrid.add_widget(cancelButton)

                deleteButton = Button(text="Delete", id="deleteButton" + room['id'], disabled='true', height=35, font_size=15,
                                      size_hint_y=None, size_hint_max_x=220)

                deleteButton.bind(on_press=self.delete_button_click)

                self.ids.RoomGrid.add_widget(deleteButton)

        self.ids.EditRoomBox.add_widget(Button(text="Add New Room", background_normal='',
                                               background_color=(1, .78, .17, 1), color=(0, 0, 0, 1), size_hint_y=.15,
                                               size_hint_max_y=20, size_hint_max_x=800, on_press=self.change_screen))

