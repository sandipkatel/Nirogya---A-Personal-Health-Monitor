from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
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
import predictor as pr

Window.size = (360, 640)


class BackgroundLayout(FloatLayout):
    pass


class HomeWindow(Screen):
    pass

class RoundedButton(Button):
    pass

class PredictorWindow(Screen):
    def predict_disease(self):
        selected_symptoms = [self.ids[symptom + '_label'].text for symptom in MDApp.get_running_app().symptoms_list if
                             self.ids[symptom + '_checkbox'].active]
        if selected_symptoms:
            result = pr.predict_dis(selected_symptoms)
            self.ids.disease_label.text = result
        else:
            self.ids.disease_label.text = "Please select at least one symptom."

    def on_enter(self):
        symptoms_list = MDApp.get_running_app().symptoms_list

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

class SymptomsWindow(Screen):
    disease_label = None
    def find_symptoms(self, disease):
        self.disease_label = disease
        result = pr.dis_symptoms(disease)
        if result:
            self.ids.symptoms.text = result
            self.add_info_button()
        else:
            self.ids.symptoms.text = "Sorry, unable to find any disease in dataset."

    def add_info_button(self):
        content = BoxLayout(orientation='vertical', pos_hint={"top": 0.5, "right": 0.1}, size_hint=(None, None))        
        content.add_widget(Label(text="Do you want to see prevention and cure?"))
        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        content.add_widget(yes_button)
        content.add_widget(no_button)
        
        yes_button.bind(on_release=lambda _: self.display_additional_info(content))
        no_button.bind(on_release=lambda _: self.clear_instance(content))
        self.ids.symptoms.remove_widget(content)
        self.ids.symptoms.add_widget(content)

    def display_additional_info(self, content):
        prevention, cure = pr.get_prevention_and_cure(self.disease_label)
        self.ids.symptoms.text += prevention
        self.ids.symptoms.text += cure
        self.ids.symptoms.remove_widget(content)

    def clear_instance(self, content):
        self.ids.symptoms.remove_widget(content)
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Do you want to see prevention and cure?"))


class Content(BoxLayout):
    pass

class SchedulerWindow(Screen):
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


class HospitalWindow(Screen):
    def on_enter(self):
        pass


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
