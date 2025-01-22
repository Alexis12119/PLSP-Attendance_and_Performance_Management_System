from supabase_manager import get_supabase_client
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.popup import Popup
from kivy.core.image import Image as CoreImage
from io import BytesIO
import qrcode
from View.class_page import ClassPage_Teacher
from Controller.class_controller import ClassController
from session_manager import SessionManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivy.graphics import Color, RoundedRectangle
from View.course_detail import CourseDetail

class Home_Student(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = get_supabase_client()
        # Grid layout for course tiles (2 columns)
        self.grid_layout = GridLayout(
            cols=3,
            spacing=15,
            size_hint_y=None,
            padding=[10, 10, 10, 10]
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        layout = FloatLayout(size_hint=(1, 1))

        self.class_controller = ClassController()

        self.session = SessionManager()

        self.student_id = self.session.get('student_id')

        full_name = self.session.get("full_name", "Guest")
        if full_name == "Guest":
            print("Warning: full_name not set in session, defaulting to 'Guest'")



        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        card_user_profile = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="230dp",
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="15dp"
        )

        profile_icon = MDIconButton(
            icon="account-circle",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="70dp",
        )
        card_user_profile.add_widget(profile_icon)

        card_user_profile.add_widget(
            MDLabel(
                text=full_name,
                halign="center",
                theme_text_color="Primary",
                font_style="H6",
                bold=True,
            )
        )

        icons_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height="50dp",
            spacing="10dp",
            pos_hint={"center_x": 0.68},
        )

        def generate_qr_code(instance):
            student_id = self.session.get("student_id", "Unknown ID")
            if student_id == "Unknown ID":
                print("Warning: student_id not set in session, defaulting to 'Unknown ID'")

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(student_id)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")

            # Save the QR code to a BytesIO object
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            # Create a CoreImage from the QR code
            qr_image = CoreImage(buffer, ext="png")

            # Custom widget with a title, QR code, and styled layout
            class CustomPopupContent(BoxLayout):
                def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    self.orientation = "vertical"
                    self.padding = 20  # Padding around the content
                    self.spacing = 15  # Spacing between title and QR code
                    with self.canvas.before:
                        Color(1, 1, 1, 1)  # White background color
                        self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
                    self.bind(pos=self.update_rect, size=self.update_rect)

                    # Add a title to the popup
                    title = MDLabel(
                        text=f"[b]Student ID: {student_id}[/b]",
                        markup=True,
                        font_name="Roboto-Bold",
                        font_size="20sp",
                        halign="center",
                        size_hint=(1, None),
                        height=50,
                    )
                    self.add_widget(title)

                    # Add the QR code image
                    qr_image_widget = Image(texture=qr_image.texture, allow_stretch=True, size_hint=(1, 1))
                    self.add_widget(qr_image_widget)

                def update_rect(self, *args):
                    self.rect.pos = self.pos
                    self.rect.size = self.size

            # Instantiate the custom content
            popup_content = CustomPopupContent()

            # Create the popup
            qr_popup = Popup(
                title="",
                content=popup_content,
                size_hint=(None, None),
                size=(400, 400),
                background_color=[0, 0, 0, 0],  # Transparent popup background
                separator_color=[0, 0, 0, 0],  # Remove separator
                auto_dismiss=True
            )
            qr_popup.open()

        qr_code_icon = MDIconButton(
            icon="qrcode",
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="30dp",
        )
        qr_code_icon.bind(on_release=generate_qr_code)

        def logout(instance):
            # Create a separate dialog instance for logout confirmation
            logout_dialog = MDDialog(
                title="Log Out",
                text="Are you sure you want to log out?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        theme_text_color="Custom",
                        text_color=(0, 0.6, 0, 1),
                        on_release=lambda x: logout_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="LOG OUT",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x: confirm_logout(logout_dialog)
                    ),
                ],
            )
            logout_dialog.open()

        def confirm_logout(dialog):
            self.session.clear()
            self.manager.current = "Login"
            dialog.dismiss()

        def open_add_class_dialog(instance):
            if not self.dialog:
                self.dialog = MDDialog(
                    title="ADD CLASS",
                    type="custom",
                    content_cls=MDTextField(
                        hint_text="Enter Class Code",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        mode="rectangle",
                    ),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            font_name="assets/fonts/Uni Sans Heavy.otf",
                            theme_text_color="Custom",
                            text_color=(0, 0.6, 0, 1),
                            on_release=lambda x: self.dialog.dismiss()
                        ),
                        MDFlatButton(
                            text="ADD",
                            theme_text_color="Custom",
                            text_color=(0, 0.6, 0, 1),
                            font_name="assets/fonts/Uni Sans Heavy.otf",
                            on_release=lambda x: self.add_class(self.dialog.content_cls.text)  # Correctly reference self.add_class
                        ),
                    ],
                )
            self.dialog.open()

        self.display_student_classes(self.student_id)

        logout_icon = MDIconButton(
            icon="logout-variant",
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="30dp",
        )
        logout_icon.bind(on_release=logout)



        add_class_button = MDIconButton(
            icon="plus-box",
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="30dp",
        )
        add_class_button.bind(on_release=open_add_class_dialog)

        icons_layout.add_widget(add_class_button)
        icons_layout.add_widget(qr_code_icon)
        icons_layout.add_widget(logout_icon)

        card_user_profile.add_widget(icons_layout)
        layout.add_widget(card_user_profile)


        card_user_class = MDCard(
            orientation="vertical",
            size_hint=(0.9, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.28},
            radius=[15, 15, 15, 15],
            padding=[10, 10, 10, 10],
        )

        # Title for Courses
        title_label = MDLabel(
            text="Courses",
            halign="center",
            theme_text_color="Custom",
            text_color=[0, 0.6, 0, 1],
            font_style="H5",
            font_name="assets/fonts/Uni Sans Heavy.otf",
            bold=True,
            size_hint_y=None,
            height="40dp"
        )
        card_user_class.add_widget(title_label)

        # ScrollView for courses
        scroll_view = ScrollView(size_hint=(1, 1))
        
        
        scroll_view.add_widget(self.grid_layout)
        card_user_class.add_widget(scroll_view)

        self.dialog = None

        layout.add_widget(card_user_class)

        # Add the main layout to the screen
        self.add_widget(layout)

    def add_class(self, class_code):
        if class_code.strip():
            # Call the controller to get the class details from Supabase
            class_data = self.class_controller.fetch_class_by_code(class_code)

            if class_data:
                id = class_data['id']
                class_name = class_data['class_name']

                # Get student_id from the session
                student_id = self.session.get("student_id", "Unknown ID")
                if student_id == "Unknown ID":
                    print("Warning: student_id not set in session, defaulting to 'Unknown ID'")

                # Call the controller to add the student to the class in Supabase
                self.class_controller.enroll_student_in_class(student_id, id)

                # Create and add the button for the new class
                new_button_layout = FloatLayout(size_hint=(None, None), size=(125, 100))

                new_icon = MDIconButton(
                    icon="notebook",
                    theme_text_color="Custom",
                    text_color=(0, 0.6, 0, 1),
                    icon_size="50dp",
                    pos_hint={"center_x": 0.5, "top": 1},
                )
                new_label = MDLabel(
                    text=class_name,  # Use the class_name fetched from Supabase
                    halign="center",
                    size_hint=(1, None),
                    height="20dp",
                    bold=True,
                    font_style="Caption",
                    pos_hint={"center_x": 0.5, "y": 0},
                )

                # Add the icon and label to the layout
                new_button_layout.add_widget(new_icon)
                new_button_layout.add_widget(new_label)

                # Add the new layout to the grid
                self.grid_layout.add_widget(new_button_layout)
            else:
                print(f"No class found for class_code: {class_code}")

            self.dialog.dismiss()
    def fetch_classes_for_student(self, student_id):
        response = self.client.table("student_classes").select("*").eq("student_id", student_id).execute()
        class_codes = []
        for res in response.data:
            class_codes.append(res['class_id'])
        return class_codes

    def display_student_classes(self, student_id):
        # Fetch class codes for the student
        class_codes = self.fetch_classes_for_student(student_id)
        
        for code in class_codes:
            # Query to fetch the class name by class_code
            response = self.client.table("classes").select("id, class_name,class_code").eq("id", code).execute()
            class_name = ""
            class_code = 0
            class_id = 0
            for res in response.data:
                class_name = res['class_name']
                class_code = res['class_code'] 
                class_id = res['id']
            
            # Create and configure UI widgets
            new_button_layout = FloatLayout(size_hint=(None, None), size=(125, 100))

            # Create a button that will handle the touch events
            new_icon = MDIconButton(
                icon="notebook",
                theme_text_color="Custom",
                text_color=(0, 0.6, 0, 1),
                icon_size="50dp",
                pos_hint={"center_x": 0.5, "top": 1},
            )
            
            # Bind the button press event
            new_icon.bind(
                on_release=lambda instance, code=code, name=class_name: self.open_course_detail(class_code, class_name, class_id)
            )

            new_label = MDLabel(
                text=class_name,
                halign="center",
                size_hint=(1, None),
                height="20dp",
                bold=True,
                font_style="Caption",
                pos_hint={"center_x": 0.5, "y": 0},
            )

            new_button_layout.add_widget(new_icon)
            new_button_layout.add_widget(new_label)

            # Add the new layout to the grid
            self.grid_layout.add_widget(new_button_layout)

    def open_course_detail(self, course_code, course_name, class_id):
        print(f"Opening course detail: {course_name} ({course_code})")
        # First, check if the screen already exists
        existing_screen = self.manager.get_screen("CourseDetail") if self.manager.has_screen("CourseDetail") else None
        
        if existing_screen:
            # Update existing screen with new details
            existing_screen.course_code = course_code
            existing_screen.course_name = course_name
        else:
            # Create new screen
            course_screen = CourseDetail(
                name="CourseDetail",
                course_code=course_code,
                course_name=course_name,
                class_id = class_id
            )
            self.manager.add_widget(course_screen)
        
        # Switch to the course detail screen
        self.manager.transition.direction = 'left'  # Optional: adds a transition effect
        self.manager.current = "CourseDetail"

