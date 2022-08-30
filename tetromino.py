import pygame
import random
import constants

from playfield import Playfield
from block import Block


class Tetromino(object):
    """
    The class used as the basic template for all the variants of the tetromino shapes used in the game.
    """

    current_bag = []
    """Stores (in a list) the current set of tetromino classes used to generate each piece in a random order"""

    def __init__(self, display_colour, image, playfield):
        """
        Initialise all the attributes required to make up any tetromino object.

        :param display_colour: The colour that the tetromino should be displayed with.
        :param image: The image of the tetromino piece that will be displayed.
        :param playfield: The instance of the Playfield class used throughout the program.
        :type display_colour: tuple
        :type image: pygame.Surface
        :type playfield: Playfield
        """

        self.x_coord = 0
        """Stores the playfield column position of the tetromino’s origin."""
        self.y_coord = 0
        """Stores the playfield row position of the tetromino’s origin."""

        self.colour = display_colour
        """Stores the RGB colour that the tetromino will be displayed with."""

        self.display_image = image
        """Stores the image of the tetromino piece that will be used to display it on the Next Queue"""

        # Size of 4, since tetromino pieces are made up of 4 square units.
        self.square_units = [None] * 4
        """Holds the four square units that make up the tetromino piece"""

        # A 'vector' stored for each square unit for each orientation.
        self.block_positions = [[[0] * 2 for i in range(4)]]
        """
        Holds the relative coordinate positions (from the tetromino's origin position) of each square unit
        of the tetromino piece, for each orientation
        """

        self.rotation_index = 0
        """ 
        Stores the current index used from the block_positions 3D list, to keep track of the tetromino's current
        orientation
        """

        self.grid = playfield
        """A reference to the playfield the tetromino is placed on"""

    @staticmethod
    def get_tetromino_set():
        """
        Returns all the class types derived from the Tetromino class in a tuple.

        :return: a tuple of class types
        """
        return ShapeI, ShapeJ, ShapeL, ShapeO, ShapeS, ShapeT, ShapeZ

    @staticmethod
    def random_generator(playfield):
        """
        A Python generator, used to generate sequences of tetromino objects in a random order, out of all the 7 types.
        Only one is returned per call - using next()

        :param playfield: a reference to the Playfield component
        :return: an instance of one of the Tetromino derived classes
        """

        # Get the tetromino set holding all the tetromino class types
        tetromino_set = Tetromino.get_tetromino_set()

        # Infinite loop, to continuously generate random sets of tetrominoes with no limit
        while True:
            # Create a copy of the set of tetromino class types and store it.
            bag = list(tetromino_set)
            # Arrange the tetromino derived classes in a random order
            random.shuffle(bag)

            # loop through each class type element to return a new instance of each tetromino class in turn
            for tetromino in bag:
                # Return a new tetromino class instance, and 'halt' the generator until the next call.
                yield tetromino(playfield)

    @staticmethod
    def create_surface(width_units, height_units):
        """
        Returns a new image with a width and height in terms of the square size of the playfield units.

        :param width_units: The width of the image in multiples of the square size of the playfield.
        :param height_units: The height of the image in multiples of the square size of the playfield.
        :type width_units: int
        :type height_units: int
        :return: A pygame Surface object which represents the image.
        """
        # get the scale of each grid square unit from the Playfield class
        scale = Playfield.get_square_size()

        # specify the width and height of the tetromino image, in multiples of the grid scale size.
        width = width_units * scale
        height = height_units * scale

        # return a new Surface object with dimensions given by width and height passed to it.
        return pygame.Surface((width, height))
        # return pygame.Surface((width, height), pygame.SRCALPHA, 32)

    def get_image(self):
        """
        Returns the image of the tetromino piece
        :return: A pygame Surface object
        """
        return self.display_image

    def shift_left(self):
        """
        Moves the block horizontally on the playfield, one space to the left.

        :return: None
        """

        # Validation: Do not shift the tetromino if it would collide with the playfield or another block
        if not self.would_collide(-1, 0):

            # Tetromino will be shifted left, therefore decrease x-origin by 1
            self.x_coord -= 1

            # First remove the square units from the playfield.
            self.remove_blocks()

            # Loop through each square unit of the tetromino piece
            for block in self.square_units:
                # Each block will be shifted to the left by one place
                block.shift_left()

            # Finally place all blocks back onto the grid.
            self.add_to_grid()

    def shift_right(self):
        """
        Moves the block horizontally on the playfield, one space to the right.

        :return: None
        """

        # Validation: Do not shift the tetromino if it would collide with the playfield or another block
        if not self.would_collide(1, 0):

            # Tetromino will be shifted right, therefore increase x-origin by 1
            self.x_coord += 1

            # First remove the square units from the playfield.
            self.remove_blocks()

            # Loop through each square unit of the tetromino piece
            for block in self.square_units:
                # Each block will be shifted to the right by one place
                block.shift_right()

            # Finally place all blocks back onto the grid.
            self.add_to_grid()

    def shift_down(self):
        """
        Moves the block vertically on the playfield, one space downwards.

        :return: None
        """

        # Tetromino will be shifted down, therefore increase y-origin by 1 (down is +ve)
        self.y_coord += 1

        # First remove the square units from the playfield.
        self.remove_blocks()

        # Loop through each square unit of the tetromino piece
        for block in self.square_units:
            # Each block will be shifted downwards by one place
            block.shift_down()

        # Finally place all blocks back onto the grid.
        self.add_to_grid()

    def would_collide(self, dx, dy):
        """
        Checks whether shifting the tetromino in a given direction will cause it to collide with the playfield
        boundaries or other blocks already on it.
        Returns true if there would be a collision.
        Returns false otherwise.

        :param dx: the change in the x position of the tetromino - to verify whether or not it would be valid.
        :param dy: the change in the y position of the tetromino - to verify whether or not it would be valid.
        :type dx: int
        :type dy: int
        :return: Boolean value
        """

        # grid = GameInterfaceModel.get_playfield() OLD!!!

        # loop through each square units of the tetromino
        for block in self.square_units:

            # define the x and y coordinates of where to check for collision
            x = block.get_x_coord() + dx
            y = block.get_y_coord() + dy

            # it would collide if the position is outside of the grid boundaries
            if not self.grid.is_in_bounds(x, y):
                return True

            # a collision would occur if the position is currently occupied
            if not self.grid.check_cell_empty(x, y):

                # get the block at the position
                block_found = self.grid.get_block(x, y)

                # the collision would only count if the block is not from the same tetromino piece
                if block_found not in self.square_units:
                    return True
        return False

    def is_on_ground(self):
        """
        Checks whether shifting the tetromino shape further downwards would cause it to collide with the bottom of the
        playfield or other blocks already on it.
        Returns true if it would collide if shifted further downwards.
        Returns false otherwise.

        :return: Boolean value
        """
        return self.would_collide(0, 1)

    def setup_blocks(self, pos_x, pos_y):
        """
        Called before spawning the tetromino piece onto the playfield. It sets up the square blocks of the tetromino
        piece, and their initial positions on the playfield.

        :param pos_x: the initial x-position to place the tetromino piece.
        :param pos_y: the initial y-position to place the tetromino piece.
        :type pos_x: int
        :type pos_y: int
        :return: None
        """

        # Set the origin coordinates of the tetromino to the parameter values passed.
        self.x_coord = pos_x
        self.y_coord = pos_y

        # Extract the relative positions of the blocks for the current orientation.
        block_vectors = self.block_positions[self.rotation_index]

        # loop through each index of the block_vectors 2D list.
        for i in range(0, len(block_vectors)):  # 0 - 4 exclusive

            # Get the relative position the block will be set at
            vector = block_vectors[i]

            # Calculate the actual position to place the block at on the grid
            x = pos_x + vector[0]
            y = pos_y + vector[1]

            # Instantiate the block, passing the initial position and colour.
            block = Block(self.colour, x, y)

            # Add the block to the square_units list at the position of the index
            self.square_units[i] = block

    def remove_blocks(self):
        """
        Removes all the square units of the tetromino from the playfield.

        :return: None
        """
        # Loop through each square unit of the tetromino
        for block in self.square_units:
            # Remove each one from the playfield.
            self.grid.remove_block(block)

    def rotate(self, dr):
        """
        Used to rotate the tetromino piece at a 90 degree interval

        :param dr: The direction that the tetromino piece should be rotated.
                    dr =  1 -> Clockwise
                    dr = -1 -> Anticlockwise

        :return: None
        """

        # Validation: Do not rotate the tetromino if it would collide with the playfield or another block
        if not self.can_rotate(dr):
            return

        # Get the number of possible orientation of the tetromino
        n = len(self.block_positions)

        # Change the rotation index by the amount given by the parameter
        self.rotation_index += dr

        """
        The index is circular - meaning it will cycle from 0 to thr highest index of block_positions
        """
        # When it passes the max index,
        if self.rotation_index == n:
            # Recycle back to the beginning
            self.rotation_index = 0

        # When it goes below the minimum index,
        elif self.rotation_index == -1:
            # recycle to the end.
            self.rotation_index = n - 1

        # Get the relative positions that each block should be placed at.
        block_vectors = self.block_positions[self.rotation_index]

        # First remove the tetromino's blocks from the playfield
        self.remove_blocks()

        # Loop through each index of the square blocks
        for i in range(0, len(self.square_units)):

            # Get the block and its position vector from the tetromino origin
            block = self.square_units[i]
            vector = block_vectors[i]

            # Calculate the column and row positions the blocks would be placed at.
            x = self.x_coord + vector[0]
            y = self.y_coord + vector[1]

            # Set the position of the block
            block.set_coords(x, y)

            # It will then be added to the playfield.
            self.grid.add_block(block)

    def can_rotate(self, dr):
        """
        Checks whether rotating the tetromino in a given direction will cause it to collide with the playfield
        boundaries or other blocks already on it.
        Returns true if there would be a collision.
        Returns false otherwise.

        :param dr: The direction to rotation - to verify whether or not it is valid.

        :return: Boolean value
        """

        # Use a temporary variable in place of rotation_index
        temp_index = self.rotation_index + dr

        # Get the number of possible orientation of the tetromino
        n = len(self.block_positions)

        """
        The index is circular - meaning it will cycle from 0 to thr highest index of block_positions
        """
        # When it passes the max index,
        if temp_index == n:
            # Recycle back to the beginning
            temp_index = 0

        # When it goes below the minimum index,
        elif temp_index == -1:
            # recycle to the end.
            temp_index = n - 1

        # Get the relative positions that each block should be placed at.
        block_vectors = self.block_positions[temp_index]

        # Iterate over each block position's vector from the tetromino's origin.
        for vector in block_vectors:

            # Calculate the column and row positions the blocks would be placed at.
            x = self.x_coord + vector[0]
            y = self.y_coord + vector[1]

            # It would collide if the position is outside of the grid boundaries
            if not self.grid.is_in_bounds(x, y):
                return False

            # A collision would occur if the position is currently occupied
            if not self.grid.check_cell_empty(x, y):

                # Get the block at the position
                block_found = self.grid.get_block(x, y)

                # The collision would only count if the block is not from the same tetromino piece
                if block_found not in self.square_units:
                    return False

        # At this point, no collisions were found, therefore the tetromino can rotate.
        return True

    def rotate_clockwise(self):
        """
        Rotates the tetromino piece 90 degrees clockwise.

        :return: None
        """
        # Simply call the rotate() method, passing the value of 1 (clockwise direction)
        self.rotate(1)

    def rotate_anticlockwise(self):
        """
        Rotates the tetromino piece 90 degrees clockwise.

        :return: None
        """
        # Simply call the rotate() method, passing the value of -1 (anticlockwise direction)
        self.rotate(-1)

    def get_rows(self):
        """
        Gets the row indexes of the playfield where at least one square unit of the tetromino can be found on.

        :return: A list containing the row indexes (integers) sorted in ascending order
        """

        # Define a new empty list, which will be returned at the end.
        rows = list()

        # Loop through each block of the tetromino
        for block in self.square_units:

            # Get the current blocks's row position
            y = block.get_y_coord()

            # Check if the row index is not already present in the list
            if y not in rows:
                # Add it to list if not present
                rows.append(y)

        # Sort the list in ascending order before returning it.
        rows.sort()
        return rows

    def get_blocks(self):
        """
        Gets the square units of the tetromino.

        :return: A list of Blocks - containing all the square units of the tetromino
        """

        return self.square_units

    def add_to_grid(self):
        """
        Places all the blocks of the tetromino on the playfield

        :return: None
        """
        # Loop through each of the tetromino's block
        for block in self.square_units:
            # Have each block added to the playfield
            self.grid.add_block(block)


