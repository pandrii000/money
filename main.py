import os
# os.environ['KIVY_METRICS_DENSITY'] = '2'
from kivy.core.text import LabelBase
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
from kivy.properties import ObjectProperty, DictProperty

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # disable red dots on right click

from transactions_screen import TransactionsScreen
from menu_screen import MenuScreen
from add_transaction_screen import AddTransactionScreen
from categories_screen import CategoriesScreen
from add_category_screen import AddCategoryScreen

from config import DB

# LabelBase.register(
#     name="SourceSerifPro",
#     fn_regular="./Source_Serif_Pro/SourceSerifPro-Regular.ttf")

# Builder.load_string('''
# <Label>:
#     font_name: 'SourceSerifPro'
# ''')

class MainApp(MDApp):
    title = "money"
    date = None
    screens = ObjectProperty()
    item_selection = DictProperty()

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        from kivy.utils import platform
        if platform == "android":
            from android import loadingscreen
            loadingscreen.hide_loading_screen()
        self.use_kivy_settings = False

        # self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style = "Dark"

        self.theme_cls.primary_palette = "Blue"

        screen_manager = ScreenManager()
        screen_manager.add_widget(MenuScreen(name='MenuScreen'))
        screen_manager.add_widget(TransactionsScreen(name='TransactionsScreen'))
        screen_manager.add_widget(AddTransactionScreen(name='AddTransactionScreen'))
        screen_manager.add_widget(CategoriesScreen(name='CategoriesScreen'))
        screen_manager.add_widget(AddCategoryScreen(name='AddCategoryScreen'))
        screen_manager.current = 'MenuScreen'
        # screen_manager.current = 'TransactionsScreen'
        # screen_manager.current = 'AddTransactionScreen'
        # screen_manager.current = 'CategoriesScreen'
        # screen_manager.current = 'AddCategoryScreen'
        return screen_manager


def run_app():
    app = MainApp()
    app.run()


if __name__ == '__main__':
    run_app()
