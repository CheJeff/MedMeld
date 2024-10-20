import reflex as rx
from rxconfig import config


class State(rx.State):
    """The app state."""

    # User data (for the example, hardcoded username and password)
    username: str = ""
    password: str = ""

    # Hardcoded credentials for Jane
    correct_username = "Jane222"
    correct_password = "ILoveToHack"

    # Tracks if the user is logged in
    logged_in: bool = False

    # Message to display login errors
    login_error: str = ""

    # Action for the login button
    def login(self):
        # Check if the username and password are correct
        if self.username == self.correct_username and self.password == self.correct_password:
            self.logged_in = True
            # Redirect to profile page upon successful login
            return rx.redirect("/profile")
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


# Function to render the login page
def login_page() -> rx.Component:
    return rx.container(
        rx.box(
            rx.heading(
                "Welcome to MedMesh!",
                font_size="35px",  # Large title size
                color="black",
                margin_bottom="10px",  # Small space below title
            ),
            rx.text(
                "Manage your medical records securely and conveniently.",
                size="4",  # Regular description size
                color="black",
                margin_bottom="20px",  # Space before the input fields
            ),
            rx.box(
                rx.text("Username", font_size="1.2em", margin_bottom="10px"),
                rx.input(
                    placeholder="Enter your username",
                    width="300px",
                    padding="10px",
                    value=State.username,
                    on_change=State.set_username,
                ),
                rx.text("Password", font_size="1.2em", margin_bottom="10px", margin_top="20px"),
                rx.input(
                    placeholder="Enter your password",
                    width="300px",
                    padding="10px",
                    type="password",
                    value=State.password,
                    on_change=State.set_password,
                ),
                rx.button(
                    "Login",
                    bg="lightblue",
                    border="2px solid black",
                    padding="10px",
                    margin_top="20px",
                    on_click=State.login,
                    _hover={"bg": "lightblue", "opacity": 0.8},  # Slight darken on hover
                ),
                rx.text(
                    State.login_error,
                    color="red",
                    margin_top="10px"
                ),
                margin_bottom="30px",  # Space between the form and the links
            ),
            rx.box(
                rx.link("Forgot your password?", href="/forgot-password", color="blue", margin_bottom="10px"),
                rx.link("Create Account", href="/create-account", color="blue"),
                display="flex",
                flex_direction="column",
                align_items="center"
            ),
            align_items="center",
            justify_content="center",
            padding="40px",
            border="2px solid black",
            border_radius="10px",
            width="400px",
            bg="white"
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="lightblue"
    )


# Function to render the profile page after login
def profile_page() -> rx.Component:
    return rx.container(
        rx.box(
            # Log out button at the top right
            rx.box(
                rx.button(
                    "[Log Out]",
                    bg="white",
                    color="blue",
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
                bg="gray",  # Placeholder for profile picture
                width="150px",
                height="150px",
                border_radius="50%",  # Make it circular
                margin_bottom="20px"
            ),
            rx.text(f"Hi {State.correct_username[:-3]}!", font_size="2em", margin_bottom="20px"),  # Shows "Hi Jane!"
            rx.button(
                "View Record",
                bg="lightblue",
                border="2px solid black",
                padding="10px",
                on_click=lambda: rx.redirect("/record"),  # Redirect to record page
                _hover={"bg": "lightblue", "opacity": 0.8},  # Slight darken on hover
            ),
            align_items="center",
            justify_content="center",
            padding="40px",
            border="2px solid black",
            border_radius="10px",
            width="400px",
            bg="white"
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="lightblue",
        position="relative"  # To ensure the log out button stays in place
    )


# Function to render the record page
def record_page() -> rx.Component:
    return rx.container(
        rx.box(
            rx.heading("Your Medical Records", font_size="30px", margin_bottom="20px"),
            rx.text("Medical Record 1: Placeholder for actual data.", margin_bottom="10px"),
            rx.text("Medical Record 2: Placeholder for actual data.", margin_bottom="10px"),
            rx.button(
                "Back to Profile",
                bg="lightblue",
                border="2px solid black",
                padding="10px",
                on_click=lambda: rx.redirect("/profile"),  # Go back to profile
                _hover={"bg": "lightblue", "opacity": 0.8},  # Slight darken on hover
            ),
            align_items="center",
            justify_content="center",
            padding="40px",
            border="2px solid black",
            border_radius="10px",
            width="500px",
            bg="white"
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        bg="lightblue"
    )


# Main function to render the index page
def index() -> rx.Component:
    # Always return the login page component
    return login_page()


# Create the Reflex app and add the pages
app = rx.App()
app.add_page(index, route="/", on_load=State.index_on_load)
app.add_page(profile_page, route="/profile", on_load=State.on_load)
app.add_page(record_page, route="/record", on_load=State.on_load)










