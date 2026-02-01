from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import time

# Цветовая палитра: Красно-Черная
RED = get_color_from_hex("#FF0000")
DARK_RED = get_color_from_hex("#8B0000")
BLACK = get_color_from_hex("#000000")
WHITE = get_color_from_hex("#FFFFFF")

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = BLACK
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=40)
        
        # Заголовок главного меню
        self.logo = Label(
            text="[b]NEOCIUM[/b]", 
            markup=True, 
            font_size='70sp', 
            color=RED
        )
        
        # Кнопка запуска - теперь это Neocium
        start_btn = Button(
            text="NEOCIUM",
            size_hint=(1, 0.25),
            background_normal='',
            background_color=RED,
            color=BLACK,
            font_size='30sp',
            bold=True
        )
        start_btn.bind(on_press=self.go_to_editor)
        
        layout.add_widget(self.logo)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def go_to_editor(self, instance):
        self.manager.current = 'editor'

class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = None
        self.running = False

        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical')

        # Хедер (Верхняя панель)
        header = BoxLayout(size_hint_y=0.15, padding=[10, 5], spacing=10)
        
        # Надпись neocium слева вверху
        title_label = Label(
            text="[b]neocium[/b]", 
            markup=True, 
            font_size='28sp', 
            color=RED,
            size_hint_x=0.4,
            halign='left'
        )
        title_label.bind(size=title_label.setter('text_size'))

        # Информация о разработчике в углу (средний шрифт)
        dev_label = Label(
            text="разработчик —\nот neocium", 
            font_size='14sp', 
            color=DARK_RED,
            halign='right',
            size_hint_x=0.6
        )
        dev_label.bind(size=dev_label.setter('text_size'))

        header.add_widget(title_label)
        header.add_widget(dev_label)

        # Панель статистики и таймера
        stats_bar = BoxLayout(size_hint_y=0.1, padding=[10, 0])
        self.timer_label = Label(text="00:00", font_size='35sp', color=RED, bold=True)
        self.stats_info = Label(text="Слов: 0 | Знаков: 0", font_size='16sp', color=WHITE)
        
        stats_bar.add_widget(self.timer_label)
        stats_bar.add_widget(self.stats_info)

        # Поле ввода
        self.input_field = TextInput(
            hint_text="Введите текст...",
            multiline=True,
            font_size='20sp',
            background_color=(0.05, 0.05, 0.05, 1),
            foreground_color=WHITE,
            cursor_color=RED,
            keyboard_suggestions=True, # Включает Т9 на клавиатуре
            input_type='text'
        )
        self.input_field.bind(text=self.on_text_change)

        main_layout.add_widget(header)
        main_layout.add_widget(stats_bar)
        main_layout.add_widget(self.input_field)
        
        self.add_widget(main_layout)

    def on_text_change(self, instance, value):
        words = len(value.strip().split())
        chars = len(value)
        self.stats_info.text = f"Слов: {words} | Знаков: {chars}"

        if chars > 0 and not self.running:
            self.running = True
            self.start_time = time.time()
            Clock.schedule_interval(self.update_timer, 0.1)
        elif chars == 0:
            self.stop_timer()

    def update_timer(self, dt):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            self.timer_label.text = f"{mins:02d}:{secs:02d}"
            return True
        return False

    def stop_timer(self):
        self.running = False
        self.start_time = None
        self.timer_label.text = "00:00"

class NeociumApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(EditorScreen(name='editor'))
        return sm

if __name__ == "__main__":
    NeociumApp().run()
