from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from Server.ServerAPI.serverconn import insert, select_all
import uuid

Builder.load_file("addAnnouncement.kv")


class AddAnnouncementWidget(Screen):

    professor_list = ['']
    professors = select_all("user")  # Return professor JSON objects
    room_list = ['']
    rooms = select_all("room")  # Return building JSON objects
    title = TextInput()
    announcement = TextInput()
    professor = Spinner()
    roomNumber = Spinner()

    def on_enter(self):
        self.ids.form_layout.clear_widgets()
        self.professor_list = ['']
        self.professors = select_all("user")
        self.room_list = ['']
        self.rooms = select_all("room")
        for professor in self.professors:          # for each returned professor...
            if professor['message_type'] != 1 and professor['prefix'] == '112':   # Check for message type & filter for profs
                self.professor_list.append(professor['last_name'] + ', ' + professor['first_name'])  # add professor name to list

        for room in self.rooms:          # for each returned building...
            if room['message_type'] != 1:   # Check for message type
                self.room_list.append(room['room_num'])  # add name of building to buildingList

        self.professor = Spinner(size_hint_y=None, height=35, font_size='20sp', values=self.professor_list)
        self.roomNumber = Spinner(size_hint_y=None, height=35, font_size='20sp', values=self.room_list)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None,
                                              height=35, text='Professor', font_size='25sp'))
        self.ids.form_layout.add_widget(self.professor)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None,
                                              height=35, text='Room Number', font_size='25sp'))
        self.ids.form_layout.add_widget(self.roomNumber)
        self.ids.form_layout.add_widget(Label(halign='right', valign='middle', size_hint_y=None,
                                              height=35, text='Title', font_size='25sp'))
        self.title = TextInput(size_hint_y=None, height=35, font_size='20sp', write_tab=False, multiline=False)
        self.ids.form_layout.add_widget(self.title)
        self.ids.form_layout.add_widget(Label(halign='right', valign='top', size_hint_y=None,
                                              height=200, size_hint_min_x=210, text='Announcement', font_size='25sp'))
        self.announcement = TextInput(size_hint_y=None, height=200, size_hint_min_x=210, font_size='20sp')
        self.ids.form_layout.add_widget(self.announcement)

    def submit_new_announcement(self, *args):
        professor_id = ''
        for professor in AddAnnouncementWidget.professors:
            if professor['message_type'] != 1 and professor['prefix'] == '112':
                if professor['last_name'] + ', ' + professor['first_name'] == self.professor.text:
                    professor_id = professor['id']

        room_id = ''
        for room in AddAnnouncementWidget.rooms:
            if room['message_type'] != 1:
                if room['room_num'] == self.roomNumber.text:
                    room_id = room['id']

        title = self.title.text
        announcement = self.announcement.text

        unique_id = uuid.uuid4()

        popup = Popup(content=Label(text='Data to be sent to DB:\n'
                                         'Title: ' + title + '\n'
                                         'Announcement: ' + announcement + '\n'
                                         'Professor ID: ' + professor_id + '\n'
                                         'Room ID: ' + room_id + '\n'
                                         'UID: ' + str(unique_id)), size_hint=(None, None), size=(400, 400))
        # popup.open()

        new_announcement = {    # Create new announcement JSON object
            "title": title,
            "info": announcement,
            "image": '',
            "professor": professor_id,
            "room_num": room_id
        }

        insert("announcements", new_announcement)

        self.title.text = ''
        self.announcement.text = ''
