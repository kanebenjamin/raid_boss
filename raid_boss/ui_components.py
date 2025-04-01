from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

class GameOutput(Label):
    text = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 400
        self.text_size = (400, None)

class GameInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 40
        self.multiline = False

class GameInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        
        self.output = GameOutput()
        self.scroll = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll.add_widget(self.output)
        
        self.input_box = GameInput()
        
        self.add_widget(self.scroll)
        self.add_widget(self.input_box) 