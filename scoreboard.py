# ----------------------------------------------------- Imports --------------------------------------------------------
from tkinter import *
from tkinter import ttk, messagebox

from pymongo.synchronous.database import Database

from image_resizer import ImageResizer
from PIL import Image, ImageTk
import random
from database import CricketDatabase
# ------------------------------------------------ Global Variables ----------------------------------------------------
width = 800
height = 600

main_bg = "#393939"
button_bg = "#2c2c2c"
gray_out_bg = "#cdcdcd"
main_text_color = "#35b690"

team_colors = ["#8B0A1A","#00BFFF","#FFC400","#8F9779","#C51077","#F7DC6F","#2E865F","#A291FF","#FF99CC","#34A85A"]
default_color1 = "#8B0A1A"
default_color2 = "#14FFA1"

form_bg = "#393939"
form_secondary = "#1c1c1c"
# --------------------------------------------------- Main Class -------------------------------------------------------
class Scoreboarde(Toplevel):
    def __init__(self, main_window):
        super().__init__()

        self.title("My Own Cricket Simulator")
        self.minsize(width,height)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.config(bg=main_bg)

        self.main_window = main_window

        self.protocol("WM_DELETE_WINDOW", self.on_click_x)

        self.match_details = {
            "teamA_name": None,
            "teamA_color": None,
            "teamA_runs": None,
            "teamA_wickets": None,
            "teamA_balls": None,
            "teamB_name": None,
            "teamB_color": None,
            "teamB_runs": None,
            "teamB_wickets": None,
            "teamB_balls": None,
            "match_name": None,
            "match_overs": None
        }

        self.current_innnings = None
        self.innings_number = 1
        self.batting_team_name = None
        self.bowling_team_name = None

        self.inning_runs = 0
        self.inning_wickets = 0
        self.inning_balls = 0
        self.innings_overs = 0
        self.total_balls = 0
        self.target = 0

        self.create_widgets()

