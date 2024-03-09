from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
#from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivymd.uix.list import TwoLineListItem, OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from scheduler import AppointmentScheduler
from datetime import datetime, date
from predictor import Prediction, Detail
from functools import partial
import ast,webbrowser,csv, requests
import pandas as pd
from datetime import datetime
import subprocess
from kivymd.uix.datatables import MDDataTable
import file as fi
from kivy.uix.anchorlayout import AnchorLayout
from display import draw

today = datetime.today()

formatted_date = today.strftime("%Y/%m/%d")



class BackgroundLayout(FloatLayout):
    pass


class HomeWindow(Screen):
    pass


class PredictorWindow(Screen):
    selected_symptoms = []
    def predict_disease(self):
        pr = Prediction()
        #selected_symptoms = [self.ids[symptom + '_label'].text for symptom in MDApp.get_running_app().symptoms_list if
          #                   self.ids[symptom + '_checkbox'].active]
        if self.selected_symptoms:
            result = pr.predict_dis(self.selected_symptoms)
            self.ids.disease_label.text = result
        else:
            self.ids.disease_label.text = "Please select at least one symptom."

        self.selected_symptoms = []
        self.ids.symptom_list.clear_widgets()

    def on_enter(self):
        self.selected_symptoms = []
        self.ids.symptom_list.clear_widgets()
        
        pass
        """ symptoms_list = MDApp.get_running_app().symptoms_list

        if symptoms_list:
            self.ids.symptom_container.clear_widgets()

            for symptom in symptoms_list:
                symptom_layout = BoxLayout(
                    orientation='horizontal', size_hint_y=None, height=dp(20))

                label = Label(text=symptom, size_hint_x=0.8)
                checkbox = CheckBox()

                self.ids[symptom + '_label'] = label
                self.ids[symptom + '_checkbox'] = checkbox
                symptom_layout.add_widget(label)
                symptom_layout.add_widget(checkbox)

                self.ids.symptom_container.add_widget(symptom_layout)
        else:
            print("Symptoms list is empty or None") """

    def show_add_symptom_dropdown(self):
        if hasattr(self, 'dropdown_menu') and isinstance(self.dropdown_menu, MDDropdownMenu):
            self.dropdown_menu.dismiss()
        searchText = self.ids.diseaseTextField.text
        symptoms_list = MDApp.get_running_app().symptoms_list
        search_items = [
    {
        "text": symptom,
        "on_release": lambda symptom=symptom: self.addSymptom(symptom),
    }for symptom in symptoms_list if searchText.lower() in symptom.lower()
        ]
        self.dropdown_menu = MDDropdownMenu(
            caller=self.ids.diseaseTextField, items=search_items
        )
        self.dropdown_menu.open()

    def addSymptom(self, symptom):
        self.selected_symptoms.append(symptom)
        symptomText = str(len(self.selected_symptoms)) + ". " + symptom
        list_item = OneLineListItem(text=symptomText)
        self.ids.symptom_list.add_widget(list_item)
        self.ids.diseaseTextField.text = ""
        self.dropdown_menu.dismiss()

