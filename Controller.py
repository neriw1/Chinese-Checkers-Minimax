from Model import Model
from CONSTANTS import Constants


class Controller:
    def __init__(self, num_of_players, players_type_list, board_size, game_direction, simu_mode=False,
                 number_of_games=100):
        self.num_of_players = num_of_players
        self.game_direction = game_direction
        self.list_of_players_numbers = self.create_list_of_players_according_to_num()
        self.model = Model(self.list_of_players_numbers, board_size)
        self.whos_turn = self.list_of_players_numbers[0]
        self.moved_item = (0, 0)
        self.last_steps = []
        self.players_type_list = players_type_list
        self.game_won = False
        self.wins = [0, 0, 0, 0, 0, 0]
        self.simulation_mode = simu_mode
        self.num_of_games = number_of_games
        """the direction in which the game will be held in a two player game:
        forward on the the r axis : 0, s axis: 1, q axis: 2 """

    def preform_move(self, oval_coordinates, finish_coordinates):
        """Preforms a move and adds the start coordinates to the last_steps list"""
        self.model.preform_move(oval_coordinates, finish_coordinates)
        if abs(oval_coordinates[0] - finish_coordinates[0]) == 2 or abs(
                oval_coordinates[1] - finish_coordinates[1]) == 2:
            self.last_steps.append(oval_coordinates)

    def get_step_options(self, oval_coordinates):
        """Returns the steps the player can preform from a given place"""
        if self.moved_item != (0, 0):
            return self.model.get_step_options(oval_coordinates, 1, self.last_steps)
        else:
            return self.model.get_step_options(oval_coordinates, 0)

    def end_turn(self):
        """Ends the turn and resets moved_item and last_steps"""
        # ("turn should end")
        if self.list_of_players_numbers.index(self.whos_turn) == self.num_of_players - 1:
            self.whos_turn = self.list_of_players_numbers[0]
        else:
            self.whos_turn = self.list_of_players_numbers[self.list_of_players_numbers.index(self.whos_turn) + 1]
        self.moved_item = (0, 0)
        self.last_steps = []
        # if self.list_of_players_numbers[self.list_of_players_numbers.index(self.whos_turn)] == 1:

    def is_win(self):
        """Returns true if the current player won, false otherwise"""
        ans = self.model.is_win(self.whos_turn)
        if ans:
            self.wins[self.whos_turn - 1] += 1
        return ans

    def reset_game(self):
        """resets the game"""
        self.whos_turn = self.list_of_players_numbers[0]
        self.model.reset_game(self.list_of_players_numbers)
        self.model.reset_game(self.list_of_players_numbers)
        self.moved_item = (0, 0)
        self.last_steps = []
        self.game_won = False

    def create_list_of_players_according_to_num(self):
        """returns a list of the number of each player -
        determining the places in which the players will be positioned on the board"""
        if self.num_of_players == 2:
            return Constants.TWO_PLAYERS_OPTIONS[self.game_direction]
        else:
            return Constants.PLAYERS_LISTS_THREE_AND_UP[self.num_of_players - 3]

    def get_player_in_oval_number(self, coordinates):
        return self.model.model_board.board[coordinates[0], coordinates[1]]

    def get_player_in_oval_color_index(self, coordinates):
        num = self.get_player_in_oval_number(coordinates)
        if num == 0:
            return -1
        else:
            return self.list_of_players_numbers.index(num)

    def get_board_size(self):
        return self.model.model_board.board_size

    def preform_turn_computer(self):
        player_type = self.get_current_player_type()
        return self.model.preform_turn_computer(player_type, self.whos_turn)

    def preform_turn_person(self, start_c, finish_c):
        player_type = self.players_type_list[self.list_of_players_numbers.index(self.whos_turn)]
        val = self.model.preform_turn_person(player_type, self.whos_turn, start_c, finish_c, self.last_steps)
        if val == 1:
            self.moved_item = finish_c
        return val

    def get_current_player_type(self):
        return self.players_type_list[self.list_of_players_numbers.index(self.whos_turn)]


