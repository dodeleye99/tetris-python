import pygame


class PauseButton(object):
    """
    The class used to represent the pause button of the game, to allow the player to temporarily stop gameplay.
    """

    def __init__(self):

        # Define the Boolean attributes of the class.
        self.is_hovered = False
        """
        Determines whether or not the mouse pointer is currently placed over the button image.
        """
        self.clicked_down = False
        """
        Determines whether or not the pause button is being clicked down on with the left mouse button
        """
        self.is_paused = True
        """
        Determines whether or not the game is in its ‘paused’ state.
        """

        dir1 = "pause-button1.png"
        dir2 = "pause-button2.png"
        dir3 = "resume-button1.png"
        dir4 = "resume-button2.png"

        # Load all the images to be used for the button, and set them to the 'image' attributes
        self.pause_image = pygame.image.load(dir1)
        """
        The regular image of the pause button that will be displayed when the game is playing,
        and the mouse pointer is on it.
        """
        self.alt_pause_image = pygame.image.load(dir2)
        """
        The 'glowing' image of the pause button that will be displayed when the game is playing 
        while the mouse pointer is on the it.
        """
        self.resume_image = pygame.image.load(dir3)
        """
        The image of the pause button that will be displayed when the game is playing,
        and the mouse pointer is on it.
        """
        self.alt_resume_image = pygame.image.load(dir4)
        """
        The 'glowing' image of the pause button that will be displayed when the game is paused, 
        while the mouse pointer is on the it.
        """

        # Temporarily store the size each image should have so that they can fit on the game interface.
        image_size = (80, 80)

        # Reduce the size of the images to the size defined above.
        self.pause_image = pygame.transform.smoothscale(self.pause_image, image_size)
        self.alt_pause_image = pygame.transform.smoothscale(self.alt_pause_image, image_size)
        self.resume_image = pygame.transform.smoothscale(self.resume_image, image_size)
        self.alt_resume_image = pygame.transform.smoothscale(self.alt_resume_image, image_size)

        self.rect_coords = self.pause_image.get_rect()
        """
        The rectangular coordinates of the pause button image being displayed on the screen.
        Stores its top-left x and y coordinates, and its width and height.
        """

        # Change the position of the rect coordinates. Set the centre position of where the image will be displayed.
        self.rect_coords.center = (270, 400)

    def get_image(self):
        """
        Returns the surface image of the pause button that it should be displayed with.

        :return: A pygame Surface object
        """

        # For when the mouse pointer 'hovers' over the pause button:
        if self.is_hovered:
            # For when the game is paused:
            if self.is_paused:
                # The 'glowing' resume image should be returned.
                return self.alt_resume_image
            # For when the game is NOT paused:
            else:
                # The 'glowing' pause image should be returned.
                return self.alt_pause_image

        # For when the mouse pointer is NOT 'hovering' over the pause button:
        else:
            # For when the game is paused:
            if self.is_paused:
                # The 'regular' resume image should be returned.
                return self.resume_image
            # For when the game is NOT paused:
            else:
                # The 'glowing' pause image should be returned.
                return self.pause_image

    def get_rect(self):
        """
        returns the rectangular coordinates of the pause button image

        :return: a pygame Rect object
        """
        return self.rect_coords

    def check_paused(self):
        """
        Returns True if the game is in its paused state. Returns False otherwise.

        :return: Boolean value
        """

        # Simply return the boolean attribute that determines this.
        return self.is_paused

    def switch_pause(self):
        """
        Switches the state of the game between 'playing' and 'paused'

        :return: None
        """
        # Simply flip the pause value
        self.is_paused = not self.is_paused

    def on_click(self):
        """
        Called whenever the button is clicked on.
        In this case, it switches the game between 'play' state and 'pause' state

        :return: None
        """
        # 'Switch' the pause value.
        self.switch_pause()

    def mouse_down(self):
        """
        Called when the left mouse button is clicked down.

        :return: None
        """
        # Check if the button is being hovered over by the mouse pointer.
        if self.is_hovered:
            # If so, then the button is being clicked down.
            self.clicked_down = True

    def mouse_up(self):
        """
        Called when the left mouse button is released.

        :return: None
        """

        """
        The button will be considered ‘clicked’ if the mouse is currently hovering over it 
        AND it is being clicked down.
        """
        if self.is_hovered and self.clicked_down:
            # Handle the processing that occurs after being clicked.
            self.on_click()
            # It was clicked, therefore no longer clicked down.
            self.clicked_down = False

    def update_status(self):
        """
        To be called once per frame, to check whether or not the image is hovered over,
        or is clicked down.

        :return: None
        """

        # Get the current position of the mouse pointer
        mouse_pos = pygame.mouse.get_pos()

        # Check whether or not the mouse is located within the rectangular bounds of the pause button image
        if self.rect_coords.collidepoint(mouse_pos):
            # If so, then the button is currently being 'hovered' over
            self.is_hovered = True

        else:
            # Otherwise, the button is not 'hovered' over.
            self.is_hovered = False
            # The 'clicked down' flag should be reset, as the mouse pointer left the button.
            self.clicked_down = False
