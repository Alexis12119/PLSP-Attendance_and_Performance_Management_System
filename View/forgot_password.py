from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from Controller.user_controller import UserController


class Forgot_Password(MDScreen):
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
            height="200dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="20dp"
        )

        enter_email = MDLabel(
            text="ENTER YOUR EMAIL HERE",
            font_name="assets/fonts/Uni Sans Heavy.otf",
            font_style="Body1",
            bold=True,
            halign="center",
        )
        card.add_widget(enter_email)

        email_field = MDTextField(
            hint_text="Email",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold",
        )
        card.add_widget(email_field)

        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height="50dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5}
        )

        def switch_to_login_screen(instance):
            self.manager.current = "Login"

        login_button = MDRaisedButton(
            text="< Back to Login",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        login_button.bind(on_release=switch_to_login_screen)
        button_layout.add_widget(login_button)

        def switch_to_forgot_password2_screen(instance):
            self.manager.add_widget(Forgot_Password2(name="forgot_password2"))
            self.manager.current = "forgot_password2"

        submit_button = MDRaisedButton(
            text="Send Code",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        submit_button.bind(on_release=switch_to_forgot_password2_screen)
        button_layout.add_widget(submit_button)

        card.add_widget(button_layout)

        layout.add_widget(card)

        self.add_widget(layout)

        def request_reset_code(instance):
            email = email_field.text
            self.email = email
            result = UserController().request_password_reset(email)
            if result["status"] == "success":
                self.reset_code = result["code"]
                print("Code sent to email.")
            else:
                print(result["message"])

        submit_button.bind(on_release=request_reset_code)


class Forgot_Password2(MDScreen):
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
            height="200dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="20dp"
        )

        enter_code = MDLabel(
            text="ENTER YOUR CODE HERE",
            font_name="assets/fonts/Uni Sans Heavy.otf",
            font_style="Body1",
            bold=True,
            halign="center",
        )
        card.add_widget(enter_code)

        self.code_field = MDTextField(
            hint_text="Code",
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold",
        )
        card.add_widget(self.code_field)

        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height="50dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5}
        )

        def switch_to_forgot_password3_screen(instance):
            entered_code = self.code_field.text
            forgot_password_screen = self.manager.get_screen('forgot_password')
            if entered_code == forgot_password_screen.reset_code:
                self.manager.add_widget(Forgot_Password3(name="forgot_password3"))
                self.manager.current = "forgot_password3"
            else:
                toast("Invalid Code")

        submit_button = MDRaisedButton(
            text="Submit Code",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        submit_button.bind(on_release=switch_to_forgot_password3_screen)
        button_layout.add_widget(submit_button)

        card.add_widget(button_layout)

        layout.add_widget(card)

        self.add_widget(layout)


class Forgot_Password3(MDScreen):
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
            height="300dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="25dp"
        )

        change_password = MDLabel(
            text="SET YOUR NEW PASSWORD",
            font_name="assets/fonts/Uni Sans Heavy.otf",
            font_style="Body1",
            bold=True,
            halign="center",
        )
        card.add_widget(change_password)

        self.password_field = MDTextField(
            hint_text="New Password",
            password=True,
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold",
        )
        card.add_widget(self.password_field)

        self.confirm_password_field = MDTextField(
            hint_text="Confirm Password",
            password=True,
            size_hint_x=1,
            mode="rectangle",
            font_name="Roboto-Bold",
        )
        card.add_widget(self.confirm_password_field)

        submit_button = MDRaisedButton(
            text="Submit",
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5},
            font_name="assets/fonts/Uni Sans Heavy.otf",
        )
        submit_button.bind(on_release=self.verify_and_submit)
        card.add_widget(submit_button)

        layout.add_widget(card)

        self.add_widget(layout)

    def verify_and_submit(self, instance):
        new_password = self.password_field.text
        confirm_password = self.confirm_password_field.text

        if not new_password or not confirm_password:
            toast("Fields cannot be empty")
            return

        if new_password != confirm_password:
            toast("Passwords do not match")
            return

        email = self.manager.get_screen('forgot_password').email

        result = UserController().model.change_password(email, new_password)
        print(result)

        # if isinstance(result, dict) and result.get("status") == "success":
        toast("Password updated successfully!")
        self.manager.current = "Login"
        # else:
        #     error_message = result.get("error", "Unknown error occurred")
        #     print(f"Error while updating password: {error_message}")
        #     toast(f"Error: {error_message}")

