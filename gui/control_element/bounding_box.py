import pygame

# TODO: confirmation box
# TODO: fix coordinates displaying when menu active

class BoundingBox:
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.font = pygame.font.SysFont("arial", 13)

        self.start_coord = None
        self.end_coord = None
        self.dragging = False

    def get_coordinates(self):
        #Returns mouse coordinates relative to the bounding box.
        if self.active:
            mpos = pygame.mouse.get_pos()
            return (mpos[0] - self.rect.x, mpos[1] - self.rect.y)
        return None

    def draw(self):
        #Draws the bounding box and the dragging selection if active.
        if self.start_coord and self.end_coord:
            drag_x = min(self.start_coord[0], self.end_coord[0]) + self.rect.x
            drag_y = min(self.start_coord[1], self.end_coord[1]) + self.rect.y
            drag_w = abs(self.end_coord[0] - self.start_coord[0])
            drag_h = abs(self.end_coord[1] - self.start_coord[1])

            dragging_box = pygame.Rect(drag_x, drag_y, drag_w, drag_h)
            pygame.draw.rect(self.screen, (200, 200, 200), dragging_box, 1)

        if self.active:
            mpos = pygame.mouse.get_pos()
            coords = self.get_coordinates()
            if coords:
                text_surface = self.font.render(str(coords), True, "white")
                self.screen.blit(text_surface, (mpos[0] + 10, mpos[1] + 10))  

    def update(self, events):
        #Handles events for mouse interaction.
        mpos = pygame.mouse.get_pos()
        self.active = self.rect.collidepoint(mpos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active:
                    self.start_coord = self.get_coordinates()
                    self.end_coord = self.start_coord  
                    self.dragging = True  
                    # print("Start: "+ str(self.start_coord))

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                if self.active:
                    self.end_coord = self.get_coordinates()  
                    

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
                # print("End: "+ str(self.end_coord))  
