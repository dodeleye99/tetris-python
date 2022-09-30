import math

import constants
from playfield import Playfield
from next_panel import NextPanel
from level_panel import LevelPanel
from score_panel import ScorePanel
from lines_panel import LinesPanel
from pause_button import PauseButton
from tetromino import Tetromino


class GameInterfaceModel(object):
    """
    Represents the model component of the MVC paradigm.
    Holds all the individual objects with their functionality together to allow for them to be accessed without
    direct communication with them (encapsulation).
    """

    instance = None
    """The single instance of the GameInterfaceModel class used throughout the program.
    :type : GameInterfaceModel
    """

    def __init__(self):

        self.score_panel = ScorePanel()
        """A reference to the ScorePanel instance used in the program"""

        self.level_panel = LevelPanel()
        """A reference to the LevelPanel instance used in the program"""

        self.next_panel = NextPanel()
        """A reference to the NextPanel instance used in the program"""

        self.lines_panel = LinesPanel()
        """A reference to the LinesPanel instance used in the program"""

        self.hud_components = list([self.score_panel,
                                    self.level_panel,
                                    self.next_panel,
                                    self.lines_panel
                                    ])
        """A list of instances from each panel class that will be used by the program and displayed on the screen."""

        # Pass this instance to the Playfield constructor
        self.grid = Playfield(self)
        """A reference to the playfield component that will be used by the program and displayed on the screen """

        self.pause_button = PauseButton()
        """A reference to the PauseButton instance that will be used by the program and displayed on the screen """

        self.random_generator = Tetromino.random_generator(self.grid)
        """ A generator object used to create sequences of each type of tetromino piece in a random order, returning 
        one at a time"""

        # Store this GameInterfaceModel instance as the single instance used throughout the program.
        GameInterfaceModel.instance = self

        # set the next tetromino piece of the NextPanel instance
        self.set_next_tetromino()

        # set the tetromino to be active on the playfield.
        self.set_active_tetromino()

    def update(self):
        """
        Update the status of the sub-model objects held by the this component.
        :return: None
        """

        # Update the status of the pause button.
        self.pause_button.update_status()

        # Nothing else should occur if the game is paused.
        if self.pause_button.check_paused():
            # Make sure the contents of the playfield and the next piece are hidden
            self.grid.set_visible(False)
            self.next_panel.set_visible(False)
            return

        # Thee contents of the playfield and the next piece should be shown.
        self.grid.set_visible(True)
        self.next_panel.set_visible(True)

        # Update the state of the playfield.
        self.grid.update()

    def get_grid(self):
        """
        Returns the playfield component of the game.

        :return: The Playfield object used in the program
        """
        return self.grid

    def get_hud_components(self):
        """
        Returns a list of all the game information containers displayed on the screen.

        :return: A list of BasePanel derived classes
        """
        return self.hud_components

    def get_pause_button(self):
        """
        Returns the pause button used in the game

        :return: The PauseButton instance used in the program
        """
        return self.pause_button

    # @staticmethod
    def generate_random_tetromino(self):
        """
        Returns a random tetromino object (using the random_generator() generator object)

        :return: an instance of the Tetromino class
        """

        # use next() to continue from  their last line where the generator was 'halted'.
        return next(self.random_generator)

    def set_next_tetromino(self):
        """
        Set the next tetromino piece to be held by the 'Next Queue'

        :return: None
        """

        # generate a random tetromino piece
        next_piece = self.generate_random_tetromino()

        # pass this to the NextPanel instance in order to set this as the next tetromino of the 'Next Queue'
        self.next_panel.set_next(next_piece)

    def set_active_tetromino(self):
        """
        Set the active tetromino piece to be placed on the playfield

        :return: None
        """

        # get the next tetromino piece from the Next Queue
        next_tetromino = self.next_panel.get_next()

        # set this tetromino as the new active piece on the playfield
        self.grid.set_tetromino(next_tetromino)

        # set the next tetromino of the Next Queue
        self.set_next_tetromino()

    def shift_tetromino_left(self):
        """
        Moves the active tetromino piece on the playfield one space to the left.

        :return: None
        """

        # Nothing should occur if the game is paused.
        if self.pause_button.check_paused():
            return

        # Simply call the same named method of the held Playfield class instance
        self.grid.shift_tetromino_left()

    def shift_tetromino_right(self):
        """
        Moves the active tetromino piece on the playfield one space to the roght.

        :return: None
        """

        # Nothing should occur if the game is paused.
        if self.pause_button.check_paused():
            return

        # Simply call the same named method of the held Playfield class instance
        self.grid.shift_tetromino_right()

    def calculate_gravity(self):
        """
        Calculates the gravity frame interval based on the current level, and returns it.

        :return: rounded up int value for the gravity
        """

        # Get the current level
        level = self.level_panel.get_current_level()
        # Use formula to calculate the gravity
        gravity = ((0.8 - ((level-1)*0.007))**(level-1)) * constants.FRAME_RATE

        # Must be an integer - so round it up to the nearest integer.
        return math.ceil(gravity)

    def activate_soft_drop(self):
        """
        Increases the rate at which the active tetromino piece falls down.

        :return: None
        """

        # Nothing should occur if the game is paused.
        if self.pause_button.check_paused():
            return
        
        self.grid.activate_soft_drop()

    def deactivate_soft_drop(self):
        """
        Sets the gravity of the active tetromino piece on the playfield back to normal.

        :return: None
        """
        self.grid.deactivate_soft_drop()

    def rotate_clockwise(self):
        """
        Used to rotate the active tetromino on the playfield 90 degrees clockwise

        :return: None
        """

        # Nothing should occur if the game is paused.
        if self.pause_button.check_paused():
            return

        # Wrapper method: simply call the method of the same name from the held Playfield instance
        self.grid.rotate_clockwise()

    def rotate_anticlockwise(self):
        """
        Used to rotate the active tetromino on the playfield 90 degrees anticlockwise

        :return:
        """

        # Nothing should occur if the game is paused.
        if self.pause_button.check_paused():
            return

        # Wrapper method: simply call the method of the same name from the held Playfield instance
        self.grid.rotate_anticlockwise()

    def increase_lines(self, n):
        """
        Increases the number of lines cleared on the playfield.
        The value displayed on the lines panel will be increased.
        The current score will be updated, and there will be a check for whether the level should increase.

        :param n: The number of full rows of blocks that have been cleared.
        :type n: int
        :return: None
        """

        # Call the method of the lines panel used to increase the number of lines cleared.
        self.lines_panel.add_lines_cleared(n)

        # Get the current level, needed to calculate the points.
        level = self.level_panel.get_current_level()

        # Increase score based on the number of lines cleared (and level)
        self.score_panel.score_lines(n, level)

        # Pass lines cleared to the level panel, to check for leveling up.
        self.level_panel.update_level(n)

    def add_soft_drop_point(self):
        """
        Adds a point to the total score due to soft dropping

        :return: None
        """
        # Simply call the add_points() method of the score panel, passing 1 -> 1 point
        self.score_panel.add_points(1)

    def switch_pause(self):
        """
        Switches the state of the game between 'playing' and 'paused'.

        :return: None
        """
        # Simply call the method of the same name from the pause button.
        self.pause_button.switch_pause()

    def mouse_down(self):
        """
        Called when the mouse is pressed down, to check if the pause button is being clicked down on.

        :return: None
        """
        # Simply call the method of the same name from the pause button.
        self.pause_button.mouse_down()

    def mouse_up(self):
        """
        Called when the mouse is released, to check if the pause button has been clicked.

        :return: None
        """
        # Simply call the method of the same name from the pause button.
        self.pause_button.mouse_up()

    def check_paused(self):
        """
        Returns True if the game is in its paused state. Returns False otherwise.

        :return: Boolean value
        """

        # Wrapper method: call the pause button's own check_paused() method.
        return self.pause_button.check_paused()

    def game_over(self):
        """
        End the game, updating the high scores file.

        :return: None
        """
        # Update the high scores file if the player's score was high enough.
        self.score_panel.update_scores()

        # Reset the game, to allow for it to be replayed again without any need to close the program.
        self.reset()

    def reset(self):
        """
        Resets all attributes to their original state, to allow for the game to be played again.

        :return: None
        """

        # Reset all attributes
        self.score_panel = ScorePanel()
        self.level_panel = LevelPanel()
        self.next_panel = NextPanel()
        self.lines_panel = LinesPanel()

        self.hud_components = list([self.score_panel,
                                    self.level_panel,
                                    self.next_panel,
                                    self.lines_panel
                                    ])

        self.grid = Playfield(self)
        self.pause_button = PauseButton()

        self.random_generator = Tetromino.random_generator(self.grid)

        # set the next tetromino piece of the NextPanel instance
        self.set_next_tetromino()

        # set the tetromino to be active on the playfield.
        self.set_active_tetromino()

        # Make sure the contents of the playfield and the next piece are hidden
        self.grid.set_visible(False)
        self.next_panel.set_visible(False)
