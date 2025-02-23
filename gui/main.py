import pygame, sys

import os  
from states.login import Login
from states.simulation import Simulation
from states.state_manager import ProgramStateManager

pygame.init()

# Constants
FPS = 120
SCREENWIDTH, SCREENHEIGHT = 1280, 720
LOGIN_WIDTH = 600
LOGIN_HEIGHT = 700
FONT = pygame.font.Font("Inter/Inter-VariableFont_opsz,wght.ttf", 18)

# Set the environment variable to center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

class Program:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Math Pathfinding Simulator')

        self.clock = pygame.time.Clock()
        self.programStateManager = ProgramStateManager('login')
        self.login = Login(self.screen, self.programStateManager)
        self.simulation = Simulation(self.screen, self.programStateManager)

        self.states = {'login': self.login, 'simulation': self.simulation}
        self.fullscreen = False

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current_state = self.programStateManager.get_state()
            self.states[current_state].run(events)

            #weird block of code

            if current_state == 'simulation' and not self.fullscreen:
                self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.NOFRAME)
                self.fullscreen = True
                
            elif current_state == 'login' and self.fullscreen:
                self.screen = pygame.display.set_mode((LOGIN_WIDTH, LOGIN_HEIGHT))
                self.fullscreen = False

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    program = Program()
    program.run()