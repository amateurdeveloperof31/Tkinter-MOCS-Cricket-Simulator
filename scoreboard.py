# ----------------------------------------------------- Imports --------------------------------------------------------
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk # Added By Me
import random

# ------------------------------------------------ Global Variables ----------------------------------------------------
width = 800
height = 600

main_bg = "#393939"
gray_out_bg = "#cdcdcd"

# --------------------------------------------------- Main Class -------------------------------------------------------
class Scoreboarde(Toplevel):
    def __init__(self, main_window, all_match_details):
        super().__init__()

        self.title("Book Cricket")
        self.minsize(width,height)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.config(bg=main_bg)

        self.main_window = main_window

        self.protocol("WM_DELETE_WINDOW", self.on_click_x)

        self.match_details = all_match_details
        self.teamA_name = all_match_details["teamA_name"]
        self.teamA_color = all_match_details["teamA_color"]
        self.teamB_name = all_match_details["teamB_name"]
        self.teamB_color = all_match_details["teamB_color"]
        self.innings_overs = all_match_details["match_overs"]

        self.bat1 = "teamA"
        self.bat2 = "teamB"
        self.current_innnings = None
        self.innings_number = 1

        self.inning_runs = 0
        self.inning_wickets = 0
        self.inning_balls = 0
        self.total_balls = self.innings_overs * 6
        self.target = 0

        self.create_widgets()

