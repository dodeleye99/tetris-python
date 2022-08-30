import constants
import pygame
from base_panel import BasePanel


class InfoPanel(BasePanel):
    """
    The abstract base class used as the template for the other classes that will hold specific game information.
    """

    # the font module must be initialised before it can be used.
    pygame.font.init()

    font = pygame.font.SysFont("Impact", 20)  # Use the impact font, size 20.
    """The font that will be used by all text displayed on each panel"""

    text_antialiased = True
    """Determines whether the text drawn on the screen will have anti-aliasing"""

    text_colour = constants.WHITE  # RGB white
    """The colour that all text on the panel will be displayed in on the screen"""

    def __init__(self, top_left, size):
        """
        Initialise all the attributes required to make up any panel object.

        :param top_left: The top left coordinates the panel object will be displayed at.
        :param size: The width and height of the surface of the panel to be displayed on the screen.
        :type top_left: tuple
        :type size: tuple
        """

        # Call the constructor of the base class, passing on the parameters.
        super().__init__(top_left, size)

    @staticmethod
    def create_text(text):
        """
        Returns a surface image of the given text, in the text colour of the panel, from the pre-defined font object

        :param text: the text to be displayed as an image
        :type text: str
        :return: a pygame Surface object for the text.
        """
        # Surface object created using the pre-defined font.
        return InfoPanel.font.render(text, InfoPanel.text_antialiased, InfoPanel.text_colour)
