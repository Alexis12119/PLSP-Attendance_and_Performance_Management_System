from kivymd.uix.card import MDCard
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton, MDIconButton
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from Controller.user_controller import UserController
from kivymd.uix.screen import MDScreen

class BaseRegistrationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_controller = UserController()
        self.registration_data = {}

    def reset_fields(self):
        # Reset all MDTextField widgets on the screen
        for field in self.get_widgets_of_type(MDTextField):
            field.text = ""

    def get_widgets_of_type(self, widget_type):
        return [widget for widget in self.walk() if isinstance(widget, widget_type)]

# In your screens where you have the login button and need to reset fields

class Registration_Type(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(2, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="220dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, -20, 20, 20],
            spacing="25dp"
        )

        self.user_type = MDRectangleFlatButton(
            text="Select User Type",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="Roboto-Bold"
        )
        user_type_menu = [
            {"text": "Student", "on_release": lambda x="Student": self.set_program(x)},
            {"text": "Teacher", "on_release": lambda x="Teacher": self.set_program(x)},
        ]
        self.user_menu = MDDropdownMenu(
            caller=self.user_type,
            items=user_type_menu,
            width_mult=4
        )
        self.user_type.bind(on_release=lambda instance: self.user_menu.open())
        card.add_widget(self.user_type)

        register_button = MDRaisedButton(
            text=">",
            text_color=[1, 1, 1, 1],
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        register_button.bind(on_release=self.go_to_next_screen)
        card.add_widget(register_button)

        def switch_to_login_screen(instance):
            self.user_type.text="Select User Type"
            self.manager.current = "Login"

        login_button = MDIconButton(
            icon="close-circle",
            size_hint=(1, None),
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            height="50dp",
            pos_hint={"center_x": 0.5},
        )
        login_button.bind(on_release=switch_to_login_screen)
        card.add_widget(login_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def set_program(self, text):
        self.user_type.text = text
        self.user_menu.dismiss()

    def go_to_next_screen(self, instance):
        if self.user_type.text == "Student":
            self.manager.add_widget(Register_Student1(name="Register_Student1"))
            self.manager.current = "Register_Student1"
            self.user_type.text="Select User Type"
        elif self.user_type.text == "Teacher":
            self.manager.add_widget(Register_Teacher1(name="Register_Teacher1"))
            self.manager.current = "Register_Teacher1"
            self.user_type.text="Select User Type"
        else:
            toast("Please select a user type!")

class Register_Student1(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(2, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="380dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="25dp"
        )

        text_fields_box = BoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint=(1, None),
        )

        self.first_name_field = MDTextField(
            hint_text="First Name",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.first_name_field)

        self.last_name_field = MDTextField(
            hint_text="Last Name",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.last_name_field)

        self.student_id_field = MDTextField(
            hint_text="Student ID",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.student_id_field)

        card.add_widget(text_fields_box)

        def submit_info(instance):
            first_name = self.first_name_field.text
            last_name = self.last_name_field.text
            student_id = self.student_id_field.text

            self.registration_data.update({"first_name": first_name})
            self.registration_data.update({"last_name": last_name})
            self.registration_data.update({"student_id": student_id})

            if not (first_name and last_name and student_id):
                toast("Please fill up the missing fields")
            else:
                result = self.user_controller.validate_user_id(student_id)
                if result.get("status") == "fail":
                    toast(result.get("message"))
                else:
                    result = self.user_controller.validate_student(first_name, last_name, student_id)
                    if result['status'] == 'fail' :
                        toast(result.get("message"))
                    else:
                        self.manager.add_widget(Register_Student2(name="Register_Student2"))
                        self.manager.current = "Register_Student2"
                        self.manager.get_screen("Register_Student2").registration_data = self.registration_data

        register_button = MDRaisedButton(
            text=">",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
            text_color=[1, 1, 1, 1],
        )
        register_button.bind(on_release=submit_info)
        card.add_widget(register_button)

        def switch_to_login_screen(instance):
            self.reset_fields()  # Clear the fields before switching
            self.manager.current = "Login"

        login_button = MDIconButton(
            icon="close-circle",
            size_hint=(1, None),
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            height="50dp",
            pos_hint={"center_x": 0.5},
        )
        login_button.bind(on_release=switch_to_login_screen)
        card.add_widget(login_button)

        layout.add_widget(card)
        self.add_widget(layout)

class Register_Student2(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(2, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="380dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="25dp"
        )

        text_fields_box = BoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint=(1, None),
        )

        self.email_field = MDTextField(
            hint_text="Email",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.email_field)

        self.password_field = MDTextField(
            hint_text="Password",
            password=True,
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.password_field)

        self.confirm_password_field = MDTextField(
            hint_text="Confirm Password",
            password=True,
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.confirm_password_field)

        card.add_widget(text_fields_box)

        def submit_info2(instance):
            password = self.password_field.text
            email = self.email_field.text
            confirm_password = self.confirm_password_field.text

            self.registration_data["password"] = password
            self.registration_data["email"] = email

            if not (password and email and confirm_password):
                toast("Please fill up the missing fields")
            elif password != confirm_password:
                toast("Passwords do not match")
            else:
                result = self.user_controller.validate_email(email)
                if result.get("status") == "fail":
                    toast(result.get("message"))
                else:
                    self.user_controller.register_student(
                        student_id=self.registration_data.get("student_id"),
                        first_name=self.registration_data.get("first_name"),
                        last_name=self.registration_data.get("last_name"),
                        email=email,
                        password=password,
                        password_code=0000,
                    )
                    toast("Registration Successful")
                    self.manager.current = "Login"

        register_button = MDRaisedButton(
            text="Register",
            size_hint=(1, None),
            text_color=[1, 1, 1, 1],
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        register_button.bind(on_release=submit_info2)
        card.add_widget(register_button)

        def switch_to_login_screen(instance):
            self.reset_fields()
            self.manager.current = "Login"

        login_button = MDIconButton(
            icon="close-circle",
            size_hint=(1, None),
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            height="50dp",
            pos_hint={"center_x": 0.5},
        )
        login_button.bind(on_release=switch_to_login_screen)
        card.add_widget(login_button)

        layout.add_widget(card)
        self.add_widget(layout)

# Apply similar changes to Register_Teacher1 and Register_Teacher2


class Register_Teacher1(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(2, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="380dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="25dp"
        )

        text_fields_box = BoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint=(1, None),
        )

        self.first_name_field = MDTextField(
            hint_text="First Name",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.first_name_field)

        self.last_name_field = MDTextField(
            hint_text="Last Name",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.last_name_field)

        self.teacher_id_field = MDTextField(
            hint_text="Teacher ID",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.teacher_id_field)

        card.add_widget(text_fields_box)

        def submit_info_teacher1(instance):
            first_name = self.first_name_field.text
            last_name = self.last_name_field.text
            teacher_id = self.teacher_id_field.text

            self.registration_data.update({"first_name": first_name})
            self.registration_data.update({"last_name": last_name})
            self.registration_data.update({"teacher_id": teacher_id})

            if not (first_name and last_name and teacher_id):
                toast("Please fill up the missing fields")
            else:
                result=self.user_controller.validate_user_id(teacher_id)
                if result.get("status") == "fail":
                    toast(result.get("message"))
                else:
                    result = self.user_controller.validate_teacher(last_name, teacher_id, first_name)
                    if result.get("status") == "fail":
                        toast(result.get("message"))
                    else:
                        self.manager.current = "Register_Teacher2"
                        self.manager.get_screen("Register_Teacher2").registration_data = self.registration_data

        register_button = MDRaisedButton(
            text=">",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
            text_color=[1, 1, 1, 1],
        )
        register_button.bind(on_release=submit_info_teacher1)
        card.add_widget(register_button)

        def switch_to_login_screen(instance):
            self.reset_fields()
            self.manager.current = "Login"

        login_button = MDIconButton(
            icon="close-circle",
            size_hint=(1, None),
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            height="50dp",
            pos_hint={"center_x": 0.5},
        )
        login_button.bind(on_release=switch_to_login_screen)
        card.add_widget(login_button)

        layout.add_widget(card)
        self.add_widget(layout)

class Register_Teacher2(BaseRegistrationScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(2, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        card = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="380dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="25dp"
        )

        text_fields_box = BoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint=(1, None),
        )

        self.email_field = MDTextField(
            hint_text="Email",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.email_field)

        self.password_field = MDTextField(
            hint_text="Password",
            password=True,
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.password_field)

        self.confirm_password_field = MDTextField(
            hint_text="Confirm Password",
            password=True,
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold"
        )
        text_fields_box.add_widget(self.confirm_password_field)

        card.add_widget(text_fields_box)

        def submit_info_teacher2(instance):
            password = self.password_field.text
            email = self.email_field.text
            confirm_password = self.confirm_password_field.text

            self.registration_data["password"] = password
            self.registration_data["email"] = email

            if not (password and email and confirm_password):
                toast("Please fill up the missing fields")
            elif password != confirm_password:
                toast("Passwords do not match")
            else:
                result = self.user_controller.validate_email(email)
                if result.get("status") == "fail":
                    toast(result.get("message"))
                else:
                    self.user_controller.register_teacher(
                        teacher_id=self.registration_data.get("teacher_id"),
                        first_name=self.registration_data.get("first_name"),
                        last_name=self.registration_data.get("last_name"),
                        email=email,
                        password=password,
                        password_code=0000,
                    )
                    toast("Registration Successful")
                    self.manager.current = "Login"

        register_button = MDRaisedButton(
            text="Register",
            size_hint=(1, None),
            text_color=[1, 1, 1, 1],
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        register_button.bind(on_release=submit_info_teacher2)
        card.add_widget(register_button)

        def switch_to_login_screen(instance):
            self.reset_fields()
            self.manager.current = "Login"

        login_button = MDIconButton(
            icon="close-circle",
            size_hint=(1, None),
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            height="50dp",
            pos_hint={"center_x": 0.5},
        )
        login_button.bind(on_release=switch_to_login_screen)
        card.add_widget(login_button)

        layout.add_widget(card)
        self.add_widget(layout)
