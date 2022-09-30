from info_panel import InfoPanel


class LevelPanel(InfoPanel):
    """
    The panel class used to represent a container component that is dedicated for displaying current speed level of the
    Tetris game.
    """

    def __init__(self):
        # temporary variables for the dimensions of the display surface of the panel.
        width = 100
        height = 60

        # Call the constructor of the BasePanel class, to setup the generic panel attributes.
        super().__init__((0, 0), (width, height))  # top left position (0,0), and screen dimensions passed.

        # Alter the rect coordinates.
        self.rect_coords.right = 320  # x-coordinate of the right side of the panel is set.
        self.rect_coords.top = 280  # y-coordinate of the top of the panel is set.

        self.level = 1
        """
        Stores the value of the current game level. This determines the speed at which the tetromino pieces will fall,
        and the amount of points gained by the player clearing lines.
        """

        self.level_label = "LEVEL"
        """ Used to hold the string that will be used for the label text of the container displaying the level."""

        self.lines_to_level = 10
        """The number of lines needed to clear per level to increase the level"""

        self.lines_left = self.lines_to_level
        """The current number of lines needed to level up"""

    def update_level(self, lines):
        """
        Takes in the number of lines cleared to check whether a level up should occur

        :param lines: The number of lines that were cleared
        :return:
        """

        # Repeat as many times as the number of lines that were cleared
        for i in range(lines):
            # Decrement the number of lines needed to level up
            self.lines_left -= 1

            # Check if enough lines have been cleared to level up
            if self.lines_left == 0:
                # Increase the level
                self.level += 1
                # Reset the lines needed for the next level
                self.lines_left = self.lines_to_level

    def get_current_level(self):
        """
        returns the current level of the game.

        :return: the value (int) of the current level.
        """
        return self.level

    def setup_display(self):
        """
        Setup the surface of the level panel, with an updated level value, before it is drawn onto the game interface.

        :return: None
        """

        # Clear the surface before redrawing.
        self.clear_surface()

        # Create surface images of the label text and level text.
        label_text = InfoPanel.create_text(self.level_label)
        level_text = InfoPanel.create_text(str(self.level).zfill(2))  # At least 2 digits are always shown

        # Get the rectangular coordinates of the text surfaces to modify them.
        label_rect = label_text.get_rect()
        level_rect = level_text.get_rect()

        """Since the text is drawn on the panel, its rect coordinates are relative to the panel
        rather than the screen"""
        # local y-coordinate of the top of the label text surface is set.
        label_rect.top = 5
        # local x position of the left side of the label text surface is set.
        label_rect.left = 10

        # local y-coordinate of the bottom of the level text surface is set.
        level_rect.bottom = self.rect_coords.height - 5
        # local x position of the left side of the level text surface is set.
        level_rect.left = 10

        # Draw both texts onto the display surface at the position given by their corresponding rectangular coordinates.
        self.display_surface.blit(label_text, label_rect)
        self.display_surface.blit(level_text, level_rect)