class ShapeI(Tetromino):
    """
    The class used to represent the 'I' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.CYAN
    """a constant tuple for the RGB colour of the tetromino (cyan)"""

    # create a surface object, with a width of 4 units, and a height of 1 unit
    image = Tetromino.create_surface(width_units=4, height_units=1)

    # completely fill the surface with the RGB colour constant
    image.fill(SURFACE_COLOUR)

    def __init__(self, playfield):

        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeI.SURFACE_COLOUR, ShapeI.image, playfield)

        # Initialise the block positions specific for this class.
        self.block_positions = [[(0,  0), (1, 0), (2, 0), (3, 0)],
                                [(2, -1), (2, 0), (2, 1), (2, 2)]]


class ShapeJ(Tetromino):
    """
    The class used to represent the 'J' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.BLUE
    """a constant tuple for the RGB colour of the tetromino (blue)"""

    # create a surface object, with a width of 3 units, and a height of 2 unit
    image = Tetromino.create_surface(width_units=3, height_units=2)

    # get the scale of each grid square unit from the Playfield class
    scale = Playfield.get_square_size()

    # specify area of top half of surface to fill
    top_region = pygame.Rect((0, 0), (scale, scale))

    # specify area of bottom half of surface to fill
    bottom_region = pygame.Rect((0, scale), (scale*3, scale))

    # fill each of these regions
    image.fill(SURFACE_COLOUR, top_region)
    image.fill(SURFACE_COLOUR, bottom_region)

    # These variables are not needed anymore, therefore discard them so they do not stay as static variables.
    del scale
    del top_region
    del bottom_region

    def __init__(self, playfield):
        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeJ.SURFACE_COLOUR, ShapeJ.image, playfield)

        # Initialise the block positions specific for this class.
        self.block_positions = [[(0,  0), (0,  1), (1, 1), (2,  1)],
                                [(2, -1), (1, -1), (1, 0), (1,  1)],
                                [(2,  1), (2,  0), (1, 0), (0,  0)],
                                [(0,  1), (1,  1), (1, 0), (1, -1)]]


