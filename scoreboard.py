from tkinter import *
import random

width = 800
height = 600

main_bg = "#393939"
gray_out_bg = "#cdcdcd"

class Scoreboarde(Toplevel):
    def __init__(self, teamA, teamB, match_overs):
        super().__init__()

        self.title("Book Cricket")
        self.minsize(width,height)
        self.resizable(False, False)
        self.config(bg=main_bg)

        self.total_score = 0
        self.total_wicket = 0
        self.total_balls = 0

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
        self.team1_frame = Frame(self.scoreboards_frame, bg=main_bg, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.team1_frame.place(relx=0, rely=0)

        self.team1_name_label = Label(self.team1_frame, text="Team A", width=10, height=1, font=("arial", 28, "bold"),
                                            justify=CENTER)
        self.team1_name_label.place(relx=0.1, rely=0.25, anchor=W)

        self.team1_scoreboard_label = Label(self.team1_frame, text="0-0", width=5, height=1, font=("arial", 20, "bold"),
                                      justify=CENTER)
        self.team1_scoreboard_label.place(relx=0.1, rely=0.55, anchor=W)

        self.team1_overs_label = Label(self.team1_frame, text="0.0", width=5, height=1, font=("arial", 12, "bold"),
                                      justify=CENTER)
        self.team1_overs_label.place(relx=0.1, rely=0.75, anchor=W)

        # Team B
        self.team2_frame = Frame(self.scoreboards_frame, bg=gray_out_bg, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.team2_frame.place(relx=0.5, rely=0)

        self.team2_name_label = Label(self.team2_frame, text="Team B", width=10, height=1, font=("arial", 28, "bold"),
                                      justify=CENTER)
        self.team2_name_label.place(relx=0.9, rely=0.25, anchor=E)
        self.team2_scoreboard_label = Label(self.team2_frame, text="0-0", width=5, height=1, font=("arial", 20, "bold"),
                                      justify=CENTER)
        self.team2_scoreboard_label.place(relx=0.9, rely=0.55, anchor=E)

        self.team2_overs_label = Label(self.team2_frame, text="0.0", width=5, height=1, font=("arial", 12, "bold"),
                                 justify=CENTER)
        self.team2_overs_label.place(relx=0.9, rely=0.75, anchor=E)

        for child in self.team2_frame.winfo_children():
            child.configure(state=DISABLED)

        # Score
        self.score_label = Label(self, width=5, height=1, font=("arial", 35, "bold"), justify=CENTER)
        self.score_label.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.score_button = Button(self, text="Play!!", width=20, command=self.scorer)
        self.score_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.score_timeline_label = Label(self, text="Timeline", bg='white')
        self.score_timeline_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.score_timeline = Text(self, width=50, height=1, font=("arial", 14, "bold"), state=DISABLED)
        self.score_timeline.place(relx=0.5, rely=0.95, anchor=CENTER)

        # Versus Label
        self.versus_v_label = Label(self, text="V", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=main_bg, fg="white")
        self.versus_v_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.versus_s_label = Label(self, text="S", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=main_bg, fg="white")
        self.versus_s_label.place(relx=0.5, rely=0.25, anchor=CENTER)

    def scorer(self):
        self.total_balls += 1
        overs = f"{int(self.total_balls/6)}.{(self.total_balls % 6)}"
        ball_score = random.randint(0,6)
        if ball_score == 5:
            self.total_wicket += 1
            ball_score = "W"
        else:
            self.total_score += ball_score

        self.score_label.config(text=ball_score)
        self.scoreboard_label.config(text=f"{self.total_score}-{self.total_wicket}")
        self.overs_label.config(text=f"{overs}")

        self.score_timeline.config(state=NORMAL)
        self.score_timeline.insert(END, f"{ball_score} ")
        self.score_timeline.config(state=DISABLED)

class AddDetailForms(Toplevel):
    def __init__(self, form_mode):
        super().__init__()

        # Form Window Settings
        self.title("Add Item")
        self.geometry("200x200")
        self.resizable(False, False)
        self.config(bg='white')
        self.grab_set()
        self.focus_set()
        self.lift()
        self.attributes("-topmost", True)
        self.update_idletasks()

if __name__ == "__main__":
    Scoreboarde()
