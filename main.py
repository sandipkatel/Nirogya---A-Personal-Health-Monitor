from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
import predictor as pr

Window.size = (360, 640)

class HomeWindow(Screen):
    pass

class PredictorWindow(Screen):
    def predict_disease(self):
        selected_symptoms = [self.ids[symptom + '_label'].text for symptom in App.get_running_app().symptoms_list if self.ids[symptom + '_checkbox'].active]
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

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("style.kv")

class MyMainApp(App):
    symptoms_list = []

    def build(self):
        return kv
    
    def on_start(self):
        self.symptoms_list = list(pr.df1.columns)
        predictor_window = self.root.get_screen('predictor')
        predictor_window.on_enter()

if __name__ == "__main__":
    MyMainApp().run()
