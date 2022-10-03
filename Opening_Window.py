from tkinter import *
from tkinter import ttk
from Player import Player
import tkinter as tk
import tkinter
class Opening_Window:
    def __init__(self, father, view):
        self.father = father
        self.view = view
        self.number_of_players = 2
        self.view.game_dir = 0
        self.y_top = 200
        self.y_bottom = self.y_top + 40
        self.x_start = 140
        self.x_finish = 180
        self.x_jump = 120
        self.game_title_frame = ttk.Frame(father)
        self.game_title_label = ttk.Label(self.game_title_frame, text="Chinese Checkers!!!!!",
                                          font=('Lucida Grande', 25))
        self.game_title_frame.pack()
        self.game_title_label.pack()
        self.choose_number_of_players_window()
        self.style = ttk.Style()
        self.visited_colors = False

    def change_number_of_players(self, event, y):
        """
        :param event: the click event
        :param x: Right if the player pressed the right arrow button and Left if the player pressed the left arrow button
        changes the current number of players according to the click
        """
        if y == "Right":
            if self.number_of_players < 6:
                self.canvas.itemconfig(self.num_choice_ovals[self.number_of_players - 2], fill="white")  # change color
                self.canvas.itemconfig(self.num_choice_ovals[self.number_of_players - 1], fill="pink")
                self.number_of_players += 1
                if self.number_of_players == 3:
                    self.canvas.tag_bind(self.continue_button, '<Button-1>',
                                         lambda event, x=self.choose_players_type_window: self.on_continue_click(event,
                                                                                                                 x))
                    self.canvas.tag_bind(self.continue_text, '<Button-1>',
                                         lambda event, x=self.choose_players_type_window: self.on_continue_click(event,
                                                                                                                 x))

        if y == "Left":
            if self.number_of_players > 2:
                self.canvas.itemconfig(self.num_choice_ovals[self.number_of_players - 2], fill="white")  # change color
                self.canvas.itemconfig(self.num_choice_ovals[self.number_of_players - 3], fill="pink")
                self.number_of_players -= 1
                if self.number_of_players == 2:
                    self.canvas.tag_bind(self.continue_button, '<Button-1>', self.choose_direction_window)
                    self.canvas.tag_bind(self.continue_text, '<Button-1>', self.choose_direction_window)

    def choose_number_of_players_window(self):
        """
        creates the first window where the player can choose the number of players in the game
        """
        self.view.game_dir = 0
        self.choice_box_frame = ttk.Frame(self.father)
        self.canvas = tkinter.Canvas(self.choice_box_frame, bg="white", height=450, width=800)
        self.choice_box_frame.pack()
        self.canvas.grid(row=1, column=0, columnspan=1)
        self.canvas.create_text(400, 80, text="Choose the number of players",font=('Lucida Grande', 15))
        vals_list = [2, 3, 4, 5, 6]
        self.num_choice_ovals = []
        for i in vals_list:
            self.canvas.create_text(self.x_start + 20 + (i-2)*self.x_jump, self.y_top - 30, text = f"{i}", font=('Lucida Grande', 15) )
            if i == self.number_of_players:
                self.oval2 = self.canvas.create_oval(self.x_start + (i-2)*self.x_jump,self.y_top,self.x_finish+(i-2)*self.x_jump ,self.y_bottom,  fill="pink")
            else:
                self.oval2 = self.canvas.create_oval(self.x_start + (i-2)*self.x_jump,self.y_top,self.x_finish+(i-2)*self.x_jump ,self.y_bottom,  fill="white")

            self.canvas.tag_bind(self.oval2, '<Button-1>', self.get_number_on_press)
            self.num_choice_ovals.append(self.oval2)
        self.continue_button = self.canvas.create_rectangle(300, 300, 500, 340, fill = "pink")
        self.continue_text = self.canvas.create_text(400, 320, text= "Continue...", font=('Lucida Grande', 15))
        self.canvas.tag_bind(self.continue_button, '<Button-1>', self.choose_direction_window)
        self.canvas.tag_bind(self.continue_text, '<Button-1>', self.choose_direction_window)
        """bind the arrow keys"""
        self.bind_left = self.view.root.bind('<Left>', lambda event, x='Left': self.change_number_of_players(event, x))
        self.bind_right = self.view.root.bind('<Right>', lambda event, x='Right': self.change_number_of_players(event, x))

    def get_number_on_press(self, event):
        """I need to change this function!!!!!!!!! it is super wasteful like really!
         should just convert the coordinates to the number with some sort of rounding mechanism"""
        i = 2
        while i < 7:
            if (self.x_start + (i-2)*self.x_jump) <= event.x <= (self.x_finish + (i-2)*self.x_jump):
                self.canvas.itemconfig(self.num_choice_ovals[self.number_of_players-2], fill="white")  # change color
                self.number_of_players = i
                self.canvas.itemconfig(self.num_choice_ovals[i-2], fill="pink")  # change color
                if i == 2:
                    self.canvas.tag_bind(self.continue_button, '<Button-1>', self.choose_direction_window)
                    self.canvas.tag_bind(self.continue_text, '<Button-1>',self.choose_direction_window)
                else:
                    self.canvas.tag_bind(self.continue_button, '<Button-1>',
                    lambda event, x=self.choose_players_type_window: self.on_continue_click(event, x))
                    self.canvas.tag_bind(self.continue_text, '<Button-1>',
                    lambda event, x=self.choose_players_type_window: self.on_continue_click(event, x))
                return
            i += 1

    def get_dir_on_press(self, event):
        i = 0
        while i < 3:
            if  (self.x_start + 73 + i * (self.x_jump+40)) <= event.x <= (self.x_finish + 73 + i * (self.x_jump + 40)):
                if self.view.game_dir == i:
                    return
                self.canvas.itemconfig(self.dir_choice_ovals[self.view.game_dir], fill="white")  # change color
                self.view.game_dir = i
                self.canvas.itemconfig(self.dir_choice_ovals[i], fill="pink")  # change color
                return
            i += 1

    def choose_direction_window(self, event):
        # self.view.root.unbind('<Left>', self.bind_left)
        # self.view.root.unbind('<Right>', self.bind_right)
        self.choice_box_frame.forget()
        self.choice_box_frame = ttk.Frame(self.father)
        self.canvas = tkinter.Canvas(self.choice_box_frame, bg="white", height=450, width=800)
        self.choice_box_frame.pack()
        self.canvas.grid(row=1, column=0, columnspan=1)
        self.canvas.create_text(400, 80, text="Choose the direction of the game", font=('Lucida Grande', 15))
        vals_list = [0, 1, 2]
        top_text = ("S->N", "SE->NW", "NE->SW")
        self.dir_choice_ovals = []
        for i in vals_list:
            self.canvas.create_text(self.x_start + 88 + i * (self.x_jump+40), self.y_top - 30, text=f"{top_text[i]}",
                                    font=('Lucida Grande', 15))
            if i == 0:
                self.oval2 = self.canvas.create_oval(self.x_start + 73 + i * (self.x_jump+40), self.y_top,
                                                     self.x_finish + 73 + (i) * (self.x_jump+40), self.y_bottom, fill="pink")
            else:
                self.oval2 = self.canvas.create_oval(self.x_start + 73 + i * (self.x_jump+40), self.y_top,
                                                     self.x_finish + 73 + (i) * (self.x_jump+40), self.y_bottom, fill="white")

            self.canvas.tag_bind(self.oval2, '<Button-1>', self.get_dir_on_press)
            self.dir_choice_ovals.append(self.oval2)
        # self.continue_button = ttk.Button(self.canvas, text = "continue").pack()
        self.continue_button = self.canvas.create_rectangle(300, 300, 500, 340, fill="pink")
        self.canvas.tag_bind(self.continue_button, '<Button-1>',
                             lambda event, x=self.choose_players_type_window: self.on_continue_click(event, x))
        self.continue_text = self.canvas.create_text(400, 320, text="Continue...", font=('Lucida Grande', 15))
        self.canvas.tag_bind(self.continue_text, '<Button-1>',
                             lambda event, x=self.choose_players_type_window: self.on_continue_click(event, x))
        """bind the arrow keys"""
        # self.bind_left = self.view.root.bind('<Left>', lambda event, x='Left': self.change_number_of_players(event, x))
        # self.bind_right = self.view.root.bind('<Right>', lambda event, x='Right': self.change_number_of_players(event, x))



    def on_continue_click(self, event, func):
        """
        :param event: the click event
        :param func: the function to be called
        calls func if the click is done in the right coordinates.
        """
        if 500 >= event.x >= 300 and 300 <= event.y <= 340:
            func()

    def choose_players_type_window(self):
        """
        creates the window in which the user will choose the names of the players and their type.
        """
        """deleting the former binds"""
        if not self.visited_colors:
            self.view.root.unbind('<Left>', self.bind_left)
            self.view.root.unbind('<Right>', self.bind_right)
        """deleting the frame and then creating a new one"""
        self.choice_box_frame.forget()
        """recreating the frame and canvas"""
        self.choice_box_frame = ttk.Frame(self.father)
        self.canvas = tkinter.Canvas(self.choice_box_frame, bg="white", height=450, width=800)
        self.choice_box_frame.pack()
        self.canvas.grid(row=1, column=0, columnspan=1)
        """the second title"""
        self.canvas.create_text(400, 80, text="Choose the name and type of the player", font=('Lucida Grande', 16))
        """creating the labels"""

        """back button creation"""
        self.back_button = self.canvas.create_rectangle(10, 10, 100, 60, fill="pink")
        self.canvas.tag_bind(self.back_button, '<Button-1>', self.back_from_players_names_window)
        self.back_text = self.canvas.create_text(55, 35, text="Back", font=('Lucida Grande', 15))
        self.canvas.tag_bind(self.back_text, '<Button-1>', self.back_from_players_names_window)

        self.view.players_list = []
        pl_list = self.view.players_list
        for i in range(self.number_of_players):
            pl_list.append(Player(i+1))
        self.name_entries = []
        self.combo_boxes = []
        values = ["human", "computer", "random"]
        for i, val in enumerate(pl_list):
            jump = (800 - 120*self.number_of_players)/(self.number_of_players+1)
            add_on_to_sides = 1 if (800 - 120*self.number_of_players)%(self.number_of_players+1) != 0 else 0
            entry1 = tk.Entry(self.view.root, font=('Lucida Grande', 12), width=13)
            entry1.insert(0, val.name)
            self.name_entries.append(entry1)
            combo_box1 = ttk.Combobox(self.view.root, font=('Lucida Grande', 12), width=11, values = values, state ="readonly")
            combo_box1.current(0)
            combo_box1.bind("<<ComboboxSelected>>", lambda event, index=i: self.selected_new_type(event, index))
            self.combo_boxes.append(combo_box1)
            self.canvas.create_window(jump+60+add_on_to_sides + (jump+120)*i, self.y_top - 50, window=entry1)
            self.canvas.create_window(jump+60+add_on_to_sides + (jump+120)*i, self.y_top, window=combo_box1)

        """this is the continuing button"""
        self.continue_button = self.canvas.create_rectangle(300, 300, 500, 340, fill="pink")
        self.canvas.tag_bind(self.continue_button, '<Button-1>', lambda event, x = self.select_colors_window : self.on_continue_click(event,x))
        self.continue_text = self.canvas.create_text(400, 320, text="Continue...", font=('Lucida Grande', 15))
        self.canvas.tag_bind(self.continue_text, '<Button-1>', lambda event, x = self.select_colors_window : self.on_continue_click(event,x))

    def selected_new_type(self, event, index):
        """
        :param event: the changing combobox value event
        :param index: the index of the changed combobox
        changes the player's type and name accordingly.
        """
        new_type = 0 if self.combo_boxes[index].get() == "human" else 1 if self.combo_boxes[index].get() == "computer" else 2
        self.view.players_list[index].type = new_type
        if self.name_entries[index].get() == f"regular-player{index+1}" and new_type == 1:
            self.view.players_list[index].name = f"computer-player{index+1}"
            self.name_entries[index].delete(0, END)
            self.name_entries[index].insert(0, self.view.players_list[index].name)
        elif self.name_entries[index].get() == f"regular-player{index+1}" and new_type == 2:
            self.view.players_list[index].name = f"random-player{index + 1}"
            self.name_entries[index].delete(0, END)
            self.name_entries[index].insert(0, self.view.players_list[index].name)
        elif self.name_entries[index].get() == f"computer-player{index+1}" and new_type == 0:
            self.view.players_list[index].name = f"regular-player{index+1}"
            self.name_entries[index].delete(0, END)
            self.name_entries[index].insert(0, self.view.players_list[index].name)
        elif self.name_entries[index].get() == f"computer-player{index+1}" and new_type == 2:
            self.view.players_list[index].name = f"random-player{index+1}"
            self.name_entries[index].delete(0, END)
            self.name_entries[index].insert(0, self.view.players_list[index].name)
        elif self.name_entries[index].get() == f"random-player{index+1}" and new_type == 0:
            self.view.players_list[index].name = f"regular-player{index+1}"
            self.name_entries[index].delete(0, END)
            self.name_entries[index].insert(0, self.view.players_list[index].name)
        elif self.name_entries[index].get() == f"random-player{index+1}" and new_type == 1:
            self.view.players_list[index].name = f"computer-player{index+1}"
            self.name_entries[index].delete(0, END)
            self.name_entries[index].insert(0, self.view.players_list[index].name)

    def select_colors_window(self):
        """
        creates the window in which the user can choose the colors for each player
        """
        if not self.update_players():
            self.canvas.create_text(400, 370, text="please make sure the names are not empty or just spaces",
                                    font=('Lucida Grande', 12), fill="red")

            return
        self.visited_colors = True
        self.choice_box_frame.forget()
        self.choice_box_frame = ttk.Frame(self.father)
        self.canvas = tkinter.Canvas(self.choice_box_frame, bg="white", height=450, width=800)
        self.choice_box_frame.pack()
        self.canvas.grid(row=1, column=0, columnspan=1)
        self.canvas.create_text(400, 80, text="Choose the color for each player", font=('Lucida Grande', 15))

        """back button creation"""
        self.back_button = self.canvas.create_rectangle(10, 10, 100, 60, fill="pink")
        self.canvas.tag_bind(self.back_button, '<Button-1>', self.back_from_players_colors_window)
        self.back_text = self.canvas.create_text(55, 35, text="Back", font=('Lucida Grande', 15))
        self.canvas.tag_bind(self.back_text, '<Button-1>', self.back_from_players_colors_window)
        # self.view.root.option_add("*TCombobox*Listbox*Background", 'green')
        self.colors_combo_boxes = []
        self.color_values = ["blue", "red", "green", "black", "cyan", "magenta", "yellow"]
        pl_list = self.view.players_list
        for i, val in enumerate(pl_list):
            jump = (800 - 120 * self.number_of_players) / (self.number_of_players + 1)
            add_on_to_sides = 1 if (800 - 120 * self.number_of_players) % (self.number_of_players + 1) != 0 else 0
            self.style.configure(f"C{i}.TCombobox", fieldbackground="white", background="white")
            combo_box1 = ttk.Combobox(self.view.root, font=('Lucida Grande', 12), width=11, values=self.color_values, state="readonly", style=f"C{i}.TCombobox")
            self.colors_combo_boxes.append(combo_box1)
            combo_box1.current(i)
            combo_box1.bind("<<ComboboxSelected>>", lambda event, index=i: self.change_color_list(event, index))
            self.canvas.create_text(jump + 60 + add_on_to_sides + (jump + 120) * i, self.y_top - 50, text=f"{val.name}" ,font=('Lucida Grande', 12))
            self.canvas.create_window(jump + 60 + add_on_to_sides + (jump + 120) * i, self.y_top, window=combo_box1)
        for i, val in enumerate(self.colors_combo_boxes):
            self.change_color_list(None, i)

        """this is the start game_button"""
        self.start_game_button = self.canvas.create_rectangle(300, 300, 500, 340, fill="pink")
        self.canvas.tag_bind(self.start_game_button, '<Button-1>', self.start_game)
        self.start_game_text = self.canvas.create_text(400, 320, text="Start Game!!!", font=('Lucida Grande', 15))
        self.canvas.tag_bind(self.start_game_text, '<Button-1>', self.start_game)

    def update_players(self):
        """
        updates the players_list of the view, with the new names and types.
        """
        for i, val in enumerate(self.view.players_list):
            val.name = self.name_entries[i].get()
            if self.combo_boxes[i].get() == "human":
                val.type = 0
            elif self.combo_boxes[i].get() == "computer":
                val.type = 1
            elif self.combo_boxes[i].get() == "random":
                val.type = 2
            if len(val.name) == 0 or val.name.isspace():
                return False
        return True

    def change_color_list(self, event, index):
        """
        :param event: the changing combobox value event
        :param index: the index of the combobox
        changes the other comboboxes (all the ones that are not the index combobox) so that two players wont be able
        to choose the same color
        """
        self.style.configure(f"C{index}.TCombobox",  fieldbackground=f"{self.colors_combo_boxes[index].get()}", background=f"{self.colors_combo_boxes[index].get()}")
        if self.view.players_list[index].color != self.colors_combo_boxes[index].get():
            to_remove_val = self.colors_combo_boxes[index].get()
            to_append_val = self.view.players_list[index].color
            for i, val in enumerate(self.colors_combo_boxes):
                if i != index:
                    values_list = list(val["values"])
                    if to_append_val is not None:
                        values_list.append(to_append_val)
                    values_list.remove(to_remove_val)
                    val["values"] = values_list
            self.view.players_list[index].color = self.colors_combo_boxes[index].get()

    def start_game(self, event):
        """
        :param event: click event
        saves the chosen colors to the players_list in the view and starts the game
        """
        for i, val in enumerate(self.view.players_list):
            if val.color is None:
                self.canvas.create_text(400, 370, text="please choose a color for all the players", font=('Lucida Grande', 12), fill="red")
                return
            val.color = self.colors_combo_boxes[i].get()
        self.view.start_game()

    def back_from_players_names_window(self, event):
        """
        :param event: click event
        forgets the current frame and calls the choose_number_of_players_window() function
        """
        self.choice_box_frame.forget()
        self.choose_number_of_players_window()

    def back_from_players_colors_window(self, event):
        """
        :param event: click event
        calls the choose_players_type_window() function
        """
        self.choose_players_type_window()








