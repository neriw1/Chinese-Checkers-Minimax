import tkinter
from tkinter import *
from tkinter import ttk
from CONSTANTS import Constants
from Controller import Controller
from PIL import Image, ImageTk
import time
import math
import pickle


class View_Board:
    def __init__(self, father, view, num_of_players, board_size, game_direction=0):
        self.controller = Controller(num_of_players, view.players_type_list, board_size, game_direction)
        self.board_size = board_size
        self.view = view
        self.canvas = tkinter.Canvas(father, bg="white", height=500, width=600)
        self.canvas.grid(row=0, column=0)
        self.pit_rows = []
        self.create_pits_and_store_in_list()
        self.chosen_pit = (0, 12)
        self.images = []
        """below are just helpful attributes for the winning window and pickling function"""
        self.win_rec = None
        self.win_text1 = None
        self.win_text2 = None
        self.win_text3 = None
        self.board_file = None
        self.check_board = None

    def create_pickle_buttons(self):
        self.dump_button = self.canvas.create_rectangle(0, 0, 20, 20, fill="pink")
        self.canvas.tag_bind(self.dump_button, '<Button-1>', self.pickle_board)
        self.load_button = self.canvas.create_rectangle(20, 0, 40, 20, fill="blue")
        self.canvas.tag_bind(self.load_button, '<Button-1>', self.get_pickled_board_and_check)

    def pickle_board(self, event):
        file = open('important', 'wb')
        pickle.dump(self.controller.model.model_board.board, file, protocol=None, fix_imports=True,
                    buffer_callback=None)
        file = open('important', 'rb')
        self.check_board = pickle.load(file)

    def get_pickled_board_and_check(self, event):
        file = open('important', 'r')
        self.check_board = pickle.load(file)

    def create_pits_and_store_in_list(self):
        """creation of the ovals on the canvas and their storing in the pit_rows list. the creation is acording to
        the model board"""
        for i in range(Constants.BOARD_SIZES[self.board_size]):
            pit_row = []
            for j in range(Constants.BOARD_SIZES[self.board_size]):
                if self.controller.get_player_in_oval_number((i, j)) != -1:
                    if self.controller.get_player_in_oval_number((i, j)) == 0:
                        oval_button1 = self.set_oval_coordinates(i, j, "white")
                    else:
                        oval_button1 = self.set_oval_coordinates(i, j, self.view.color_list[
                            self.controller.get_player_in_oval_color_index((i, j))])
                    self.canvas.tag_bind(oval_button1, '<Button-1>', self.on_oval_click)
                    pit_row.append(oval_button1)
                else:
                    pit_row.append(None)
            self.pit_rows.append(pit_row)
        # self.create_pickle_buttons()

    def on_oval_click(self, event):
        """Marking the chosen oval - the one that is clicked on.
        Will not work if there was a moved item (the player jumped)"""
        if self.controller.moved_item != (0, 0) or self.controller.get_current_player_type() > 0:
            return
        self.reset_oval_onclick()
        self.delete_options_on_board(self.chosen_pit)
        r, q = self.pixel_to_hex(event.x, event.y, self.board_size)
        """if r < 0:
            r += 1
        if q < 0:
            q += 1
        if r > 16:
            r -= 1
        if q > 16:
            q -= 1"""
        chosen_oval = self.pit_rows[r][q]
        # if chosen_oval is None:

        self.canvas.itemconfig(chosen_oval, width="4", outline="#f7d414")  # change color
        self.chosen_pit = (r, q)
        self.show_options_on_board()

    def mark_moving_item(self, r, q):
        chosen_oval = self.pit_rows[r][q]
        # if chosen_oval is None:
        self.canvas.itemconfig(chosen_oval, width="4", outline="#f7d414")  # change color
        self.chosen_pit = (r, q)
        if self.controller.players_type_list[
            self.controller.list_of_players_numbers.index(self.controller.whos_turn)] == 0:
            self.show_options_on_board()

    def on_move_click(self, finish_coordinates):
        """Marks the pit in the finish_coordinates as the chosen pit"""
        self.chosen_pit = (finish_coordinates[0], finish_coordinates[1])
        chosen_oval = self.pit_rows[finish_coordinates[0]][finish_coordinates[1]]
        self.canvas.itemconfig(chosen_oval, width="4", outline="#f7d414")  # change color

    def reset_oval_onclick(self):
        """resets the pit that was previously chosen"""
        r, q = self.chosen_pit
        chosen_oval = self.pit_rows[r][q]
        self.canvas.itemconfig(chosen_oval, width="1", outline="black")  # change color

    def letters_key_click(self, event, x):
        if self.controller.moved_item != (0, 0):
            return
        r, q = self.chosen_pit
        s = -r - q
        self.reset_oval_onclick()
        self.delete_options_on_board(self.chosen_pit)
        if x == 'R-Up' and r > 0 and self.pit_rows[r - 1][q] is not None:
            self.chosen_pit = (r - 1, q)
        elif x == 'R-Down' and r < 16 and self.pit_rows[r + 1][q] is not None:
            self.chosen_pit = (r + 1, q)
        elif x == 'Q-Up' and q < 16 and self.pit_rows[r][q + 1] is not None:
            self.chosen_pit = (r, q + 1)
        elif x == 'Q-Down' and q > 0 and self.pit_rows[r][q - 1] is not None:
            self.chosen_pit = (r, q - 1)
        elif x == 'S-Up' and r > 0 and q < 16 and self.pit_rows[r - 1][q + 1] is not None:
            self.chosen_pit = (r - 1, q + 1)
        elif x == 'S-Down' and r < 16 and q > 0 and self.pit_rows[r + 1][q - 1] is not None:
            self.chosen_pit = (r + 1, q - 1)
        chosen_oval = self.pit_rows[self.chosen_pit[0]][self.chosen_pit[1]]
        self.canvas.itemconfig(chosen_oval, width="4", outline="#f7d414")  # change color
        self.show_options_on_board()

    """def move(self, event):

        preforms a move on the board.
        if the move is a regular move the turn will end.
        in the case of a jump: if there are no options to move to, the turn will end as well.
                               if there are place that the player can move to, they will be marked.

        finish_coordinates = self.pixel_to_hex(event.x, event.y, self.board_size)
        start_coordinates = (self.chosen_pit[0], self.chosen_pit[1])
        # this might become a problem
        start_c = (self.chosen_pit[0], self.chosen_pit[1])
        self.delete_options_on_board(self.chosen_pit)
        self.controller.preform_move(self.chosen_pit, finish_coordinates)
        finish_pit = self.pit_rows[finish_coordinates[0]][finish_coordinates[1]]
        start_pit = self.pit_rows[start_coordinates[0]][start_coordinates[1]]
        finish_color = "white"
        start_color = "white"
        finish_color_index = self.controller.get_player_in_oval_color_index(finish_coordinates)
        start_color_index = self.controller.get_player_in_oval_color_index(start_c)
        if finish_color_index != -1:
            finish_color = self.view.color_list[finish_color_index]
        if start_color_index != -1:
            finish_color = self.view.color_list[start_color_index]
        self.canvas.itemconfig(start_pit, fill=start_color)  # change color
        self.canvas.itemconfig(finish_pit, fill=finish_color)  # change color
        # changing frame color of the chosen pit to black again
        self.reset_oval_onclick()
        # changing the frame color of the finish pit to gold
        self.on_move_click(finish_coordinates)
        if abs(finish_coordinates[0] - start_coordinates[0]) == 2 or abs(finish_coordinates[1] - start_coordinates[1]) == 2:
            self.controller.moved_item = (finish_coordinates[0], finish_coordinates[1])
            if len(self.controller.get_step_options(finish_coordinates)) == 0:
                if self.controller.is_win():
                    self.on_win()
                    return
                else:
                    self.view.on_finish_turn_visual()
            else:
                self.show_options_on_board()
        else:
            if self.controller.is_win():
                self.on_win()
                return
            else:
                self.view.on_finish_turn_visual()
        start_coordinates, finish_coordinates = self.controller.get_computer_random_move()
        if start_coordinates is not None:
            self.computer_random_move(start_coordinates, finish_coordinates)
    """
    """def computer_random_move(self, start_coordinates, finish_coordinates):
        # make the chosen pit the start coordinates
        self.chosen_pit = start_coordinates
        self.mark_moving_item(start_coordinates[0], start_coordinates[1])
        self.show_options_on_board()
        self.view.root.update()
        time.sleep(Constants.SLEEP_TIME)
        self.view.root.update()
        # for some reason convert the chosen pit to a list
        start_c = (self.chosen_pit[0], self.chosen_pit[1])
        # trying to mark the item.
        self.mark_moving_item(start_c[0], start_c[1])
        # deleting the options on the board because the computer is preforming a move
        self.delete_options_on_board(self.chosen_pit)
        # preforming the move in the controller
        self.controller.preform_move(self.chosen_pit, finish_coordinates)
        # getting the id of the finish_pit and start_pit from the pit_rows
        finish_pit = self.pit_rows[finish_coordinates[0]][finish_coordinates[1]]
        start_pit = self.pit_rows[start_coordinates[0]][start_coordinates[1]]
        finish_color = "white"
        start_color = "white"
        # getting the colors according to the numbers on the model_board
        finish_color_index = self.controller.get_player_in_oval_color_index(finish_coordinates)
        start_color_index = self.controller.get_player_in_oval_color_index(start_c)
        if finish_color_index != -1:
            finish_color = self.view.color_list[finish_color_index]
        if start_color_index != -1:
            finish_color = self.view.color_list[start_color_index]
        # changing the color of the pits on the the view_board according to the color in the model_board
        self.canvas.itemconfig(start_pit, fill=start_color)  # change color
        self.canvas.itemconfig(finish_pit, fill=finish_color)  # change color
        self.reset_oval_onclick()
        self.on_move_click(finish_coordinates)
        if self.controller.is_win():
            self.on_win()
            return
        # if the move is a jump:
        if abs(finish_coordinates[0] - start_coordinates[0]) == 2 or abs(
                finish_coordinates[1] - start_coordinates[1]) == 2:
            # change the moved item so it will point to the place where the turn will end
            self.controller.moved_item = (finish_coordinates[0], finish_coordinates[1])
            # if there is no other jump to make after this jump:
            if len(self.controller.get_step_options(finish_coordinates)) == 0:
                # if the player won
                # if the player didn't win and there are no other jumps to make after this jump end the turn
                self.view.on_finish_turn_visual()
                # if the turn ended
                start_coordinates, finish_c = self.controller.get_computer_random_move()
                if start_coordinates is not None:
                    self.computer_random_move(start_coordinates, finish_c)
            else:
                start_coordinates, finish_c = self.controller.get_computer_random_move()
                if start_coordinates is not None:
                    if start_coordinates == (0, 0):
                        self.view.on_finish_turn_visual()
                        start_coordinates, finish_c = self.controller.get_computer_random_move()
                        if start_coordinates is not None:
                            self.computer_random_move(start_coordinates, finish_c)
                    else:
                        self.computer_random_move(start_coordinates, finish_c)
        else:
            # in case there was no jump:
            self.view.on_finish_turn_visual()
        # self.show_options_on_board()
        start_coordinates, finish_coordinates = self.controller.get_computer_random_move()
        if start_coordinates is not None:
            self.computer_random_move(start_coordinates, finish_coordinates)"""

    def person_move(self, event):
        """
        preforms a move on the board.
        if the move is a regular move the turn will end.
        in the case of a jump: if there are no options to move to, the turn will end as well.
                               if there are place that the player can move to, they will be marked.
        """
        finish_coordinates = self.pixel_to_hex(event.x, event.y, self.board_size)
        start_coordinates = (self.chosen_pit[0], self.chosen_pit[1])
        start_c = (self.chosen_pit[0], self.chosen_pit[1])
        self.delete_options_on_board(self.chosen_pit)
        val = self.controller.preform_turn_person(self.chosen_pit, finish_coordinates)
        self.change_color_on_board(start_coordinates)
        self.change_color_on_board(finish_coordinates)
        self.reset_oval_onclick()
        self.on_move_click(finish_coordinates)
        if val == 0:
            self.view.on_finish_turn_visual()
            self.computer_move()
        elif val == 1:
            self.show_options_on_board()
        else:
            self.on_win()

    def computer_move(self):
        self.view.root.update()
        time.sleep(Constants.SLEEP_TIME)
        self.view.root.update()
        moves_list, is_win = self.controller.preform_turn_computer()
        if moves_list is None:
            return
        color = None
        first_move = True
        for start_c, finish_c in moves_list:
            self.mark_moving_item(start_c[0], start_c[1])
            if first_move:
                chosen_oval = self.pit_rows[self.chosen_pit[0]][self.chosen_pit[1]]
                color = self.canvas.itemcget(chosen_oval, 'fill')
                first_move = False
            self.view.root.update()
            time.sleep(Constants.SLEEP_TIME)
            self.view.root.update()
            self.change_color_on_board(start_c)
            self.change_color_on_board(finish_c, color)
            self.reset_oval_onclick()
            self.view.root.update()
            time.sleep(Constants.SLEEP_TIME)
            self.view.root.update()
            self.on_move_click(finish_c)
        if is_win:
            self.on_win()
        else:
            self.view.on_finish_turn_visual()
            self.computer_move()

    def show_options_on_board(self):
        options = self.controller.get_step_options(self.chosen_pit)
        chosen_oval = self.pit_rows[self.chosen_pit[0]][self.chosen_pit[1]]
        if self.canvas.itemcget(chosen_oval, 'fill') != "white":
            if self.controller.list_of_players_numbers[
                self.view.color_list.index(self.canvas.itemcget(chosen_oval, 'fill'))] == self.controller.whos_turn:
                if self.controller.moved_item == (0, 0) or (
                        self.controller.moved_item != (0, 0) and self.controller.moved_item == self.chosen_pit):
                    for pit in options:
                        self.canvas.itemconfig(self.pit_rows[pit[0]][pit[1]], width="4",
                                               outline=self.canvas.itemcget(chosen_oval, 'fill'))  # change color
                        self.canvas.tag_bind(self.pit_rows[pit[0]][pit[1]], '<Button-1>', self.person_move)

    def delete_options_on_board(self, coordinates):
        options = self.controller.get_step_options(coordinates)
        for pit in options:
            self.canvas.itemconfig(self.pit_rows[pit[0]][pit[1]], width="1", outline="black")  # change color
            self.canvas.tag_bind(self.pit_rows[pit[0]][pit[1]], '<Button-1>', self.on_oval_click)

    def on_win(self):
        """creation of a black rectangle of the board after a win
            Also calls the controller win function.
        """
        self.controller.game_won = True
        self.create_rectangle(0, 0, 600, 500, fill="black", alpha=.85)
        self.view.on_win_visual(self.controller.whos_turn)
        if self.controller.simulation_mode and self.controller.num_of_games > 0:
            self.controller.num_of_games -= 1
            self.view.reset_game_view()
        elif self.controller.simulation_mode and self.controller.num_of_games == 0:
            print(self.controller.wins)

    def create_rectangle(self, x, y, a, b, **options):
        if 'alpha' in options:
            # Calculate the alpha transparency for every color(RGB)
            alpha = int(options.pop('alpha') * 255)
            # Use the fill variable to fill the shape with transparent color
            fill = options.pop('fill')
            fill = self.view.root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (a - x, b - y), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.rec_img = self.canvas.create_image(x, y, image=self.images[-1], anchor='nw')
            self.win_rec = self.canvas.create_rectangle(x, y, a, b, **options)

    def delete_win_page(self):
        self.canvas.delete(self.win_rec)
        self.canvas.delete(self.rec_img)
        self.canvas.delete(self.win_text1)
        self.canvas.delete(self.win_text2)
        self.canvas.delete(self.win_text3)

    def set_oval_coordinates(self, i, j, color):
        x_middle, y_middle = self.hex_to_pixel(i, j, self.board_size)
        radius = Constants.OVAL_RADIUS[self.board_size]
        return self.canvas.create_oval(x_middle - radius, y_middle - radius, x_middle + radius, y_middle + radius,
                                       fill=color)

    def change_color_on_board(self, coordinates, color=None):
        the_pit = self.pit_rows[coordinates[0]][coordinates[1]]
        the_color = "white"
        color_index = self.controller.get_player_in_oval_color_index(coordinates)
        if color_index != -1:
            the_color = self.view.color_list[color_index]
        if color is not None:
            the_color = color
        self.canvas.itemconfig(the_pit, fill=the_color)  # change color

    def reset_game(self):
        if self.controller.game_won:
            self.delete_win_page()
        self.controller.reset_game()
        for i in range(Constants.BOARD_SIZES[self.board_size]):
            for j in range(Constants.BOARD_SIZES[self.board_size]):
                if self.controller.get_player_in_oval_number((i, j)) != -1:
                    self.change_color_on_board((i, j))
                    the_pit = self.pit_rows[i][j]
                    self.canvas.tag_bind(the_pit, '<Button-1>', self.on_oval_click)

    @staticmethod
    def hex_to_pixel(r, q, board_size):
        hex_side_size = 2 * Constants.OVAL_RADIUS[board_size] / math.sqrt(3)
        x = hex_side_size * (math.sqrt(3) * q + math.sqrt(3) / 2 * r) - 60
        y = hex_side_size * (
                3. / 2 * r) + Constants.OVAL_RADIUS[board_size] + 5
        return x, y

    @staticmethod
    def pixel_to_hex(x, y, board_size):
        hex_side_size = 2 * Constants.OVAL_RADIUS[board_size] / math.sqrt(3)
        q = (math.sqrt(3) / 3 * (x + 60) - 1. / 3 * (y - Constants.OVAL_RADIUS[board_size] - 5)) / hex_side_size
        r = (2. / 3 * (y - Constants.OVAL_RADIUS[board_size] - 5)) / hex_side_size
        return View_Board.axial_round(r, q)

    @staticmethod
    def axial_round(frac_r, frac_q):
        r, q, s = View_Board.cube_round(frac_r, frac_q, - frac_r - frac_q)
        return r, q

    @staticmethod
    def cube_round(frac_r, frac_q, frac_s):
        q = round(frac_q)
        r = round(frac_r)
        s = round(frac_s)
        q_diff = abs(q - frac_q)
        r_diff = abs(r - frac_r)
        s_diff = abs(s - frac_s)
        if q_diff > r_diff and q_diff > s_diff:
            q = -r - s
        elif r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
        return r, q, s











