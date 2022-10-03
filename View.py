from tkinter import *
from tkinter import ttk
from Controller import Controller
from View_Board import View_Board
import tkinter.font as tkFont
import tkinter
from Opening_Window import Opening_Window
from Player import Player
from PIL import ImageTk, Image


# from tkinter import Image

class View:
    def __init__(self):
        self.root = Tk()
        # width = self.root.winfo_screenwidth()
        # height = self.root.winfo_screenheight()
        # self.root.geometry("%dx%d" % (width, height))
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack()
        # self.build_board_screen(self.main_frame, 6)
        # self.shadow = Frame(self.root, width = 200, height = 200, bg="#000000")
        # self.shadow.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        # self.view_board.on_win()
        self.players_list = []
        self.game_dir = 0
        Opening_Window(self.main_frame, self)
        self.instruction_open = False
        # Instructions(self.main_frame)
        self.root.mainloop()

    def start_game(self):
        """
        forgets the current main frame and creates a new one, consisting the game board
        """
        self.main_frame.forget()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack()
        self.color_list = [i.color for i in self.players_list]
        self.players_names = [i.name for i in self.players_list]
        self.players_type_list = [i.type for i in self.players_list]
        self.build_board_screen(self.main_frame, len(self.players_list))
        self.key_board_binding()
        self.view_board.controller.num_of_games -= 1
        self.view_board.computer_move()

    def key_board_binding(self):
        """
        creation of the keyboard and mouse bindings, so that the user can end his turn with the enter key or right click
        and move along the board with the keyboard
        """
        self.root.bind('<w>', lambda event, x='R-Up': self.view_board.letters_key_click(event, x))
        self.root.bind('<x>', lambda event, x='R-Down': self.view_board.letters_key_click(event, x))
        self.root.bind('<d>', lambda event, x='Q-Up': self.view_board.letters_key_click(event, x))
        self.root.bind('<a>', lambda event, x='Q-Down': self.view_board.letters_key_click(event, x))
        self.root.bind('<e>', lambda event, x='S-Up': self.view_board.letters_key_click(event, x))
        self.root.bind('<z>', lambda event, x='S-Down': self.view_board.letters_key_click(event, x))
        self.root.bind('<Key>', self.end_turn)
        self.root.bind('<Button-3>', self.end_turn)

    def end_turn(self, event):
        """ends the current player's turn, only if he already made a jump, and thus have the option to choose if to
        end his turn or continue"""
        if len(self.view_board.controller.last_steps) > 0:
            self.view_board.delete_options_on_board(self.view_board.chosen_pit)
            self.view_board.canvas.itemconfig(
                self.view_board.pit_rows[self.view_board.chosen_pit[0]][self.view_board.chosen_pit[1]], width="1",
                outline="black")  # change color
            self.on_finish_turn_visual()
            self.view_board.computer_move()

    def build_board_screen(self, father, num_of_players):
        """
        :param father: the frame in which all the widgets that are created in this function will be in.
        :param num_of_players: the chosen number of players --> will be passed to the view_board
        """
        self.top_frame = ttk.Frame(father)
        self.top_frame = ttk.Frame(father)
        fontStyle = tkFont.Font(family="Lucida Grande", size=(40 // num_of_players))
        self.title_label = ttk.Label(self.top_frame, text=" VS ".join(self.players_names[:]), font=fontStyle,
                                     justify="center", anchor="center")
        self.leaders_board_title = ttk.Label(self.top_frame, text="The leader is.....", font=fontStyle,
                                             justify="center", anchor="center")
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TButton', background='#30D7D7', foreground='black', width=20, borderwidth=1, focusthickness=2,
                        focuscolor='none', font=('Lucida Grande', 12))
        style.map('TButton', background=[('active', '#30D7D7')])
        self.instructions_button = ttk.Button(self.top_frame, text="Instructions", command=self.instruction_click)
        self.leaders_board_button = ttk.Button(self.top_frame, text="Leaders Board")
        self.reset_game_button = ttk.Button(self.top_frame, text="Reset Game", command=self.reset_game_view)
        self.return_to_main_button = ttk.Button(self.top_frame, text="Return To Main", command=self.return_to_main)

        self.top_frame.pack()
        self.title_label.grid(row=0, column=0, columnspan=4, sticky='nesw')
        self.leaders_board_title.grid(row=1, column=0, columnspan=4)
        self.instructions_button.grid(row=2, column=0)
        self.leaders_board_button.grid(row=2, column=1)
        self.reset_game_button.grid(row=2, column=2)
        self.return_to_main_button.grid(row=2, column=3)

        self.game_frame = ttk.Frame(father)
        self.view_board = View_Board(self.game_frame, self, num_of_players, 1, self.game_dir)
        fontStyle = tkFont.Font(family="Lucida Grande", size=13)
        # color = self.color_list[self.view_board.controller.list_of_players_numbers.index(self.view_board.controller.whos_turn)]
        color = "white"
        self.whos_turn_label = ttk.Label(self.game_frame,
                                         text=f"It is\n {self.players_names[self.view_board.controller.list_of_players_numbers.index(self.view_board.controller.whos_turn)]}'s\n Turn:)",
                                         font=fontStyle, justify="center", anchor="center", width=15, background=color,
                                         wraplength=125)

        self.game_frame.pack()
        self.game_frame.columnconfigure(0, weight=4)
        self.game_frame.columnconfigure(1, weight=1)

        self.whos_turn_label.grid(row=0, column=1, sticky='nesw')
        # self.view_board.on_win()

    def on_finish_turn_visual(self):
        """
        changes the whos_turn_label on the end of a turn
        """
        self.view_board.controller.end_turn()
        chosen_oval = self.view_board.pit_rows[self.view_board.chosen_pit[0]][self.view_board.chosen_pit[1]]
        self.view_board.canvas.itemconfig(chosen_oval, width="1", outline="black")  # change color
        self.view_board.chosen_pit = [8, 8]
        self.whos_turn_label[
            'text'] = f"It is\n {self.players_names[self.view_board.controller.list_of_players_numbers.index(self.view_board.controller.whos_turn)]}'s\n Turn:)"
        # color = self.color_list[self.view_board.controller.list_of_players_numbers.index(self.view_board.controller.whos_turn)]
        color = "white"
        self.whos_turn_label['background'] = color

    def on_win_visual(self, whos_turn):
        """
        :param whos_turn: the players who's turn it is
        creates the text on the board whenever a player wins.
        """
        winners_name = self.players_names[self.view_board.controller.list_of_players_numbers.index(whos_turn)]
        self.view_board.win_text1 = self.view_board.canvas.create_text(300, 130,
                                                                       text=f"THE WINNER IS {winners_name}!!!",
                                                                       font=tkFont.Font(family="Lucida Grande", size=18,
                                                                                        weight='bold', underline='1'),
                                                                       fill="white")
        self.view_board.win_text2 = self.view_board.canvas.create_text(300, 180,
                                                                       text="To restart the game press the reset game button",
                                                                       font=tkFont.Font(family="Lucida Grande", size=13,
                                                                                        weight='bold'), fill='white')
        self.view_board.win_text3 = self.view_board.canvas.create_text(300, 200,
                                                                       text="To start a new game press the return to main button",
                                                                       font=tkFont.Font(family="Lucida Grande", size=13,
                                                                                        weight='bold'), fill='white')

    def reset_game_view(self):
        """
        creates a new board.
        """
        self.view_board.reset_game()
        self.whos_turn_label[
            'text'] = f"It is\n {self.players_names[self.view_board.controller.list_of_players_numbers.index(self.view_board.controller.whos_turn)]}'s\n Turn:)"
        # color = self.color_list[self.view_board.controller.list_of_players_numbers.index(self.view_board.controller.whos_turn)]
        color = "white"
        self.whos_turn_label['background'] = color
        # start_c, finish_c = self.view_board.controller.get_next_move()
        # if start_c is not None:
        #     self.view_board.computer_ab_move(start_c, finish_c)
        self.view_board.computer_move()

    def return_to_main(self):
        """
        forgets the current frame and create the opening window
        """
        self.main_frame.forget()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack()
        self.open_win = Opening_Window(self.main_frame, self)

    def create_instructions(self):
        self.back_ground = self.view_board.canvas.create_rectangle(0, 0, 600, 400, fill="black", tag="rec1")
        self.img = Image.open("instrutionsimg.png")
        self.img = self.img.resize((600, 500), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.rec_img = self.view_board.canvas.create_image(0, 0, image=self.img, anchor='nw', tag="img1")
        self.instruction_open = True

    def delete_instructions(self):
        self.view_board.canvas.delete("rec1")
        self.view_board.canvas.delete("img1")
        self.instruction_open = False

    def instruction_click(self):
        if self.instruction_open:
            self.delete_instructions()
        else:
            self.create_instructions()
