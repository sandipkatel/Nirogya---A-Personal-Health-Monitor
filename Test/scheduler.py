# schedular.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from datetime import datetime
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton

KV = '''
<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "200dp"
    
    MDTextField:
        id: date_input
        hint_text: "Date"
        on_focus: app.show_date_picker()
    MDTextField:
        id: time_input
        hint_text: "Time(HH:MM)"
    MDTextField:
        id: name_input
        hint_text: "Name"

MDFloatLayout:
    BoxLayout:
        orientation: 'vertical'
        MDRaisedButton:
            text: "Add Appointment"
            size_hint_y: None
            height: "48dp"
            on_release: app.show_add_appointment_popup()
        Label:
            id: appointments_label
            text: 'Appointments:'
            color :0,0,1,1
'''

class Content(BoxLayout):
    pass

class SchedulerApp(MDApp):
    dialog = None
    
    def build(self):
        self.scheduler = AppointmentScheduler()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def save_appointment(self):
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

    def update_appointments_label(self):
        appointments = self.scheduler.appointments.queue
        appointment_texts = [f'{app[1][0]} - {app[1][1]}' for app in appointments]
        if appointment_texts:
            appointments_text = '\n'.join(appointment_texts)
        else:
            appointments_text = "No appointments scheduled."
        self.root.ids.appointments_label.text = f'Appointments:\n{appointments_text}'

    def show_add_appointment_popup(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Appointment:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.on_cancel
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda *args: self.save_appointment()
                    ),
                ],
            )
        self.dialog.open()

    def show_error_popup(self, message):
        content = Label(text=message)
        error_popup = Popup(title='Error', content=content, size_hint=(None, None), size=(300, 200))
        error_popup.open()

    def on_cancel(self, *args):
        self.date_picker_open = False
        self.dialog.dismiss()

    def on_save(self, instance, value, date_range):
        try:
            self.dialog.content_cls.ids.date_input.text = str(value)  
        except ValueError:
            self.show_error_popup('Invalid Date Format')
        finally:
            self.date_picker_open = False

    def show_date_picker(self):
        if not hasattr(self, 'date_picker_open') or not self.date_picker_open:
            self.date_picker_open = True
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
            date_dialog.open()

class AppointmentScheduler:
    def __init__(self):
        self.appointments = PriorityQueue()

    def schedule_appointment(self, appointment_time, patient_name):
        self.appointments.push((appointment_time, patient_name), appointment_time)

    def cancel_appointment(self, appointment_time, patient_name):
        self.appointments.remove((appointment_time, patient_name))

    def next_appointment(self):
        return self.appointments.peek()

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

if __name__ == '__main__':
    SchedulerApp().run()
