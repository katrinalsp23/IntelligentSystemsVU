#!/usr/bin/env python
"""
This is a bot that applies propositional logic reasoning to determine its strategy.
The strategy it uses is determined by what is defined in load.py. Here it is to always
pick a Jack to play whenever this is a legal move.

It loads general information about the game, as well as the definition of a strategy,
from load.py.
"""

from api import State, util, Deck
import random, load, copy

from bots.ultra import kb
from kb import KB, Boolean, Integer

kb = KB()


class Bot:
    __RANKS = ["a", "t", "k", "q", "j"]


    def __init__(self):
        # kb = KB()

        pass

    def returnMove(self, state):
        moves = state.moves()
        trump_suit = state.get_trump_suit()
        whose_turn = state.whose_turn()
        leader = state.leader()


        played_card = state.get_opponents_played_card()

        if Deck.get_suit(played_card) == trump_suit:  # Check if played card is trump
            for move in moves:
                candidate_card, _ = move
                if candidate_card != None:
                    if Deck.get_suit(
                            candidate_card) == trump_suit:  # Still not checking for the lowest possible trump card
                        if candidate_card % 5 < played_card % 5:
                            return (candidate_card, None)

            lowest_card, _ = moves[0]
            for move in moves:
                candidate_card, _ = move
                if candidate_card != None:
                    if Deck.get_suit(
                            candidate_card) != trump_suit:  # Logic will still give exception if nothing is present other than trump cards, which is absurd, because that is not possible (think about it)
                        if candidate_card % 5 > lowest_card % 5:
                            lowest_card = candidate_card

            return (lowest_card, None)

        for move in moves:  # Else try to find a stronger card of same suit
            candidate_card, _ = move
            if candidate_card != None:
                if Deck.get_suit(candidate_card) == Deck.get_suit(played_card):
                    if candidate_card % 5 < played_card % 5:
                        return (candidate_card, None)

        for move in moves:  # Else try to find a a card from trump suit
            candidate_card, _ = move
            if candidate_card != None:
                if Deck.get_suit(candidate_card) == trump_suit:
                    return (candidate_card, None)

        lowest_card, _ = moves[0]

        for move in moves:  # By this position, losing the trick is certain, so we try and find the lowest card
            candidate_card, _ = move
            if candidate_card != None:
                if Deck.get_suit(candidate_card) != trump_suit:
                    if candidate_card % 5 > lowest_card % 5:
                        lowest_card = candidate_card

        if Deck.get_suit(lowest_card) == trump_suit:
            for move in moves:
                candidate_card, _ = move
                if candidate_card != None:
                    if candidate_card % 5 > lowest_card % 5:
                        lowest_card = candidate_card

        return (lowest_card, None)

    def get_move(self, state):
        whose_turn = state.whose_turn()
        leader = state.leader()
        trump_suit = state.get_trump_suit()

        if whose_turn == leader:
            global kb
            moves = state.moves()

            for move in moves:
                if move[0] is None:
                    return move

            for move in moves:
                if move[1] is not None:
                    return move

            if state.get_points(whose_turn) >= 45:
                for move in moves:
                    if Deck.get_suit(move[0]) == trump_suit:
                        return move


            random.shuffle(moves)
            for move in moves:
                if not self.kb_consistent(state, move):
                    print "Strategy Applied"
                    return move


            chosen_move = moves[0]
            for index, move in enumerate(moves):
                if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
                    chosen_move = move

            return chosen_move

            # lowest_card, _ = moves[0]
            # for move in moves:
            #     candidate_card, _ = move
            #     if candidate_card != None:
            #         if Deck.get_suit(candidate_card) != trump_suit:
            #             if candidate_card % 5 > lowest_card % 5:
            #                 lowest_card = candidate_card
            #
            # if Deck.get_suit(lowest_card) == trump_suit:
            #     for move in moves:
            #         candidate_card, _ = move
            #         if candidate_card != None:
            #             if candidate_card % 5 > lowest_card % 5:
            #                 lowest_card = candidate_card
            # return (lowest_card, None)

        else:
            return self.returnMove(state)

    def kb_consistent(self, state, move):
    # type: (State, move) -> bool

        index = move[0]

        if (Deck.get_suit(index) == state.get_trump_suit()):
            return True

        if (Deck.get_rank(index) == "A"):
            return False

        kb = self.prepareKB(state)

        load.strategy_knowledge(kb)

        variable_string = "pc" + str(index)
        strategy_variable = Boolean(variable_string)

        kb.add_clause(~strategy_variable)

        return kb.satisfiable()

    def prepareKB(self, state):
        readyKB = KB()

        for card in state.get_perspective(self):
            index = -1
            if card == "P1W":
                index = state.get_perspective(self).index("P1W")
            if card == "P2W":
                index = state.get_perspective(self).index("P2W")

            if index != -1:
                tempString = self.__RANKS[index % 5]
                tempString += str(index % 5)
                readyKB.add_clause(Boolean(tempString))

        return readyKB
