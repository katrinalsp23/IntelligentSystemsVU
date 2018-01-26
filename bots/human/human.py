"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""
#TODO: Make functions get_lowest_trump, get_lowest etc. to make shit easier
# Import the API objects
from api import State, Deck
import sys
import random


class Bot:

    def __init__(self):
        # self.get_move()
        pass


    def get_move(self,state):
        # type: (State) -> tuple[int, int]

        # moves = state.moves()


        __RANKS = ["A", "T", "K", "Q", "J"]
        __SUITS = ["C", "D", "H", "S"]


        # while 1 :
        # sys.stdin.flush()
        hello = sys.stdin.readline()
        print(hello)
        rank = raw_input("Enter Rank: ")
        suit = raw_input("Enter Suit: ")

        rankIndex = __RANKS.index(rank)
        suitIndex = __SUITS.index(suit)

        cardIndex = (suitIndex * 5) + rankIndex
        print(cardIndex)
            # for move in moves:
            #     if cardIndex == move[0]:
            #         break

        return (cardIndex, None)
