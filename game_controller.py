import pygame  # Must be imported to allow for access to the library.

import constants
# Import model and view classes.
from game_interface_model import GameInterfaceModel
from game_interface_view import GameInterfaceView


class GameController(object):

    """
    Represents the controller component of the MVC paradigm.
    It involves updating both the model and view components every frame while the game is being played.
    It also acts as the main entry point of the program, to set up all components and objects.
    """

    AUTOREPEAT_FRAMES = 15
    """The number of frames that the left/right key must be held for before applying DAS (Delayed Auto Shift)"""

    def __init__(self, width, height):
        """
        Initialise the controller component, as well as instantiate view and controller components and store references.

        :param width: The width to make the screen in pixels.
        :type width: int

        :param height: The height to make the screen in pixels.
        :type height: int
        """

        # Set up the top level display screen, specifying the screen dimensions it should have.
        pygame.display.set_mode([width, height])

        self.model = GameInterfaceModel()
        """Stores reference of the model component"""

        self.view = GameInterfaceView(self.model)
        """Stores reference of the view component"""

        self.autorepeat_counter = 0
        """The frame counter used to determine when the left/right key has been held long enough to apply DAS"""

        self.left_key_held = False
        """Determines whether or not the left arrow key is being held or not."""

        self.right_key_held = False
        """Determines whether or not the right arrow key is being held or not."""

        self.is_running = True
        """
        Records whether or not the game is playing, to determine whether the main loop should stop.
        """

    def main_loop(self):
        """
        The main game loop of the program, to get user input, invoke model behaviour, and update the appearance of
        the screen every frame.

        :return: None
        """

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        # Set the frame rate that the game should be limited to. (number of frames per second)
        frame_rate = constants.FRAME_RATE

        # The actual main loop - each loop counts as 1 frame.
        while self.is_running:
            
            # Get the state of the game - either paused or un-paused
            paused = self.model.check_paused()
            # Force the mouse to stay within the display window if the game is playing.
            pygame.event.set_grab(not paused)

            # Pause the game (if not already) if the window does not have keyboard focus
            if not pygame.key.get_focused():
                if not paused:
                    self.model.switch_pause()

            # process the input events
            self.evaluate_input()

            # carry out the processing for auto-shift movement.
            self.autorepeat()

            # Update the model and view components.
            self.update_model()
            self.update_view()

            # Limit the frame rate, which causes a delay the loop for a very short period of time.
            clock.tick(frame_rate)

    def update_model(self):
        """
        Update the model component. To be called once per frame.

        :return: None
        """
        self.model.update()

    def update_view(self):
        """
        Update the view component. To be called once per frame.

        :return: None
        """
        self.view.redraw()

    def autorepeat(self):
        """
        Sub-method of main_loop().
        It handles the functionality for DAS, and checking whether or not it should be applied.

        :return: None
        """

        # Check whether the game is in its paused state
        if self.model.check_paused():
            # Do not allow DAS to be processed.
            self.left_key_held = False
            self.right_key_held = False
            # Ensure that the counter is set to 0.
            self.autorepeat_counter = 0
            # Exit the method.
            return

        # Increment the auto-repeat counter for every frame where the left or right key is held down.
        if self.left_key_held or self.right_key_held:
            self.autorepeat_counter += 1

        # Check if the auto-repeat counter has surpassed the number of frames required to activate DAS.
        if self.autorepeat_counter > GameController.AUTOREPEAT_FRAMES:

            # If holding the left key:
            if self.left_key_held:
                # Shift the tetromino piece one space to the left
                self.model.shift_tetromino_left()

                # Slightly push back the counter - to add a bit of delay between auto shifts.
                self.autorepeat_counter -= 3

            # If holding the right key:
            if self.right_key_held:
                # Shift the tetromino piece one space to the right
                self.model.shift_tetromino_right()

                # Slightly push back the counter - to add a bit of delay between auto shifts.
                self.autorepeat_counter -= 3

    def evaluate_input(self):
        """
        Sub-method of main_loop()
        It reviews the inputs entered by the user, such as arrow keys, and processes them accordingly.

        :return:None
        """

        # Get the input events triggered by the user
        input_events = pygame.event.get()

        # Loop through each input event triggered by the user.
        for event in input_events:
            # After clicking the close button, end the main loop
            if event.type == pygame.QUIT:
                self.is_running = False

            # Check if any keys have been pressed down on this frame
            if event.type == pygame.KEYDOWN:
                # If the left arrow key was pressed down:
                if event.key == pygame.K_LEFT:
                    # left key is now being held down
                    self.left_key_held = True
                    # both keys should not be able to be held down simultaneously.
                    self.right_key_held = False

                    # shift the active tetromino piece one space to the left
                    self.model.shift_tetromino_left()
                    # ensure that the auto-repeat counter is reset
                    self.autorepeat_counter = 0

                # If the right arrow key was pressed down:
                elif event.key == pygame.K_RIGHT:
                    # right key is now being held down
                    self.right_key_held = True
                    # both keys should not be able to be held down simultaneously.
                    self.left_key_held = False

                    # shift the active tetromino piece one space to the left
                    self.model.shift_tetromino_right()
                    # ensure that the auto-repeat counter is reset
                    self.autorepeat_counter = 0

                # If the down arrow key was pressed down:
                if event.key == pygame.K_DOWN:
                    # make the tetromino fall faster.
                    self.model.activate_soft_drop()

                # If the X key was pressed down:
                if event.key == pygame.K_x:
                    # rotate the tetromino 90 degrees clockwise.
                    self.model.rotate_clockwise()

                # If the Z key was pressed down:
                if event.key == pygame.K_z:
                    # rotate the tetromino 90 degrees anticlockwise.
                    self.model.rotate_anticlockwise()

                # If the escape key was pressed down:
                if event.key == pygame.K_ESCAPE:
                    # switch the state of the game between 'playing' and 'paused'
                        self.model.switch_pause()

            # check if any keys have been released on this frame
            if event.type == pygame.KEYUP:

                # If the left arrow key was released
                if event.key == pygame.K_LEFT:
                    # left key is no longer being held down
                    self.left_key_held = False
                    # ensure that the auto-repeat counter is reset
                    self.autorepeat_counter = 0

                # If the right arrow key was released
                elif event.key == pygame.K_RIGHT:
                    # right key is no longer being held down
                    self.right_key_held = False
                    # ensure that the auto-repeat counter is reset
                    self.autorepeat_counter = 0

                # If the down arrow key was released
                if event.key == pygame.K_DOWN:
                    # make the tetromino fall at normal speed
                    self.model.deactivate_soft_drop()

            # check if the left mouse key has been pressed down on this frame
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Notify the model component of this event.
                self.model.mouse_down()

            # check if the left mouse key has been released down on this frame
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Notify the model component of this event.
                self.model.mouse_up()
