from tkinter import *
import random

class BookCricket:
    def __init__(self):

        self.windows = Tk()
        self.windows.title("Book Cricket")
        self.windows.minsize(600,600)
        self.windows.resizable(False, False)
        self.windows.config(bg='white')

        self.total_score = 0
        self.total_wicket = 0
        self.total_balls = 0

        self.scoreboard_label = Label(self.windows, text="0-0", width=5, height=1, font=("arial", 50, "bold"),
                                      justify=CENTER)
        self.scoreboard_label.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.overs_label = Label(self.windows, text="0.0", width=5, height=1, font=("arial", 12, "bold"),
                                      justify=CENTER)
        self.overs_label.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.score_label = Label(self.windows, width=5, height=1, font=("arial", 50, "bold"), justify=CENTER)
        self.score_label.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.score_button = Button(self.windows, text="Play!!", width=20, command=self.scorer)
        self.score_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.score_timeline_label = Label(self.windows, text="Timeline", bg='white')
        self.score_timeline_label.place(relx=0.5, rely=0.75, anchor=CENTER)
        self.score_timeline = Text(self.windows, width=40, height=1, font=("arial", 14, "bold"), state=DISABLED)
        self.score_timeline.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.windows.mainloop()

    def scorer(self):
        self.total_balls += 1
        overs = f"{int(self.total_balls/6)}.{(self.total_balls % 6)}"
        ball_score = random.randint(0,6)
        if ball_score == 5:
            self.total_wicket += 1
        else:
            self.total_score += ball_score

        self.score_label.config(text=ball_score)
        self.scoreboard_label.config(text=f"{self.total_score}-{self.total_wicket}")
        self.overs_label.config(text=f"{overs}")

        self.score_timeline.config(state=NORMAL)
        self.score_timeline.insert(END, f"{ball_score} ")
        self.score_timeline.config(state=DISABLED)

BookCricket()