class ShapeL(Tetromino):
    """
    The class used to represent the 'L' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.ORANGE
    """a constant tuple for the RGB colour of the tetromino (orange)"""

    # create a surface object, with a width of 3 units, and a height of 2 unit
    image = Tetromino.create_surface(width_units=3, height_units=2)

    # get the scale of each grid square unit from the Playfield class
    scale = Playfield.get_square_size()

    # specify area of top half of surface to fill
    top_region = pygame.Rect((scale*2, 0), (scale, scale))

    # specify area of bottom half of surface to fill
    bottom_region = pygame.Rect((0, scale), (scale*3, scale))

    # fill each of these regions
    image.fill(SURFACE_COLOUR, top_region)
    image.fill(SURFACE_COLOUR, bottom_region)

    # These variables are not needed anymore, therefore discard them so they do not stay as static variables.
    del scale
    del top_region
    del bottom_region

    def __init__(self, playfield):
        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeL.SURFACE_COLOUR, ShapeL.image, playfield)

        # Initialise the block positions specific for this class.
        self.block_positions = [[(0,  1), (1, 1), (2,  1), (2,  0)],
                                [(1, -1), (1, 0), (1,  1), (2,  1)],
                                [(2,  0), (1, 0), (0,  0), (0,  1)],
                                [(1,  1), (1, 0), (1, -1), (0, -1)]]


class ShapeO(Tetromino):
    """
    The class used to represent the 'O' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.YELLOW
    """a constant tuple for the RGB colour of the tetromino (yellow)"""

    # create a surface object, with a width of 2 units, and a height of 2 units
    image = Tetromino.create_surface(width_units=2, height_units=2)

    # completely fill the surface with the RGB colour constant
    image.fill(SURFACE_COLOUR)

    def __init__(self, playfield):
        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeO.SURFACE_COLOUR, ShapeO.image, playfield)

        # Initialise the block positions specific for this class.
        self.block_positions = [[(1, 0), (1, 1), (2, 1), (2, 0)]]

    def rotate(self, dr):
        """
        Tetromino-O does not change position when rotated, therefore have nothing happen the rotate() method is callled
        """
        return


