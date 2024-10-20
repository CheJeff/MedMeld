import sys
import os

# Add the path where gemini.py is located to sys.path
gemini_path = '../'
if gemini_path not in sys.path:
    sys.path.append(gemini_path)

import reflex as rx
import gemini  # Now Python should be able to find gemini.py
import bureau
from rxconfig import config

class State(rx.State):
    """The app state."""

    # User data
    username: str = ""
    password: str = ""

    # Hardcoded credentials for Jane
    correct_username = "Jane222"
    correct_password = "ILoveToHack"

    # Tracks if the user is logged in
    logged_in: bool = False

    # Message to display login errors
    login_error: str = ""

    # New attributes for question and answer
    question: str = ""
    answer: str = ""

    # Action for the login button
    def login(self):
        # Check if the username and password are correct
        if (self.username == self.correct_username
            and self.password == self.correct_password):

            self.logged_in = True
            return rx.redirect("/profile") # Redirect to profile page upon successful login
        else:
            # If credentials are wrong, show an error message
            self.login_error = "Invalid username or password."

    # Method to log the user out
    def logout(self):
        # Reset the login state and redirect to the home page
        self.logged_in = False
        self.username = ""
        self.password = ""
        return rx.redirect("/")

    # Method to run when the profile page loads
    def on_load(self):
        # Redirect to login page if not logged in
        if not self.logged_in:
            return rx.redirect("/")

    # Method to run when the index page loads
    def index_on_load(self):
        # Redirect to profile page if already logged in
        if self.logged_in:
            return rx.redirect("/profile")

    # Updated method to generate the answer using the function from gemini.py
    def generate_answer(self):
        json_input = "" #bureau.get_combined_patient_data("John Doe")
        #print("the json data is:" + json_input)
        try:
            # Call the generate_info function from the gemini module
            self.answer = gemini.generate_info(json_input, self.question)
        except Exception as e:
            self.answer = f"An error occurred: {str(e)}"

    def submit_signup(self):
        return rx.redirect("/healthcare-providers")

