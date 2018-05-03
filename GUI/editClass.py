"""
editRoom.py
Programmer:     Ashley Joyner
Date:           4/23/2018
Purpose:        Allows the user to edit Classes in the Database.
"""

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import Server.ServerAPI.serverconn as serverCon

Builder.load_file('editClass.kv')

# Create our initial Popup that will show the user what information they input that will be sent to the DB.
##popup = Popup(title='Success!',
##                    content=Label(text='Hello world'),
##                    size_hint=(None, None), size=(200, 200))
##


'''
AddBuildingWidget
This widget serves as the page to add buildings to the System.
'''


class EditClassWidget(Screen):
    classToSave = {'id':'', 'name': '', 'crn': '', 'section': '', 'start': '', 'end': '', 'professor': '', 'room_num': ''}
    user = {'id': '', 'first_name': '', 'last_name': '', 'prefix': '', 'office': ''}
    room = {'id': '', 'type': '', 'room_num': '', 'building': ''}
    classList = serverCon.select_all('class')
    userList = serverCon.select_all('user')
    userNames = {}
    userNamesReversed = {}
    roomList = serverCon.select_all('room')
    roomNums = {}
    roomNumsReversed = {}

    for user in userList:
        if 'last_name' in user:
            userNames[user['id']] = user['last_name']
            userNamesReversed[user['last_name']] = user['id']

    for room in roomList:
        if 'room_num' in room:
            roomNums[room['id']] = room['room_num']
            roomNumsReversed[room['room_num']] = room['id']

    def change_screen(self, instance):
        self.parent.current = 'addClass'

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
        for myClass in self.classList:
            if 'id' in myClass:
                if myClass['id'] == idToDelete:
                    self.classList.remove(myClass)
        for child in self.ids.ClassGrid.children:
            if child.id == "name" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == "room" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == "crn" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == "section" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == "prof" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == "start" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == "end" + (instance.id).replace("deleteButton", ""):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == (instance.id).replace("deleteButton", "editButton"):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == (instance.id).replace("deleteButton", "cancelButton"):
                self.ids.ClassGrid.remove_widget(child)
        for child in self.ids.ClassGrid.children:
            if child.id == instance.id:
                self.ids.ClassGrid.remove_widget(child)

    '''
    edit_button_click(instance)
    Parameters: instance: the edit/save button that was clicked. 
    Purpose:    Unlocks the editable fields and the delete button. Changes the edit button's text to "Save"
    '''
    def edit_button_click(self, instance):
        for child in self.ids.ClassGrid.children:
            if child.id == "name" + (instance.id).replace("editButton", ""):
                self.classToSave['name'] = child.text
                self.classToSave["id"] = (instance.id).replace("editButton", "")
                child.disabled = False
            elif child.id == "room" + (instance.id).replace("editButton", ""):
                self.classToSave["room_num"] = self.roomNumsReversed[child.text]
                child.disabled = False
            elif child.id == "crn" + (instance.id).replace("editButton", ""):
                self.classToSave["crn"] = child.text
                child.disabled = False
            elif child.id == "section" + (instance.id).replace("editButton", ""):
                self.classToSave["section"] = child.text
                child.disabled = False
            elif child.id == "prof" + (instance.id).replace("editButton", ""):
                self.classToSave["professor"] = self.userNamesReversed[child.text]
                child.disabled = False
            elif child.id == "start" + (instance.id).replace("editButton", ""):
                self.classToSave["start"] = child.text
                child.disabled = False
            elif child.id == "end" + (instance.id).replace("editButton", ""):
                self.classToSave["end"] = child.text
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
        for child in self.ids.ClassGrid.children:
            if child.id == "name" + (instance.id).replace("cancelButton", ""):
                child.text = self.classToSave["name"]
                child.disabled = True
            elif child.id == "room" + (instance.id).replace("cancelButton", ""):
                child.text = self.roomNums[self.classToSave["room_num"]]
                child.disabled = True
            elif child.id == "crn" + (instance.id).replace("cancelButton", ""):
                child.text = self.classToSave["crn"]
                child.disabled = True
            elif child.id == "section" + (instance.id).replace("cancelButton", ""):
                child.text = self.classToSave["section"]
                child.disabled = True
            elif child.id == "prof" + (instance.id).replace("cancelButton", ""):
                child.text = self.userNames[self.classToSave["professor"]]
                child.disabled = True
            elif child.id == "start" + (instance.id).replace("cancelButton", ""):
                child.text = self.classToSave["start"]
                child.disabled = True
            elif child.id == "end" + (instance.id).replace("cancelButton", ""):
                child.text = self.classToSave["end"]
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
        classToSend = {'id':'', 'name': '', 'crn': '', 'section': '', 'start': '', 'end': '', 'professor': '', 'room_num': ''};
        for child in self.ids.ClassGrid.children:
            if child.id == "name" + (instance.id).replace("editButton", ""):
                classToSend["name"] = child.text
                self.classToSave["name"] = child.text
                child.disabled = True
            elif child.id == "room" + (instance.id).replace("editButton", ""):
                classToSend["room_num"] = child.text
                self.classToSave["room_num"] = self.roomNumsReversed[child.text]
                child.disabled = True
            elif child.id == "crn" + (instance.id).replace("editButton", ""):
                classToSend["crn"] = child.text
                self.classToSave["crn"] = child.text
                child.disabled = True
            elif child.id == "section" + (instance.id).replace("editButton", ""):
                classToSend["section"] = child.text
                self.classToSave["section"] = child.text
                child.disabled = True
            elif child.id == "prof" + (instance.id).replace("editButton", ""):
                classToSend["professor"] = child.text
                self.classToSave["professor"] = self.userNamesReversed[child.text]
                child.disabled = True
            elif child.id == "start" + (instance.id).replace("editButton", ""):
                classToSend["start"] = child.text
                self.classToSave["start"] = child.text
                child.disabled = True
            elif child.id == "end" + (instance.id).replace("editButton", ""):
                classToSend["end"] = child.text
                self.classToSave["end"] = child.text
                child.disabled = True
            elif child.id == instance.id:
                self.edit_mode(child)
                child.unbind(on_press=self.save_changes)
                child.bind(on_press=self.edit_button_click)
            elif child.id == (instance.id).replace("editButton", "deleteButton"):
                child.disabled = True
            elif child.id == (instance.id).replace("editButton", "cancelButton"):
                child.disabled = True

        for myClass in self.classList:
            if 'crn' in myClass:
                if myClass["id"] == self.classToSave["id"]:
                    myClass["name"] = self.classToSave["name"]
                    myClass["crn"] = self.classToSave["crn"]
                    myClass["section"] = self.classToSave["section"]
                    myClass["start"] = self.classToSave["start"]
                    myClass["end"] = self.classToSave["end"]
                    myClass["professor"] = self.classToSave["professor"]
                    myClass["room_num"] = self.classToSave["room_num"]

        # popup = Popup(content=Label(text='Data to be sent to DB:\n'
        #                                  'Type: ' + self.roomToSave["type"] + '\n'
        #                                  'Number: ' + self.roomToSave["room_num"] + '\n'
        #                                 'Building Name: ' + self.roomToSave["building"] + '\n'
        #                             ), size_hint=(None, None), size=(400, 400))
        # popup.open()


    def on_enter(self):
        self.ids.ClassGrid.clear_widgets()
        self.ids.EditClassBox.clear_widgets()
        for myClass in self.classList:
            if 'id' in myClass:
                self.ids.ClassGrid.add_widget(TextInput(text=myClass['name'], disabled='true', id="name" + myClass['id'], height=50, font_size=15, size_hint_y=None, size_hint_max_x=250))
                self.ids.ClassGrid.add_widget(TextInput(text=myClass['crn'], disabled='true', id="crn" + myClass['id'], height=50, font_size=15, size_hint_y=None, size_hint_max_x=250))
                ##self.ids.ClassGrid.add_widget(TextInput(text=myClass['section'], disabled='true', id="section" + myClass['id'], height=50, font_size=15, size_hint_y=None, size_hint_max_x=250))
                self.ids.ClassGrid.add_widget(TextInput(text=myClass['start'], disabled='true', id="start" + myClass['id'], height=50, font_size=15, size_hint_y=None, size_hint_max_x=250))
                self.ids.ClassGrid.add_widget(TextInput(text=myClass['end'], disabled='true', id="end" + myClass['id'], height=50, font_size=15, size_hint_y=None, size_hint_max_x=250))

                profSpinner = Spinner(id="prof" + myClass['id'], disabled='true', size_hint_y=None, height=50, font_size=15, size_hint_max_x=270, text=self.userNames[myClass['professor']])
                profSpinner.values = self.userNames.values()
                self.ids.ClassGrid.add_widget(profSpinner)
                rawClass = serverCon.select_all("class")
                # self.ids.RoomGrid.add_widget(TextInput(text=room.type, disabled='true', id="type" + room.uid))

                roomSpinner = Spinner(id="room" + myClass['id'], disabled='true', height=50, font_size=15, size_hint_y=None, size_hint_max_x=270, text=self.roomNums[myClass['room_num']])
                roomSpinner.values = self.roomNums.values()
                self.ids.ClassGrid.add_widget(roomSpinner)
                # self.ids.RoomGrid.add_widget(TextInput(text=room.bldgName, disabled='true', id="bldgName" + room.uid))

                editButton = Button(text="Edit", id="editButton" + myClass['id'], height=50, font_size=15, size_hint_y=None, size_hint_max_x=220)
                editButton.bind(on_press=self.edit_button_click)
                self.ids.ClassGrid.add_widget(editButton)
                cancelButton = Button(text="Cancel", id="cancelButton" + myClass['id'], disabled="true", height=50, font_size=15, size_hint_y=None, size_hint_max_x=220)
                cancelButton.bind(on_press=self.cancel_button_click)
                self.ids.ClassGrid.add_widget(cancelButton)
                deleteButton = Button(text="Delete", id="deleteButton" + myClass['id'], disabled='true', height=50, font_size=15,
                                      size_hint_y=None, size_hint_max_x=220)
                deleteButton.bind(on_press=self.delete_button_click)
                self.ids.ClassGrid.add_widget(deleteButton)

        self.ids.EditClassBox.add_widget(Button(text="Add New Class", size_hint_y=.15, size_hint_max_y=20, size_hint_max_x=800, on_press=self.change_screen))