class SymptomOptionField(ButtonBehavior, BoxLayout):
    selected = BooleanProperty(False)
    symptom = StringProperty("")

    def __init__(self, symptom, **kwargs):
        super(SymptomOptionField, self).__init__(**kwargs)
        self.symptom = symptom
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.label = MDLabel(text=symptom, size_hint_x=None, width=dp(150))
        self.add_widget(self.label)
        self.toggle_selection_color()

    def toggle_selection_color(self):
        if self.selected:
            self.label.color = (0, 0, 0, 1)  # Change text color when selected
            self.background_color = (0.3, 0.3, 0.3, 1)  # Change background color when selected
        else:
            self.label.color = (1, 1, 1, 1)  # Restore text color when deselected
            self.background_color = (1, 1, 1, 1)  # Restore background color when deselected

    def on_release(self):
        self.selected = not self.selected
        self.toggle_selection_color()


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
    dropdown_menus = {}
    def on_enter(self):
        self.ids.hospitalList.clear_widgets()
        nameList = self.readData("dataset\hospitals.csv")
        for name, address in zip(nameList[0], nameList[1]):
            
            item = TwoLineListItem(
            text=name,
            secondary_text = address
                            )
            button = MDFlatButton(text = "[color=#0000ff]view in map[/color]", pos_hint = {"top": 0.6, 'x': 0.95},
                                   on_release= partial(self.view_in_map, name))
            item.add_widget(button)
            self.ids.hospitalList.add_widget(item)
    
            
    
    def view_in_map(self, name, *args):
        nameList = self.readData("dataset\hospitals.csv")
        for names in nameList[0]:
            if name == names:
                nameIndex = nameList[0].index(names)
                latlon = nameList[-1][nameIndex]
                latlon = ast.literal_eval(latlon)
                lat = latlon[0]
                lon = latlon[1]
                url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                webbrowser.open(url)

    
    def show_sort_popup(self):
        sort_items = [
            {
                "text": "sort by name",
                "on_release": lambda: self.sort_by_name(),
            },
             {
                "text": "sort by distance",
                "on_release": lambda: self.sort_by_distance(),
            } 
        ]
        MDDropdownMenu(
            caller=self.ids.sort, items=sort_items
        ).open()

    def sort_by_name(self):
        self.ids.hospitalList.clear_widgets()
        nameList = self.read_csv("dataset\hospitals.csv")
        self.merge_sort(nameList, key='Name')
        self.write_csv("dataset\hospitalstd.csv",nameList)
        
        nameList = self.readData("dataset\hospitalstd.csv")
        for name, address in zip(nameList[0], nameList[1]):
            
            item = TwoLineListItem(
            text=name,
            secondary_text = address
                            )
            button = MDFlatButton(text = "[color=#0000ff]view in map[/color]", pos_hint = {"top": 0.6, 'x': 0.95},
                                   on_release= partial(self.view_in_map, name))
            item.add_widget(button)
            self.ids.hospitalList.add_widget(item)
        
    
    def sort_by_distance(self):
        add = requests.get("https://api.ipify.org").text 
        url = "https://get.geojs.io/v1/ip/geo/" + add + ".json"
        geo_request = requests.get(url)
        geo_data = geo_request.json()
        g=[float(geo_data['latitude']), float(geo_data['longitude'])]
        #g=[27.664077, 85.341975] 
        df = pd.read_csv("dataset\hospitals.csv", encoding="ISO-8859-1")
        nameList = self.readData("dataset\hospitals.csv")
        distanceList = []
        for coordinates in nameList[3]:
            coordinates = ast.literal_eval(coordinates)
            distance = ((g[0]- coordinates[0])**2 + (g[1]- coordinates[1])**2)**(1/2)
            distanceList.append(distance)
        df['distance'] = distanceList
        df.to_csv("dataset\hospitalstd.csv", index=False)

        self.ids.hospitalList.clear_widgets()
        nameList = self.read_csv("dataset\hospitalstd.csv")
        self.merge_sort(nameList, key='distance')
        self.write_csv("dataset\hospitalstd.csv",nameList)
        
        nameList = self.readData("dataset\hospitalstd.csv")
        for name, address in zip(nameList[0], nameList[1]):
            
            item = TwoLineListItem(
            text=name,
            secondary_text = address
                            )
            button = MDFlatButton(text = "[color=#0000ff]view in map[/color]", pos_hint = {"top": 0.6, 'x': 0.95},
                                   on_release= partial(self.view_in_map, name))
            item.add_widget(button)
            self.ids.hospitalList.add_widget(item)
        
        

    def searchHospital(self, searchIndex):
        searchText = self.ids.search_hospital.text
        self.ids.hospitalList.clear_widgets()
        nameList = self.readData("dataset\hospitals.csv")
        for name, address in zip(nameList[0], nameList[1]):
            searchWhat = name if searchIndex == 0 else address
            if searchText.lower() in searchWhat.lower():
                item = TwoLineListItem(
                text=name,
                secondary_text = address
                                )
                button = MDFlatButton(text = "[color=#0000ff]view in map[/color]",  pos_hint = {"top": 0.6, 'x': 0.95},
                                    on_release= partial(self.view_in_map, name))
                item.add_widget(button)
                self.ids.hospitalList.add_widget(item)
    
    def toggleSearch(self):

        if self.ids.search_hospital.hint_text == "Search by Address":
            self.ids.search_hospital.hint_text = "Search by Name"
        else:
            self.ids.search_hospital.hint_text= "Search by Address"

    

    def readData(self, filename):
        df = pd.read_csv(filename, encoding="ISO-8859-1")
        data_list = df.T.values.tolist()
        return data_list
          
    def on_start(self):
        pass

    def merge_sort(self, arr, key):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            self.merge_sort(left_half, key)
            self.merge_sort(right_half, key)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i][key] < right_half[j][key]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1

    def read_csv(self,filename):
        data = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
        
    def write_csv(self,filename, data):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


class ContentDialog(Popup):
    def __init__(self, title='', content_cls=None, buttons=[], **kwargs):
        super(ContentDialog, self).__init__(**kwargs)
        self.title = title
        self.content_cls = content_cls
        self.buttons = buttons


