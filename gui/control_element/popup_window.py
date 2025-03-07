import pygame
import sys
import textwrap
from utils.paths import REGULAR

class PopupWindow:
    def __init__(self, screen, width=400, height=300, title="Popup", file_path=None):
        """Initialize the popup window."""
        self.screen = screen
        self.width = width
        self.height = height
        self.title = title
        self.file_path = file_path

        # Popup rectangle
        self.popup_rect = pygame.Rect(
            (screen.get_width() - width) // 2,
            (screen.get_height() - height) // 2,
            width,
            height
        )

        # Close button rectangle
        self.close_rect = pygame.Rect(self.popup_rect.right - 30, self.popup_rect.top + 10, 20, 20)

        # Scrollbar settings
        self.scrollbar_width = 15
        self.scrollbar_rect = pygame.Rect(self.popup_rect.right - self.scrollbar_width, self.popup_rect.top + 50, self.scrollbar_width, height - 70)
        self.scroll_position = 0
        self.scroll_speed = 20
        self.dragging_scrollbar = False

        # Colors
        self.BACKGROUND_COLOR = (36, 36, 36)
        self.BORDER_COLOR = (50, 50, 50)
        self.CLOSE_COLOR = (200, 50, 50)
        self.SCROLLBAR_COLOR = (150, 150, 150)
        self.SCROLLBAR_TRACK_COLOR = (200, 200, 200)
        self.TEXT_COLOR = (255, 255, 255)
        self.DIM_COLOR = (0, 0, 0, 150)

        # Fonts
        self.title_font = pygame.font.Font(REGULAR, 32) 
        self.subtitle_font = pygame.font.Font(REGULAR, 24)
        self.body_font = pygame.font.Font(REGULAR, 18) 

        # Content
        self.content_lines = []
        if file_path:
            self.load_content(file_path)

        # State
        self.visible = False
        self.dragging = False
        self.drag_offset = (0, 0)

    def _wrap_text(self, text, max_width, font):
        """Wrap text into lines that fit within the given width."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines
    
    def load_content(self, file_path):
        """Load content from a text file and wrap it with specific fonts."""
        try:
            with open(file_path, "r") as file:
                raw_lines = file.readlines()
                wrapped_lines = []
                max_width = self.width - 60 - self.scrollbar_width

                current_font = self.body_font  # Default font
                for line in raw_lines:
                    line = line.strip()

                    # Detect markers and set fonts
                    if line.startswith("[title]"):
                        current_font = self.title_font
                        line = line.replace("[title]", "")
                    elif line.startswith("[subtitle]"):
                        current_font = self.subtitle_font
                        line = line.replace("[subtitle]", "")
                    elif line.startswith("[body]"):
                        current_font = self.body_font
                        line = line.replace("[body]", "")
                    else:
                        current_font = self.body_font

                    # Wrap text and store with the associated font
                    for wrapped_line in self._wrap_text(line, max_width, current_font):
                        wrapped_lines.append((wrapped_line, current_font))

                self.content_lines = wrapped_lines

        except FileNotFoundError:
            self.content_lines = [("Error: File not found.", self.body_font)]
        except Exception as e:
            self.content_lines = [(f"Error: {str(e)}", self.body_font)]


    # def load_content(self, file_path):
    #     """Load content from a text file and wrap it."""
    #     try:
    #         with open(file_path, "r") as file:
    #             raw_lines = file.readlines()
    #             wrapped_lines = []
    #             # Wrap each line to fit inside the popup (subtract padding and scrollbar width)
    #             max_width = self.width - 60 - self.scrollbar_width
    #             for line in raw_lines:
    #                 wrapped_lines.extend(self._wrap_text(line.strip(), max_width))
    #             self.content_lines = wrapped_lines
    #     except FileNotFoundError:
    #         self.content_lines = ["Error: File not found."]
    #     except Exception as e:
    #         self.content_lines = [f"Error: {str(e)}"]

    def show(self, file_path=None):
        """Show the popup window and load content if a file is provided."""
        if file_path:
            self.load_content(file_path)
        self.scroll_position = 0  # Reset scroll
        self.visible = True

    def hide(self):
        """Hide the popup window."""
        self.visible = False

    def handle_event(self, event):
        """Handle events for the popup window."""
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Close button
                if self.close_rect.collidepoint(event.pos):
                    self.hide()

                # Dragging popup
                elif self.popup_rect.collidepoint(event.pos) and event.pos[1] < self.popup_rect.top + 40:
                    self.dragging = True
                    self.drag_offset = (event.pos[0] - self.popup_rect.x, event.pos[1] - self.popup_rect.y)

                # Scrollbar dragging
                elif self.scrollbar_rect.collidepoint(event.pos):
                    self.dragging_scrollbar = True

            # Scroll using mouse wheel
            elif event.button == 4:  # Scroll up
                self.scroll_position = min(self.scroll_position + self.scroll_speed, 0)
            elif event.button == 5:  # Scroll down
                total_text_height = sum(font.get_height() + 10 for _, font in self.content_lines)
                max_scroll = max(total_text_height - (self.height - 100), 0)
                self.scroll_position = max(self.scroll_position - self.scroll_speed, -max_scroll)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                self.dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION:
            # Dragging popup
            if self.dragging:
                self.popup_rect.x = event.pos[0] - self.drag_offset[0]
                self.popup_rect.y = event.pos[1] - self.drag_offset[1]

            # Dragging scrollbar
            elif self.dragging_scrollbar:
                max_scroll = max(len(self.content_lines) * 30 - (self.height - 100), 0)
                scroll_area_height = self.popup_rect.height - 70
                mouse_y = event.pos[1] - self.popup_rect.top - 50
                scroll_ratio = mouse_y / scroll_area_height
                self.scroll_position = -scroll_ratio * max_scroll

    def draw(self):
        """Draw the popup window."""
        if not self.visible:
            return

        # Dim background
        dim_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        dim_surface.fill(self.DIM_COLOR)
        self.screen.blit(dim_surface, (0, 0))

        # Popup box
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, self.popup_rect)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, self.popup_rect, width=2)

        # Recalculate close button
        self.close_rect = pygame.Rect(self.popup_rect.right - 30, self.popup_rect.top + 10, 20, 20)
        pygame.draw.circle(self.screen, self.CLOSE_COLOR, self.close_rect.center, 10)

        # Title
        title_surface = self.title_font.render(self.title, True, self.TEXT_COLOR)
        self.screen.blit(title_surface, (self.popup_rect.x + 20, self.popup_rect.y + 10))

        # ------------------- CLIPPING -------------------
        # Create a surface that acts as a mask to limit drawing inside the popup
        text_area_rect = pygame.Rect(self.popup_rect.x + 20, self.popup_rect.y + 60,
                                     self.width - 60 - self.scrollbar_width, self.height - 100)
        popup_surface = pygame.Surface((text_area_rect.width, text_area_rect.height))
        popup_surface.fill(self.BACKGROUND_COLOR)

        # Draw wrapped text onto popup_surface
        y_offset = self.scroll_position
        for line, font in self.content_lines:
            line_height = font.get_height() + 10
            if y_offset + line_height > 0 and y_offset < text_area_rect.height:
                text_surface = font.render(line, True, self.TEXT_COLOR)
                popup_surface.blit(text_surface, (0, y_offset))
            y_offset += line_height

        # Blit the clipped surface onto the screen
        self.screen.blit(popup_surface, text_area_rect.topleft)

        # ------------------- SCROLLBAR -------------------
        # # Scrollbar track
        # pygame.draw.rect(self.screen, self.SCROLLBAR_TRACK_COLOR,
        #                  (self.popup_rect.right - self.scrollbar_width, self.popup_rect.top + 50,
        #                   self.scrollbar_width - 10, self.popup_rect.height - 70))

        # Scrollbar thumb
        # Ensure scrollbar is within bounds
        if len(self.content_lines) * 30 > self.height - 100:
            total_text_height = sum(font.get_height() + 10 for _, font in self.content_lines)
            max_scroll = max(total_text_height - (self.height - 100), 1)  # Avoid division by zero

            scroll_area_height = self.popup_rect.height - 70
            scroll_ratio = min(1, (self.height - 100) / total_text_height)
            thumb_height = max(int(scroll_ratio * scroll_area_height), 20)  # Ensure a minimum scrollbar size

            # Ensure scrollbar doesn't go past bounds
            scroll_position_ratio = -self.scroll_position / max_scroll
            thumb_y = self.popup_rect.top + 50 + int(scroll_position_ratio * (scroll_area_height - thumb_height))
            thumb_y = max(self.popup_rect.top + 50, min(thumb_y, self.popup_rect.bottom - 20 - thumb_height))

            self.scrollbar_rect = pygame.Rect(self.popup_rect.right - self.scrollbar_width, thumb_y, self.scrollbar_width - 5, thumb_height)
            pygame.draw.rect(self.screen, self.SCROLLBAR_COLOR, self.scrollbar_rect)

