import numpy
from Model_Board import Model_Board
from CONSTANTS import Constants
import numpy as np
import random
import time as time


class Model:
    def __init__(self, list_of_players, board_size):
        self.model_board = Model_Board(list_of_players, board_size)
        self.direction_vectors = [[(1, 0), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, 1)],
                                  [(-1, 0), (0, -1), (-1, 1), (1, -1), (0, 1), (1, 0)],
                                  [(0, -1), (1, -1), (1, 0), (-1, 0), (0, 1), (-1, 1)],
                                  [(-1, 0), (-1, 1), (0, 1), (0, -1), (1, 0), (1, -1)],
                                  [(0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1)],
                                  [(0, 1), (-1, 1), (1, 0), (-1, 0), (0, -1), (1, -1)]]
        self.last_steps_made = []
        self.board_size = board_size

    def check_full_and_empty_neighbors(self, oval_coordinates):
        """
        :param oval_coordinates: the coordinates of a place in the board
        :return: returns a tuple of lists that store the coordinates of the neighbors
        """
        full_neighbors = []
        empty_neighbors = []
        row_num = np.size(self.model_board.board, 0)
        col_num = np.size(self.model_board.board, 1)
        player = self.model_board.board[oval_coordinates[0], oval_coordinates[1]]
        if player < 1:
            return
        for dir_vec in self.direction_vectors[player - 1]:
            neighbor_coordinates = (oval_coordinates[0] + dir_vec[0], oval_coordinates[1] + dir_vec[1])
            if 0 <= neighbor_coordinates[0] < row_num and \
                    0 <= neighbor_coordinates[1] < col_num:
                if self.model_board.board[neighbor_coordinates[0], neighbor_coordinates[1]] > 0:
                    full_neighbors.append(neighbor_coordinates)
                elif self.model_board.board[neighbor_coordinates[0], neighbor_coordinates[1]] == 0:
                    empty_neighbors.append(neighbor_coordinates)
        return empty_neighbors, full_neighbors

    def get_step_options(self, oval_coordinates, jumps, last_steps=[]):
        """

        :param oval_coordinates: the coordinates of a piece on the board
        :param jumps: 1 if the player has to jump (in case he already jumped) else 0
        :param last_steps: a list of the coordinates on the board the player has already been to in the current turn
        :return: a list of the places in which a piece can move to
        """
        options_list = []
        if not self.model_board.board[oval_coordinates[0], oval_coordinates[1]] < 1:
            empty_neighbors, full_neighbors = self.check_full_and_empty_neighbors(oval_coordinates)
            for neighbor in full_neighbors:
                jump_coordinates = (neighbor[0] * 2 - oval_coordinates[0], neighbor[1] * 2 - oval_coordinates[1])
                if jump_coordinates not in last_steps:
                    if -1 < jump_coordinates[0] < Constants.BOARD_SIZES[self.model_board.board_size] and -1 < \
                            jump_coordinates[1] < Constants.BOARD_SIZES[self.model_board.board_size] and \
                            self.model_board.board[jump_coordinates[0], jump_coordinates[1]] == 0:
                        options_list.append(jump_coordinates)
            if jumps == 0:
                for e_n in empty_neighbors:
                    options_list.append(e_n)
            return options_list
        return []

    def is_win(self, player):
        """
        :param player: the number of the players pieces
        the function checks specifically the square in which the player's target triangle is positioned. it will check if it matches the
        triangle in the win_board, which is an attribute of the model_board.
        :return: true if the player won, false otherwise
        """
        if player < 4:
            against_player = player + 3
        else:
            against_player = player - 3
        target_player_place_slices = Constants.TRIANGLE_SLICES[self.model_board.board_size][against_player - 1]
        current_part = self.model_board.board[target_player_place_slices[0]:target_player_place_slices[1],
                       target_player_place_slices[2]: target_player_place_slices[3]]
        desirable_part = self.model_board.win_board[target_player_place_slices[0]:target_player_place_slices[1],
                         target_player_place_slices[2]: target_player_place_slices[3]]
        return numpy.array_equal(current_part, desirable_part)

    def preform_move(self, start_oval_coordinates, finish_oval_coordinates):
        """
        :param start_oval_coordinates: the coordinates in which the player was first.
        :param finish_oval_coordinates: the coordinates the player is going to.
        """
        s_x, s_y = start_oval_coordinates
        f_x, f_y = finish_oval_coordinates
        self.model_board.board[f_x, f_y] = self.model_board.board[s_x, s_y]
        self.model_board.board[s_x, s_y] = 0

    def reset_game(self, list_of_players):
        """

        :param list_of_players: list of numbers, that represents each player on the model_board
        resets the game by creating a new Model_Board
        """
        self.model_board = Model_Board(list_of_players, self.board_size)

    def get_all_player_indices(self, player):
        return np.argwhere(self.model_board.board == player)

    def next_player_options(self, jumps, player, moved_item, last_steps):
        next_options = {}
        if jumps == 1:
            next_options[moved_item] = self.get_step_options(moved_item, jumps, last_steps)
            return next_options
        p_indices = self.get_all_player_indices(player)
        for i, val in enumerate(p_indices):
            start_piece = (val[0], val[1])
            piece_options = self.get_step_options(start_piece, jumps)
            if len(piece_options):
                next_options[start_piece] = piece_options
        return next_options

    def is_jump(self, start_pos, finish_pos):
        if abs(start_pos[0] - finish_pos[0]) == 2 or abs(start_pos[1] - finish_pos[1]) == 2:
            return True
        return False

    def generate_random_move(self, jumps, player, moved_item, last_steps=[]):
        next_options = self.next_player_options(jumps, player, moved_item, last_steps)
        if jumps:
            next_options[(0, 0)] = (0, 0)
        piece_indices = random.choice(list(next_options.keys()))
        place_to_move = random.choice(next_options[piece_indices])
        return piece_indices, place_to_move

    def alpha_beta(self, jumps, max_player, min_player, moved_item, last_steps, depth):
        self.last_steps_made = last_steps
        options = self.next_player_options(jumps, max_player, moved_item, last_steps)
        best_move = (0, 0), (0, 0)
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        options_counter = 0
        starting_positions = options.keys()
        if jumps:
            for start_pos in starting_positions:
                for finish_pos in options[start_pos]:
                    options_counter += 1
                    self.place_move(start_pos, finish_pos, start_pos)
                    score2 = self.max_play(1, depth, max_player, min_player, finish_pos, alpha, beta)
                    self.remove_move(start_pos, finish_pos)
                    if score2 > best_score:
                        best_score = score2
                        best_move = start_pos, finish_pos
                    if best_score > alpha:
                        alpha = best_score
                    if beta <= alpha:
                        break
            last_steps = self.last_steps_made.copy()
            score1 = self.min_play(0, depth - 1, max_player, min_player, (0, 0), alpha, beta)
            self.last_steps_made = last_steps
            if score1 > best_score:
                best_score = score1
                best_move = ((0, 0), (0, 0))
            if best_score > alpha:
                alpha = best_score
        else:
            for start_pos in starting_positions:
                for finish_pos in options[start_pos]:
                    options_counter += 1
                    if self.is_jump(start_pos, finish_pos):
                        self.place_move(start_pos, finish_pos, start_pos)
                        score = self.max_play(1, depth, max_player, min_player, finish_pos, alpha, beta)
                        self.remove_move(start_pos, finish_pos, start_pos)
                    else:
                        self.place_move(start_pos, finish_pos)
                        last_steps = self.last_steps_made
                        score = self.min_play(0, depth - 1, max_player, min_player, (0, 0), alpha, beta)
                        self.last_steps_made = last_steps
                        self.remove_move(start_pos, finish_pos)
                    if score > best_score:
                        best_score = score
                        best_move = start_pos, finish_pos
                    if best_score > alpha:
                        alpha = best_score
                    if beta <= alpha:
                        break
        return best_move

    def min_play(self, jumps, depth, max_player, min_player, moved_item, alpha, beta):
        if not jumps:
            self.last_steps_made = []
        if self.is_win(min_player) or self.is_win(max_player) or depth == 0:
            return self.evaluate1(max_player, min_player, depth)
        min_score = float('inf')
        options = self.next_player_options(jumps, min_player, moved_item, self.last_steps_made)
        starting_positions = options.keys()
        if jumps:
            for start_pos in starting_positions:
                for finish_pos in options[start_pos]:
                    self.place_move(start_pos, finish_pos, start_pos)
                    score2 = self.min_play(1, depth, max_player, min_player, finish_pos, alpha, beta)
                    self.remove_move(start_pos, finish_pos)
                    if score2 < min_score:
                        min_score = score2
                    if min_score < beta:
                        beta = min_score
                    if beta <= alpha:
                        break

            last_steps = self.last_steps_made.copy()
            score1 = self.max_play(0, depth - 1, max_player, min_player, (0, 0), alpha, beta)
            self.last_steps_made = last_steps
            if score1 < min_score:
                min_score = score1
            if min_score < beta:
                beta = min_score
        else:
            for start_pos in starting_positions:
                for finish_pos in options[start_pos]:
                    if self.is_jump(start_pos, finish_pos):
                        self.place_move(start_pos, finish_pos, start_pos)
                        score = self.min_play(1, depth, max_player, min_player, finish_pos, alpha, beta)
                        self.remove_move(start_pos, finish_pos, start_pos)
                    else:
                        self.place_move(start_pos, finish_pos)
                        last_steps = self.last_steps_made.copy()
                        score = self.max_play(0, depth - 1, max_player, min_player, (0, 0), alpha, beta)
                        self.last_steps_made = last_steps
                        self.remove_move(start_pos, finish_pos)
                    if score < min_score:
                        min_score = score
                    if min_score < beta:
                        beta = min_score
                    if beta <= alpha:
                        break
        return min_score

    def max_play(self, jumps, depth, max_player, min_player, moved_item, alpha, beta):
        if not jumps:
            self.last_steps_made = []
        if self.is_win(min_player) or self.is_win(max_player) or depth == 0:
            return self.evaluate1(max_player, min_player, depth)
        max_score = float('-inf')
        options = self.next_player_options(jumps, max_player, moved_item, self.last_steps_made)
        starting_positions = options.keys()
        if jumps:
            for start_pos in starting_positions:
                for finish_pos in options[start_pos]:
                    self.place_move(start_pos, finish_pos, start_pos)
                    score2 = self.max_play(1, depth, max_player, min_player, finish_pos, alpha, beta)
                    self.remove_move(start_pos, finish_pos)
                    if score2 > max_score:
                        max_score = score2
                    if max_score > alpha:
                        alpha = max_score
                    if beta <= alpha:
                        break
            last_steps = self.last_steps_made.copy()
            score1 = self.min_play(0, depth - 1, max_player, min_player, (0, 0), alpha, beta)
            self.last_steps_made = last_steps
            if score1 > max_score:
                max_score = score1
            if max_score > alpha:
                alpha = max_score
        else:
            for start_pos in starting_positions:
                for finish_pos in options[start_pos]:
                    if self.is_jump(start_pos, finish_pos):
                        self.place_move(start_pos, finish_pos, start_pos)
                        score = self.max_play(1, depth, max_player, min_player, finish_pos, alpha, beta)
                        self.remove_move(start_pos, finish_pos, start_pos)
                    else:
                        self.place_move(start_pos, finish_pos)
                        last_steps = self.last_steps_made.copy()
                        score = self.min_play(0, depth - 1, max_player, min_player, (0, 0), alpha, beta)
                        self.last_steps_made = last_steps
                        self.remove_move(start_pos, finish_pos)
                    if score > max_score:
                        max_score = score
                    if max_score > alpha:
                        alpha = max_score
                    if beta <= alpha:
                        break
        return max_score

    def evaluate1(self, max_player, min_player, depth):
        if self.is_win(max_player):
            return 1000000000 * depth
        if self.is_win(min_player):
            return -1000000000 * depth
        max_a, max_b, max_c = self.a_b_c_values(max_player, min_player)
        min_a, min_b, min_c = self.a_b_c_values(min_player, max_player)
        val = self.check_annoying_marbles(max_player, min_player)
        target_pit = Constants.TARGET_PITS[self.model_board.board_size][max_player - 1]
        val -= (self.model_board.board[target_pit[0], target_pit[1]] == max_player) * 1
        val += (self.model_board.board[target_pit[0], target_pit[1]] == min_player) * 1
        score = Constants.W1 * (min_a - max_a) + (min_b - max_b) * Constants.W2 + (
                    max_c - min_c) * Constants.W3 - val * 20
        return score

    def place_move(self, start_pos, finish_pos, add_to_last_steps=None):
        self.model_board.board[finish_pos[0], finish_pos[1]] = self.model_board.board[start_pos[0], start_pos[1]]
        self.model_board.board[start_pos[0], start_pos[1]] = 0
        if add_to_last_steps is not None:
            self.last_steps_made.append(add_to_last_steps)

    def remove_move(self, start_pos, finish_pos, remove_from_last_steps=None):
        self.model_board.board[start_pos[0], start_pos[1]] = self.model_board.board[finish_pos[0], finish_pos[1]]
        self.model_board.board[finish_pos[0], finish_pos[1]] = 0
        if remove_from_last_steps is not None:
            self.last_steps_made.remove(remove_from_last_steps)

    def a_b_c_values(self, player, other_player):
        # a -> squared sum of the distances to the destination corner for all pieces of the player
        # b -> the squared sum of the distances to the vertical center line for all pieces of the player
        # c ->maximum vertical advance for all pieces of the player
        target_pit = Constants.TARGET_PITS[self.model_board.board_size][player - 1]
        home_pit = Constants.TARGET_PITS[self.model_board.board_size][other_player - 1]
        a = 0
        b = 0
        c = float('-inf')
        all_indices = self.get_all_player_indices(player)
        # if the player is moving forward on the the r axis and sideways on the q axis
        if player % 3 == 1:
            for indices in all_indices:
                r, q = indices
                s = -r - q
                row_mid = Constants.ROW_MIDDLES[self.model_board.board_size][r]
                a += (target_pit[0] - r) ** 2
                b += (row_mid - q) ** 2
                if c < abs(r - home_pit[0]):
                    c = abs(r - home_pit[0])
        # if the player is moving forward on the the s axis and sideways on the r axis
        if player % 3 == 2:
            for indices in all_indices:
                r, q = indices
                s = -1 * r - q
                if self.model_board.board_size == 1:
                    row_mid = Constants.ROW_MIDDLES[self.model_board.board_size][s + 18]
                else:
                    row_mid = Constants.ROW_MIDDLES[self.model_board.board_size][s + 24]
                a += (target_pit[2] - s) ** 2
                b += (row_mid - r) ** 2
                if c < abs(s - home_pit[2]):
                    c = abs(s - home_pit[2])
        # if the player is moving forward on the the q axis and side ways on the s axis
        if player % 3 == 0:
            for indices in all_indices:
                r, q = indices
                s = -r - q
                row_mid = Constants.ROW_MIDDLES[self.model_board.board_size][q]
                a += (target_pit[1] - q) ** 2
                if self.model_board.board_size == 1:
                    b += (-18 + row_mid - s) ** 2
                else:
                    b += (-24 + row_mid - s) ** 2
                if c < abs(q - home_pit[1]):
                    c = abs(q - home_pit[1])
        return a, b, c

    def alpha_beta_player(self, jumps, player, moved_item, last_steps=[]):
        if player <= 3:
            min_player = player + 3
        else:
            min_player = player - 3
        move, ans = self.first_move_win_heuristic(player, moved_item, last_steps)
        if ans:
            return move
        return self.alpha_beta(jumps, player, min_player, moved_item, last_steps, 3)

    def first_move_win_heuristic(self, player, moved_item, last_steps=None):
        self.last_steps_made = last_steps
        options = self.next_player_options(0, player, moved_item, last_steps)
        starting_positions = options.keys()
        for start_pos in starting_positions:
            for finish_pos in options[start_pos]:
                found_win = False
                self.place_move(start_pos, finish_pos)
                found_win = self.is_win(player)
                self.remove_move(start_pos, finish_pos)
                if found_win:
                    return (start_pos, finish_pos), 1
                return ((0, 0), (0, 0)), 0

    def preform_turn_computer(self, player_type, player):
        if player_type == 0:
            return None, None
        moves_list = []
        last_steps = []
        jumps = 0
        moved_item = (0, 0)
        while True:
            if player_type == 2:
                start_c, finish_c = self.generate_random_move(jumps, player, moved_item, last_steps)
            elif player_type == 1:
                start_c, finish_c = self.alpha_beta_player(jumps, player, moved_item, last_steps)
            if start_c == (0, 0):
                break
            moves_list.append((start_c, finish_c))
            self.preform_move(start_c, finish_c)
            if self.is_win(player):
                return moves_list, 1
            if self.is_jump(start_c, finish_c):
                last_steps.append(start_c)
                moved_item = finish_c
                jumps = 1
                if len(self.get_step_options(finish_c, jumps, last_steps)) == 0:
                    break
            else:
                break
        return moves_list, 0

    def preform_turn_person(self, player_type, player, start_c, finish_c, last_steps):
        self.preform_move(start_c, finish_c)
        if self.is_win(player):
            return 2
        if player_type == 0:
            if self.is_jump(start_c, finish_c):
                last_steps.append(start_c)
                if len(self.get_step_options(finish_c, 1, last_steps)) == 0:
                    return 0
                return 1
            else:
                return 0

    def check_annoying_marbles(self, max_player, min_player):
        cnt = 0
        slice = self.model_board.get_triangle_indices(min_player)
        row_num = np.size(self.model_board.board, 0)
        col_num = np.size(self.model_board.board, 1)
        step_options = 1e9
        for i in range(slice[0], slice[1]):
            for j in range(slice[2], slice[3]):
                if self.model_board.board[i][j] == min_player:
                    player = min_player
                    step_options = 0
                    for dir_vec in self.direction_vectors[player - 1]:
                        neighbor = (i + dir_vec[0], j + dir_vec[1])
                        jump_coordinates = (i + 2 * dir_vec[0], j + 2 * dir_vec[1])
                        if 0 <= neighbor[0] < row_num and 0 <= neighbor[1] < col_num:
                            nei_player = self.model_board.board[neighbor[0], neighbor[1]]
                            if nei_player == 0:
                                step_options += 1
                                continue
                            if 0 <= jump_coordinates[0] < row_num and 0 <= jump_coordinates[1] < col_num:
                                j_player = self.model_board.board[jump_coordinates[0], jump_coordinates[1]]
                                if j_player == 0:
                                    step_options += 1
                                if nei_player > 0 and j_player == max_player:
                                    cnt += 1
                                elif nei_player == max_player:
                                    cnt += 1
                            elif nei_player == max_player:
                                cnt += 1

            if cnt > 0 and step_options == 0:
                return 100
            # return cnt
            return 0



























