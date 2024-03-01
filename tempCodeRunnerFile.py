    popup = Popup(title="Select a Date", size_hint=(None, None), size=(400, 400))
        date_picker = DatePicker()
        date_picker.bind(on_date=self.update_date_input)
        popup.content = date_picker
        popup.open()
