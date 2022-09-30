import pygame
import constants


class BasePanel(object):
    """
    The abstract base class used as the template for the other classes, each holding specific data which will be
    displayed within a boxed region while the Tetris is being played.
    """

    outline_colour = constants.WHITE  # RGB white
    """The outline colour that each panel will be surrounded with when displayed on the screen"""

    bg_colour = constants.BLACK  # RGB black
    """The background colour that each panel will have when displayed on the screen"""

    def __init__(self, top_left, size):
        """
        Initialise all the attributes required to make up any panel object.

        :param top_left: The top left coordinates the panel object will be displayed at.
        :param size: The width and height of the surface of the panel to be displayed on the screen.
        :type top_left: tuple
        :type size: tuple
        """

        self.rect_coords = pygame.Rect(top_left, size)
        """
        The rectangular coordinates of the panel surface being displayed on the screen.
        Stores its top-left x and y coordinates, and its width and height.
        """

        self.display_surface = pygame.Surface(size)
        """The surface object used to represent the image of the panel displayed on the screen."""

    @staticmethod
    def get_outline_colour():
        """
        returns the gridline colour of the panel

        :return: RGB colour format in within a list [r,g,b]
        """
        return BasePanel.outline_colour

    def setup_display(self):
        """
        An abstract method that will be overridden by derived panel classes to update its surface before drawn onto the
        screen.

        :return: None
        """
        pass  # Due to being abstract, it will not be implemented.

    def get_surface(self):
        """
        returns the display surface of the panel.

        :return: A pygame Surface object
        """
        return self.display_surface

    def get_rect(self):
        """
        returns the rectangular coordinates of the panel surface.

        :return: a pygame Rect object
        """
        return self.rect_coords

    def clear_surface(self):
        """
        # Fills the panel surface with the shared background colour.

        :return: None
        """
        self.display_surface.fill(BasePanel.bg_colour)
