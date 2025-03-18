from tkinter import *
from scoreboard import Scoreboarde

width = 800
height = 600

main_bg = "#393939"
gray_out_bg = "#cdcdcd"

class BookCricket:
    def __init__(self):

        self.windows = Tk()
        self.windows.title("Book Cricket")
        self.windows.minsize(width,height)
        self.windows.resizable(False, False)
        self.windows.config(bg=main_bg)

        # Match Type
        self.title_frame = Frame(self.windows, bg=main_bg, width=width, height=75, relief=SUNKEN, border=2)
        self.title_frame.place(relx=0, rely=0)
        self.title_label = Label(self.title_frame, text="MOBC", font=("arial", 40, "bold"), justify=CENTER,
                                      bg=main_bg, fg="#ffff00")
        self.title_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.main_label = Label(self.windows, text="My Own Book Cricket", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=main_bg, fg="white")
        self.main_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.score_button = Button(self.windows, text="Play!!", width=20, command=self.open_details_form)
        self.score_button.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.windows.mainloop()

    def open_details_form(self):
        teamA = AddDetailForms("teamA")
        if teamA:
            teamB = AddDetailForms("teamB")
            if teamB:
                match_overs = AddDetailForms("match_overs")
                if match_overs:
                    Scoreboarde(teamA, teamB, match_overs)
                else:
                    teamA = None
                    teamB = None
            else:
                teamA = None

class AddDetailForms(Toplevel):
    def __init__(self, form_mode):
        super().__init__()

        # Form Window Settings
        self.title("Add Item")
        self.resizable(False, False)
        self.config(bg='white')
        self.grab_set()
        self.focus_set()
        self.lift()
        self.attributes("-topmost", True)
        self.update_idletasks()

        if form_mode == "teamA":
            self.team_name_label = Label(self, text="Enter Team A Name:", font=('Helvetica', 12, 'normal'))
            self.team_name_label.place(relx=0.5, rely=0.25, anchor=E)

            self.team_name_label = Label(self, text="Enter Team A Name:", font=('Helvetica', 12, 'normal'))
            self.team_name_label.place(relx=0.5, rely=0.25, anchor=E)

        elif form_mode == "teamB":
            self.team_name_label = Label(self, text="Enter Team B Name:", font=('Helvetica', 12, 'normal'))
            self.team_name_label.place(relx=0.5, rely=0.25, anchor=E)

        else:
            self.over_selection_label = Label(self, text="Select No. of Overs", font=('Helvetica', 12, 'normal'))
            self.over_selection_label.pack()
            options = ["1-O", "Duel 2", "3ple Threat", "4 Play", "F5", "6 Slam", "Lucky 7", "High Oc8ane", "9 Thrive", "Ten10"]

            clicked = StringVar()
            clicked.set("F5")

            over_options = OptionMenu(self, clicked, *options)
            over_options.pack()


if __name__ == "__main__":
    BookCricket()
