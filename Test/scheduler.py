from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout

# KV = '''
# <Content>
#     orientation: "vertical"
#     spacing: "12dp"
#     size_hint_y: None
#     height: "200dp"

#     MDTextField:
#         id: date_input
#         hint_text: "Date"
#         on_focus: app.show_date_picker()

#     MDTextField:
#         id: time_input
#         hint_text: "Time(HH:MM)"

#     MDTextField:
#         id: name_input
#         hint_text: "Name"

# MDFloatLayout:
#     BoxLayout:
#         orientation: 'vertical'
#         MDRaisedButton:
#             text: "Add Appointment"
#             size_hint_y: None
#             height: "48dp"
#             on_release: app.save_appointment()
#         Label:
#             id: appointments_label
#             text: 'Appointments:'
#             color :0,0,1,1
# '''

class Content(BoxLayout):
    def clear_fields(self):
        self.ids.date_input.text = ''
        self.ids.time_input.text = ''
        self.ids.name_input.text = ''

class SchedulerScreen(Screen):
    def __init__(self, **kwargs):
        super(SchedulerScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        self.date_input = MDTextField(hint_text="Date")
        self.date_input.bind(on_focus=self.show_date_picker)
        time_input = MDTextField(hint_text="Time(HH:MM)")
        name_input = MDTextField(hint_text="Name")
        add_button = MDRaisedButton(text="Add Appointment", on_release=self.save_appointment)
        appointments_label = MDLabel(text='Appointments:', halign='center')

        layout.add_widget(self.date_input)
        layout.add_widget(time_input)
        layout.add_widget(name_input)
        layout.add_widget(add_button)
        layout.add_widget(appointments_label)

        self.add_widget(layout)

    def show_date_picker(self, instance, value):
        if value:
            date_dialog = MDDatePicker(callback=self.set_date)
            date_dialog.open()

    def set_date(self, instance, value, date_range):
        date_input = self.ids.date_input
        date_input.text = value.strftime('%Y-%m-%d')

    def save_appointment(self, instance):
        date_str = self.dialog.content_cls.ids.date_input.text
        time_str = self.dialog.content_cls.ids.time_input.text
        name = self.dialog.content_cls.ids.name_input.text
        try:
            appointment_time = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            self.scheduler.schedule_appointment(appointment_time, name)
            self.update_appointments_label()
            self.dialog.dismiss()
        except ValueError:
            self.show_error_popup('Invalid Date/Time Format')

    def show_error_popup(self, message):
        error_dialog = MDDialog(title='Error', text=message, size_hint=(0.5, 0.5))
        error_dialog.open()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        switch_screen_button = MDRaisedButton(text="Go to Scheduler Screen", on_release=self.switch_screen)
        layout.add_widget(switch_screen_button)
        self.add_widget(layout)

    def switch_screen(self, instance):
        self.manager.current = 'scheduler'


class SchedulerApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SchedulerScreen(name='scheduler'))
        return sm

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, item, priority):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda x: x[0])

    def pop(self):
        if self.queue:
            return self.queue.pop(0)[1]
        else:
            return None

    def peek(self):
        if self.queue:
            return self.queue[0][1]
        else:
            return None

    def remove(self, item):
        self.queue = [(priority, value) for priority, value in self.queue if value != item]

class AppointmentScheduler:
    def __init__(self):
        self.appointments = PriorityQueue()

    def schedule_appointment(self, appointment_time, patient_name):
        self.appointments.push((appointment_time, patient_name), appointment_time)

    def cancel_appointment(self, appointment_time, patient_name):
        self.appointments.remove((appointment_time, patient_name))

    def next_appointment(self):
        return self.appointments.peek()

if __name__ == '__main__':
    SchedulerApp().run()
