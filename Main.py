from tkinter import *

class Poker:

    def __init__(self, parent):
        """Sets up the GUI."""
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

        # sets up cards
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

        p1c1 = Label(p1_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        p1c1.place(relx=.25, rely=0.7, anchor=CENTER)

        p1c2 = Label(p1_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        p1c2.place(relx=.75, rely=0.7, anchor=CENTER)

        p2c1 = Label(p2_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        p2c1.place(relx=.25, rely=0.7, anchor=CENTER)

        p2c2 = Label(p2_cards_frame, width=12, height=10, text="n/a", bg="Yellow")
        p2c2.place(relx=.75, rely=0.7, anchor=CENTER)


        pot_label = Label(p1_cards_frame, width=20, height=6, text="pot value", bg="Yellow")
        pot_label.place(relx=.5, rely=0.3, anchor=CENTER)

        turn_display = Label(p2_cards_frame, width=15, height=6, text="Player 1 turn", bg="Yellow")
        turn_display.place(relx=.3, rely=0.3, anchor=CENTER)

        end_turn_btn = Button(p2_cards_frame, width=15, height=6,
                              text="End turn", bg="Yellow", command=self.end_turn)
        end_turn_btn.place(relx=.7, rely=0.3, anchor=CENTER)

    def end_turn(self):
        pass


if __name__ == "__main__":
    root = Tk()
    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()
    root.title("Poker")
    Poker(root)
    root.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    root.mainloop()
