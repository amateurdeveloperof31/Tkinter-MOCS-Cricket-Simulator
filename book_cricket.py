# ----------------------------------------------------- Imports --------------------------------------------------------
from tkinter import *
from tkinter import messagebox, ttk
from scoreboard import Scoreboarde
# ------------------------------------------------ Global Variables ----------------------------------------------------
width = 800
height = 600

main_bg = "#393939"
gray_out_bg = "#cdcdcd"

team_colors = ["#8B0A1A","#00BFFF","#FFC400","#8F9779","#C51077","#F7DC6F","#2E865F","#A291FF","#FF99CC","#34A85A"]

# --------------------------------------------------- Main Class -------------------------------------------------------
class BookCricket:
    def __init__(self):

        self.windows = Tk()
        self.windows.title("Book Cricket")
        self.windows.minsize(width,height)
        self.windows.resizable(False, False)
        self.windows.config(bg=main_bg)

        # Variables
        self.teamA = {}
        self.teamB = {}
        self.match_overs = None

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

# ---------------------------------------------------- Methods ---------------------------------------------------------
# -------------------------------------------- Open Match Details Form -------------------------------------------------
    def open_details_form(self):
        form = AddDetailForms(self.windows)
        self.windows.wait_window(form)
        if hasattr(form, 'match_details'):
            all_match_details = form.match_details
            if all_match_details:
                scoreboard_window = Scoreboarde(self, all_match_details)
                self.windows.withdraw()

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

        fonter = ('Helvetica', 12, 'normal')

        # Scoreboards
        self.scoreboards_frame = Frame(self, bg=main_bg, width=width, height=200, relief=SUNKEN,
                                       border=2)
        self.scoreboards_frame.place(relx=0, rely=0.02)

        # Team A
        self.team1_frame = Frame(self.scoreboards_frame, bg=main_bg, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.team1_frame.place(relx=0, rely=0)

        self.team1_name_label = Label(self.team1_frame, text=" Enter Team A's Name", width=20, height=1,
                                      font=("arial", 14, "bold"), justify=CENTER)
        self.team1_name_label.place(relx=0.1, rely=0.2, anchor=W)

        self.team1_name_entry = Entry(self.team1_frame, width=20, font=("arial", 20, "bold"), justify=LEFT)
        self.team1_name_entry.place(relx=0.1, rely=0.4, anchor=W)

        self.team1_colors_label = Label(self.team1_frame, text="Choose Team A's color", width=20, height=1,
                                       font=("arial", 14, "bold"), justify=CENTER)
        self.team1_colors_label.place(relx=0.1, rely=0.6, anchor=W)

        x = 0.2
        for colors in team_colors:
            self.team_color_buttons = Button(self.team1_frame, width=1, bg=colors,
                                             command=lambda c=colors: self.chosen_color(c, "teamA"))
            self.team_color_buttons.place(relx=x, rely=0.8, anchor=CENTER)
            x += 0.05

        # Team B
        self.team2_frame = Frame(self.scoreboards_frame, bg=main_bg, width=width - (width / 2), height=200,
                                 relief=SUNKEN, border=2)
        self.team2_frame.place(relx=0.5, rely=0)

        self.team2_name_label = Label(self.team2_frame, text="Enter Team B's Name", width=20, height=1,
                                      font=("arial", 14, "bold"), justify=CENTER)
        self.team2_name_label.place(relx=0.9, rely=0.2, anchor=E)

        self.team2_name_entry = Entry(self.team2_frame, width=20, font=("arial", 20, "bold"), justify=RIGHT)
        self.team2_name_entry.place(relx=0.9, rely=0.4, anchor=E)

        self.team2_colors_label = Label(self.team2_frame, text="Choose Team B's color", width=20, height=1,
                                       font=("arial", 14, "bold"), justify=CENTER)
        self.team2_colors_label.place(relx=0.9, rely=0.6, anchor=E)

        x = 0.8
        for colors in team_colors:
            self.team_color_buttons = Button(self.team2_frame, width=1, bg=colors,
                                             command=lambda c=colors: self.chosen_color(c, "teamB"))
            self.team_color_buttons.place(relx=x, rely=0.8, anchor=CENTER)
            x -= 0.05

        self.over_selection_label = Label(self, text="Select No. of Overs: ", font=('Helvetica', 12, 'normal'), bg='white')
        self.over_selection_label.place(relx=0.4, rely=0.75, anchor=CENTER)
        self.options = {"1-O": 1, "Duel 2": 2, "3ple Threat": 3, "4 Play": 4, "F5": 5, "6 Slam": 6, "Lucky 7": 7,
                   "High Oc8ane": 8, "9 Thrive": 9, "Ten10": 10}

        self.clicked = StringVar()
        keys_list = list(self.options.keys())

        self.over_options = ttk.OptionMenu(self, self.clicked, keys_list[4], *self.options.keys())
        self.over_options.place(relx=0.52, rely=0.75, anchor=W)

        self.clicked.set(keys_list[4])

        self.ok_button = Button(self, text="OK!", font=fonter, bg=main_bg, fg='white', command=self.enter_match_details)
        self.ok_button.place(relx=0.5, rely=0.9, anchor=CENTER)

# -------------------------------------------------- Match Details -----------------------------------------------------
    def enter_match_details(self):
        self.match_overs = self.options[self.clicked.get()]
        teamA_name = self.team1_name_entry.get().capitalize()
        teamB_name = self.team2_name_entry.get().capitalize()

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
            self.match_details = {
                "teamA_name": teamA_name,
                "teamA_color": self.teamA_color,
                "teamB_name": teamB_name,
                "teamB_color": self.teamB_color,
                "match_overs": self.match_overs
            }
            self.destroy()

# ---------------------------------------------------- Colors ----------------------------------------------------------
    def chosen_color(self, color, teame):
        if teame == "teamA":
            self.teamA_color = color
            self.team1_name_entry. config(bg=color, fg='white')
        else:
            self.teamB_color = color
            self.team2_name_entry.config(bg=color, fg='white')
# -------------------------------------------------- Run Program -------------------------------------------------------
if __name__ == "__main__":
    BookCricket()
