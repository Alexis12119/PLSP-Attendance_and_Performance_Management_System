from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import ScreenManager
# from View.class_page import ClassPage_Student, ClassPage_Teacher
from View.login import Login

class MainApp(MDApp):
    def build(self):
        Window.size = (360, 640)

        self.theme_cls.primary_palette = "Green"

        screen_manager = ScreenManager()

        screen_manager.add_widget(Login(name="Login"))

        return screen_manager

if __name__ == "__main__":
    MainApp().run()
