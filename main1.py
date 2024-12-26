import os
import requests
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.widget import Widget
import asynckivy

KV = '''
<ProductCard>
    adaptive_height: True
    radius: 16

    MDListItem:
        radius: 16
        theme_bg_color: "Custom"
        md_bg_color: self.theme_cls.secondaryContainerColor

        MDListItemLeadingAvatar:
            source: root.thumbnail

        MDListItemHeadlineText:
            text: root.title

        MDListItemSupportingText:
            text: f"Цена: ${root.price}"


MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: "vertical"
        padding: "12dp"
        spacing: "12dp"

        MDLabel:
            adaptive_height: True
            text: "Товары"
            theme_font_style: "Custom"
            font_style: "Display"
            role: "small"
        
        MDBoxLayout:
            orientation: 'horizontal'
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            size_hint_y: None
            MDTextField:
                id: search_field
                mode: "outlined"
                MDTextFieldLeadingIcon:
                    icon: "magnify"
                MDTextFieldHintText:
                    text: "Найти товар"
            MDButton:
                style: "elevated"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: app.search_products()

                MDButtonText:
                    text: "Найти"
        
        MDDropDownItem:
            id: dropdown
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: app.open_menu(self)

            MDDropDownItemText:
                id: drop_text
                text: "Выберите категорию"

        RecycleView:
            id: card_list
            viewclass: "ProductCard"
            bar_width: 0

            RecycleBoxLayout:
                orientation: 'vertical'
                spacing: "16dp"
                padding: "16dp"
                default_size: None, dp(72)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
'''


class ProductCard(MDBoxLayout):
    title = StringProperty()
    price = StringProperty()
    thumbnail = StringProperty()


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(KV)

    def on_start(self):
        self.load_categories()
        self.load_all_products()

    def load_categories(self):
        url = "https://dummyjson.com/products/category-list"

        async def fetch_categories():
            response = requests.get(url)
            if response.status_code == 200:
                categories = response.json()
                menu_items = [
                    {
                        "text": category,
                        "on_release": lambda x=category: self.load_products_by_category(x),
                    } for category in categories
                ]
                MDDropdownMenu(caller=self.root.ids.dropdown, items=menu_items).open()

        Clock.schedule_once(lambda x: asynckivy.start(fetch_categories()))

    def load_all_products(self):
        url = "https://dummyjson.com/products"

        async def fetch_products():
            response = requests.get(url)
            if response.status_code == 200:
                products = response.json().get("products", [])
                self.root.ids.card_list.data = []
                for product in products:
                    self.root.ids.card_list.data.append(
                        {
                            "title": product.get("title", ""),
                            "price": str(product.get("price", "")),
                            "thumbnail": product.get("thumbnail", ""),
                        }
                    )

        Clock.schedule_once(lambda x: asynckivy.start(fetch_products()))

    def load_products_by_category(self, category):
        url = f"https://dummyjson.com/products/category/{category}"

        async def fetch_products():
            response = requests.get(url)
            if response.status_code == 200:
                products = response.json().get("products", [])
                self.root.ids.card_list.data = []
                for product in products:
                    self.root.ids.card_list.data.append(
                        {
                            "title": product.get("title", ""),
                            "price": str(product.get("price", "")),
                            "thumbnail": product.get("thumbnail", ""),
                        }
                    )

        Clock.schedule_once(lambda x: asynckivy.start(fetch_products()))

    def search_products(self):
        search_text = self.root.ids.search_field.text
        url = f"https://dummyjson.com/products/search?q={search_text}"

        async def fetch_products():
            response = requests.get(url)
            if response.status_code == 200:
                products = response.json().get("products", [])
                self.root.ids.card_list.data = []
                for product in products:
                    self.root.ids.card_list.data.append(
                        {
                            "title": product.get("title", ""),
                            "price": str(product.get("price", "")),
                            "thumbnail": product.get("thumbnail", ""),
                        }
                    )

        Clock.schedule_once(lambda x: asynckivy.start(fetch_products()))

    def open_menu(self, item):
        self.load_categories()

    def menu_callback(self, text_item):
        self.root.ids.drop_text.text = text_item

Example().run()