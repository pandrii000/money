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
<AddTransactionScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Balance:'
                size_hint: (1., 1.)

            MDDropDownItem:
                id: button_balance
                text: 'Select balance'
                # pos_hint: { 'center_x': .5, 'center_y': .5, }
                on_release: root.balance_menu.open()

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Category:'

            MDDropDownItem:
                id: button_category
                text: 'Select category'
                pos_hint: { 'center_x': .5, 'center_y': .5, }
                on_release: root.category_menu.open()

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Datetime:'

            MDRectangleFlatButton:
                id: button_date
                on_press: root.show_date_picker(self)
                pos_hint: { 'center_x': .5, 'center_y': .5, }

            MDRectangleFlatButton:
                id: button_time
                on_press: root.show_time_picker(self)
                pos_hint: { 'center_x': .5, 'center_y': .5, }

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Amount:'

            MDTextField:
                id: amount_textbox
                text: '0.0'
                pos_hint: { 'center_x': .5, 'center_y': .5, }

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Is income:'

            MDCheckbox:
                id: is_income_checkbox
                pos_hint: { 'center_x': .5, 'center_y': .5, }

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Description:'

            MDTextField:
                id: description_textbox
                text: ''
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

class AddTransactionScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.button_date.text = datetime.now().strftime('%Y-%m-%d')
        self.ids.button_time.text = datetime.now().strftime('%H:%M:%S')

        self.categories = DB.get_categories()
        self.balances = DB.get_balances()
        print(self.categories)

        self.selected_balance_i = 0
        self.selected_category_i = 0

        self.ids.button_balance.set_item(self.balances[self.selected_balance_i]['balance_name'])
        self.ids.button_category.set_item(self.categories[self.selected_category_i]['category_name'])

        self.ids.is_income_checkbox.active = self.categories[self.selected_category_i]['category_is_income']

        self.balance_menu = MDDropdownMenu(
            caller=self.ids.button_balance,
            position="auto",
            items=[{
                'text': self.balances[i]['balance_name'],
                'viewclass': 'MDDropDownItem',
                "on_release":
                    lambda i=i: self.balance_menu_callback(i, self.balances[i]['balance_name']),
            } for i in range(len(self.balances))]
        )

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

    def balance_menu_callback(self, i, balance_name):
        self.balance_menu.dismiss()

        self.ids.selected_balance_i = i
        self.ids.button_balance.set_item(balance_name)

    def category_menu_callback(self, i, category_name):
        self.category_menu.dismiss()

        self.selected_category_i = i
        self.ids.button_category.set_item(category_name)
        self.ids.is_income_checkbox.active = self.categories[self.selected_category_i]['category_is_income']

    def set_date(self, obj, date, others):
        self.ids.button_date.text = date.strftime('%Y-%m-%d')

    def set_time(self, instance, time):
        self.ids.button_time.text = time.strftime('%H:%M:%S')

    def show_date_picker(self, x):
        date_dialog = MDDatePicker(
            year=int(datetime.now().year),
            month=datetime.now().month,
            day=datetime.now().day,
            pos_hint={'center_x': .5, 'center_y': .5},
        )
        date_dialog.bind(on_save=self.set_date)
        date_dialog.open()

    def show_time_picker(self, x):
        time_dialog = MDTimePicker(pos_hint={'center_x': .5, 'center_y': .5})
        time_dialog.bind(time=self.set_time)
        time_dialog.open()

    def on_press_button_exit_transaction(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'TransactionsScreen'

    def on_press_button_save_transaction(self, save):
        balance_id = self.balances[self.selected_balance_i]['balance_id']
        date_time = datetime.strptime(
                '{} {}'.format(self.ids.button_date.text, self.ids.button_time.text),
                '%Y-%m-%d %H:%M:%S',
        )
        amount = abs(float(self.ids.amount_textbox.text))
        is_income = self.ids.is_income_checkbox.active
        category_id = self.categories[self.selected_category_i]['category_id']
        description = self.ids.description_textbox.text
        DB.insert_transaction(balance_id, date_time, amount, is_income, category_id, description)

        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'TransactionsScreen'


if __name__ == '__main__':
    class MainApp(MDApp):
        def build(self):
            screen_manager = ScreenManager()
            screen_manager.add_widget(AddTransactionScreen(name='AddTransactionScreen'))
            return screen_manager

    MainApp().run()