class ShapeS(Tetromino):
    """
    The class used to represent the 'S' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.GREEN
    """a constant tuple for the RGB colour of the tetromino (green)"""

    # create a surface object, with a width of 3 units, and a height of 2 unit
    image = Tetromino.create_surface(width_units=3, height_units=2)

    # get the scale of each grid square unit from the Playfield class
    scale = Playfield.get_square_size()

    # specify area of top half of surface to fill
    top_region = pygame.Rect((scale, 0), (scale*2, scale))

    # specify area of bottom half of surface to fill
    bottom_region = pygame.Rect((0, scale), (scale*2, scale))

    # fill each of these regions
    image.fill(SURFACE_COLOUR, top_region)
    image.fill(SURFACE_COLOUR, bottom_region)

    # These variables are not needed anymore, therefore discard them so they do not stay as static variables.
    del scale
    del top_region
    del bottom_region

    def __init__(self, playfield):
        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeS.SURFACE_COLOUR, ShapeS.image, playfield)
        # Initialise the block positions specific for this class.
        self.block_positions = [[(0,  1), (1, 1), (1, 0), (2, 0)],
                                [(0, -1), (0, 0), (1, 0), (1, 1)]]


class ShapeT(Tetromino):
    """
    The class used to represent the 'T' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.PURPLE
    """a constant tuple for the RGB colour of the tetromino (purple)"""

    # create a surface object, with a width of 3 units, and a height of 2 unit
    image = Tetromino.create_surface(width_units=3, height_units=2)

    # get the scale of each grid square unit from the Playfield class
    scale = Playfield.get_square_size()

    # specify area of top half of surface to fill
    top_region = pygame.Rect((scale, 0), (scale, scale))

    # specify area of bottom half of surface to fill
    bottom_region = pygame.Rect((0, scale), (scale*3, scale))

    # fill each of these regions
    image.fill(SURFACE_COLOUR, top_region)
    image.fill(SURFACE_COLOUR, bottom_region)

    # These variables are not needed anymore, therefore discard them so they do not stay as static variables.
    del scale
    del top_region
    del bottom_region

    def __init__(self, playfield):
        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeT.SURFACE_COLOUR, ShapeT.image, playfield)

        # Initialise the block positions specific for this class.
        self.block_positions = [[(1, 0), (0,  1), (1, 1), (2,  1)],
                                [(2, 0), (1, -1), (1, 0), (1,  1)],
                                [(1, 1), (2,  0), (1, 0), (0,  0)],
                                [(0, 0), (1,  1), (1, 0), (1, -1)]]