class Home_Teacher(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.session = SessionManager()
        self.class_controller = ClassController()

        # Get teacher info from session
        full_name = self.session.get("full_name", "Guest")
        teacher_id = self.session.get("teacher_id", None)

        if full_name == "Guest":
            print("Warning: full_name not set in session, defaulting to 'Guest'")

        if not teacher_id:
            print("Error: Teacher ID is not available.")
            return

        layout = FloatLayout(size_hint=(1, 1))

        background = Image(
            source="assets/background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(background)

        # Profile card with teacher's name
        card_user_profile = MDCard(
            orientation="vertical",
            size_hint=(0.9, None),
            height="230dp",
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            radius=[15, 15, 15, 15],
            padding=[20, 20, 20, 20],
            spacing="15dp"
        )

        profile_icon = MDIconButton(
            icon="account-circle",
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="70dp",
        )
        card_user_profile.add_widget(profile_icon)

        card_user_profile.add_widget(
            MDLabel(
                text=full_name,
                halign="center",
                theme_text_color="Primary",
                font_style="H6",
                bold=True,
            )
        )

        # Logout button
        def logout(instance):
            logout_dialog = MDDialog(
                title="Log Out",
                text="Are you sure you want to log out?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        theme_text_color="Custom",
                        text_color=(0, 0.6, 0, 1),
                        on_release=lambda x: logout_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="LOG OUT",
                        font_name="assets/fonts/Uni Sans Heavy.otf",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x: confirm_logout(logout_dialog)
                    ),
                ],
            )
            logout_dialog.open()

        def confirm_logout(dialog):
            self.session.clear()
            self.manager.current = "Login"
            dialog.dismiss()

        def open_add_class_dialog(instance):
            if not self.dialog:
                self.dialog = MDDialog(
                    title="ADD CLASS",
                    type="custom",
                    content_cls=MDTextField(
                        hint_text="Enter Class Name",
                        font_name="Roboto-Bold",
                        mode="rectangle",
                    ),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            font_name="assets/fonts/Uni Sans Heavy.otf",
                            theme_text_color="Custom",
                            text_color=(0, 0.6, 0, 1),
                            on_release=lambda x: self.dialog.dismiss()
                        ),
                        MDFlatButton(
                            text="ADD",
                            theme_text_color="Custom",
                            text_color=(0, 0.6, 0, 1),
                            font_name="assets/fonts/Uni Sans Heavy.otf",
                            on_release=lambda x: add_class(self.dialog.content_cls.text)
                        ),
                    ],
                )
            self.dialog.open()

        icon_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            width="120dp",
            height="50dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5},
        )
        card_user_profile.add_widget(icon_layout)

        add_class_button = MDIconButton(
            icon="plus-box",
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="30dp",
            pos_hint={"center_x": 0.5},
        )
        add_class_button.bind(on_release=open_add_class_dialog)
        icon_layout.add_widget(add_class_button)

        logout_icon = MDIconButton(
            icon="logout-variant",
            theme_text_color="Custom",
            text_color=(0, 0.6, 0, 1),
            icon_size="30dp",
            pos_hint={"center_x": 0.5},
        )
        logout_icon.bind(on_release=logout)
        icon_layout.add_widget(logout_icon)

        layout.add_widget(card_user_profile)

        # Card for displaying classes
        card_user_class = MDCard(
            orientation="vertical",
            size_hint=(0.9, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.28},
            radius=[15, 15, 15, 15],
            padding=[10, 10, 10, 10],
        )

        # ScrollView for the grid of classes
        scroll_view = ScrollView(size_hint=(1, 1))

        # GridLayout to hold the class icons
        self.grid_layout = GridLayout(
            cols=3,
            spacing=5,
            size_hint_y=None,
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter("height"))

        scroll_view.add_widget(self.grid_layout)
        card_user_class.add_widget(scroll_view)

        self.dialog = None

        # Fetch and display the teacher's classes
        self.display_teacher_classes(teacher_id)

        def add_class(class_name):
            if class_name.strip():
                teacher_id = self.session.get("teacher_id", None)
                if not teacher_id:
                    print("Error: Teacher ID is not available.")
                    return

                result = self.class_controller.create_class(class_name, teacher_id)

                if "error" in result:
                    toast(f"{result['error']}")
                else:
                    new_button_layout = FloatLayout(size_hint=(None, None), size=(130, 100))

                    new_icon = MDIconButton(
                        icon="notebook",
                        theme_text_color="Custom",
                        text_color=(0, 0.6, 0, 1),
                        icon_size="50dp",
                        pos_hint={"center_x": 0.5, "top": 1},
                    )
                    new_label = MDLabel(
                        text=class_name,
                        halign="center",
                        size_hint=(1, None),
                        height="20dp",
                        bold=True,
                        font_style="Caption",
                        pos_hint={"center_x": 0.5, "y": 0},
                    )

                    new_button_layout.add_widget(new_icon)
                    new_button_layout.add_widget(new_label)

                    new_icon.bind(
                        on_release=lambda instance, name=class_name: self.go_to_class_page(name, "Unknown Code"))

                    self.grid_layout.add_widget(new_button_layout)

            self.dialog.dismiss()

        layout.add_widget(card_user_class)

        # Add the main layout to the screen
        self.add_widget(layout)

    def go_to_class_page(self, class_name, result):
        # Store class information in the session
        self.session.set("class_name", class_name)
        self.session.set("class_code", result)
        self.manager.add_widget(ClassPage_Teacher(name="ClassPage_Teacher", class_id=60, student_id=2205879))
        self.manager.current = "ClassPage_Teacher"

    def display_teacher_classes(self, teacher_id):
        classes = self.class_controller.fetch_classes_for_teacher(teacher_id)
        if "error" in classes:
            print(f"Error: {classes['error']}")
        else:
            for class_info in classes:
                class_name = class_info.get("class_name", "")
                class_code = class_info.get("class_code", "")

                new_button_layout = FloatLayout(size_hint=(None, None), size=(125, 100))

                new_icon = MDIconButton(
                    icon="notebook",
                    theme_text_color="Custom",
                    text_color=(0, 0.6, 0, 1),
                    icon_size="50dp",
                    pos_hint={"center_x": 0.5, "top": 1},
                )
                new_label = MDLabel(
                    text=class_name,
                    halign="center",
                    size_hint=(1, None),
                    height="20dp",
                    bold=True,
                    font_style="Caption",
                    pos_hint={"center_x": 0.5, "y": 0},
                )

                new_button_layout.add_widget(new_icon)
                new_button_layout.add_widget(new_label)


                new_icon.bind(
                    on_release=lambda instance, name=class_name, code=class_code: self.go_to_class_page(name, code)
                )

                self.grid_layout.add_widget(new_button_layout)
