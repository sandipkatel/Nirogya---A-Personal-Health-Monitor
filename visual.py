from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from scheduler import AppointmentScheduler

Window.size = (360, 640)


class BackgroundLayout(FloatLayout):
    pass


class HomeWindow(Screen):
    pass

class RoundedButton(Button):
    pass

class PredictorWindow(Screen):
    def predict_disease(self):
        selected_symptoms = [self.ids[symptom + '_label'].text for symptom in App.get_running_app().symptoms_list if
                             self.ids[symptom + '_checkbox'].active]
        if selected_symptoms:
            result = pr.predict_dis(selected_symptoms)
            self.ids.disease_label.text = result
        else:
            self.ids.disease_label.text = "Please select at least one symptom."

    def on_enter(self):
        symptoms_list = App.get_running_app().symptoms_list

        if symptoms_list:
            self.ids.symptom_container.clear_widgets()

            for symptom in symptoms_list:
                symptom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))

                label = Label(text=symptom, size_hint_x=0.8)
                checkbox = CheckBox()

                self.ids[symptom + '_label'] = label
                self.ids[symptom + '_checkbox'] = checkbox
                symptom_layout.add_widget(label)
                symptom_layout.add_widget(checkbox)

                self.ids.symptom_container.add_widget(symptom_layout)
        else:
            print("Symptoms list is empty or None")


class SchedulerWindow(Screen):
    dialog = None
    appointments_label = ObjectProperty(None)
    date_input = ObjectProperty(None)
    time_input = ObjectProperty(None)
    name_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SchedulerWindow, self).__init__(**kwargs)
        self.scheduler = AppointmentScheduler()

    def save_appointment(self):
        date_str = self.date_input.text
        time_str = self.time_input.text
        name = self.name_input.text
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
        self.appointments_label.text = f'Appointments:\n{appointments_text}'

    def show_add_appointment_popup(self):
        if not self.dialog:
            self.dialog = ContentDialog(
                title="Add Appointment:",
                content_cls=Content(),
                buttons=[
                    Button(
                        text="CANCEL",
                        on_release=self.on_cancel
                    ),
                    Button(
                        text="OK",
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

    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.date_input = TextInput(hint_text="Date", on_focus=self.show_date_picker,
                                    size_hint=(None, None), size=(150, 48), pos_hint={"center_x": 0.5})
        layout.add_widget(self.date_input)
        return layout

    def show_date_picker(self, instance, value):
        date_picker_popup = DatePickerPopup(self.update_date_input)
        date_picker_popup.open()

    def update_date_input(self, date):
        self.date_input.text = date.strftime("%Y-%m-%d")


class ContentDialog(Popup):
    def __init__(self, title='', content_cls=None, buttons=[], **kwargs):
        super(ContentDialog, self).__init__(**kwargs)
        self.title = title
        self.content_cls = content_cls
        self.buttons = buttons


class WindowManager(ScreenManager):
    pass


# Load the kv file
kv = Builder.load_file("style.kv")
