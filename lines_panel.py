from info_panel import InfoPanel


class LinesPanel(InfoPanel):
    """
    The panel class used to represent a container component that is dedicated for displaying the total number of lines
    cleared (full rows of blocks) by the player during the Tetris game.
    """

    def __init__(self):

        # temporary variables for the dimensions of the display surface of the panel.
        width = 200
        height = 30
        # Call the constructor of the BasePanel class, to setup the generic panel attributes.
        super().__init__((0, 0), (width, height))

        # Alter the rect coordinates accordingly.
        self.rect_coords.left = 10
        self.rect_coords.top = 10

        self.lines = 0
        """Stores the number of full rows of blocks cleared by the player"""

        self.lines_label = "LINES CLEARED"
        """ Used to hold the string that will be used as the label text for the lines value displayed in the panel"""

    def add_lines_cleared(self, lines_cleared):
        """
        increases the total number of lines cleared by a given amount.

        :param lines_cleared: The number of lines to add to the current lines total
        :type lines_cleared: int
        :return: None
        """
        self.lines += lines_cleared

    def setup_display(self):
        """
        Setup the surface of the lines panel, with an updated lines value, before it is drawn onto the game interface.

        :return: None
        """

        # Clear the surface before redrawing.
        self.clear_surface()

        """
        Arrange the string of text that will be displayed on the screen. It is the combination of the label string and
        the value of the number of lines cleared. At least 3 digits are always shown for the lines value.
        """
        display_string = self.lines_label + " - -    " + str(self.lines).zfill(3)

        # Create surface images of the single string consisting of the label text and lines text
        display_text = InfoPanel.create_text(display_string)

        # Get the rectangular coordinates of the text surface to modify them.
        text_rect = display_text.get_rect()

        """Since the text is drawn on the panel, its rect coordinates are relative to the panel
        rather than the screen"""

        """
        local y position of the centre of the label text is set to half the height of the surface so it is positioned
        at the centre of the surface.
        """
        text_rect.centery = self.rect_coords.height // 2
        # local x position of the left side of the level text surface is set.
        text_rect.left = 10

        # Draw the text surface onto the display surface at the position given by its rectangular coordinates.
        self.display_surface.blit(display_text, text_rect)