class ContentDialog(Popup):
    def __init__(self, title='', content_cls=None, buttons=[], **kwargs):
        super(ContentDialog, self).__init__(**kwargs)
        self.title = title
        self.content_cls = content_cls
        self.buttons = buttons


class WindowManager(ScreenManager):
    pass



class DataWindow(Screen):
    def on_enter(self):
        pass

    def __init__(self, **kw):
        super().__init__(**kw)
        layout=AnchorLayout()
        table = MDDataTable(
            pos_hint={'center_x': 0.6, 'top': 0.2},
            size_hint=(1, 1),
            column_data=[
                ("SN.", dp(30)),
                ("NAME", dp(30)),
                ("RANGE", dp(30)),
                ("UNIT", dp(30))
                            
            ],
            row_data=[
                ["1", "Pressure", "120/80","mm/HG"],
                ["2", "Weight", "50","kg"],
                ["3", "Screen tiime","2-4", "hour"],
                ["4", "Water intake","2-4", "litre"]
            ]
        )
        layout.add_widget(table)

    def click(self):
        if(self.ids.pressure.text!= ''):
            string=formatted_date+":"+self.ids.pressure.text+" mmHg"+"\n"
            fi.update_last_line("dependecies\Pressure.txt", string)


        if(self.ids.weight.text!= ''):
            string=formatted_date+":"+self.ids.weight.text+"\n"
            fi.update_last_line("dependecies\Weight.txt", string)

        if(self.ids.screen.text!= ''):
            string=formatted_date+":"+self.ids.screen.text+"\n"
            fi.update_last_line("dependecies\Screen.txt", string)

        if(self.ids.water.text!= ''):
            string=formatted_date+":"+self.ids.water.text+"\n"
            fi.update_last_line("dependecies\Water.txt", string)



class BloodWindow(Screen):
    def on_enter(self):
        pass

    def __init__(self, **kw):
        super().__init__(**kw)


    def clickk(self):
        if(self.ids.RBC.text!= ''):
            string=formatted_date+":"+self.ids.RBC.text+"\n"
            fi.update_last_line("dependecies\RBC.txt", string)


        if(self.ids.WBC.text!= ''):
            string=formatted_date+":"+self.ids.WBC.text+"\n"
            fi.update_last_line("dependecies\WBC.txt", string)

        if(self.ids.Platelets.text!= ''):
            string=formatted_date+":"+self.ids.Platelets.text+"\n"
            fi.update_last_line("dependecies\Platelets.txt", string)

        if(self.ids.Haemoglobin.text!= ''):
            string=formatted_date+":"+self.ids.Haemoglobin.text+"\n"
            fi.update_last_line("dependecies\Haemoglobin.txt", string)
        return

class GraphWindow(Screen):
    def on_enter(self):
        pass
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def click(self,button_name):
        if(button_name=="Platelets"):
            MonthWindow.what="Platelets"
            self.manager.current = "month"
        if(button_name=="Haemoglobin"):
            MonthWindow.what="Haemoglobin"
            self.manager.current = "month"
        if(button_name=="WBC"):
            MonthWindow.what="WBC"
            self.manager.current = "month"
        if(button_name=="RBC"):
            MonthWindow.what="RBC"
            self.manager.current = "month"
        if(button_name=="Weight"):
            MonthWindow.what="Weight"
            self.manager.current = "month"
        if(button_name=="Pressure"):
            MonthWindow.what="Pressure"
            self.manager.current = "month"
        if(button_name=="Screen"):
            MonthWindow.what="Screen"
            self.manager.current = "month"
        if(button_name=="Water"):
            MonthWindow.what="Water"
            self.manager.current = "month"

class MonthWindow(Screen):
    what= None
    def on_enter(self):
        pass
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def click(self,button_name):
        if(button_name=="January"):
            draw(self.what,button_name)
        if(button_name=="February"):
            draw(self.what,button_name)
        if(button_name=="March"):
            draw(self.what,button_name)
        if(button_name=="April"):
            draw(self.what,button_name)
        if(button_name=="May"):
            draw(self.what,button_name)
        if(button_name=="June"):
            draw(self.what,button_name)
        if(button_name=="July"):
            draw(self.what,button_name)
        if(button_name=="August"):
            draw(self.what,button_name)
        if(button_name=="September"):
            draw(self.what,button_name)
        if(button_name=="October"):
            draw(self.what,button_name)
        if(button_name=="November"):
            draw(self.what,button_name)
        if(button_name=="December"):
            draw(self.what,button_name)


# Load the kv file
kv = Builder.load_file("style.kv")
