from kivymd.uix.screen import MDScreen

import os
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
from config import DB



Builder.load_string("""
<AddCategoryScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Name:'

            MDTextField:
                id: name_textbox
                text: ''
                pos_hint: { 'center_x': .5, 'center_y': .5, }

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Parent Category:'

            MDDropDownItem:
                id: button_category
                text: 'Select parent category'
                pos_hint: { 'center_x': .5, 'center_y': .5, }
                on_release: root.category_menu.open()

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Is income:'

            MDCheckbox:
                id: is_income_checkbox
                pos_hint: { 'center_x': .5, 'center_y': .5, }

        MDBoxLayout:
            orientation: 'horizontal'

            MDRectangleFlatButton:
                text: 'Exit'
                on_press: root.on_press_button_exit_transaction(self)
                pos_hint: { 'center_x': .5, 'center_y': .5, }
                size_hint: (.5, 1)

            MDRectangleFlatButton:
                text: 'Save'
                on_press: root.on_press_button_save_transaction(self)
                pos_hint: { 'center_x': .5, 'center_y': .5, }
                size_hint: (.5, 1)

""")

class AddCategoryScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories = DB.get_categories()

        self.selected_category_i = 0

        self.ids.button_category.set_item(self.categories[self.selected_category_i]['category_name'])

        self.category_menu = MDDropdownMenu(
            caller=self.ids.button_category,
            position="auto",
            items=[{
                'text': self.categories[i]['category_name'],
                'viewclass': 'MDDropDownItem',
                "on_release":
                    lambda i=i: self.category_menu_callback(i, self.categories[i]['category_name']),
            } for i in range(len(self.categories))]
        )

    def category_menu_callback(self, i, category_name):
        self.category_menu.dismiss()

        self.selected_category_i = i
        self.ids.button_category.set_item(category_name)
        self.ids.is_income_checkbox.active = self.categories[self.selected_category_i]['category_is_income']

    def on_press_button_exit_transaction(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'CategoriesScreen'

    def on_press_button_save_transaction(self, save):
        category_name = self.ids.name_textbox.text
        category_parent_id = self.categories[self.selected_category_i]['category_id']
        category_is_income = self.ids.is_income_checkbox.active
        DB.insert_category(category_name, category_is_income, category_parent_id)

        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'CategoriesScreen'


if __name__ == '__main__':
    class MainApp(MDApp):
        def build(self):
            screen_manager = ScreenManager()
            screen_manager.add_widget(AddCategoryScreen(name='AddCategoryScreen'))
            return screen_manager

    MainApp().run()
