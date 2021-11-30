from datetime import datetime
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, MDList
from config import DB

Builder.load_string("""
<CategoriesScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1

            MDRectangleFlatButton:
                text: 'Menu'
                pos_hint_x: 0.1
                on_release: root.on_menu_button_press(self)

            MDLabel:
                text: 'Categories'
                halign: "center"
                size_hint: (.9, 1.0)

        MDBoxLayout:
            size_hint_y: 0.8
            orientation: 'vertical'

            ScrollView:

                MDList:
                    id: container

        MDRectangleFlatButton:
            text: '+'
            size_hint: (1., .1)
            on_release: root.on_add_button_press(self)
""")

class CategoriesScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.categories = DB.get_categories()
        for c in self.categories:
            self.ids.container.add_widget(
                OneLineListItem(text=c['category_name'])
            )

    def on_add_button_press(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'AddCategoryScreen'

    def on_menu_button_press(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'MenuScreen'


if __name__ == '__main__':
    class MainApp(MDApp):
        def build(self):
            screen_manager = ScreenManager()
            screen_manager.add_widget(CategoriesScreen(name='CategoriesScreen'))
            return screen_manager
    MainApp().run()
