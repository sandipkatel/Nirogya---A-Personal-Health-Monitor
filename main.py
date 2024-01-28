from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from predictor import predict_dis



Window.size = (9*38,19*38)
#Window.clearcolor=(1,1,1,1)
class HomeWindow(Screen):
    pass

class PredictorWindow(Screen):
    def predict_dis(self,symptomList):
        disease = predict_dis(symptomList)
        if disease == None:
            self.ids.disease_label.text = "No symptoms matched"
        else:
            self.ids.disease_label.text = str(list(disease.keys())[0])
        
        

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("style.kv")

class myMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    myMainApp().run()
    
#harey k ho yo