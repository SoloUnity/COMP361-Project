import pygame

# TODO: confirmation box
# TODO: fix coordinates displaying when menu active

class BoundingBox:
    def __init__(self, display, x, y, w, h):
        self.display = display
        self.coords = None
        self.rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.font = pygame.font.SysFont("arial", 13)
        self.start_coord = None
        self.end_coord = None
        self.dragging = False

    def get_bounds(self):
        return self.start_coord, self.end_coord

    def reset(self):
        self.start_coord = None
        self.end_coord = None

    def draw(self, coords):
        #Draws the bounding box and the dragging selection if active.
        if self.start_coord and self.end_coord:
            drag_x = min(self.start_coord[0], self.end_coord[0])
            drag_y = min(self.start_coord[1], self.end_coord[1])
            drag_w = abs(self.end_coord[0] - self.start_coord[0])
            drag_h = abs(self.end_coord[1] - self.start_coord[1])

            dragging_box = pygame.Rect(drag_x, drag_y, drag_w, drag_h)
            pygame.draw.rect(self.display, (200, 200, 200), dragging_box, 1)

        if self.active:
            mpos = pygame.mouse.get_pos()
            if coords:
                text_surface = self.font.render(str(coords), True, "white")
                
                # If mpos not close to right edge
                if mpos[0] < self.display.get_width() - text_surface.get_width() - 30:
                    text_pos = (mpos[0] + 10, mpos[1] + 10)
                # If mpos too close to right edge, put text on left side
                else:
                    text_pos = (mpos[0] - text_surface.get_width() - 5, mpos[1] + 10)

                self.display.blit(text_surface, text_pos)

    def update(self, events):
        #Handles events for mouse interaction.
        mpos = pygame.mouse.get_pos()
        self.active = self.rect.collidepoint(mpos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active:
                    self.start_coord = mpos
                    self.end_coord = mpos
                    self.dragging = True  
                    # print("Start: "+ str(self.start_coord))

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                if self.active:
                    self.end_coord = mpos
                    
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
                # print("End: "+ str(self.end_coord))  