class ShapeZ(Tetromino):
    """
    The class used to represent the 'Z' shaped tetrominoes
    """

    SURFACE_COLOUR = constants.RED
    """a constant tuple for the RGB colour of the tetromino (red)"""

    # create a surface object, with a width of 3 units, and a height of 2 unit
    image = Tetromino.create_surface(width_units=3, height_units=2)

    # get the scale of each grid square unit from the Playfield class
    scale = Playfield.get_square_size()

    # specify area of top half of surface to fill
    top_region = pygame.Rect((0, 0), (scale*2, scale))

    # specify area of bottom half of surface to fill
    bottom_region = pygame.Rect((scale, scale), (scale*2, scale))

    # fill each of these regions
    image.fill(SURFACE_COLOUR, top_region)
    image.fill(SURFACE_COLOUR, bottom_region)

    # These variables are not needed anymore, therefore discard them so they do not stay as static variables.
    del scale
    del top_region
    del bottom_region

    def __init__(self, playfield):
        # call the constructor of the Tetromino class, passing the colour tuple, image and the playfield instance
        super().__init__(ShapeZ.SURFACE_COLOUR, ShapeZ.image, playfield)

        # Initialise the block positions specific for this class.
        self.block_positions = [[(0,  0), (1, 0), (1, 1), (2, 1)],
                                [(2, -1), (2, 0), (1, 0), (1, 1)]]
