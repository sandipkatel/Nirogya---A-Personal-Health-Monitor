from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from scheduler import AppointmentScheduler
from datetime import datetime, date
from predictor import Prediction, Detail


class BackgroundLayout(FloatLayout):
    pass


class HomeWindow(Screen):
    pass

            
class SymptomCheckbox(MDCheckbox):
    def __init__(self, symptom, **kwargs):
        super(SymptomCheckbox, self).__init__(**kwargs)
        self.symptom = symptom
        self.size_hint_x = None
        self.width = dp(30)
        self.on_release = self.toggle_checkbox_color

    def toggle_checkbox_color(self):
        if self.active:
            self.color = (0, 0, 1, 1)  # Change color to red when checked
        else:
            self.color = (0, 0, 0, 1)

class PredictorWindow(Screen):
    def predict_disease(self):
        pr = Prediction()
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
                symptom_checkbox = SymptomCheckbox(symptom)
                symptom_label = MDLabel(text=symptom)

                layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
                layout.add_widget(symptom_checkbox)
                layout.add_widget(symptom_label)

                self.ids.symptom_container.add_widget(layout)


class SymptomsWindow(Screen):
    disease_label = None

    def find_info(self, disease):
        dtl = Detail()
        self.ids.all_info.clear_widgets()
        
        disease_label = disease
        result = dtl.dis_description(disease)
        if result:
            self.ids.all_info.text = result
            symptoms, prevention, cure = dtl.dis_detail()
            self.ids.all_info.text += symptoms
            self.ids.all_info.text += prevention
            self.ids.all_info.text += cure
        else:
            self.ids.all_info.text = f"Sorry, unable to find any disease named {disease} in dataset."

class Content(BoxLayout):
    pass


class SchedulerWindow(Screen):
    scheduler = AppointmentScheduler()

    def save_appointment(self):
        date_str = self.ids.date_input.text
        time_str = self.ids.time_input.text
        name = self.ids.name_input.text
        try:
            appointment_time = datetime.strptime(
                date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            self.scheduler.schedule_appointment(appointment_time, name)
            self.update_appointments_label()
        except ValueError:
            self.show_error_popup('Invalid Date/Time Format')

    def update_appointments_label(self):
        appointments = self.scheduler.appointments.queue
        appointment_texts = [
            f'{app[1][0]} - {app[1][1]}' for app in appointments]
        if appointment_texts:
            appointments_text = '\n'.join(appointment_texts)
        else:
            appointments_text = "No appointments scheduled."
        self.ids.appointments_label.text = f'Appointments:\n{appointments_text}'

    # def show_add_appointment_popup(self):
    #     self.dialog = MDDialog(
    #     title="Add Appointment:",
    #     type="custom",
    #     content_cls=Content(),

    #     )
    #     self.dialog.open()

    def show_error_popup(self, message):
        content = Label(text=message)
        error_popup = Popup(title='Error', content=content,
                            size_hint=(None, None), size=(300, 200))
        error_popup.open()

    def on_cancel_date(self, *args):
        self.date_picker_open = False

    def on_save_date(self, instance, value, date_range):
        self.ids.date_input.text = value.strftime("%Y-%m-%d")
        self.date_picker_open = False

    def on_cancel_time(self, *args):
        self.time_picker_open = False

    def on_save_time(self, instance, time):
        self.ids.time_input.text = time.strftime("%H:%M")
        self.time_picker_open = False

    def show_date_picker(self):
        if not hasattr(self, 'date_picker_open') or not self.date_picker_open:
            self.date_picker_open = True
            screen_width, screen_height = Window.size
            picker_width = screen_width * 0.8  # Adjust as needed
            picker_height = screen_height * 0.6  # Adjust as needed
            date_dialog = MDDatePicker(min_date=date.today(), max_date=date(
                date.today().year,
                date.today().month+6,
                date.today().day,
            ),
            )
            date_dialog.size_hint_max = (picker_width, picker_height)
            date_dialog.size_hint_min = (picker_width, picker_height)
            # date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_save_date,
                             on_cancel=self.on_cancel_date)
            date_dialog.open()
        

    def show_time_picker(self):
        if not hasattr(self, 'time_picker_open') or not self.time_picker_open:
            self.time_picker_open = True
            time_dialog = MDTimePicker()
            time_dialog.bind(on_save=self.on_save_time,
                             on_cancel=self.on_cancel_time)
            time_dialog.open()
        

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
