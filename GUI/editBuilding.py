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

Builder.load_file('editBuilding.kv')

# Create our initial Popup that will show the user what information they input that will be sent to the DB.
popup = Popup(title='Success!',
                    content=Label(text='Hello world'),
                    size_hint=(None, None), size=(200, 200))


'''
AddBuildingWidget
This widget serves as the page to add buildings to the System.
'''


class EditBuildingWidget(Screen):
    bldgToSave = {'id': '', 'name': '', 'campus': ''}
    bldg = {'id': '', 'name': '', 'name': ''}
    bldgList = serverCon.select_all('building')
    campusList = serverCon.select_all('campus')
    campusNames = {}
    campusNamesReversed = {}
    for campus in campusList:
        if 'name' in campus:
            campusNames[campus['id']] = campus['name']
            campusNamesReversed[campus['name']] = campus['id']

    def change_screen(self, instance):
        self.parent.current = 'addBuilding'

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
        for building in self.bldgList:
            if 'name' in building:
                if building['id'] == idToDelete:
                    self.bldgList.remove(building)
        for child in self.ids.BuildingGrid.children:
            if child.id == "name" + (instance.id).replace("deleteButton", ""):
                self.ids.BuildingGrid.remove_widget(child)
        for child in self.ids.BuildingGrid.children:
            if child.id == "campus" + (instance.id).replace("deleteButton", ""):
                self.ids.BuildingGrid.remove_widget(child)
        for child in self.ids.BuildingGrid.children:
            if child.id == (instance.id).replace("deleteButton", "editButton"):
                self.ids.BuildingGrid.remove_widget(child)
        for child in self.ids.BuildingGrid.children:
            if child.id == (instance.id).replace("deleteButton", "cancelButton"):
                self.ids.BuildingGrid.remove_widget(child)
        for child in self.ids.BuildingGrid.children:
            if child.id == instance.id:
                self.ids.BuildingGrid.remove_widget(child)

    '''
    edit_button_click(instance)
    Parameters: instance: the edit/save button that was clicked. 
    Purpose:    Unlocks the editable fields and the delete button. Changes the edit button's text to "Save"
    '''
    def edit_button_click(self, instance):
        for child in self.ids.BuildingGrid.children:
            if child.id == "name" + (instance.id).replace("editButton", ""):
                self.bldgToSave['name'] = child.text
                self.bldgToSave["id"] = (instance.id).replace("editButton", "")
                child.disabled = False
            elif child.id == "campus" + (instance.id).replace("editButton", ""):
                self.bldgToSave["campus"] = self.campusNamesReversed[child.text]
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
        for child in self.ids.BuildingGrid.children:
            if child.id == "name" + (instance.id).replace("cancelButton", ""):
                child.text = self.bldgToSave["name"]
                child.disabled = True
            elif child.id == "campus" + (instance.id).replace("cancelButton", ""):
                child.text = self.campusNames[self.bldgToSave["campus"]]
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
        roomToSend = {'room_num': '', 'message_type': '', 'type': '', 'id': '', 'building': ''};
        for child in self.ids.BuildingGrid.children:
            if child.id == "name" + (instance.id).replace("editButton", ""):
                roomToSend["name"] = child.text
                self.bldgToSave["name"] = child.text
                child.disabled = True
            elif child.id == "campus" + (instance.id).replace("editButton", ""):
                roomToSend["campus"] = child.text
                self.bldgToSave["campus"] = self.campusNamesReversed[child.text]
                child.disabled = True
            elif child.id == instance.id:
                self.edit_mode(child)
                child.unbind(on_press=self.save_changes)
                child.bind(on_press=self.edit_button_click)
            elif child.id == (instance.id).replace("editButton", "deleteButton"):
                child.disabled = True
            elif child.id == (instance.id).replace("editButton", "cancelButton"):
                child.disabled = True

        for building in self.bldgList:
            if 'number' in building:
                if building["id"] == self.bldgToSave["id"]:
                    building["campus"] = int(self.bldgToSave["campus"])
                    building["name"] = self.bldgToSave["name"]
        serverCon.update('building', self.bldgToSave)

        # popup = Popup(content=Label(text='Data to be sent to DB:\n'
        #                                  'Type: ' + self.roomToSave["type"] + '\n'
        #                                  'Number: ' + self.roomToSave["room_num"] + '\n'
        #                                 'Building Name: ' + self.roomToSave["building"] + '\n'
        #                             ), size_hint=(None, None), size=(400, 400))
        # popup.open()


    def on_enter(self):
        self.ids.BuildingGrid.clear_widgets()
        self.ids.EditBuildingBox.clear_widgets()
        self.bldgList = serverCon.select_all('building')
        self.campusList = serverCon.select_all('campus')
        for building in self.bldgList:
            if 'name' in building:
                campusSpinner = Spinner(id="campus" + building['id'], disabled='true', size_hint_y=None, height=35, font_size=15, size_hint_max_x=270, text=self.campusNames[building['campus']])

                campusSpinner.values = self.campusNames.values()

                self.ids.BuildingGrid.add_widget(campusSpinner)

                self.ids.BuildingGrid.add_widget(TextInput(text=building['name'], disabled='true', id="name" + building['id'], height=35, font_size=15, size_hint_y=None, size_hint_max_x=250))

                editButton = Button(text="Edit", id="editButton" + building['id'], height=35, font_size=15, size_hint_y=None, size_hint_max_x=220)

                editButton.bind(on_press=self.edit_button_click)

                self.ids.BuildingGrid.add_widget(editButton)

                cancelButton = Button(text="Cancel", id="cancelButton" + building['id'], disabled="true", height=35, font_size=15, size_hint_y=None, size_hint_max_x=220)

                cancelButton.bind(on_press=self.cancel_button_click)

                self.ids.BuildingGrid.add_widget(cancelButton)

                deleteButton = Button(text="Delete", id="deleteButton" + building['id'], disabled='true', height=35, font_size=15,
                                      size_hint_y=None, size_hint_max_x=220)

                deleteButton.bind(on_press=self.delete_button_click)

                self.ids.BuildingGrid.add_widget(deleteButton)

        self.ids.EditBuildingBox.add_widget(Button(text="Add New Building", background_normal='',
                                                   background_color=(1, .78, .17, 1), color=(0, 0, 0, 1),
                                                   size_hint_y=.15, size_hint_max_y=20, size_hint_max_x=800,
                                                   on_press=self.change_screen))

