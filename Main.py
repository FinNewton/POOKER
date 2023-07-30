from tkinter import *
from texasholdem import Card
from texasholdem.evaluator import evaluate, rank_to_string

class Poker:

    def __init__(self, parent):
        """Sets up the GUI."""
        self.cards = ["Ad", "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "Td", "Jd", "Qd", "Kd",
                 "Ah", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "Th", "Jh", "Qh", "Kh",
                 "As", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "Ts", "Js", "Qs", "Ks",
                 "Ac", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "Tc", "Jc", "Qc", "Kc"]

        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)

        community_card_frame = Frame(parent, width=WIDTH, height=HEIGHT/3, bg="Black", bd=5)
        community_card_frame.grid(row=0, column=0, columnspan=3, sticky=N+S+E+W)

        p1_cards_frame = Frame(parent, width=WIDTH/3, height=HEIGHT/1.5, bg="Blue")
        p1_cards_frame.grid(row=1, column=0, sticky=N+S+E+W)

        p2_cards_frame = Frame(parent, width=WIDTH / 3, height=HEIGHT / 1.5, bg="Blue")
        p2_cards_frame.grid(row=1, column=2, sticky=N+S+E+W)

        betting_frame = Frame(parent, width=WIDTH / 3, height=HEIGHT / 1.5, bg="Grey")
        betting_frame.grid(row=1, column=1, sticky=N+S+E+W)

        # locks frames in place
        community_card_frame.grid_propagate(False)
        p2_cards_frame.grid_propagate(False)
        p1_cards_frame.grid_propagate(False)
        betting_frame.grid_propagate(False)

        # sets up cards river turn flop
        self.community_cards = []
        index = 0
        x_coord = .5
        for i in range(5):
            self.community_cards.append(Label(community_card_frame,
                                              width=12, height=10, text="n/a", bg="Yellow"))
            self.community_cards[index].place(relx=x_coord, rely=0.5, anchor=CENTER)
            index += 1
            if index == 1:
                x_coord = .15
            elif index == 2:
                x_coord = .85
            elif index == 3:
                x_coord = 0.675
            elif index == 4:
                x_coord = 0.325

        # sets up both players cards
        self.p1c1 = Label(p1_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        self.p1c1.place(relx=.25, rely=0.7, anchor=CENTER)

        self.p1c2 = Label(p1_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        self.p1c2.place(relx=.75, rely=0.7, anchor=CENTER)

        self.p2c1 = Label(p2_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        self.p2c1.place(relx=.25, rely=0.7, anchor=CENTER)

        self.p2c2 = Label(p2_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        self.p2c2.place(relx=.75, rely=0.7, anchor=CENTER)

        # sets up aditonal info.
        self.pot_label = Label(p1_cards_frame, width=20, height=6, text="pot value", bg="Yellow")
        self.pot_label.place(relx=.5, rely=0.3, anchor=CENTER)

        self.turn_display = Label(p2_cards_frame, width=15, height=6, text="Player 1 turn", bg="Yellow")
        self.turn_display.place(relx=.3, rely=0.3, anchor=CENTER)

        self.end_turn_btn = Button(p2_cards_frame, width=15, height=6,
                              text="End turn", bg="Yellow", command=self.end_turn)
        self.end_turn_btn.place(relx=.7, rely=0.3, anchor=CENTER)

        # sets up the turn options bets etc

        self.call_btn = Button(betting_frame, width=25, height=6, text="call", bg="Sky blue")
        self.call_btn.bind("<Button-1>", self.bet)
        self.call_btn.place(relx=.3, rely=0.15, anchor=CENTER)

        self.raise_btn = Button(betting_frame, width=25, height=6, text="raise", bg="Sky blue")
        self.raise_btn.bind("<Button-1>", self.bet)
        self.raise_btn.place(relx=.3, rely=0.40, anchor=CENTER)

        self.fold_btn = Button(betting_frame, width=25, height=6, text="fold", bg="Sky blue")
        self.fold_btn.bind("<Button-1>", self.bet)
        self.fold_btn.place(relx=.3, rely=0.65, anchor=CENTER)

        # slider for betting.
        current_value = DoubleVar()
        self.bet_amount = Scale(betting_frame, from_=100, to=0, orient="vertical",
                                variable=current_value, bg="Sky blue", label="Raise")
        self.bet_amount.place(relx=.8, rely=0.5, anchor=CENTER)

        # displays amount to call.
        self.call_amount = Label(betting_frame, width=20, height=4, text="No bet", bg="Sky blue")
        self.call_amount.place(relx=.3, rely=0.9, anchor=CENTER)

    def end_turn(self):
        pass

    def bet(self, event):
        pass


if __name__ == "__main__":
    root = Tk()
    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()
    root.title("Poker")
    Poker(root)
    root.state("zoomed")
    root.mainloop()