# ---------------------------------------------------- Methods ---------------------------------------------------------
# ------------------------------------------------ Create Widgets ------------------------------------------------------
    def create_widgets(self):

        # Match Type
        self.match_type_frame = Frame(self, bg=main_bg, width=width, height=75, relief=SUNKEN, border=2)
        self.match_type_frame.place(relx=0, rely=0)
        self.match_type_label = Label(self.match_type_frame, text="MOBC", font=("arial", 40, "bold"), justify=CENTER,
                                      bg=main_bg, fg="#ffff00")
        self.match_type_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Scoreboards
        self.scoreboards_frame = Frame(self, bg=main_bg, width=width, height=200, relief=SUNKEN,
                                      border=2)
        self.scoreboards_frame.place(relx=0, rely=0.13)

        # Team A
        self.teamA_frame = Frame(self.scoreboards_frame, bg=self.teamA_color, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.teamA_frame.place(relx=0, rely=0)

        self.teamA_name_label = Label(self.teamA_frame, text=self.teamA_name, width=10, height=1, justify=CENTER,
                                      font=("arial", 28, "bold"))
        self.teamA_name_label.place(relx=0.1, rely=0.25, anchor=W)

        self.teamA_scoreboard_label = Label(self.teamA_frame, text="0-0", width=5, height=1, font=("arial", 20, "bold"),
                                      justify=CENTER)
        self.teamA_scoreboard_label.place(relx=0.1, rely=0.55, anchor=W)

        self.teamA_overs_label = Label(self.teamA_frame, text=f"0.0 ({self.innings_overs})", width=8, height=1,
                                       font=("arial", 12, "bold"), justify=CENTER)
        self.teamA_overs_label.place(relx=0.1, rely=0.75, anchor=W)

        # Team B
        self.teamB_frame = Frame(self.scoreboards_frame, bg=self.teamB_color, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.teamB_frame.place(relx=0.5, rely=0)

        self.teamB_name_label = Label(self.teamB_frame, text=self.teamB_name, width=10, height=1, justify=CENTER,
                                      font=("arial", 28, "bold"))
        self.teamB_name_label.place(relx=0.9, rely=0.25, anchor=E)
        self.teamB_scoreboard_label = Label(self.teamB_frame, text="0-0", width=5, height=1, font=("arial", 20, "bold"),
                                      justify=CENTER)
        self.teamB_scoreboard_label.place(relx=0.9, rely=0.55, anchor=E)

        self.teamB_overs_label = Label(self.teamB_frame, text=f"0.0 ({self.innings_overs})", width=8, height=1,
                                       font=("arial", 12, "bold"), justify=CENTER)
        self.teamB_overs_label.place(relx=0.9, rely=0.75, anchor=E)

        # for child in self.teamB_frame.winfo_children():
        #     child.configure(state=DISABLED)

        self.coin_toss_button = Button(self, text="Coin Toss!!", width=20, command=self.open_coin_toss)
        self.coin_toss_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Versus Label
        self.versus_v_label = Label(self, text="V", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=main_bg, fg="white")
        self.versus_v_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.versus_s_label = Label(self, text="S", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=main_bg, fg="white")
        self.versus_s_label.place(relx=0.5, rely=0.25, anchor=CENTER)

# --------------------------------------------------- Coin Toss --------------------------------------------------------
    def open_coin_toss(self):
        self.coin_toss_button.destroy()
        CoinTossForm(self, self.match_details)

# ------------------------------------------------ Further Widgets -----------------------------------------------------
    def widgets_continued(self, toss_winner, bat_ball_selection):
        # Score
        self.score_label = Label(self, width=5, height=1, font=("arial", 35, "bold"), justify=CENTER)
        self.score_label.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.score_button = Button(self, text="Play!!", width=20, command=self.scorer)
        self.score_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.score_timeline_label = Label(self, text="Timeline", bg='white')
        self.score_timeline_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.score_timeline = Text(self, width=50, height=1, font=("arial", 14, "bold"), state=DISABLED)
        self.score_timeline.place(relx=0.5, rely=0.95, anchor=CENTER)

        if ((toss_winner == self.teamA_name and bat_ball_selection == "bat") or
                (toss_winner == self.teamB_name and bat_ball_selection == "bowl")):
            self.current_innings = "teamA"
            bat_x = 0.4
            ball_x = 0.6
        else:
            self.current_innings = "teamB"
            bat_x = 0.6
            ball_x = 0.4

        # Icons
        self.bat_image = self.image_resier("images/bat.png", 40)
        self.main_window.bat_icon_label = Label(self, image=self.bat_image, bg='white')
        self.main_window.bat_icon_label.place(relx=bat_x, rely=0.22, anchor=CENTER)

        self.ball_image = self.image_resier("images/ball.png", 40)
        self.main_window.ball_icon_label = Label(self, image=self.ball_image, bg='white')
        self.main_window.ball_icon_label.place(relx=ball_x, rely=0.22, anchor=CENTER)

# -------------------------------------------------- Main Scorer -------------------------------------------------------
    def scorer(self):
        if self.inning_balls < self.total_balls:
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

        else:
            if self.innings_number == 1:
                self.innings_number = 2
                messagebox.showinfo("End of 1st Innings",
                        f"{self.current_innings} has scored {self.inning_runs} for {self.inning_wickets}",
                                    parent=self)
                if self.current_innings == "teamA":
                    self.teamA_score = self.inning_runs
                    self.teamA_wickets = self.inning_wickets
                    self.current_innings = "teamB"
                else:
                    self.teamB_score = self.inning_runs
                    self.teamB_wickets = self.inning_wickets
                    self.current_innings = "teamA"
                self.target = self.inning_runs + 1
                messagebox.showinfo("Target",
                                    f"Target for {self.current_innings} is {self.target}", parent=self)

                self.inning_runs = 0
                self.inning_wickets = 0
                self.inning_balls = 0
                self.total_balls = self.innings_overs * 6

            else:
                self.score_button.config(state=DISABLED)
                self.teamB_score = self.inning_runs

                if self.teamA_score > self.teamB_score:
                    runs_win = self.teamA_score - self.teamB_score
                    messagebox.showinfo("End of the Match",
                            f"{self.current_innings} has scored {self.inning_runs} for {self.inning_wickets}",
                                        parent=self)
                    messagebox.showinfo("End of the Match",
                            f"{self.current_innings} has won by {runs_win} runs.", parent=self)
                elif self.teamA_score < self.teamB_score:
                    wickets_win = 10 - self.teamB_wickets
                    messagebox.showinfo("End of the Match",
                            f"{self.current_innings} has scored {self.inning_runs} for {self.inning_wickets}",
                                        parent=self)
                    messagebox.showinfo("End of the Match",
                            f"{self.current_innings} has won by {wickets_win} wickets.", parent=self)

# ------------------------------------------------- On Clicking X ------------------------------------------------------
    def on_click_x(self):
        confirm_x = messagebox.askyesno("Quit?", "Are you sure you want to quit?", parent=self)
        if confirm_x:
            self.grab_release()
            self.destroy()
            self.main_window.windows.deiconify()

# ------------------------------------------------- Image Resizer ------------------------------------------------------
    def image_resier(self, image_location, image_wd):
        self.imager = Image.open(image_location)
        aspect_ratio = self.imager.height / self.imager.width
        width = image_wd
        self.imager = self.imager.resize((width, int(width * aspect_ratio)))
        return ImageTk.PhotoImage(self.imager)

# ------------------------------------------------- Coin Toss Form -----------------------------------------------------
class CoinTossForm(Toplevel):
    def __init__(self, main_window, match_details):
        super().__init__()

        # Form Window Settings
        self.title("Coin Toss")
        self.geometry("300x200")
        self.resizable(False, False)
        self.config(bg='white')
        self.transient(main_window)
        self.grab_set()
        self.focus_set()

        self.teamA_name = match_details["teamA_name"]
        self.teamA_color = match_details["teamA_color"]
        self.teamB_name = match_details["teamB_name"]
        self.teamB_color = match_details["teamB_color"]
        self.innings_overs = match_details["match_overs"]

        self.main_window = main_window

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

        self.head_image = self.main_window.image_resier("images/head.jpg", 70)
        self.tail_image = self.main_window.image_resier("images/tail.jpg", 70)
        self.head_button = Button(self, image=self.head_image, bg='white', activebackground='white',
                                  command=lambda:self.coin_toss_animation(0))
        self.head_button.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.tail_button = Button(self, image=self.tail_image, bg='white', activebackground='white',
                                  command=lambda:self.coin_toss_animation(1))
        self.tail_button.place(relx=0.75, rely=0.7, anchor=CENTER)

        self.mainloop()

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

        self.bat_image = self.main_window.image_resier("images/bat.png", 70)
        self.bat_button = Button(self, image=self.bat_image, bg='white', activebackground='white',
                                  command=lambda: self.choose_to_bat_ball(toss_winner, "bat"))
        self.bat_button.place(relx=0.25, rely=0.7, anchor=CENTER)

        self.ball_image = self.main_window.image_resier("images/ball.png", 70)
        self.ball_button = Button(self, image=self.ball_image, bg='white', activebackground='white',
                                  command=lambda: self.choose_to_bat_ball(toss_winner, "bowl"))
        self.ball_button.place(relx=0.75, rely=0.7, anchor=CENTER)

    def choose_to_bat_ball(self, toss_winner, bat_ball_selection):
        self.destroy()
        self.main_window.widgets_continued(toss_winner, bat_ball_selection)

    def coin_toss_animation(self, coin_side_selection):
        self.head_button.destroy()
        self.tail_button.destroy()

        gif = Image.open('images/coinToss.gif')
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

# -------------------------------------------------- Run Program -------------------------------------------------------
if __name__ == "__main__":
    match_details = {
        "teamA_name": "teamA",
        "teamA_color": "#8B0A1A",
        "teamB_name": "teamB",
        "teamB_color": "#00BFFF",
        "match_overs": 10
    }

    root = Tk()
    Scoreboarde(root, match_details)
    root.mainloop()

    # CoinTossForm(root, match_details)
