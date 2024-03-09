from kivymd.app import MDApp
import visual as vs
# import predictor as pr
from predictor import Prediction
from kivy.core.window import Window

Window.size = (360, 640)


class MyMainApp(MDApp):
    symptoms_list = []
    pr = Prediction()
    predictor_window = None
    scheduler_window = None
    doctor_window = None
    hospital_window = None
    symptoms_window = None
    about_window = None

    def build(self):
        wm = vs.WindowManager()
        self.predictor_window = vs.PredictorWindow(name='predictor')
        self.scheduler_window = vs.SchedulerWindow(name='scheduler')
        self.hospital_window = vs.HospitalWindow(name='hospital')
        self.symptoms_window = vs.SymptomsWindow(name='symptoms')
        self.doctor_window = vs.DoctorWindow(name='doctor')
        self.data_window = vs.DataWindow(name='data')
        self.blood_window = vs.BloodWindow(name='blood')
        self.graph_window = vs.GraphWindow(name='graph')
        self.month_window = vs.MonthWindow(name='month')
        self.about_window = vs.AboutWindow(name = 'about')
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        wm.add_widget(vs.HomeWindow(name='home'))
        wm.add_widget(self.predictor_window)
        wm.add_widget(self.doctor_window)
        wm.add_widget(self.scheduler_window)
        wm.add_widget(self.hospital_window)
        wm.add_widget(self.symptoms_window)
        wm.add_widget(self.data_window)
        wm.add_widget(self.blood_window)
        wm.add_widget(self.graph_window)
        wm.add_widget(self.month_window)
        wm.add_widget(self.about_window)
        return wm

    def on_start(self):
        self.symptoms_list = list(self.pr.get_columns())
        if self.predictor_window:
            self.predictor_window.on_enter()
        if self.scheduler_window:
            self.scheduler_window.on_enter()
        if self.doctor_window:
            self.doctor_window.on_enter()
        if self.hospital_window:
            self.hospital_window.on_enter()
        if self.symptoms_window:
            self.symptoms_window.on_enter()
        if self.data_window:
            self.data_window.on_enter()
        if self.blood_window:
            self.blood_window.on_enter()
        if self.graph_window:
            self.graph_window.on_enter()
        if self.month_window:
            self.month_window.on_enter()


if __name__ == "__main__":
    MyMainApp().run()
