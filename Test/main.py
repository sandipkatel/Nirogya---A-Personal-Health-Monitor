from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from schedular_backend import AppointmentScheduler

KV_FILENAME = "schedular_frontend.kv"

class Content(BoxLayout):
    pass

class SchedulerApp(MDApp):
    dialog = None
    
    def build(self):
        self.scheduler = AppointmentScheduler()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        Builder.load_file(KV_FILENAME)
        return Content()

    def save_appointment(self):
        date_str = self.root.ids.date_input.text
        time_str = self.root.ids.time_input.text
        name = self.root.ids.name_input.text
        try:
            appointment_time = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            self.scheduler.schedule_appointment(appointment_time, name)
            self.update_appointments_label()
            self.dialog.dismiss()
        except ValueError:
            self.show_error_popup('Invalid Date/Time Format')

    def update_appointments_label(self):
        appointments = self.scheduler.appointments
        appointment_texts = [f'{app[0]} - {app[1]}' for app in appointments]
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
        self.dialog.dismiss()

    def on_save(self, instance, value, date_range):
        try:
            self.root.ids.date_input.text = str(value)  
        except ValueError:
            self.show_error_popup('Invalid Date Format')

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

if __name__ == '__main__':
    SchedulerApp().run()
