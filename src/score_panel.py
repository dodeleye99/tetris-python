import json

from info_panel import InfoPanel


class ScorePanel(InfoPanel):

    def __init__(self):
        """
        The panel class used to represent a container component that is dedicated for displaying the current score
        and high score of the Tetris game.
        """

        # temporary variables for the dimensions of the display surface of the panel.
        width = 100
        height = 140
        # Call the constructor of the BasePanel class, to setup the generic panel attributes.
        super().__init__((0, 0), (width, height))  # top left position (0,0), and screen dimensions passed.

        # Alter the rect coordinates.
        self.rect_coords.right = 320  # x-coordinate of the right side of the panel is set.
        self.rect_coords.top = 10  # y-coordinate of the top of the panel is set.

        self.score = 0
        """Stores the value of the player's current score."""
        self.high_score = 0
        """Stores the value of the highest score obtained from the game """

        self.score_label = "SCORE"
        """ Used to hold the string that will be used as the label text for the score value displayed in the panel"""

        self.high_score_label = "HIGH SCORE"
        """ Used to hold the string that will be used as the label text for the high score value displayed in the panel
        """

        # Set the high score value displayed to the highest score stored in the data file.
        self.set_high_score()

    def add_points(self, points):
        """
        increases the current score by the given amount.

        :param points: The number of points to add to the score
        :type points: int
        :return: None
        """
        self.score += points

    def get_high_score(self):
        """
        returns the high score of the game.

        :return: integer value of the high score
        """
        return self.high_score

    def setup_display(self):
        """
        Setup the surface of the score panel, with the updated value of the player's current score and the high score,
        before it is drawn onto the game interface.

        :return: None
        """

        # Clear the surface before redrawing.
        self.clear_surface()

        # Create surface images of the label text and scores text
        score_label_text = InfoPanel.create_text(self.score_label)
        high_label_text = InfoPanel.create_text(self.high_score_label)

        # The current score and high score text will have at least 6 digits.
        score_text = InfoPanel.create_text(str(self.score).zfill(6))
        high_score_text = InfoPanel.create_text(str(self.high_score).zfill(6))

        # Get the rectangular coordinates of the text surfaces to modify them.
        score_label_rect = score_label_text.get_rect()
        high_label_rect = high_label_text.get_rect()
        score_rect = score_text.get_rect()
        high_score_rect = high_score_text.get_rect()

        """Since the text is drawn on the panel, its rect coordinates are relative to the panel
        rather than the screen"""
        # local y-coordinate of the top of the label text surface is set.
        high_label_rect.top = 5
        """
        local x position of the centre of the label text is set to half the width of the surface so it is positioned
        at the centre of the surface.
        """
        high_label_rect.centerx = self.rect_coords.width // 2

        # the top of the high score text surface will be 5 pixels below its label.
        high_score_rect.top = high_label_rect.bottom + 5
        high_score_rect.left = 10

        # the top of the current score label text surface will be 10 pixels below the high score value text surface.
        score_label_rect.top = high_score_rect.bottom + 10
        score_label_rect.left = 10

        # the top of the current score text surface will be 5 pixels below its label.
        score_rect.top = score_label_rect.bottom + 5
        score_rect.left = 10

        # Draw all texts onto the display surface at the position given by their corresponding rectangular coordinates.
        self.display_surface.blit(high_label_text, high_label_rect)
        self.display_surface.blit(score_label_text, score_label_rect)
        self.display_surface.blit(high_score_text, high_score_rect)
        self.display_surface.blit(score_text, score_rect)

    def score_lines(self, lines, level):
        """
        Calculates the points gained from clearing lines, and adds them to the current score.

        :param lines: The number of lines that were cleared
        :param level: The current level
        :return: None
        """

        # Define a dictionary that acts as a 'switch/case' for calculating the points.
        """
        SCORE MODIFIERS:
        
        40 points for 1 line
        100 points for 2 lines
        300 points for 3 lines
        1200 points for 4 lines (maximum possible)
        """
        points_dict = {"1": 40,
                       "2": 100,
                       "3": 300,
                       "4": 1200
                       }

        # Calculate the number of points gained. If the number of lines is invalid, the result will be 0.
        points = points_dict.get(str(lines), 0) * level

        # Add the points to the score.
        self.score += points

    def set_high_score(self):

        file_dir = "high-scores.json"

        # Open the high scores data file for reading
        with open(file_dir, 'r') as json_file:

            # Load the data as a JSON object (represented by a Python dictionary)
            json_data = json.load(json_file)
            # Get the list of scores mapped by the "high scores" key
            scores_list = json_data["high scores"]

            # The high score attribute will be set to the greatest value stored in the list.
            self.high_score = max(scores_list)

            # Close the file
            json_file.close()

    def update_scores(self):

        file_dir = "high-scores.json"

        # Open the high scores data file for reading
        with open(file_dir, 'r') as json_file:

            # Load the data as a JSON object (represented by a Python dictionary)
            json_data = json.load(json_file)

            # Close the file
            json_file.close()

        # Get the list of scores mapped by the "high scores" key
        scores_list = json_data["high scores"]

        # The score will only be stored if it is greater than the minimum value stored in the list.
        if not self.score > min(scores_list):
            # Exit the method if the score is not high enough to be stored.
            return

        # First sort the array in descending order in case it isn’t already
        scores_list.sort(reverse=True)

        # Get the index that points to the end of the list
        end_index = len(scores_list) - 1

        # Add the player’s score to this position.
        scores_list[end_index] = self.score

        # Sort the list again in descending order.
        scores_list.sort(reverse=True)

        # Set the value mapped by the "high scores" key to this updated list.
        json_data["high scores"] = scores_list

        # Open the high scores data file again, this time for writing
        with open(file_dir, 'w') as json_file:

            # Overwrite the JSON file with the updated scores list.
            json.dump(json_data, json_file, indent=4)

            # Close the file
            json_file.close()
