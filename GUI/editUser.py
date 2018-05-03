from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import Server.ServerAPI.serverconn as serverCon

Builder.load_file('editUser.kv')

'''
AddUserWidget
This widget serves as the page to add buildings to the System.
'''


class EditUserWidget(Screen):
    userToSave = {'id': '', 'first_name': '', 'last_name': '', 'prefix': '', 'office': ''}
    userList = serverCon.select_all('user')
    userTypes = {'100': "Admin", '112': "Professor"}
    userTypesReversed = {"Admin": "100", "Professor": "112"}
    room = {'id': '', 'type': '', 'room_num': '', 'building': ''}
    roomList = serverCon.select_all('room')
    roomNames = {}
    roomNamesReversed = {}
    for room in roomList:
        if 'room_num' in room:
            roomNames[room['id']] = room['room_num']
            roomNamesReversed[room['room_num']] = room['id']

    def change_screen(self, instance):
        self.parent.current = 'addUser'

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
        for user in self.userList:
            if 'user_num' in user:
                if user['id'] == idToDelete:
                    self.userList.remove(user)
        for child in self.ids.UserGrid.children:
            if child.id == "first_name" + (instance.id).replace("deleteButton", ""):
                self.ids.UserGrid.remove_widget(child)
        for child in self.ids.UserGrid.children:
            if child.id == "last_name" + (instance.id).replace("deleteButton", ""):
                self.ids.UserGrid.remove_widget(child)
        for child in self.ids.UserGrid.children:
            if child.id == "prefix" + (instance.id).replace("deleteButton", ""):
                self.ids.UserGrid.remove_widget(child)
        for child in self.ids.UserGrid.children:
            if child.id == "office" + (instance.id).replace("deleteButton", ""):
                self.ids.UserGrid.remove_widget(child)
        for child in self.ids.UserGrid.children:
            if child.id == (instance.id).replace("deleteButton", "editButton"):
                self.ids.UserGrid.remove_widget(child)
        for child in self.ids.UserGrid.children:
            if child.id == (instance.id).replace("deleteButton", "cancelButton"):
                self.ids.UserGrid.remove_widget(child)
        for child in self.ids.UserGrid.children:
            if child.id == instance.id:
                self.ids.UserGrid.remove_widget(child)

    '''
    edit_button_click(instance)
    Parameters: instance: the edit/save button that was clicked. 
    Purpose:    Unlocks the editable fields and the delete button. Changes the edit button's text to "Save"
    '''
    def edit_button_click(self, instance):
        for child in self.ids.UserGrid.children:
            if child.id == "first_name" + (instance.id).replace("editButton", ""):
                self.userToSave['first_name'] = child.text
                child.disabled = False
            elif child.id == "last_name" + (instance.id).replace("editButton", ""):
                self.userToSave["last_name"] = child.text
                child.disabled = False
            elif child.id == "prefix" + (instance.id).replace("editButton", ""):
                self.userToSave['prefix'] = self.userTypesReversed[child.text]
                self.userToSave["id"] = (instance.id).replace("editButton", "")
                child.disabled = False
            if child.id == "office" + (instance.id).replace("editButton", ""):
                self.userToSave["office"] = self.roomNamesReversed[child.text]
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
        for child in self.ids.UserGrid.children:
            if child.id == "first_name" + (instance.id).replace("cancelButton", ""):
                child.text = self.userToSave["first_name"]
                child.disabled = True
            elif child.id == "last_name" + (instance.id).replace("cancelButton", ""):
                child.text = self.userToSave["last_name"]
                child.disabled = True
            elif child.id == "prefix" + (instance.id).replace("cancelButton", ""):
                child.text = self.userTypes[self.userToSave["prefix"]]
                child.disabled = True
            elif child.id == "office" + (instance.id).replace("cancelButton", ""):
                child.text = self.roomNames[self.userToSave["office"]]
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
        userToSend = {'first_name':'', 'last_name': '', 'prefix': '', 'office': '', 'id': ''};
        for child in self.ids.UserGrid.children:
            if child.id == "first_name" + (instance.id).replace("editButton", ""):
                userToSend["first_name"] = child.text
                self.userToSave["first_name"] = child.text
                child.disabled = True
            elif child.id == "last_name" + (instance.id).replace("editButton", ""):
                userToSend["last_name"] = child.text
                self.userToSave["last_name"] = child.text
                child.disabled = True
            elif child.id == "prefix" + (instance.id).replace("editButton", ""):
                userToSend["prefix"] = self.userTypesReversed[child.text]
                self.userToSave["prefix"] = self.userTypesReversed[child.text]
                child.disabled = True
            elif child.id == "office" + (instance.id).replace("editButton", ""):
                userToSend["office"] = self.roomNamesReversed[child.text]
                self.userToSave["office"] = self.roomNamesReversed[child.text]
                child.disabled = True
            elif child.id == instance.id:
                self.edit_mode(child)
                child.unbind(on_press=self.save_changes)
                child.bind(on_press=self.edit_button_click)
            elif child.id == (instance.id).replace("editButton", "deleteButton"):
                child.disabled = True
            elif child.id == (instance.id).replace("editButton", "cancelButton"):
                child.disabled = True

        for user in self.userList:
            if 'id' in user:
                if user["id"] == self.userToSave["id"]:
                    user["first_name"] = self.userToSave["first_name"]
                    user["last_name"] = self.userToSave["last_name"]
                    user["prefix"] = self.userToSave["prefix"]
                    user["office"] = self.userToSave["office"]
        serverCon.update('user', self.userToSave)

    def on_enter(self):
        self.ids.UserGrid.clear_widgets()
        self.ids.EditUserBox.clear_widgets()
        self.roomList = serverCon.select_all('room')
        for user in self.userList:
            if 'id' in user:
                typeSpinner = Spinner(id="prefix" + user['id'], disabled='true', size_hint_y=None, height=35, font_size=15, size_hint_max_x=270, text=self.userTypes[user['prefix']])
                typeSpinner.values = self.userTypes.values()
                self.ids.UserGrid.add_widget(typeSpinner)

                self.ids.UserGrid.add_widget(TextInput(text=user['first_name'], disabled='true', id="first_name" + user['id'], height=35, font_size=15, size_hint_y=None, size_hint_max_x=250))
                self.ids.UserGrid.add_widget(TextInput(text=user['last_name'], disabled='true', id="last_name" + user['id'], height=35,font_size=15, size_hint_y=None, size_hint_max_x=250))

                offcSpinner = Spinner(id="office" + user['id'], disabled='true', height=35, font_size=15, size_hint_y=None, size_hint_max_x=270, text=self.roomNames[user['office']])
                offcSpinner.values = self.roomNames.values()
                self.ids.UserGrid.add_widget(offcSpinner)
                editButton = Button(text="Edit", id="editButton" + user['id'], height=35, font_size=15, size_hint_y=None, size_hint_max_x=220)
                editButton.bind(on_press=self.edit_button_click)
                self.ids.UserGrid.add_widget(editButton)
                cancelButton = Button(text="Cancel", id="cancelButton" + user['id'], disabled="true", height=35, font_size=15, size_hint_y=None, size_hint_max_x=220)
                cancelButton.bind(on_press=self.cancel_button_click)
                self.ids.UserGrid.add_widget(cancelButton)
                deleteButton = Button(text="Delete", id="deleteButton" + user['id'], disabled='true', height=35, font_size=15,
                                      size_hint_y=None, size_hint_max_x=220)
                deleteButton.bind(on_press=self.delete_button_click)
                self.ids.UserGrid.add_widget(deleteButton)

        self.ids.EditUserBox.add_widget(Button(text="Add New User", background_normal='',
                                               background_color=(1, .78, .17, 1), color=(0, 0, 0, 1), size_hint_y=.15,
                                               size_hint_max_y=20, size_hint_max_x=800, on_press=self.change_screen))
