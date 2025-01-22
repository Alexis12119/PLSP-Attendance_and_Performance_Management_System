from supabase_manager import get_supabase_client
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from Controller.class_controller import ClassController
from session_manager import SessionManager

class ClassPage_Teacher(MDScreen):
    def __init__(self, class_id, student_id, **kwargs):
        super().__init__(**kwargs)

        self.dialog = None  # Initialize dialog variable
        layout = FloatLayout(size_hint=(1, 1))

        self.class_controller = ClassController()
        self.session = SessionManager()
        self.client = get_supabase_client()
        # Get the class information from the session
        class_name = self.session.get("class_name", "Class")
        class_code = self.session.get("class_code", "Code")

        # Background image setup
        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        response = self.client.table("student_classes").select("*").eq("class_id", class_id).execute()
        print(response)
        total_count = len(response.data)
        # Card layout for content
        card_class = MDCard(
            orientation="vertical",
            size_hint=(0.9, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding="20dp",
            spacing="10dp",
        )
        layout.add_widget(card_class)

        back_button_layout = FloatLayout(size_hint=(1, 1))
        layout.add_widget(back_button_layout)

        back_button = MDIconButton(
            icon="arrow-left",
            size_hint=(None, None),
            height="40dp",
            width="40dp",
            pos_hint={"x": 0.05, "y": 0.78},  # Top-left of the layout
            theme_text_color="Custom",
            text_color=[0, 0, 0, 1],
        )
        back_button_layout.add_widget(back_button)
        back_button.bind(on_release=self.navigate_back)

        # Course label layout
        course_label_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height="100dp",
            spacing="5dp",
        )
        card_class.add_widget(course_label_layout)

        course_code_label = MDLabel(
            text="Course Code",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[0, 0.6, 0, 1],
            font_name="Roboto-Bold",
            bold=True,
        )
        course_label_layout.add_widget(course_code_label)

        course_class_label = MDRaisedButton(
            text=class_code,
            elevation=0,
            size_hint=(0.5, None),
            height="40dp",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        course_label_layout.add_widget(course_class_label)

        # Course class layout
        course_label_class_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height="100dp",
            spacing="5dp",
        )
        card_class.add_widget(course_label_class_layout)

        course_code_class_label = MDLabel(
            text="Course Name",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[0, 0.6, 0, 1],
            font_name="Roboto-Bold",
            bold=True,
        )
        course_label_class_layout.add_widget(course_code_class_label)

        course_name_class_label = MDRaisedButton(
            text=class_name,
            elevation=0,
            size_hint=(0.5, None),
            height="40dp",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        course_label_class_layout.add_widget(course_name_class_label)

        # Course count layout
        course_count_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height="100dp",
            spacing="5dp",
        )
        card_class.add_widget(course_count_layout)

        course_count_class_label = MDLabel(
            text="No. of Students",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=[0, 0.6, 0, 1],
            font_name="Roboto-Bold",
            bold=True,
        )
        course_count_layout.add_widget(course_count_class_label)

        student_count_label = MDRaisedButton(
            text=str(total_count),
            elevation=0,
            size_hint=(0.5, None),
            height="40dp",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        course_count_layout.add_widget(student_count_label)

        # Button layout
        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height="50dp",
            spacing="10dp",
        )

        card_class.add_widget(button_layout)

        attendance_button = MDRaisedButton(
            text="Attendance",
            size_hint=(1, None),
            height="40dp",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        button_layout.add_widget(attendance_button)

        activity_button = MDRaisedButton(
            text="Activity",
            size_hint=(1, None),
            height="40dp",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        button_layout.add_widget(activity_button)

        delete_button = MDRaisedButton(
            text="Delete Class",
            size_hint=(1, None),
            height="40dp",
            theme_text_color="Custom",
            text_color=[0.6, 0, 0, 1],
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        card_class.add_widget(delete_button)

        delete_button.bind(on_release=self.show_confirmation_dialog)

        self.add_widget(layout)

    def navigate_back(self, instance):
        self.manager.current = "Home_Teacher"

    def show_confirmation_dialog(self, instance):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Confirm Deletion",
                text="Are you sure you want to delete this class?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        theme_text_color="Custom",
                        text_color=(0, 0.6, 0, 1),
                        on_release=self.close_dialog,
                    ),
                    MDFlatButton(
                        text="DELETE",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        theme_text_color="Custom",
                        text_color=(0.6, 0, 0, 1),
                        on_release=self.confirm_delete_class,
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def confirm_delete_class(self, instance):
        self.dialog.dismiss()
        self.delete_class()

    def delete_class(self):
        # Defer the import to avoid circular dependency
        from View.home_page import Home_Teacher

        class_code = self.session.get("class_code", "Code")
        response = self.class_controller.delete_class(class_code)

        if response['status'] == 'success':
            self.manager.add_widget(Home_Teacher(name="Home_Teacher"))
            self.manager.current = "Home_Teacher"
        else:
            print("Error deleting class:", response['message'])