# Function to render the login page
def login_page() -> rx.Component:
    return rx.container(
        rx.box(
            rx.heading(
                "Welcome to MedMeld!",
                font_size="43px",
                color="#000000",
                margin_bottom="30px",
            ),
            rx.text(
                "Your personal health assistant to help you understand and access your medical records at your fingertips.",
                font_size="1.2em",
                color="#000000",
                margin_bottom="30px",
            ),
            rx.box(
                rx.text("Username", font_size="1.5em", margin_bottom="10px", color="#000000"),
                rx.input(
                    placeholder="Enter your username",
                    width="400px",
                    height="50px",
                    padding="15px",
                    font_size="1.2em",
                    value=State.username,
                    on_change=State.set_username,
                    bg="#FFFFFF",
                    color="#000000",
                    border="2px solid #000000",
                ),
                rx.text(
                    "Password",
                    font_size="1.5em",
                    margin_bottom="10px",
                    margin_top="20px",
                    color="#000000"
                ),
                rx.input(
                    placeholder="Enter your password",
                    width="400px",
                    height="50px",
                    padding="15px",
                    font_size="1.2em",
                    type="password",
                    value=State.password,
                    on_change=State.set_password,
                    bg="#FFFFFF",
                    color="#000000",
                    border="2px solid #000000",
                ),
                rx.button(
                    "Login",
                    bg="#ADD8E6",
                    border="2px solid #000000",
                    padding="25px 30px",
                    margin_top="30px",
                    font_size="1.5em",
                    color="#000000",
                    _hover={"bg": "#ADD8E6", "opacity": 0.8},
                    _active={"bg": "#ADD8E6", "opacity": 0.9},
                    on_click=State.login,
                ),
                rx.text(State.login_error, color="#FF0000", margin_top="20px"),
                margin_bottom="40px",
            ),
            rx.box(
                rx.link(
                    "Forgot your password?",
                    href="/forgot-password",
                    color="#0000FF",
                    margin_bottom="15px",
                    font_size="1.2em",
                ),
                rx.link("Create Account", href="/create-account", color="#0000FF", font_size="1.2em"),
                display="flex",
                flex_direction="column",
                align_items="center",
            ),
            align_items="center",
            justify_content="center",
            padding="60px",
            border="2px solid #000000",
            border_radius="15px",
            width="600px",
            bg="#FFFFFF",
            position="relative",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="#ADD8E6",
    )

# Function to render the profile page after login
def profile_page() -> rx.Component:
    return rx.container(
        rx.box(
            # Log out button at the top right
            rx.box(
                rx.button(
                    "[Log Out]",
                    bg="#FFFFFF",
                    color="#0000FF",
                    border="none",
                    on_click=State.logout,
                    _hover={"text_decoration": "underline"},
                ),
                position="absolute",
                top="10px",
                right="20px",
            ),
            # Profile info
            rx.box(
                bg="#CCCCCC",  # Placeholder for profile picture
                width="200px",
                height="200px",
                border_radius="50%",  # Make it circular
                margin_bottom="30px",
            ),
            rx.text(
                f"Hi {State.correct_username[:-3]}!",
                font_size="3em",
                margin_bottom="30px",
                text_align="center",
            ),  # Shows "Hi Jane!" with larger font size
            rx.button(
                "Query Record",
                bg="#ADD8E6",
                border="2px solid #000000",
                padding="25px",
                font_size="1.5em",
                margin_top="20px",
                on_click=lambda: rx.redirect("/record"),  # Redirect to record page
                _hover={"bg": "#ADD8E6", "opacity": 0.8},
            ),
            align_items="center",
            justify_content="center",
            display="flex",
            flex_direction="column",
            padding="60px",
            border="2px solid #000000",
            border_radius="15px",
            width="500px",
            bg="#FFFFFF",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="#ADD8E6",
        position="relative",  # To ensure the log out button stays in place
    )

# Function to render the record page with AI integration
def record_page() -> rx.Component:
    return rx.container(
        rx.box(
            # Two text boxes side by side
            rx.box(
                # Left box: Input for the question
                rx.text(
                    "Enter your question:", font_size="1.2em", margin_bottom="10px"
                ),
                rx.text_area(
                    placeholder="Type your question here...",
                    width="400px",
                    height="200px",
                    padding="10px",
                    value=State.question,
                    on_change=State.set_question,
                    bg="#FFFFFF",
                    color="#000000",
                    border="1px solid #000000",
                ),
                rx.button(
                    "Submit",
                    bg="#ADD8E6",
                    border="2px solid #000000",
                    padding="10px",
                    margin_top="10px",
                    on_click=State.generate_answer,
                    _hover={"bg": "#ADD8E6", "opacity": 0.8},
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
                margin_right="20px",
            ),
            rx.box(
                # Right box: Output for the answer
                rx.text("Answer:", font_size="1.2em", margin_bottom="10px"),
                rx.text_area(
                    placeholder="Answer will appear here...",
                    width="400px",
                    height="200px",
                    padding="10px",
                    value=State.answer,
                    is_read_only=True,
                    bg="#FFFFFF",
                    color="#000000",
                    border="1px solid #000000",
                ),
                display="flex",
                flex_direction="column",
                align_items="center",
            ),
            display="flex",
            flex_direction="row",
            align_items="flex_start",
            justify_content="center",
            padding="40px",
            border="2px solid #000000",
            border_radius="10px",
            bg="#FFFFFF",
        ),
        # Back to Profile button
        rx.button(
            "Back to Profile",
            bg="#ADD8E6",
            border="2px solid #000000",
            padding="10px",
            on_click=lambda: rx.redirect("/profile"),
            _hover={"bg": "#ADD8E6", "opacity": 0.8},
            position="absolute",
            top="20px",
            left="20px",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="#ADD8E6",
        position="relative",
    )

# Function to render the create account page
def create_account_page() -> rx.Component:
    return rx.container(
        rx.box(
            rx.heading(
                "Create Your Account",
                font_size="43px",
                color="#000000",
                margin_bottom="30px",
            ),
            # First Name and Last Name side by side
            rx.box(
                rx.box(
                    rx.text("First Name", font_size="1.5em", margin_bottom="10px", color="#000000"),
                    rx.input(
                        placeholder="Enter your first name",
                        width="330px",
                        height="65px",
                        padding="15px",
                        font_size="1.3em",
                        bg="#FFFFFF",
                        color="#000000",
                        border="2px solid #000000",
                    ),
                ),
                rx.box(
                    rx.text("Last Name", font_size="1.5em", margin_bottom="10px", color="#000000"),
                    rx.input(
                        placeholder="Enter your last name",
                        width="330px",
                        height="65px",
                        padding="15px",
                        font_size="1.3em",
                        bg="#FFFFFF",
                        color="#000000",
                        border="2px solid #000000",
                    ),
                ),
                display="flex",
                gap="20px",
                margin_bottom="20px",
            ),
            # Email Address and Phone Number side by side
            rx.box(
                rx.box(
                    rx.text("Email Address", font_size="1.5em", margin_bottom="10px", color="#000000"),
                    rx.input(
                        placeholder="Enter your email address",
                        width="330px",
                        height="65px",
                        padding="15px",
                        font_size="1.3em",
                        bg="#FFFFFF",
                        color="#000000",
                        border="2px solid #000000",
                    ),
                ),
                rx.box(
                    rx.text("Phone Number", font_size="1.5em", margin_bottom="10px", color="#000000"),
                    rx.input(
                        placeholder="Enter your phone number",
                        width="330px",
                        height="65px",
                        padding="15px",
                        font_size="1.3em",
                        bg="#FFFFFF",
                        color="#000000",
                        border="2px solid #000000",
                    ),
                ),
                display="flex",
                gap="20px",
                margin_bottom="20px",
            ),
            # Username and Password side by side
            rx.box(
                rx.box(
                    rx.text("Username", font_size="1.5em", margin_bottom="10px", color="#000000"),
                    rx.input(
                        placeholder="Choose a username",
                        width="330px",
                        height="65px",
                        padding="15px",
                        font_size="1.3em",
                        bg="#FFFFFF",
                        color="#000000",
                        border="2px solid #000000",
                    ),
                ),
                rx.box(
                    rx.text("Password", font_size="1.5em", margin_bottom="10px", color="#000000"),
                    rx.input(
                        placeholder="Enter your password",
                        width="330px",
                        height="65px",
                        padding="15px",
                        type="password",
                        font_size="1.3em",
                        bg="#FFFFFF",
                        color="#000000",
                        border="2px solid #000000",
                    ),
                ),
                display="flex",
                gap="20px",
                margin_bottom="30px",
            ),
            # Sign Up Button
            rx.button(
                "Sign Up",
                bg="#28a745",
                border="2px solid #000000",
                padding="25px 30px",
                font_size="1.5em",
                color="#FFFFFF",
                _hover={"bg": "#218838", "opacity": 0.8},
                margin_bottom="20px",
                on_click=State.submit_signup,
            ),
            align_items="center",
            justify_content="center",
            padding="60px",
            border="2px solid #000000",
            border_radius="15px",
            width="800px",
            bg="#FFFFFF",
            position="relative",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="#ADD8E6",
    )

# Function to render the healthcare providers page after signup
def healthcare_providers_page() -> rx.Component:
    return rx.container(
        rx.box(
            # Greeting message
            rx.heading(
                f"Hello {State.username}!",
                font_size="43px",
                color="#000000",
                margin_bottom="20px",
            ),
            rx.text(
                "Please list your healthcare providers:",
                font_size="1.5em",
                margin_bottom="20px",
                color="#000000",
            ),
            # Simple input form for adding a healthcare provider
            rx.input(
                placeholder="Enter healthcare provider name",
                width="400px",
                height="50px",
                padding="15px",
                font_size="1.3em",
                margin_bottom="10px",
                bg="#FFFFFF",
                color="#000000",
                border="2px solid #000000",
            ),
            rx.button(
                "Submit",
                bg="#28a745",  # Green background for the submit button
                border="2px solid #000000",
                padding="15px 20px",
                font_size="1.5em",
                color="#FFFFFF",
                _hover={"bg": "#218838", "opacity": 0.8},
                margin_top="20px",
            ),
            align_items="center",
            justify_content="center",
            padding="40px",
            border="2px solid #000000",
            border_radius="15px",
            width="700px",
            bg="#FFFFFF",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="#ADD8E6",
    )


# Updated Main function to render the index page and add new create account page
def index() -> rx.Component:
    # Always return the login page component
    return login_page()

# Create the Reflex app and add the pages
app = rx.App()
# Add the new page to the app
app.add_page(create_account_page, route="/create-account")
app.add_page(healthcare_providers_page, route="/healthcare-providers")
app.add_page(index, route="/", on_load=State.index_on_load)
app.add_page(profile_page, route="/profile", on_load=State.on_load)
app.add_page(record_page, route="/record", on_load=State.on_load)
