from kivy.app import App
import visual as vs
import predictor as pr


class MyMainApp(App):
    symptoms_list = []
    predictor_window = None
    scheduler_window = None

    def build(self):
        wm = vs.WindowManager()
        self.predictor_window = vs.PredictorWindow(name='predictor')
        self.scheduler_window = vs.SchedulerWindow(name='scheduler')
        wm.add_widget(vs.HomeWindow(name='home'))
        wm.add_widget(self.predictor_window)
        wm.add_widget(self.scheduler_window)
        return wm

    def on_start(self):
        self.symptoms_list = list(pr.df1.columns)
        if self.predictor_window:
            self.predictor_window.on_enter()
        if self.scheduler_window:
            self.scheduler_window.on_enter()


if __name__ == "__main__":
    MyMainApp().run()
