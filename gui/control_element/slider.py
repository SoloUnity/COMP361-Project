import pygame

class Slider:
    def __init__(self, step, color_bar, color_slider, color_active, x, y, w, h, initial_value=0, min_value=-1, max_value=1):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.color_bar = color_bar
        self.color_slider = color_slider
        self.color_active = color_active
        self.rect = pygame.Rect(x, y, w, h)
        
        # Set the slider handle size
        self.slider_rect = pygame.Rect(x, y, 10, h)
        self.dragging = False
        self.value = initial_value if initial_value is not None else min_value
        self.update_slider_position()

    def update_slider_position(self):
        """Update slider position based on current value"""
        if self.max_value - self.min_value == 0:
            relative_position = 0
        else:
            relative_position = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.slider_rect.x = self.rect.x + int(relative_position * (self.rect.width - self.slider_rect.width))

    def draw(self, display):
        """Draw slider components"""
        pygame.draw.line(display, self.color_bar, 
                        (self.rect.x, self.rect.centery), 
                        (self.rect.right, self.rect.centery), 4)
        pygame.draw.rect(display, 
                        self.color_active if self.dragging else self.color_slider, 
                        self.slider_rect)

    def _update_value_from_pos(self, mouse_x):
        """Update value based on mouse position with 2 decimal precision"""
        new_x = max(self.rect.x, min(mouse_x, self.rect.right - self.slider_rect.width))
        relative_position = (new_x - self.rect.x) / (self.rect.width - self.slider_rect.width)
        raw_value = self.min_value + relative_position * (self.max_value - self.min_value)
        
        # Snap to nearest step and round to 2 decimals
        self.value = round(raw_value / self.step) * self.step
        self.value = round(self.value, 2)
        self.update_slider_position()

    def update(self, events):
        """Handle events and return current value"""
        mpos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(mpos):
                    self.dragging = True
                    self._update_value_from_pos(mpos[0])
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self._update_value_from_pos(mpos[0])
        return self.value