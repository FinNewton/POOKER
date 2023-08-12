from datetime import datetime
from tkinter import *
import random as r
from texasholdem import Card
from texasholdem.evaluator import evaluate, rank_to_string

SMALL_BLIND = 5
BIG_BLIND = 10


class Poker:

    def __init__(self, parent):
        """Sets up the GUI."""
        self.call_requirement = 0
        self.action = True
        self.player_turn = True
        self.plays = 0
        self.turn = 0
        self.min_bet = BIG_BLIND
        self.p1_money = 120
        self.p2_money = 150
        # random card 0,1 are hand 1: card 2,3 are hand 2, 4,5,6,7,8 are community cards.
        self.random_cards = []
        self.cards = ["Ad", "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "Td", "Jd", "Qd", "Kd",
                      "Ah", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "Th", "Jh", "Qh", "Kh",
                      "As", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "Ts", "Js", "Qs", "Ks",
                      "Ac", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "Tc", "Jc", "Qc", "Kc"]

        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)

        community_card_frame = Frame(parent, width=WIDTH, height=HEIGHT / 3, bg="Black", bd=5)
        community_card_frame.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W)

        p1_cards_frame = Frame(parent, width=WIDTH / 3, height=HEIGHT / 1.5, bg="Blue")
        p1_cards_frame.grid(row=1, column=0, sticky=N + S + E + W)

        p2_cards_frame = Frame(parent, width=WIDTH / 3, height=HEIGHT / 1.5, bg="Blue")
        p2_cards_frame.grid(row=1, column=2, sticky=N + S + E + W)

        self.betting_frame = Frame(parent, width=WIDTH / 3, height=HEIGHT / 1.5, bg="Grey")
        self.betting_frame.grid(row=1, column=1, sticky=N + S + E + W)

        # locks frames in place
        community_card_frame.grid_propagate(False)
        p2_cards_frame.grid_propagate(False)
        p1_cards_frame.grid_propagate(False)
        self.betting_frame.grid_propagate(False)

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

        # sets up both players cards and money
        self.p1_money_label = Label(p1_cards_frame, width=30, height=5, text=f"Player 1\n Money: {self.p1_money}",
                                    bg="Yellow")
        self.p1_money_label.place(relx=.5, rely=0.1, anchor=CENTER)

        self.p2_money_label = Label(p2_cards_frame, width=30, height=5, text=f"Player 2\n Money: {self.p2_money}",
                                    bg="Yellow")
        self.p2_money_label.place(relx=.5, rely=0.1, anchor=CENTER)

        self.p1c1 = Button(p1_cards_frame, width=12, height=10, text="Card 1", bg="Yellow", command=self.reveal)

        self.p1c2 = Button(p1_cards_frame, width=12, height=10, text="Card 2", bg="Yellow", command=self.reveal)

        self.p2c1 = Button(p2_cards_frame, width=12, height=10, text="Card 1", bg="Yellow", command=self.reveal)

        self.p2c2 = Button(p2_cards_frame, width=12, height=10, text="Card 2", bg="Yellow", command=self.reveal)

        # Sets up aditonal info.
        self.pot_label = Label(p1_cards_frame, width=20, height=6, text="0", bg="Yellow")
        self.pot_label.place(relx=.5, rely=0.4, anchor=CENTER)
        self.pot_label1 = Label(p1_cards_frame, width=5, height=3, font=('TkDefaultFont', 15), text="Pot:", bg="Yellow")
        self.pot_label1.place(relx=.4, rely=0.4, anchor=CENTER)

        self.turn_display = Label(p2_cards_frame, width=15, height=6, text="Player 1 turn", bg="Yellow")
        self.turn_display.place(relx=.3, rely=0.4, anchor=CENTER)

        self.end_turn_btn = Button(p2_cards_frame, width=15, height=6,
                                   text="Start game", bg="Yellow", command=self.deal_hand)
        self.end_turn_btn.place(relx=.7, rely=0.4, anchor=CENTER)

        # sets up the turn options bets etc
        self.call_btn = Button(self.betting_frame, width=25, height=6, text="call", bg="Sky blue", command=self.call)
        self.call_btn.place(relx=.3, rely=0.15, anchor=CENTER)

        self.raise_btn = Button(self.betting_frame, width=25, height=6, text="raise", bg="Sky blue",
                                command=self.raise_amount)
        self.raise_btn.place(relx=.3, rely=0.40, anchor=CENTER)

        self.fold_btn = Button(self.betting_frame, width=25, height=6, text="fold", bg="Sky blue", command=self.fold)
        self.fold_btn.place(relx=.3, rely=0.65, anchor=CENTER)

        # slider for betting.
        current_value = DoubleVar()
        self.bet_amount = Scale(self.betting_frame, from_=100, to=BIG_BLIND, orient="vertical",
                                variable=current_value, bg="Sky blue", label="Raise")
        self.bet_amount.place(relx=.8, rely=0.5, anchor=CENTER)

        # displays amount to call.
        self.call_amount = Label(self.betting_frame, width=20, height=4, text="No bet", bg="Sky blue")
        self.call_amount.place(relx=.3, rely=0.9, anchor=CENTER)

    def p1(self):
        self.turn_display.configure(text="Player 1 turn")
        self.p1c1.configure(command=self.reveal)
        self.p1c2.configure(command=self.reveal)
        self.p2c1.configure(command=self.unbind)
        self.p2c2.configure(command=self.unbind)
        if self.call_requirement != 0:
            self.bet_amount.configure(from_=self.p1_money, to=self.call_requirement)
        if self.turn != 1:
            self.bet_amount.configure(from_=self.p1_money, to=1)
        else:
            self.bet_amount.configure(from_=self.p1_money, to=BIG_BLIND)
        self.reset()
        self.action = False

    def p2(self):
        # displays blinds info.
        if self.turn == 1:
            self.call_amount.configure(text=f"SMALL BLIND {SMALL_BLIND}\nTo call {self.pot_label.cget('text')}")
        self.turn_display.configure(text="Player 2 turn")
        # Resets cards
        self.p2c1.configure(command=self.reveal)
        self.p2c2.configure(command=self.reveal)
        self.p1c1.configure(command=self.unbind)
        self.p1c2.configure(command=self.unbind)
        # sets min to call value, blind amount or 1 dollar.
        if self.call_requirement != 0:
            self.bet_amount.configure(from_=self.p2_money, to=self.call_requirement)
        elif self.turn == 1:
            self.bet_amount.configure(from_=self.p2_money, to=BIG_BLIND)
            self.call_requirement = BIG_BLIND
        else:
            self.bet_amount.configure(from_=self.p2_money, to=1)
        self.reset()
        self.action = False

    def deal_hand(self):
        # Turn = 0 when game starts deal each person a hand.
        if self.turn == 0:
            self.reveal_cards()
            self.p1()
        elif self.action is False and self.turn != 0:
            self.betting_frame.configure(bg="Red")
        elif self.call_requirement == 0 and self.plays > 1:
            if self.player_turn == True:
                self.reveal_cards()
                self.p2()
                self.player_turn = False
            else:
                self.reveal_cards()
                self.p1()
                self.player_turn = True
        elif self.call_requirement != 0 or self.plays <= 1:
            if self.player_turn == True:
                self.p2()
                self.player_turn = False
            else:
                self.p1()
                self.player_turn = True

    def reveal_cards(self):
        """Whenever the betting of a round has ended,
        the next set of cards will be turned. this function will turn the appropiate cards.
        will also trigger the hand eval calculations if the game ends naturally."""
        if self.turn == 0:
            # sets up the hand.
            self.p1c1.place(relx=.25, rely=0.8, anchor=CENTER)
            self.p1c2.place(relx=.75, rely=0.8, anchor=CENTER)
            self.p2c1.place(relx=.25, rely=0.8, anchor=CENTER)
            self.p2c2.place(relx=.75, rely=0.8, anchor=CENTER)
            self.end_turn_btn.configure(text="End Turn")
            self.call_amount.configure(text=f"BIG BLIND \n{BIG_BLIND}")
            # gets random cards for the game.
            self.random_cards = r.sample(range(0, len(self.cards)), 9)
            # unbinds the btn press.
            self.call_requirement = BIG_BLIND
        elif self.turn == 1:
            self.community_cards[0].configure(text=f"{self.cards[self.random_cards[4]]}")
            self.community_cards[1].configure(text=f"{self.cards[self.random_cards[5]]}")
            self.community_cards[4].configure(text=f"{self.cards[self.random_cards[6]]}")
        elif self.turn == 2:
            self.community_cards[3].configure(text=f"{self.cards[self.random_cards[7]]}")
        elif self.turn == 3:
            self.community_cards[2].configure(text=f"{self.cards[self.random_cards[8]]}")
        elif self.turn == 4:
            self.community_cards[2].configure(text="game over")
        self.plays = 0
        self.turn += 1

    def reveal(self):
        """will show the cards for the correct players turn. """
        # player 2s turn.
        if self.player_turn == False:
            self.p2c1.configure(text=f"{self.cards[self.random_cards[2]]}")
            self.p2c2.configure(text=f"{self.cards[self.random_cards[3]]}")
            self.p2c1.configure(command=self.reset)
            self.p2c2.configure(command=self.reset)
        # player 1s turn.
        else:
            self.p1c1.configure(text=f"{self.cards[self.random_cards[0]]}")
            self.p1c2.configure(text=f"{self.cards[self.random_cards[1]]}")
            self.p1c1.configure(command=self.reset)
            self.p1c2.configure(command=self.reset)

    def reset(self):
        # will hide the card again.
        if self.player_turn == False:
            self.p2c1.configure(text="Card 1")
            self.p2c2.configure(text="Card 2")
            self.p2c1.configure(command=self.reveal)
            self.p2c2.configure(command=self.reveal)
        else:
            self.p1c1.configure(text="Card 1")
            self.p1c2.configure(text="Card 2")
            self.p1c1.configure(command=self.reveal)
            self.p1c2.configure(command=self.reveal)

    def pot_amount(self, addition):
        # adds to the pot
        return int(self.pot_label.cget('text')) + int(addition)

    def raise_amount(self):
        """will raise the total pot value. has re raising functions.
        will make sure the play doesn't end."""
        self.betting_frame.configure(bg="Grey")
        if self.action is False:
            # will increase pot value by x amount.
            if self.bet_amount.get() == self.call_requirement:
                self.call()
            else:
                if self.bet_amount.get() != self.call_requirement and self.plays >= 1:
                    self.call_requirement =  self.bet_amount.get() - self.call_requirement
                    self.call_amount.configure(text=f"Re Raised {self.call_requirement}")
                else:
                    self.call_requirement = self.bet_amount.get()
                    self.call_amount.configure(text=f"Raised {self.call_requirement}")
                # deducts money from correct player.
                if self.player_turn == False:
                    self.p2_money -= self.bet_amount.get()
                else:
                    self.p1_money -= self.bet_amount.get()
                # set the amount called, increase pot value, changes slider min to call value.
                self.pot_label.configure(text=f"{self.pot_amount(self.bet_amount.get())}")
                self.bet_amount.configure(to=self.call_requirement)
                self.action = True
            self.p1_money_label.configure(text=f"Player 1\n Money: {self.p1_money}")
            self.p2_money_label.configure(text=f"Player 2\n Money: {self.p2_money}")
            self.plays += 1

    def call(self):
        """ will match the players called value.
        Will also act as a check if you dont want to bet."""
        self.betting_frame.configure(bg="Grey")
        if self.action is False:
            if self.call_requirement != 0:
                if self.player_turn == False:
                    self.p2_money -= self.call_requirement
                else:
                    self.p1_money -= self.call_requirement
                self.pot_label.configure(text=f"{self.pot_amount(self.call_requirement)}")
                self.call_amount.configure(text=f"Called {self.call_requirement}")
                if self.turn != 1 or self.player_turn == False:
                    self.call_requirement = 0
            else:
                self.call_amount.configure(text=f"Called {self.call_requirement}")
            self.action = True
            self.p1_money_label.configure(text=f"Player 1\n Money: {self.p1_money}")
            self.p2_money_label.configure(text=f"Player 2\n Money: {self.p2_money}")
            self.plays += 1

    def fold(self):
        self.betting_frame.configure(bg="Grey")
        if self.turn > 0 and self.action is False:
            # if they fold when the blinds haven't been paid will force pay blinds.
            if self.player_turn == 0 and self.turn <= 2:
                self.p2_money -= SMALL_BLIND
                self.pot_label.configure(text=f"{self.pot_amount(SMALL_BLIND)}")

            elif self.turn < 2:
                self.p1_money -= BIG_BLIND
                self.pot_label.configure(text=f"{self.pot_amount(BIG_BLIND)}")

            # Gives pot value to other player and ends the game.
            if self.player_turn == False:
                self.p1_money += int(self.pot_label.cget('text'))
            else:
                self.p2_money += int(self.pot_label.cget('text'))
            self.pot_label.configure(text="0")
            self.p1_money_label.configure(text=f"Player 1\n Money: {self.p1_money}")
            self.p2_money_label.configure(text=f"Player 2\n Money: {self.p2_money}")
            self.end_round()

    def unbind(self):
        pass

    def end_round(self):
        self.end_turn_btn.destroy()


if __name__ == "__main__":
    root = Tk()
    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()
    root.title("Poker")
    Poker(root)
    root.state("zoomed")
    root.mainloop()
