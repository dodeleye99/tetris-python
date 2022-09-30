import pygame
import constants
from game_interface_model import GameInterfaceModel


class GameInterfaceView(object):

    """
    Represents the view component of the MVC paradigm.
    It involves outputting a visual representation of the game while it is running.
    """
    
    def __init__(self, model_instance):
        """
        Setup the view component.
        :param model_instance: A reference to the model component of the program to store in this class for easy access.
        :type model_instance: GameInterfaceModel
        """

        # Store a reference to the model component passed to the constructor.
        self.model = model_instance
        """
        Stores a reference to the model component for easy access.
        """

        # Set the background colour of the screen: RGB red.
        self.bg_colour = constants.RED
        """
        Stores the background colour of the program window.
        """

    def redraw(self):
        """
        Update the display of the screen to match the updated models.
        :return: None
        """

        # Clear the screen first.
        self.clear_screen()

        # Draw all the panel components holding game information.
        self.draw_hud()

        # Draw the playfield onto the screen.
        self.draw_grid()

        # Draw the pause button onto the screen
        self.draw_pause_button()

        # Must refresh the display screen to show all changes made to it.
        pygame.display.flip()

    def clear_screen(self):
        """
        Clears all the contents of the screen to allow for redrawing.
        :return: None
        """

        # Get the top-level display screen.
        screen = pygame.display.get_surface()
        # Fill it with the RGB colour given by the background colour attribute.
        screen.fill(self.bg_colour)

    def draw_hud(self):
        """
        draw all the panel components with their updated data onto the screen.

        :return: None
        """

        # Get a reference to a list of all the panel components from the model component of the program.
        panel_list = self.model.get_hud_components()

        # Get a reference to the top level surface where everything is drawn onto.
        screen = pygame.display.get_surface()

        # Iterate over each panel object in the list.
        for panel in panel_list:
            # First update the visual display of the panel so it is ready to be redrawn onto the screen.
            panel.setup_display()
            # Get the updated display surface and the rectangular coordinates of the panel object.
            surface = panel.get_surface()
            rect = panel.get_rect()

            # Get a reference to the outline colour of the panel object.
            outline_colour = panel.get_outline_colour()
            # Draw the surface of the panel onto the screen, at its rect position.
            screen.blit(surface, rect)
            # Draw an outline around the panel surface with its outline colour, with width (thickness) of 2.
            pygame.draw.rect(screen, outline_colour, rect, 2)

    def draw_grid(self):
        """
        draw the updated grid component onto the screen.

        :return: None
        """

        # Get a reference to the playfield from the model component of the program.
        grid = self.model.get_grid()

        # Get a reference to the top level surface where everything is drawn onto.
        screen = pygame.display.get_surface()

        # Update the visual display of the grid, ready to be redrawn onto the screen.
        grid.setup_display()

        # Get the updated display surface and the rectangular coordinates of the grid.
        surface = grid.get_surface()
        rect = grid.get_rect()

        # Draw the surface of the grid onto the screen, at its rect position.
        screen.blit(surface, rect)

        # Get a reference to the outline colour of the grid.
        outline_colour = grid.get_outline_colour()

        # Draw an outline around the playfield surface with its outline colour, with width (thickness) of 2.
        pygame.draw.rect(screen, outline_colour, rect, 2)

    def draw_pause_button(self):
        """
        draw the pause button component onto the screen.

        :return: None
        """

        # Get a reference to the pause button from the model component of the program.
        pause_button = self.model.get_pause_button()

        # Get a reference to the top level surface where everything is drawn onto.
        screen = pygame.display.get_surface()

        # Get the image and the rectangular coordinates of the pause button.
        image = pause_button.get_image()
        rect = pause_button.get_rect()

        # Draw the surface of the pause button onto the screen, at its rect position.
        screen.blit(image, rect)
