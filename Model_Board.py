import numpy as np
from CONSTANTS import Constants
import pickle


class Model_Board:
    def __init__(self, list_of_players, board_size):
        self.board_size = board_size
        self.board = np.full((Constants.BOARD_SIZES[self.board_size], Constants.BOARD_SIZES[self.board_size]), -1)
        self.win_board = np.full((Constants.BOARD_SIZES[self.board_size], Constants.BOARD_SIZES[self.board_size]), -1)
        self.list_of_players = list_of_players
        self.fill_board_for_game_start(self.list_of_players)
        self.fill_board_for_game_end(self.list_of_players)

    def fill_triangle(self, num, full=False):
        """

        :param num: the number of the triangle in the board (1-6) (starts from the bottom and goes counter
        clockwise)
        :param full: True if the triangle should be full. if so will fill the triangle with the number of he
        triangle. if false than will fill the places with 0 which indicates free space on the board
        :return: changes self.board itself

        the function slices the board, flips it, changes the triangle and than flips it again.
        this is done bocause the indices return from tril_indices and triu_indices are the upper right triangle
        and the down left triangle. because I had to change the upper left and down right the board is flipped
         horizontally
        """
        indices = [np.tril_indices(Constants.LROW_SIZE[self.board_size]),
                   np.triu_indices(Constants.LROW_SIZE[self.board_size])]
        slice = Constants.TRIANGLE_SLICES[self.board_size][num - 1]
        a = np.fliplr(self.board[slice[0]:slice[1], slice[2]: slice[3]])
        a[indices[num % 2]] = num if full else 0
        a = np.fliplr(a)
        self.board[slice[0]:slice[1], slice[2]: slice[3]] = a

    def fill_triangle_end(self, num, full=False):
        """
        :param num: the number of the triangle in the board (1-6) (starts from the bottom and goes counter
        clockwise)
        :param full: True if the triangle should be full. if so will fill the triangle with the number of the
        rival triangle. if false than will fill the places with 0, which indicates free space on the board
        :return: changes self.win_board itself

        the function slices the board, flips it changes the triangle and than filps it again.
        this is done bocause the indices return from tril_indices and triu_indices are the upper right triangle
        and the down left triangle. because I had to change the upper left and down right the board is fliped
         horizontaly
        """
        indices = [np.tril_indices(Constants.LROW_SIZE[self.board_size]),
                   np.triu_indices(Constants.LROW_SIZE[self.board_size])]
        rival_num = num - 3 if num > 3 else num + 3
        slice = Constants.TRIANGLE_SLICES[self.board_size][rival_num - 1]
        a = np.fliplr(self.win_board[slice[0]:slice[1], slice[2]: slice[3]])
        a[indices[rival_num % 2]] = num if full else 0
        a = np.fliplr(a)
        self.win_board[slice[0]:slice[1], slice[2]: slice[3]] = a

    def fill_triangles_according_to_players(self, list_of_players):
        """
        :param list_of_players: list of numbers of players in the game
        fills the triangles for the start of the game in the board
        """
        for i in range(6):
            self.fill_triangle(i + 1, True if i + 1 in list_of_players else False)

    def fill_triangles_according_to_end_players(self, list_of_players):
        """
           :param list_of_players: list of numbers of players in the game
           fills the triangles for the win_check in the win_board
        """
        for i in range(6):
            self.fill_triangle_end(i + 1, True if i + 1 in list_of_players else False)

    def fill_board_for_game_start(self, list_of_players):
        """

        :param list_of_players: list of players' numbers.
        fills the entire board according to the game start
        """
        num = Constants.LROW_SIZE[self.board_size]
        self.board[num: np.size(self.board, 0) - num, num: np.size(self.board, 1) - num] = 0
        self.fill_triangles_according_to_players(list_of_players)

    def fill_board_for_game_start2(self):
        """just for checking things, Is not used in the real game"""
        file = open('important', 'rb')
        self.board = pickle.load(file)

    def fill_board_for_game_end(self, list_of_players):
        """
        :param list_of_players: list of players' numbers.
        fills the entire board according to the game end.
        """
        num = Constants.LROW_SIZE[self.board_size]
        self.win_board[num: np.size(self.board, 0) - num, num: np.size(self.board, 1) - num] = 0
        self.fill_triangles_according_to_end_players(list_of_players)

    def get_triangle_indices(self, num):
        return Constants.TRIANGLE_SLICES[self.board_size][num - 1]




