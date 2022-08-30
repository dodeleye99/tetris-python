

class Block(object):
    """
    The class used to represent a single square unit of a tetromino piece, taking up one cell of the playfield
    """
    def __init__(self, surface_colour, x, y):
        """
        Initialise the class, setting its surface colour and initial coordinates, then adding it to the grid.

        :param surface_colour: The colour it should be displayed with on the grid.
        :param x: The x coordinate it should start at on the grid.
        :param y: The y coordinate it should start at on the grid.
        :type surface_colour: tuple
        :type x: int
        :type y: int
        """

        # Initialise the attributes
        self.colour = surface_colour
        """Stores the RGB colour that the block will be displayed with on the playfield."""
        self.x_coord = x
        """Stores the column index that the block is stored at on the playfield"""
        self.y_coord = y
        """Stores the row index that the block is stored at on the playfield"""

    def get_colour(self):
        """
        Get the colour that the block is displayed with.

        :return: RGB colour format in within a tuple (r,g,b)
        """

        return self.colour

    def get_x_coord(self):
        """
        Get the x coordinates the block is set at on the grid.

        :return: int value for the x coordinate
        """

        return self.x_coord

    def get_y_coord(self):
        """
        Get the y coordinate the block is set at on the grid.

        :return: int value for the y coordinate
        """

        return self.y_coord

    def set_coords(self, x, y):
        """
        Sets the row and column position of the block

        :param x: the column position to set the block to
        :param y: the row position to set the block to
        :type x: int
        :type y: int
        :return: None
        """
        self.x_coord = x
        self.y_coord = y

    def set_x_coord(self, x):
        """
        Sets the column position of the block

        :param x: the row position to set the block to
        :type x: int
        :return: None
        """
        self.x_coord = x

    def set_y_coord(self, y):
        """
        Sets the row position of the block

        :param y: the row position to set the block to
        :type y: int
        :return: None
        """
        self.y_coord = y

    def translate(self, dx=0, dy=0):
        """
        Moves the block along the playfield, horizontally or vertically.

        :param dx: The change in the x coordinate of the block (+ve = right, -ve = left)
        :param dy: The change in the y coordinate of the block (+ve = down, -ve = up)
        :type dx: int
        :type dy: int

        :return: None
        """

        # Change the x and y coordinates
        self.x_coord += dx
        self.y_coord += dy

    def shift_left(self):
        """
        Moves the block horizontally on the playfield, one space to the left.

        :return: None
        """

        # Simply call the translate method, passing -1 to dx to move the block one space to the left.
        self.translate(dx=-1)

    def shift_right(self):
        """
        Moves the block horizontally on the playfield, one space to the right.

        :return: None
        """

        # Simply call the translate method, passing 1 to dx to move the block one space to the right.
        self.translate(dx=1)

    def shift_down(self):
        """
        Moves the block vertically on the playfield, one space downwards.

        :return: None
        """

        # Simply call the translate method, passing 1 to dy to move the block one space downwards.
        self.translate(dy=1)
