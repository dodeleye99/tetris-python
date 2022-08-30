from info_panel import InfoPanel


class NextPanel(InfoPanel):
    """
    The panel class used to represent a container component that is dedicated for displaying the next
    tetromino piece on the screen.
    """
    def __init__(self):

        # temporary variables for the dimensions of the display surface of the panel.
        width = 100
        height = 100

        # Call the constructor of the BasePanel class, to setup the generic panel attributes.
        super().__init__((0, 0), (width, height))  # top left position (0,0), and screen dimensions passed.

        # Alter the rect coordinates.
        self.rect_coords.right = 320  # x-coordinate of the right side of the panel is set.
        self.rect_coords.top = 170  # y-coordinate of the top of the panel is set.

        self.next_label = "NEXT PIECE"
        """ Used to hold the string that will be used for the label text for the container displayed."""

        self.next_tetromino = None
        """The next tetromino piece that will be placed on the playfield after the current one."""

        self.show_next_piece = True
        """Determines whether or not the next piece should be shown"""

    def setup_display(self):
        """
        Setup the surface of the next panel before it is drawn onto the game interface.

        :return: None
        """

        # Clear the surface before redrawing.
        self.clear_surface()

        # Create a surface image of the label text.
        label_text = InfoPanel.create_text(self.next_label)

        # Get the rectangular coordinates of the text surface to modify them.
        label_rect = label_text.get_rect()

        """Since the text is drawn on the panel, its rect coordinates are relative to the panel
        rather than the screen"""
        # local y-coordinate of the top of the text surface is set.
        label_rect.top = 5
        # Set the local center-x position of the text surface to the middle of the panel surface
        label_rect.centerx = self.rect_coords.width // 2

        # Draw the label text onto the display surface at the position given by its rectangular coordinates.
        self.display_surface.blit(label_text, label_rect)

        # Stop at this point if the next piece should not be displayed.
        if not self.show_next_piece:
            return

        # Get the image of the next tetromino piece
        tetromino_image = self.next_tetromino.get_image()

        # Get the rectangular coordinates of the image to modify them
        tetromino_rect = tetromino_image.get_rect()

        # Define the centre x and y positions of the panel surface
        centre_x = self.rect_coords.width // 2
        centre_y = self.rect_coords.height // 2

        # Set the centre position of the Rect object to the centre of the panel, but 10 pixels downwards.
        tetromino_rect.center = (centre_x, centre_y + 10)

        # Draw the tetromino image onto the panel surface at the positon given by the rectangular coordinates
        self.display_surface.blit(tetromino_image, tetromino_rect)

    def set_next(self, next_piece):
        """
        Sets the next tetromino piece to place on the playfield after the current one.

        :param next_piece: the new tetromino piece that should be set as the next one.
        :return: None
        """
        self.next_tetromino = next_piece

    def get_next(self):
        """
        Returns the next tetromino piece.

        :return: A Tetromino class instance of next tetromino piece
        """
        return self.next_tetromino

    def set_visible(self, is_visible):
        """
        Change the state of the Next Queue, to either show or hide the next piece.

        :param is_visible: The value used to determine whether or not the piece should be displayed
        :type is_visible: bool
        :return: None
        """
        # Simply set the parameter to the attribute used for this purpose.
        self.show_next_piece = is_visible
