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
from kivymd.uix.list import OneLineListItem, TwoLineListItem, MDList, ImageLeftWidget
from config import DB


from kivymd.icon_definitions import md_icons
Builder.load_string("""
#:import images_path kivymd.images_path
<TransactionsScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1

            MDRectangleFlatButton:
                text: 'Menu'
                size_hint: (.1, 1.)
                # pos_hint_x: .2
                # pos_hint_x: .1
                on_release: root.on_menu_button_press(self)

            MDLabel:
                text: 'Transactions'
                halign: "center"
                size_hint: (1., 1.)

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.8

            ScrollView:

                MDList:
                    id: container

        MDBoxLayout:
            # size_hint_y: 0.1
            orientation: 'vertical'

            MDRectangleFlatButton:
                text: '+'
                pos_hint: { 'center_x': .5, 'center_y': .5, }
                size_hint: (1., 0.1)
                on_press: root.on_add_button_press(self)

""")

class TransactionsScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transactions = DB.get_transactions()
        for t in self.transactions:
            self.ids.container.add_widget(
                self.create_transaction_item(t)
            )

    def create_transaction_item(self, t):
        balance_name = DB.get_balance_by_id(t['transaction_balance_id'])['balance_name']
        datetime = t['transaction_date']
        sign = '' if t['transaction_is_income'] else '-'
        amount = t['transaction_amount']
        text = f"{datetime}, {balance_name}"
        secondary_text = f"{sign}{amount}"

        line = TwoLineListItem(text=text, secondary_text=secondary_text)
        line.bind(on_touch_down=self.on_line_select)
        line = OneLineListItem(text=text)
        image = ImageLeftWidget(
            source='./folder.png',
            size_hint=(0.1, 0.1),
            pos_hint={ 'center_x': .0, 'center_y': .5, },
        )
        line.add_widget(image)

        return line

    def on_line_select(self, instance, touch):
        if touch.button == 'right':
            print(123)

    def on_menu_button_press(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'MenuScreen'

    def on_add_button_press(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'AddTransactionScreen'


if __name__ == '__main__':
    class MainApp(MDApp):
        def build(self):
            screen_manager = ScreenManager()
            screen_manager.add_widget(TransactionsScreen(name='TransactionsScreen'))
            return screen_manager
    MainApp().run()