# ---------------------------------------------------- Methods ---------------------------------------------------------
# ------------------------------------------------ Create Widgets ------------------------------------------------------
    def create_widgets(self):

        # Match Type
        self.match_type_frame = Frame(self, bg=main_bg, width=width, height=75, relief=SUNKEN, border=2)
        self.match_type_frame.place(relx=0, rely=0)
        self.match_type_label = Label(self.match_type_frame, text="MOCS", font=("arial", 40, "bold"),
                                      justify=CENTER, bg=main_bg, fg=main_text_color)
        self.match_type_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Scoreboards
        self.scoreboards_frame = Frame(self, bg=main_bg, width=width, height=200, relief=SUNKEN,
                                      border=2)
        self.scoreboards_frame.place(relx=0, rely=0.13)

        # Team A
        self.teamA_frame = Frame(self.scoreboards_frame, bg=default_color1, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.teamA_frame.place(relx=0, rely=0)

        self.teamA_name_label = Label(self.teamA_frame, width=10, height=1, justify=CENTER, bg='white',
                                      font=("arial", 28, "bold"))
        self.teamA_name_label.place(relx=0.1, rely=0.25, anchor=W)

        self.teamA_scoreboard_label = Label(self.teamA_frame, text="0-0", width=5, height=1, font=("arial", 20, "bold"),
                                      justify=CENTER, bg='white')
        self.teamA_scoreboard_label.place(relx=0.1, rely=0.55, anchor=W)

        self.teamA_overs_label = Label(self.teamA_frame, text=f"0.0 ({self.innings_overs})", width=8, height=1,
                                       font=("arial", 12, "bold"), justify=CENTER, bg='white')
        self.teamA_overs_label.place(relx=0.1, rely=0.75, anchor=W)

        # Team B
        self.teamB_frame = Frame(self.scoreboards_frame, bg=default_color2, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.teamB_frame.place(relx=0.5, rely=0)

        self.teamB_name_label = Label(self.teamB_frame, width=10, height=1, justify=CENTER, bg='white',
                                      font=("arial", 28, "bold"))
        self.teamB_name_label.place(relx=0.9, rely=0.25, anchor=E)
        self.teamB_scoreboard_label = Label(self.teamB_frame, text="0-0", width=5, height=1, font=("arial", 20, "bold"),
                                      justify=CENTER, bg='white')
        self.teamB_scoreboard_label.place(relx=0.9, rely=0.55, anchor=E)

        self.teamB_overs_label = Label(self.teamB_frame, text=f"0.0 ({self.innings_overs})", width=8, height=1,
                                       font=("arial", 12, "bold"), justify=CENTER, bg='white')
        self.teamB_overs_label.place(relx=0.9, rely=0.75, anchor=E)

        self.main_play_button = Button(self, text="Start", width=15, bg="#2c2c2c", fg='white',
                                    command=lambda: self.open_details_form("match_details"),font=("arial", 12, "bold"))
        self.main_play_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Versus Label

        self.versus_v_label = Label(self, text="V", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=default_color1, fg="white")
        self.versus_v_label.place(relx=0.472, rely=0.2, anchor=CENTER)

        self.versus_s_label = Label(self, text="S", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=default_color2, fg="white")
        self.versus_s_label.place(relx=0.528, rely=0.25, anchor=CENTER)

# ------------------------------------------------ Further Widgets -----------------------------------------------------
    def widgets_continued(self, toss_winner, bat_ball_selection):
        self.toss_winner = toss_winner
        self.bat_ball_selection = bat_ball_selection

        # Score
        self.score_label = Label(self, width=5, height=1, font=("arial", 35, "bold"), justify=CENTER)
        self.score_label.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.main_play_button.config(text="Play!!", command=self.checker)
        self.main_play_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.score_timeline_label = Label(self, text="Timeline", bg='white')
        self.score_timeline_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.score_timeline = Text(self, width=50, height=1, font=("arial", 14, "bold"), state=DISABLED)
        self.score_timeline.place(relx=0.5, rely=0.95, anchor=CENTER)

        if ((toss_winner == self.match_details['teamA_name'] and bat_ball_selection == "bat") or
                (toss_winner == self.match_details['teamB_name'] and bat_ball_selection == "bowl")):
            self.current_innings = "teamA"
            self.batting_team_name = self.match_details['teamA_name']
            self.bowling_team_name = self.match_details['teamB_name']
            bat_x = 0.4
            ball_x = 0.6
        else:
            self.current_innings = "teamB"
            self.batting_team_name = self.match_details['teamB_name']
            self.bowling_team_name = self.match_details['teamA_name']
            bat_x = 0.6
            ball_x = 0.4

        # Icons
        self.bat_image = ImageResizer("assets/images/bat.png", 40)
        self.bat_icon_label = Label(self, image=self.bat_image.image, bg='white')
        self.bat_icon_label.place(relx=bat_x, rely=0.22, anchor=CENTER)

        self.ball_image = ImageResizer("assets/images/ball.png", 40)
        self.ball_icon_label = Label(self, image=self.ball_image.image, bg='white')
        self.ball_icon_label.place(relx=ball_x, rely=0.22, anchor=CENTER)

# -------------------------------------------------- Match Status Checker -------------------------------------------------------
    def checker(self):
        if self.innings_number == 1:
            if (self.inning_balls < self.total_balls) and (self.inning_wickets < 10): # 1st Innings
                self.scorer()
            else:
                self.innings_number = 2

                self.batting_team_score = self.inning_runs
                self.batting_team_wickets = self.inning_wickets

                messagebox.showinfo("End of 1st Innings",
                        f"{self.batting_team_name} has scored {self.inning_runs} for {self.inning_wickets}.",
                                    parent=self)

                if self.current_innings == "teamA":
                    self.current_innings = "teamB"
                    self.batting_team_name = self.match_details['teamB_name']
                    self.bowling_team_name = self.match_details['teamA_name']
                    self.match_details["teamA_runs"] = self.inning_runs
                    self.match_details["teamA_wickets"] = self.inning_wickets
                    self.match_details["teamA_balls"] = self.inning_balls
                    bat_x = 0.6
                    ball_x = 0.4
                else:
                    bat_x = 0.4
                    ball_x = 0.6
                    self.current_innings = "teamA"
                    self.batting_team_name = self.match_details['teamA_name']
                    self.bowling_team_name = self.match_details['teamB_name']
                    self.match_details["teamB_runs"] = self.inning_runs
                    self.match_details["teamB_wickets"] = self.inning_wickets
                    self.match_details["teamB_balls"] = self.inning_balls

                # Icons
                self.bat_icon_label.place(relx=bat_x, rely=0.22, anchor=CENTER)
                self.ball_icon_label.place(relx=ball_x, rely=0.22, anchor=CENTER)

                self.bowling_team_score = self.batting_team_score
                self.bowling_team_wickets = self.batting_team_wickets

                self.target = self.inning_runs + 1
                messagebox.showinfo("Target",
                                    f"Target for {self.batting_team_name} is {self.target}", parent=self)

                self.inning_runs = 0
                self.inning_wickets = 0
                self.inning_balls = 0

        else: # 2nd Innings
            if (self.inning_balls < self.total_balls) and (self.inning_wickets < 10) and (self.inning_runs < self.target):
                self.scorer()
            else:
                self.batting_team_score = self.inning_runs
                self.batting_team_wickets = self.inning_wickets

                messagebox.showinfo("End of 2nd Innings",
                            f"{self.batting_team_name} has scored {self.inning_runs} for {self.inning_wickets}",
                                    parent=self)

                self.main_play_button.config(state=DISABLED)
                self.teamB_score = self.inning_runs

                if self.current_innings == "teamA":
                    self.match_details["teamA_runs"] = self.inning_runs
                    self.match_details["teamA_wickets"] = self.inning_wickets
                    self.match_details["teamA_balls"] = self.inning_balls
                else:
                    self.match_details["teamB_runs"] = self.inning_runs
                    self.match_details["teamB_wickets"] = self.inning_wickets
                    self.match_details["teamB_balls"] = self.inning_balls

                if self.bowling_team_score > self.batting_team_score:
                    runs_win = self.bowling_team_score - self.batting_team_score
                    messagebox.showinfo("End of the Match",
                                    f"{self.bowling_team_name} has won by {runs_win} runs.", parent=self)
                elif self.bowling_team_score < self.batting_team_score:
                    wickets_win = 10 - self.batting_team_wickets
                    messagebox.showinfo("End of the Match",
                                    f"{self.batting_team_name} has won by {wickets_win} wickets.", parent=self)
                else:
                    messagebox.showinfo("End of the Match", f"Scores are Level. Match Tied!!", parent=self)

                score_dict = {
                    "match_name": self.match_details["match_name"],
                    "match_overs": self.match_details["match_overs"],
                    "toss": self.toss_winner,
                    "choice": self.bat_ball_selection,
                    "teamA_name": self.match_details["teamA_name"],
                    "teamA_color": self.match_details["teamA_color"],
                    "teamA_runs": self.match_details["teamA_runs"],
                    "teamA_wickets": self.match_details["teamA_wickets"],
                    "teamA_balls": self.match_details["teamA_balls"],
                    "teamB_name": self.match_details["teamB_name"],
                    "teamB_color": self.match_details["teamB_color"],
                    "teamB_runs": self.match_details["teamB_runs"],
                    "teamB_wickets": self.match_details["teamB_wickets"],
                    "teamB_balls": self.match_details["teamB_balls"]
                }

                cricketDatabase = CricketDatabase()

                try:
                    cricketDatabase.connect()
                    database_rec = cricketDatabase.db_column.insert_one(score_dict)
                except Exception as e:
                    print("Database Error:", e)
                else:
                    cricketDatabase.close()
                    messagebox.showinfo("Match Saved", "Match saved to the database. Thanks for Playing!!",
                                        parent=self)

# ---------------------------------------------------- Scorer ----------------------------------------------------------
    def scorer(self):
            self.inning_balls += 1
            overs = f"{int(self.inning_balls/6)}.{(self.inning_balls % 6)}"
            ball_score = random.randint(0,6)
            if ball_score == 5:
                self.inning_wickets += 1
                ball_score = "W"
            else:
                self.inning_runs += ball_score

            self.score_label.config(text=ball_score)

            label_name = f"{self.current_innings}_scoreboard_label"
            label = getattr(self, label_name)
            label.config(text=f"{self.inning_runs}-{self.inning_wickets}")

            label_name = f"{self.current_innings}_overs_label"
            label = getattr(self, label_name)
            label.config(text=f"{overs}")

            self.score_timeline.config(state=NORMAL)
            self.score_timeline.insert(END, f"{ball_score} ")
            self.score_timeline.config(state=DISABLED)

# ------------------------------------------------- On Clicking X ------------------------------------------------------
    def on_click_x(self):
        confirm_x = messagebox.askyesno("Quit?", "Are you sure you want to quit?", parent=self)
        if confirm_x:
            self.grab_release()
            self.destroy()
            self.main_window.windows.deiconify()

# -------------------------------------------- Open Match Details Form -------------------------------------------------
    def open_details_form(self, mode):
        if mode == "match_details":
            form = AddDetailForms(self)
        else:
            form = CoinTossForm(self, self.match_details)

# ---------------------------------------------- Update Match Details --------------------------------------------------
    def update_details(self):
        # Match Title
        self.match_type_label.config(text=self.match_details["match_name"])

        # Team A
        self.teamA_frame.config(bg=self.match_details["teamA_color"])
        self.teamA_name_label.config(text=self.match_details["teamA_name"])

        # Team B
        self.teamB_frame.config(bg=self.match_details["teamB_color"])
        self.teamB_name_label.config(text=self.match_details["teamB_name"])

        self.versus_v_label.config(bg=self.match_details["teamA_color"])
        self.versus_s_label.config(bg=self.match_details["teamB_color"])

        self.total_balls = self.match_details["match_overs"] * 6

        self.main_play_button.config(text="Coin Toss", command=lambda: self.open_details_form("coin_toss"))

# ----------------------------------------------- Match Details Form ---------------------------------------------------
class AddDetailForms(Toplevel):
    def __init__(self, main_window):
        super().__init__()

        # Form Window Settings
        x = main_window.winfo_x()
        y = main_window.winfo_y()
        self.geometry(f"800x300+{x}+{y}")

        self.title("Match Details")
        self.resizable(False, False)
        self.config(bg='white')
        self.transient(main_window)
        self.grab_set()
        self.focus_set()

        self.teamA_color = None
        self.teamB_color = None

        self.main_window = main_window

        fonter = ('Helvetica', 12, 'normal')

        # Scoreboards
        self.scoreboards_frame = Frame(self, bg=form_bg, width=width, height=200, relief=SUNKEN,
                                       border=2)
        self.scoreboards_frame.place(relx=0, rely=0)

        # Team A
        self.team1_frame = Frame(self.scoreboards_frame, bg="#1c1c1c", width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.team1_frame.place(relx=0, rely=0)

        self.team1_name_label = Label(self.team1_frame, text=" Enter Team A's Name", width=20, height=1,
                                      font=("arial", 14, "bold"), justify=CENTER, bg='white')
        self.team1_name_label.place(relx=0.1, rely=0.2, anchor=W)

        self.team1_name_entry = Entry(self.team1_frame, width=20, font=("arial", 20, "bold"), justify=LEFT)
        self.team1_name_entry.place(relx=0.1, rely=0.4, anchor=W)

        self.team1_colors_label = Label(self.team1_frame, text="Choose Team A's color", width=20, height=1,
                                       font=("arial", 14, "bold"), justify=CENTER, bg='white')
        self.team1_colors_label.place(relx=0.1, rely=0.6, anchor=W)

        x = 0.2
        for colors in team_colors:
            self.team_color_buttons = Button(self.team1_frame, width=1, bg=colors,
                                             command=lambda c=colors: self.chosen_color(c, "teamA"))
            self.team_color_buttons.place(relx=x, rely=0.8, anchor=CENTER)
            x += 0.05

        # Team B
        self.team2_frame = Frame(self.scoreboards_frame, bg="#1c1c1c", width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.team2_frame.place(relx=0.5, rely=0)

        self.team2_name_label = Label(self.team2_frame, text="Enter Team B's Name", width=20, height=1,
                                      font=("arial", 14, "bold"), justify=CENTER, bg='white')
        self.team2_name_label.place(relx=0.9, rely=0.2, anchor=E)

        self.team2_name_entry = Entry(self.team2_frame, width=20, font=("arial", 20, "bold"), justify=RIGHT)
        self.team2_name_entry.place(relx=0.9, rely=0.4, anchor=E)

        self.team2_colors_label = Label(self.team2_frame, text="Choose Team B's color", width=20, height=1,
                                       font=("arial", 14, "bold"), justify=CENTER, bg='white')
        self.team2_colors_label.place(relx=0.9, rely=0.6, anchor=E)

        x = 0.8
        for colors in team_colors:
            self.team_color_buttons = Button(self.team2_frame, width=1, bg=colors,
                                             command=lambda c=colors: self.chosen_color(c, "teamB"))
            self.team_color_buttons.place(relx=x, rely=0.8, anchor=CENTER)
            x -= 0.05

        self.over_selection_label = Label(self, text="Select No. of Overs: ", font=('Helvetica', 12, 'normal'),
                                          bg='white', fg='black')
        self.over_selection_label.place(relx=0.4, rely=0.75, anchor=CENTER)
        self.options = {"1-O": 1, "Duel 2": 2, "3ple Threat": 3, "4 Play": 4, "F5": 5, "6 Slam": 6, "Lucky 7": 7,
                   "High Oc8ane": 8, "9 Thrive": 9, "Ten10": 10}

        self.clicked = StringVar()
        keys_list = list(self.options.keys())

        self.over_options = ttk.OptionMenu(self, self.clicked, keys_list[4], *self.options.keys())
        self.over_options.place(relx=0.52, rely=0.75, anchor=W)

        self.clicked.set(keys_list[4])

        self.ok_button = Button(self, text="OK", font=fonter, bg=form_secondary, fg='white',
                                command=self.enter_match_details, width=15)
        self.ok_button.place(relx=0.5, rely=0.9, anchor=CENTER)

# -------------------------------------------------- Match Details -----------------------------------------------------
    def enter_match_details(self):
        self.match_overs = self.options[self.clicked.get()]
        self.match_name = self.clicked.get()
        teamA_name = self.team1_name_entry.get().upper()
        teamB_name = self.team2_name_entry.get().upper()

        if not teamA_name and not self.teamA_color:
            messagebox.showerror("No Team A Name / Color", "Enter Team A Name and Select a color!!")
            return
        if not teamB_name and not self.teamB_color:
            messagebox.showerror("No Team B Name", "Enter Team B Name and Select a color!!!!")
            return
        if (teamA_name == teamB_name) or (self.teamA_color == self.teamB_color):
            messagebox.showerror("Same Team Color", "Select Different Names / Colours for Both Teams")
            return
        if teamA_name and self.teamA_color and teamB_name and self.teamB_color and self.match_overs:
            self.main_window.match_details = {
                "teamA_name": teamA_name,
                "teamA_color": self.teamA_color,
                "teamB_name": teamB_name,
                "teamB_color": self.teamB_color,
                "match_name": self.match_name,
                "match_overs": self.match_overs
            }

            self.destroy()
            self.main_window.update_details()

# ---------------------------------------------------- Colors ----------------------------------------------------------
    def chosen_color(self, color, teame):
        if teame == "teamA":
            self.teamA_color = color
            self.team1_name_entry. config(bg=color, fg='white')
        else:
            self.teamB_color = color
            self.team2_name_entry.config(bg=color, fg='white')

# ------------------------------------------------- Coin Toss Form -----------------------------------------------------
class CoinTossForm(Toplevel):
    def __init__(self, main_window, match_details):
        super().__init__()

        # Form Window Settings
        x = main_window.winfo_x()
        y = main_window.winfo_y()
        self.geometry(f"300x200+{x}+{y}")
        self.title("Coin Toss")
        self.resizable(False, False)
        self.config(bg='white')
        self.transient(main_window)
        self.grab_set()
        self.focus_set()

        self.teamA_name = match_details["teamA_name"]
        self.teamA_color = match_details["teamA_color"]
        self.teamB_name = match_details["teamB_name"]
        self.teamB_color = match_details["teamB_color"]

        self.main_window = main_window

        self.protocol("WM_DELETE_WINDOW", self.do_nothing)

        fonter = ('Helvetica', 12, 'normal')

        # Scoreboards
        self.scoreboards_frame = Frame(self, bg="white", width=300, height=200, relief=SUNKEN,
                                       border=2)
        self.scoreboards_frame.place(relx=0, rely=0.02)

        # Toss
        self.toss_frame = Frame(self.scoreboards_frame, bg="white", width=300, height=200,
                                 relief=SUNKEN, border=2)
        self.toss_frame.place(relx=0, rely=0)

        self.toss_tocall_label = Label(self.toss_frame, text=f"Coin Toss\n\n{self.teamB_name} to call",
                                      font=("arial", 14, "bold"), bg="white", justify=CENTER)
        self.toss_tocall_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.head_image = ImageResizer("assets/images/head.png", 70)
        self.tail_image = ImageResizer("assets/images/tail.png", 70)
        self.head_button = Button(self, image=self.head_image.image, bg='white', activebackground='white',
                                  command=lambda:self.coin_toss_animation(0))
        self.head_button.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.tail_button = Button(self, image=self.tail_image.image, bg='white', activebackground='white',
                                  command=lambda:self.coin_toss_animation(1))
        self.tail_button.place(relx=0.75, rely=0.7, anchor=CENTER)

        self.mainloop()

# -------------------------------------------------- Coin Tossing ------------------------------------------------------
    def toss_coin(self, coin_side_selection):

        self.toss_tocall_label.destroy()
        self.toss_tocall_label = Label(self.toss_frame, font=("arial", 14, "bold"), bg="white", justify=CENTER)
        self.toss_tocall_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        coin_toss = random.randint(0, 1)

        if coin_toss == 0:
            toss_result = "Heads"
        else:
            toss_result = "Tails"

        if coin_side_selection == coin_toss:
            toss_winner = self.teamB_name
        else:
            toss_winner = self.teamA_name
        self.toss_tocall_label.config(text=f"It's {toss_result}!!\n {toss_winner} wins the toss!!")

        self.bat_image = ImageResizer("assets/images/bat.png", 70)
        self.bat_button = Button(self, image=self.bat_image.image, bg='white', activebackground='white',
                                  command=lambda: self.choose_to_bat_ball(toss_winner, "bat"))
        self.bat_button.place(relx=0.25, rely=0.7, anchor=CENTER)

        self.ball_image = ImageResizer("assets/images/ball.png", 70)
        self.ball_button = Button(self, image=self.ball_image.image, bg='white', activebackground='white',
                                  command=lambda: self.choose_to_bat_ball(toss_winner, "bowl"))
        self.ball_button.place(relx=0.75, rely=0.7, anchor=CENTER)

# ------------------------------------------------ Bat/Field Choice ----------------------------------------------------
    def choose_to_bat_ball(self, toss_winner, bat_ball_selection):
        self.destroy()
        self.main_window.widgets_continued(toss_winner, bat_ball_selection)

# ----------------------------------------------- Coin Toss Animation --------------------------------------------------
    def coin_toss_animation(self, coin_side_selection):
        self.head_button.destroy()
        self.tail_button.destroy()

        gif = Image.open('assets/images/coinToss.gif')
        frames = []
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.copy()
            frames.append(ImageTk.PhotoImage(frame))
        self.toss_tocall_label.place_configure(relx=0.5, rely=0.5, anchor=CENTER)
        self.toss_tocall_label.config(image=frames[0])

        def animate_gif(frame_number):
            self.toss_tocall_label.config(image=frames[frame_number])
            self.toss_tocall_label.image = frames[frame_number]
            if frame_number < len(frames) - 1:
                self.after(10, animate_gif, frame_number + 1)
            else:
                self.toss_coin(coin_side_selection)

        animate_gif(0)

# ---------------------------------------------------- Eat 5-star ------------------------------------------------------
    def do_nothing(self):
        pass

# -------------------------------------------------- Run Program -------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    Scoreboarde(root)
    root.mainloop()
