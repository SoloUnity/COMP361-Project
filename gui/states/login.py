import pygame
from gui.key_verifier import KeyVerifier
from utils.paths import REGULAR, get_image
pygame.init()

# Constants for UI
TEXT_COLOR = (0, 0, 0)
ERROR_COLOR = (255, 0, 0)  # Color for error messages, set to red
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
OFF_WHITE = (217,217,217)
WHITE = (255, 255, 255)
LOGIN_BLUE = (8, 158, 222)
SCREENWIDTH, SCREENHEIGHT = 1280, 720

# App states
START_SCREEN = "start"
LOGIN_SCREEN = "login"

class Login:
    def __init__(self, display, program_state_manager):
        # Setup display for the login window
        self.display = display
        self.program_state_manager = program_state_manager

        # GUI elements initialization
        self.font = pygame.font.Font(REGULAR, 18)
        self.license_key_text = ''
        self.license_current_color = WHITE
        self.login_b_current_color = LOGIN_BLUE
        self.license_key_rect = pygame.Rect(480, 300, 312, 43)
        self.login_button = pygame.Rect(480, 415, 312, 43)
        self.invalid_key = False  # Track if the entered key is invalid
        self.active_input = None
        self.current_screen = START_SCREEN
        

    def draw_start_screen(self, width, height):
        """Draws the start screen with background image."""
        background = pygame.image.load(get_image('background.png'))
        background = pygame.transform.scale(background, (width, height))
        self.display.blit(background, (0,0))

    def draw_login_screen(self):
        """Draws the login form with username and password input fields."""

        placeholder = "Enter license key"

        # Input boxes
        pygame.draw.rect(self.display, OFF_WHITE, (159, 125, 963, 486))
        pygame.draw.rect(self.display, self.license_current_color, self.license_key_rect, border_radius=40)
        pygame.draw.rect(self.display, BLACK, self.license_key_rect, 1, border_radius=40)
        pygame.draw.rect(self.display, self.login_b_current_color, self.login_button, border_radius=40)
    #pygame.draw.rect(screen, GRAY if active_input != "password" else BLACK, password_box, 2)

        #Logo
        logo = pygame.image.load(get_image('logo_name.png'))
        logo = pygame.transform.scale(logo, (606, 404))
        self.display.blit(logo, (395, 0))

        # Labels
        login_surface = self.font.render("Log In", True, WHITE)
        self.display.blit(login_surface, (self.login_button.x + 124, self.login_button.y + 10))

        # Display placeholder if empty and inactive
        if self.invalid_key:
            self.draw_text("Invalid key, try again.", (self.license_key_rect.x + 78, self.license_key_rect.y - 30), ERROR_COLOR)

        if self.license_key_text == "" and self.active_input == None:
            placeholder_surface = self.font.render(placeholder, True, (150, 150, 150))
            self.display.blit(placeholder_surface, (self.license_key_rect.x + 78, self.license_key_rect.y + 10))

        else:
            # Render text inside input boxes
            license_key_surface = self.font.render(self.license_key_text, True, BLACK)
            self.display.blit(license_key_surface, (self.license_key_rect.x + 78, self.license_key_rect.y + 10))

    def get_user_input(self):
        """Retrieve the current user input."""
        return self.user_input

    def draw_text(self, text, position, color=TEXT_COLOR):
        """Draw text on the screen at a given position with a specified color."""
        text_surface = self.font.render(text, True, color)
        self.display.blit(text_surface, position)

    def check_key(self, key_to_check):
        """Check if the provided key is valid using KeyVerifier."""
        verifier = KeyVerifier()
        return verifier.verify_license_key(key_to_check)

    def run(self, events):
        """Handle events and update the login screen."""
        for event in events:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is over the license key rectangle
            if self.license_key_rect.collidepoint(mouse_pos):
                self.license_current_color = (200, 220, 255)  # Hover color
            else:
                self.license_current_color = WHITE  # Default color

            # Check if mouse is over the log in rectangle
            if self.login_button.collidepoint(mouse_pos):
                self.login_b_current_color = (5, 130, 190)  # Hover color
            else:
                self.login_b_current_color = LOGIN_BLUE # Default color
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_screen == START_SCREEN:
                    self.current_screen = LOGIN_SCREEN  # Switch to login screen
                else:
                    # Check if user clicked on input fields
                    if self.license_key_rect.collidepoint(mouse_pos):
                        self.active_input = "license_key"
                        self.invalid_key = False
                        #print("Clicked on input")

                    elif self.login_button.collidepoint(mouse_pos):
                        self.active_input = "login_press"
                        key_authorized = self.check_key(self.license_key_text)

                        if key_authorized:
                            self.program_state_manager.set_state('simulation')
                            self.invalid_key = False
                        else:
                            self.invalid_key = True  # Set invalid key flag
                            self.license_key_text = ''  # Clear input
                    else:
                        self.active_input = None  # Clicked outside input fields

            
            if event.type == pygame.KEYDOWN:
                if self.active_input:
                    if event.key == pygame.K_BACKSPACE:
                        if self.active_input == "license_key":
                            self.license_key_text = self.license_key_text[:-1]
                        elif self.active_input == "login_press":
                            password_text = password_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        #print(f"Username: {self.license_key_text}")  # Replace with actual login handling
                        key_authorized = self.check_key(self.license_key_text)
                        if key_authorized:
                            self.program_state_manager.set_state('simulation')
                            self.invalid_key = False
                        else:
                            self.invalid_key = True  # Set invalid key flag
                            self.license_key_text = ''  # Clear input
                    else:
                        if self.active_input == "license_key":
                            self.license_key_text += event.unicode
                        elif self.active_input == "login_press":
                            password_text += event.unicode

        # Render the appropriate screen
        if self.current_screen == START_SCREEN:
            self.draw_start_screen(SCREENWIDTH, SCREENHEIGHT)
        elif self.current_screen == LOGIN_SCREEN:
            self.draw_login_screen()

        
        
        #pygame.display.update()
