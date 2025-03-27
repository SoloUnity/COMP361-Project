import pygame
from gui.control_element.edit_rover import EditRover
from models.rover import Rover

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    # pygame.display.set_caption("Rover Editor")

    clock = pygame.time.Clock()
    running = True

    rover = Rover()
    editor = EditRover(screen, rover)
    button_rect = pygame.Rect(250, 300, 100, 50)

    while running:
        screen.fill((255, 255, 255))

        events = pygame.event.get()  # Retrieve events once

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    editor.toggle_popup()
                    print(f'Popup active: {editor.active}')

        editor.update(events)  # Pass the same event list

        editor.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
