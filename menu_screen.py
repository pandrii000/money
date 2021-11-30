from kivymd.uix.screen import MDScreen
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


Builder.load_string("""
<MenuScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDRectangleFlatButton:
            text: 'Transactions'
            pos_hint: { 'center_x': .5, 'center_y': .5, }
            size_hint: (1, 1)
            on_press: root.on_transactions_button_press(self)

        MDRectangleFlatButton:
            text: 'Categories'
            pos_hint: { 'center_x': .5, 'center_y': .5, }
            size_hint: (1, 1)
            on_press: root.on_categories_button_press(self)
""")

class MenuScreen(MDScreen):

    def on_transactions_button_press(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'TransactionsScreen'

    def on_categories_button_press(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'CategoriesScreen'


if __name__ == '__main__':
    class MainApp(MDApp):
        def build(self):
            screen_manager = ScreenManager()
            screen_manager.add_widget(MenuScreen(name='MenuScreen'))
            return screen_manager
    MainApp().run()
