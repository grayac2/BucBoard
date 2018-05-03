from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from Server.ServerAPI.serverconn import insert, select_all
import uuid

Builder.load_file("addClass.kv")


class AddClassWidget(Screen):

    professor_list = ['']
    professors = select_all("user")  # Return professor JSON objects
    room_list = ['']
    rooms = select_all("room")  # Return building JSON objects
    classNameTextBox = TextInput()
    crnTextBox = TextInput()
    sectionTextBox = TextInput()
    startTimeTextBox = TextInput()
    endTimeTextBox = TextInput()
    hostTextBox = Spinner()
    classRoomTextBox = Spinner()

    def on_enter(self):
        self.ids.form_layout.clear_widgets()
        self.professor_list = ['']
        self.professors = select_all("user")  # Return professor JSON objects
        self.room_list = ['']
        self.rooms = select_all("room")  # Return building JSON objects
        for professor in self.professors:  # for each returned professor...
            if professor['message_type'] != 1 and professor['prefix'] == '112':  # Check message type & filter for profs
                self.professor_list.append(
                    professor['last_name'] + ', ' + professor['first_name'])  # add professor name to list

        for room in self.rooms:  # for each returned building...
            if room['message_type'] != 1:  # Check for message type
                self.room_list.append(room['room_num'])  # add room number to list

        self.classNameTextBox = TextInput(size_hint_y=None, height=35, font_size='20sp', write_tab=False,
                                          multiline=False)
        self.crnTextBox = TextInput(size_hint_y=None, height=35, font_size='20sp', write_tab=False, multiline=False)
        self.sectionTextBox = TextInput(size_hint_y=None, height=35, font_size='20sp', write_tab=False, multiline=False)
        self.startTimeTextBox = TextInput(size_hint_y=None, height=35, font_size='20sp', write_tab=False,
                                          multiline=False)
        self.endTimeTextBox = TextInput(size_hint_y=None, height=35, font_size='20sp', write_tab=False, multiline=False)
        self.hostTextBox = Spinner(size_hint_y=None, height=35, font_size='20sp', values=self.professor_list)
        self.classRoomTextBox = Spinner(size_hint_y=None, height=35, font_size='20sp', values=self.room_list)

        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              text='Class Name', font_size='25sp'))
        self.ids.form_layout.add_widget(self.classNameTextBox)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              size_hint_min_x=260, text='Classroom Number', font_size='25sp'))
        self.ids.form_layout.add_widget(self.classRoomTextBox)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              text='CRN', font_size='25sp'))
        self.ids.form_layout.add_widget(self.crnTextBox)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              text='Section Number', font_size='25sp'))
        self.ids.form_layout.add_widget(self.sectionTextBox)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              text='Professor or Host', font_size='25sp'))
        self.ids.form_layout.add_widget(self.hostTextBox)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              text='Start Time', font_size='25sp'))
        self.ids.form_layout.add_widget(self.startTimeTextBox)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None, height=35,
                                              text='End Time', font_size='25sp'))
        self.ids.form_layout.add_widget(self.endTimeTextBox)

    def submit_new_classroom(self, *args):
        professor_id = ''
        for professor in AddClassWidget.professors:
            if professor['message_type'] != 1 and professor['prefix'] == '112':
                if professor['last_name'] + ', ' + professor['first_name'] == self.hostTextBox.text:
                    professor_id = professor['id']

        room_id = ''
        for room in AddClassWidget.rooms:
            if room['message_type'] != 1:
                if room['room_num'] == self.classRoomTextBox.text:
                    room_id = room['id']

        class_name_text_box = self.classNameTextBox.text
        crn_text_box = self.crnTextBox.text
        section_text_box = self.crnTextBox.text
        start_time_text_box = self.startTimeTextBox.text
        end_time_text_box = self.endTimeTextBox.text

        unique_id = uuid.uuid4()

        popup = Popup(content=Label(text='Data to be sent to DB:\n'
                                         'Class Name: ' + class_name_text_box + '\n'
                                         'Classroom ID: ' + room_id + '\n'
                                         'CRN: ' + crn_text_box + '\n'
                                         'Section: ' + section_text_box + '\n'
                                         'Professor/Host: ' + professor_id + '\n'
                                         'Start Time: ' + start_time_text_box + '\n'
                                         'End Time: ' + end_time_text_box + '\n'
                                         'UID: ' + str(unique_id)), size_hint=(None, None), size=(400, 400))
        # popup.open()

        new_class = {
            "name": class_name_text_box,
            "crn": crn_text_box,
            "section": section_text_box,
            "start": start_time_text_box,
            "end": end_time_text_box,
            "professor": professor_id,
            "room_num": room_id
        }

        insert("class", new_class)

        self.classNameTextBox.text = ''
        self.crnTextBox.text = ''
        self.startTimeTextBox.text = ''
        self.endTimeTextBox.text = ''
