import pygame
import constants
from base_panel import BasePanel
import game_interface_model


class Playfield(BasePanel):
    """
    The class used to represent the grid component of the game interface called the playfield where Tetris is actually
    played on.
    """

    square_size = 20
    """ The square length in pixels for each grid cell when it is displayed on the screen.
    Will often be used to define the x and y intervals to draw on the playfield surface."""

    SOFT_DROP_GRAVITY = 1
    """The frame interval for gravity for when the active tetromino piece is allowed to drop at a faster rate."""

    def __init__(self, model_instance):
        """
        Initialises the Playfield instance

        :param model_instance: The single GameInterfaceModel instance used throughout the program
        :type model_instance: game_interface_model.GameInterfaceModel
        """

        # Define the grid dimensions.
        self.grid_width = 10
        """the width of the playfield - the number of units that can fit in a single row."""

        self.grid_height = 22
        """the height of the playfield - the number of units that can fit in a single column"""

        self.hidden_rows = 2  # Note: must always be less than the grid height.
        """the number of rows (from the top) that will not be displayed on the screen."""

        """
        Temporary variables used to define the rect and surface attributes. This is simply the dimensions of the 
        display surface of the playfield in pixels. The reason for multiplying the grid dimensions by square_size is 
        because each individual cell of the grid has the dimensions given by square_size.
        """
        surface_width = self.grid_width * self.square_size
        surface_height = (self.grid_height - self.hidden_rows) * self.square_size   # hidden rows will not be displayed

        """
        Temporary variables used to define the top-left x and y coordinates for the playfield surface - to be passed to
        the rect attribute.
        """
        top_left_x = 10
        top_left_y = 50

        # Call the constructor of the BasePanel class, to setup the generic panel attributes.
        super().__init__((top_left_x, top_left_y), (surface_width, surface_height))

        self.gridline_colour = constants.WHITE  # RGB White
        """The gridline colour that the playfield will have with when displayed on the screen"""

        self.active_tetromino = None
        """The tetromino piece currently being controlled (by the player) on the playfield"""

        # Initialise the grid data structure as an empty list of lists.
        self.matrix = [[None] * self.grid_width for _ in range(self.grid_height)]
        """The data structure for storing the square units of the tetromino pieces currently on the playfield"""

        self.model = model_instance
        """A reference of the single GameInterfaceModel instance used throughout the program"""

        # Calculate the initial gravity value
        self.gravity = self.model.calculate_gravity()
        """The frame interval that needs to be passed before dropping the active tetromino piece each time"""
        self.lock_delay = 30
        """The frame interval that needs to be passed before the active tetromino completely locks onto the playfield"""
        self.entry_delay = 25
        """The frame interval that needs to be passed before spawning the next tetromino
        after the previous tetromino locks onto the playfield."""

        self.gravity_counter = 0
        """The frame counter used to determine when the gravity frame interval has been passed"""
        self.lock_counter = 0
        """The frame counter used to determine when the lock delay frame interval has been passed"""
        self.entry_counter = 0
        """The frame counter used to determine when the entry delay frame interval has been passed"""

        self.in_lock_phase = False
        """Determines whether or not the active tetromino should be going through the lock phase"""
        self.tetromino_isactive = False
        """Determines whether or not the active tetromino is currently active (is not locked onto the playfield) """

        self.in_clear_phase = False
        """Determines whether or not the active tetromino should be going through the line clear phase"""

        self.clear_delay = 40
        """The frame interval that will be used to carry out the line clerar phase, before continuing the game."""

        self.game_over = False
        """Determines whether or not a game over condition has been met. The game should end after being set to True."""

        self.end_generator = self.game_over_generator()
        """Holds a generator object from GameOverGenerator(), used to carry out the game over phase"""
        self.clear_generator = None
        """Holds a generator object from LineClearGenerator(), used to carry out the line clear phase"""

        self.soft_drop_isactive = False
        """Determines whether or not soft drop gravity (fast falling) is being applied to the active tetromino"""

        self.grid_visible = True
        """Determines whether or not the contents on the grid should be displayed"""

    @staticmethod
    def get_square_size():
        """
        Returns the square length of each square unit on the playfield.

        :return: the value (int) of the square scale size.
        """
        return Playfield.square_size

    def setup_display(self):
        """
        Setup the playfield surface before it is drawn onto the game interface.

        :return: None
        """

        # Clear the surface before redrawing.
        self.clear_surface()

        # Stop at this point if the playfield's contents should not be displayed
        if not self.grid_visible:
            return

        # Draw the blocks on the playfield.
        self.draw_blocks()

        # Draw the gridlines of the playfield.
        self.draw_gridlines()

    def draw_blocks(self):
        """
        Sub-method of setup_display().
        Used to draw the square blocks on the playfield at their respective positions.

        :return: None
        """

        # Loop through each visible row of the playfield - the hidden rows will be skipped
        for row in range(self.hidden_rows, self.grid_height):

            # The actual y pixel coordinate of where the top left of the block will be drawn from.
            y_coord = (row - self.hidden_rows) * self.square_size

            # Loop through each column of the playfield
            for column in range(0, self.grid_width):

                # The actual x pixel coordinate of where the top left of the block will be drawn from.
                x_coord = column * self.square_size

                # Check if the position to get a block from is empty
                if self.check_cell_empty(column, row):
                    # No block to display, so move on to the block at next column
                    continue

                # Get the block at the current position
                block = self.matrix[row][column]

                # Define the area where the block will be drawn at on the surface.
                area_rect = pygame.Rect((x_coord, y_coord), (self.square_size, self.square_size))

                # Get the colour that the block will be displayed with.
                colour = block.get_colour()

                # Draw the block on the surface by filling the area position its display colour
                self.display_surface.fill(colour, area_rect)

    def draw_gridlines(self):
        """
        Sub-method of setup_display().
        Used to draw the horizontal and vertical gridlines of the playfield.

        :return: None
        """

        # Variables used for the lower-bounds of the nested for loop iteration for each row and column of the grid.
        x1 = 1
        y1 = 1

        # Get the width and height of the surface.
        width = self.rect_coords.width
        height = self.rect_coords.height

        # Variables used for the upper-bounds of the nested for loop iteration for each row and column of the grid.
        # Using floor division just to ensure that x2 and y2 are integers, otherwise an error would be raised.
        x2 = width // self.square_size  # Should end up as 10   - number of columns
        y2 = height // self.square_size  # Should end up as 20 - number of visible rows

        """
        Draw all the horizontal gridlines.
        Loop through the all the rows of the playfield not including the boundaries (0 and 19)
        (Python's range method is exclusive)
        """
        for y in range(y1, y2):
            # The actual y pixel coordinate where each horizontal gridline is drawn from
            y_coord = y * self.square_size
            # Draw a horizontal gridline with the gridline colour, and width of 1.
            pygame.draw.line(self.display_surface, self.gridline_colour, [0, y_coord], [width, y_coord], 1)

        """
        Draw all the vertical gridlines.
        Loop through the all the columns of the playfield not including the boundaries (0 and 9)
        (Python's range method is exclusive)
        """
        for x in range(x1, x2):
            # The actual x pixel coordinate where each vertical gridline is drawn from
            x_coord = x * self.square_size
            # Draw a veritcal gridline with the gridline colour, and width of 1
            pygame.draw.line(self.display_surface, self.gridline_colour, [x_coord, 0], [x_coord, height], 1)

    def update(self):
        """
        Updates the state of the playfield. Should be called once per frame.

        :return: None
        """

        # Continue the game over animation if a game over condition has been met
        if self.game_over:
            next(self.end_generator)

        # Continue to clear lines if in the line clear phase
        elif self.in_clear_phase:
            next(self.clear_generator)

        # Go through the drop phase and lock phase if there is a tetromino active
        elif self.tetromino_isactive:
            self.drop_phase()
            self.lock_phase()

        else:
            # Go through the spawn phase if there is no tetromino active - to generate the next active tetromino
            self.spawn_phase()

    def drop_phase(self):
        """
        Sub-method of update(). Handles the functionality for dropping the active tetromino further down onto the
        playfield.

        :return: None
        """

        # check if the active tetromino should drop on this frame.
        if self.gravity_counter > self.gravity:

            # for when the active tetromino is already on the ground
            if self.active_tetromino.is_on_ground():

                # engage the lock phase to allow for lock delay.
                self.in_lock_phase = True

            else:
                # not on the ground, so ensure no lock delay.
                self.in_lock_phase = False
                # apply gravity to the active tetromino piece.
                self.active_tetromino.shift_down()
                # reset counter to ensure that lock delay is reset.
                self.lock_counter = 0

                # If the active tetromino has oft drop,
                if self.soft_drop_isactive:
                    # Increase score by 1 due to soft drop
                    self.model.add_soft_drop_point()

            # the gravity counter must be reset, as the interval has passed
            self.gravity_counter = 0

        # for when the tetromino should not drop on this frame.
        else:

            # if the space below the tetromino is empty
            if not self.active_tetromino.is_on_ground():

                # no lock delay should be applied.
                self.in_lock_phase = False

                # increment the gravity counter.
                self.gravity_counter += 1

            else:
                # For when lock delay is being applied
                if self.in_lock_phase:
                    # reset gravity counter if the tetromino is on ground.
                    self.gravity_counter = 0

                # For when lock delay is not being applied
                else:
                    # increment the gravity counter.
                    self.gravity_counter += 1

    def lock_phase(self):
        """
        Sub-method of update(). Handles functionality for locking the active tetromino onto the playfield, and
        managing lock delay.

        :return: None
        """
        # check whether or not the lock phase should even occur
        if self.in_lock_phase:

            # increment the lock counter
            self.lock_counter += 1

            # If the active tetromino should lock on this frame, where lock delay has ended
            if self.lock_counter > self.lock_delay:
                # Have the active tetromino locked, thus ending the lock phase.
                self.lock_tetromino()

    def spawn_phase(self):
        """
        Sub-method of update(). Handles functionality for spawning the next tetromino piece onto the playfield, and
        managing entry delay.

        :return: None
        """

        # check if the next tetromino should spawn on this frame
        if self.entry_counter > self.entry_delay:

            # make the model setup the next tetromino to be active.
            self.model.set_active_tetromino()

            # reset the entry delay counter
            self.entry_counter = 0

        else:
            # increment the entry delay counter
            self.entry_counter += 1

    def set_tetromino(self, next_piece):
        """
        Sets the next tetromino piece to be placed onto the playfield.

        :param next_piece: The tetromino piece that will be placed on the grid as the active piece.
        :type next_piece: tetromino.Tetromino
        :return: None
        """

        # Set the next piece as the active tetromino on the playfield
        self.active_tetromino = next_piece

        # There is now a tetromino active, so record this
        self.tetromino_isactive = True

        # Define the top-left coordinates of the where the tetromino piece will spawn
        top_left_x = 3
        top_left_y = 2

        # Setup the square units of the active tetromino
        self.active_tetromino.setup_blocks(top_left_x, top_left_y)

        # If the tetromino would collide at its current position,
        if self.active_tetromino.would_collide(0, 0):

            """
            Allow the tetromino to spawn one cell higher
            """
            top_left_y -= 1

            # Re-setup the square units of the active tetromino
            self.active_tetromino.setup_blocks(top_left_x, top_left_y)

            # However, if it still collides, then a game over is reached.
            if self.active_tetromino.would_collide(0, 0):

                # A game over condition has been met - hence set the game over flag to True
                self.game_over = True

                # The tetromino should not be active due to the game over
                self.tetromino_isactive = False

                """
                Have the blocks added to the grid nevertheless
                """
                # First get the blocks from the tetromino.
                blocks = self.active_tetromino.get_blocks()

                # Iterate over each block of the tetromino
                for block in blocks:

                    # Get the block’s row and column positions
                    x = block.get_x_coord()
                    y = block.get_y_coord()

                    # Have it added to the grid data structure at the position, even if it overlaps
                    self.matrix[y][x] = block

            # No collisions will occur if shifted upwards, so the tetromino is added
            else:
                self.active_tetromino.add_to_grid()

        # No collisions will occur if the tetromino is added
        else:
            # Have the tetromino add itself to the playfield
            self.active_tetromino.add_to_grid()

    def shift_tetromino_left(self):
        """
        Shifts the tetromino piece one space to the left.

        :return: None
        """
        # Can only be shifted if there is an active tetromino.
        if self.tetromino_isactive:
            self.active_tetromino.shift_left()

    def shift_tetromino_right(self):
        """
        Shifts the tetromino piece one space to the right.

        :return: None
        """

        # Can only be shifted if there is an active tetromino.
        if self.tetromino_isactive:
            self.active_tetromino.shift_right()

    def get_block(self, x, y):
        """
        Returns the block stored in the matrix at the position passed.

        :param x: the column of the block to get
        :param y: the row of the block to get
        :type x: int
        :type y: int

        :return: A Block class instance of the block to get.
        """

        # get the block held at the position given by the parameters.
        block = self.matrix[y][x]

        # In case no block was found (to assist with debugging):
        if block is None:
            raise ValueError("No block found on the grid at:\nrow " + str(y) + "\ncolumn " + str(x))

        return block

    def add_block(self, block):
        """
        Places a block onto the grid, at the position given by its coordinate attributes

        :param block: The block to add to the grid
        :type block: Block
        :return: None
        """

        # get the x and y coordinates of the Block instance passed.
        x = block.get_x_coord()
        y = block.get_y_coord()

        # do not allow the block to be placed if there is already one at that position (to assist with debugging)
        if not self.check_cell_empty(x, y):
            raise ValueError("A block is already at the position:\nrow " + str(y) + "\ncolumn " + str(x))

        else:
            # add the block to the position if the cell is empty
            self.matrix[y][x] = block

    def remove_block(self, block):
        """
        Removes a block from the grid, at the position given by its own coordinates

        :param block: The block to be removed from the grid.
        :type block: Block
        :return: None
        """

        # In case the block is not at the position, do not remove anything from the grid.
        if not self.check_block_position(block):
            # Debug message
            raise ValueError("The block to remove is not located at its supposed position:\nrow "
                             + str(block.get_y_coord())
                             + "\ncolumn "
                             + str(block.get_x_coord()))
        else:
            # get the coordinates of the block.
            x = block.get_x_coord()
            y = block.get_y_coord()

            # set the value stored at the coordinates to nothing, thus removing it from the grid.
            self.matrix[y][x] = None

    def check_cell_empty(self, x, y):
        """
        Returns true if there is nothing on the grid at the passed coordinates.
        Returns false otherwise

        :param x: the column of the cell to check
        :param y: the row of the cell to check
        :type x: int
        :type y: int
        :return: bool value
        """

        # get the apparent block from the grid at the position passed
        block = self.matrix[y][x]

        # True if nothing is found at the position. False otherwise
        return block is None

    def check_block_position(self, block):
        """
        Used to verify whether or not a block is located on the grid at its own supposed coordinates
        Returns true if it is at the correct position.
        Otherwise returns false.

        :param block: The block that is being checked
        :type block: Block
        :return: bool value
        """

        # Get the apparent coordinates of where the block is stored at
        x = block.get_x_coord()
        y = block.get_y_coord()

        # get the Block instance found at that position
        block_found = self.matrix[y][x]

        """
        Return True if the Block object found is the same instance as the Block object passed as a parameter.
        Otherwise return False
        """
        return block is block_found

    def is_in_bounds(self, x, y):
        """
        Checks whether or not that the passed position lies within the grid boundaries.
        Returns true if it does lie within the boundaries
        Returns false otherwise

        :param x: the column position to check
        :param y: the row position to check
        :return: bool value
        """

        # will be out of bounds if x is not 0 - (9)
        if x < 0 or x > self.grid_width - 1:
            return False

        # will be out of bounds if x is not 0 - (21)
        if y < 0 or y > self.grid_height - 1:
            return False

        return True

    def activate_soft_drop(self):
        """
        Increases the rate at which the active tetromino piece falls down.

        :return: None
        """
        # Set the current gravity value to the constant soft-drop gravity value
        self.gravity = Playfield.SOFT_DROP_GRAVITY

        # Soft drop is now active
        self.soft_drop_isactive = True

        # When in the lock phase,
        if self.in_lock_phase:
            # When the active tetromino is on the ground,
            if self.active_tetromino.is_on_ground():
                # lock delay cancels when soft drop is activated"""
                self.lock_tetromino()

    def deactivate_soft_drop(self):
        """
        Sets the gravity of the active tetromino piece on the playfield back to normal.

        :return: None
        """
        # Set gravity back to normal by recalculating the value depending on level.
        self.gravity = self.model.calculate_gravity()

        # Soft drop is no longer active
        self.soft_drop_isactive = False

    def lock_tetromino(self):
        """
        Locks the active tetromino on the playfield.

        :return: None
        """
        # reset the lock counter
        self.lock_counter = 0
        # the tetromino will be locked, thus no longer active
        self.tetromino_isactive = False
        # the tetromino is now locked, so end the lock phase
        self.in_lock_phase = False

        # Check if the tetromino locked entirely out of visible bounds
        if self.check_lock_out():
            # if so, set the game over flag to true
            self.game_over = True

        else:
            # Otherwise, go through the pattern phase – check if any rows should be cleared
            self.pattern_phase()

    def rotate_clockwise(self):
        """
        Used to rotate the active tetromino 90 degrees clockwise.

        :return: None
        """
        # Only rotate if the tetromino is active.
        if self.tetromino_isactive:
            # Call the method of the same name from the active tetromino
            self.active_tetromino.rotate_clockwise()

    def rotate_anticlockwise(self):
        """
        Used to rotate the active tetromino 90 degrees anticlockwise.

        :return: None
        """

        # Only rotate if the tetromino is active.
        if self.tetromino_isactive:
            # Call the method of the same name from the active tetromino
            self.active_tetromino.rotate_anticlockwise()

    def get_top_block_row(self):
        """
        Gets the highest row index that is not empty.
        If the playfield is completely empty, -1 is returned.

        :return: integer value of row index.
        """

        # Loop through each row index of the playfield
        for row in range(0, self.grid_height - 1):

            # Once a row is found to not be empty, then this is the top row with at least one block.
            if not self.check_row_empty(row):
                return row

        # -1 is returned if all rows are empty.
        return -1

    def check_row_empty(self, row):
        """
        Checks whether or not a given row of the playfield is empty
        Returns true if the row is empty, and false if not.

        :param row: the index of the row being checked for emptiness
        :type row: int
        :return: None
        """
        # Get the row of blocks from grid at position given by the row index passed
        block_row = self.matrix[row]

        # Loop through each (apparent) block on the row
        for block in block_row:
            # If the not a ‘null’ type, then this must be a block
            if block is not None:
                # This means that the row is not empty
                return False

        # At this point, all elements of the row are null, so it is empty
        return True

    def check_grid_empty(self):
        """
        Checks whether or not the whole playfield is empty.
        Returns true if it is empty, and false if not.

        :return: None
        """
        # Loop through each row index of the grid
        for row in range(0, self.grid_height):

            # If the row is not empty, then the grid is not completely empty
            if not self.check_row_empty(row):
                return False

        # At this point, all rows are checked, and they are empty. Therefore the whole grid is empty.
        return True

    def pattern_phase(self):
        """
        Checks for any lines that have been cleared after a tetromino locks.

        :return: None
        """

        # Define an empty list, to hold the row indexes of full blocks
        full_rows = list()

        # Get the row indexes of where the active tetromino locked
        block_rows = self.active_tetromino.get_rows()

        # Iterate through each row the active tetromino locked at
        for row_index in block_rows:

            # Check whether or not the row is full
            if self.check_row_full(row_index):
                # Add it the full_rows list if full
                full_rows.append(row_index)

        # If the full_rows list is not empty, then it means that at least one line needs to be cleared.
        if len(full_rows) > 0:
            # The line clear phase should now be gone through
            self.in_clear_phase = True

            # Set the attribute to a new generator object of the line_clear_generator() generator method
            self.clear_generator = self.line_clear_generator(full_rows)

    def check_row_full(self, row):
        """
        Checks whether or not a given row of the playfield is completely full of blocks
        Returns true if the row is full, and false if not.

        :param row: the index of the row being checked
        :type row: int
        :return: None
        """
        # Get the row of blocks from grid at position given by the row index passed
        block_row = self.matrix[row]

        # Loop through each (apparent) block on the row
        for block in block_row:
            # If it is a ‘null’ type, then the cell is empty
            if block is None:
                # This means that the row is not full
                return False

        # At this point, all elements of the row list are blocks, so it is full
        return True

    def check_lock_out(self):
        """
        Checks whether or not the active tetromino was locked completely out of visible bounds.
        Returns True if it would lock out of visible bounds. If not, it returns False

        :return: Boolean value
        """

        # Get the list of row indexes the tetromino locked at
        row_list = self.active_tetromino.get_rows()

        # Loop through each row index in the list
        for row in row_list:

            # Any rows that are in the visible bounds mean that the tetromino is at least partially in bounds
            if row > self.hidden_rows - 1:
                # Therefore the tetromino was not locked out.
                return False

        # At this point, all the row indexes point to the hidden rows, meaning that the tetromino was locked out.
        return True

    def shift_rows_down(self, full_rows):
        """
        Applies line clear gravity to the rows of blocks above the cleared lines (They are shifted downwards).

        :param full_rows: the row indexes of the playfield that were completely filled with blocks.
        :type full_rows: list(int)
        """

        # No need to shift any rows if the grid is completely cleared
        if self.check_grid_empty():
            return

        # Loop through each index of the full_rows list
        for i in range(0, len(full_rows)):

            """
            Shift from the top row of blocks, to the cleared row currently pointed to
            """
            start_row = self.get_top_block_row()
            end_row = full_rows[i]

            """
            Define variable to temporarily store block rows on the grid.
            """
            # Start with the top block row.
            temp_blocks = self.matrix[start_row]

            # Empty the start row of blocks from the grid, as they need to be shifted downwards.
            self.clear_row(start_row)

            # Loop from the start and end row indexes.
            for y in range(start_row, end_row):

                # Temporarily hold the block list at current index
                blocks = self.matrix[y+1]

                # Remove that row of blocks from the grid, replacing it with the blocks held by temp_blocks.
                self.matrix[y+1] = temp_blocks

                # Now have temp_blocks hold the blocks that were removed.
                temp_blocks = blocks

    def line_clear_generator(self, full_rows):
        """
        A Python generator used to carry out the line clear phase

        :param full_rows: the row indexes of the playfield that are completely filled with blocks.
        :type full_rows: list(int)
        :return: None
        """

        # Use a frame counter in correspondence to clear_delay, to determine when the delay should end
        delay_counter = 0

        # Get the number of lines to be cleared
        num_of_lines = len(full_rows)

        """
        This loop clears one block on each line per frame, resulting in a clear animation.
        """
        # Loop through each column index of the playfield
        for x in range(0, self.grid_width):

            # Loop through each row index of the lines to clear
            for row_index in full_rows:
                # Use the indexes to remove the block from the grid data structure
                self.matrix[row_index][x] = None

            # Increment delay counter
            delay_counter += 1
            # Exit the generator, returning to this point after it is called again.
            yield

            # Use a frame timer to allow for delays between each 'animation' frame, so it plays less quickly.
            frame_interval = 1

            # Wait until the frame interval have passed
            for i in range(0, frame_interval):
                # Still increment the delay counter
                delay_counter += 1
                # Exit the generator - will continue from this point when next called
                yield

        # Wait until the delay has ended
        while delay_counter <= self.clear_delay:
            # Increment delay counter
            delay_counter += 1
            # Exit the generator, returning to this point after it is called again.
            yield

        """
        At this point, the delay has been passed.
        """
        # Apply line clear gravity to the rows above the cleared lines
        self.shift_rows_down(full_rows)

        # End the clear phase
        self.in_clear_phase = False

        # Increase the number of lines cleared, and update the current level
        self.model.increase_lines(num_of_lines)

        # Re-calculate gravity (except if in soft drop)
        if not self.soft_drop_isactive:
            self.gravity = self.model.calculate_gravity()

        """
        End of generator
        """
        while True:
            # Still allow for yielding endlessly, but do not let anything occur.
            yield

    def clear_row(self, row_index):
        """
        Empties a single row on the grid at a given row index.

        :param row_index: The index of the row to empty

        :return: None
        """

        # Set the row to a new empty list with the grid width size.
        self.matrix[row_index] = [None] * self.grid_width

    def game_over_generator(self):
        """
        A Python generator used to carry out the game over phase, where an 'animation' is played after a game over
        occurs.

        :return: None
        """

        # Define the initial delay frame time
        delay = 60

        # Define a counter for the delay
        delay_counter = 0

        """
        Wait until the delay has ended
        """
        # Loop until the delay time has passed
        while delay_counter <= delay:

            # Increment the delay counter
            delay_counter += 1
            # Exit the generator - will continue from this point when next called
            yield

        """
        Animation for game over – clearing remaining blocks from grid
        """

        # Starting from the top row, loop through each row index from the largest to the smallest.
        for row_index in range(0, self.grid_height):

            # Clear the row
            self.clear_row(row_index)

            # Exit the generator - will continue from this point when next called
            yield

            # The number of frames to wait until the next row is cleared
            clear_frames = 3

            # Wait until the frame timer reaches 0
            while clear_frames > 0:
                # Decrement the frame timer
                clear_frames -= 1
                # Exit the generator - will continue from this point when next called
                yield

        """
        End of generator
        """
        # Notify the model component that the game should end.
        self.model.game_over()
        while True:
            # Still allow for yielding endlessly, but do not let anything occur.
            yield

    def set_visible(self, is_visible):
        """
        Change the state of the playfield, to either show or hide the its contents.

        :param is_visible: The value used to determine whether or not the grid blocks should be displayed
        :type is_visible: bool
        :return: None
        """
        # Simply set the parameter to the attribute used for this purpose.
        self.grid_visible = is_visible
