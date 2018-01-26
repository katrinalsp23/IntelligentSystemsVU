"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""
#TODO: Make functions get_lowest_trump, get_lowest etc. to make shit easier
# Import the API objects
from api import State, Deck
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """
        moves = state.moves()
        trump_suit = state.get_trump_suit()
        whose_turn = state.whose_turn()
        leader = state.leader()

        if whose_turn == leader:
            lowest_card, _ = moves[0]

            for move in moves:
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
            # All legal moves
            # rank = {}
            # for move in moves:
            #     candidate_card, _ = move
            #     rank.append(candidate_card % 5)
        else:
            played_card = state.get_opponents_played_card()

            if Deck.get_suit(played_card) == trump_suit: #Check if played card is trump
                for move in moves:
                    candidate_card, _ = move
                    if candidate_card != None:
                        if Deck.get_suit(candidate_card) == trump_suit: #Still not checking for the lowest possible trump card
                            if candidate_card % 5 < played_card % 5:
                                return (candidate_card, None)

                lowest_card, _ = moves[0]
                for move in moves:
                    candidate_card, _ = move
                    if candidate_card != None:
                        if Deck.get_suit(candidate_card) != trump_suit: #Logic will still give exception if nothing is present other than trump cards, which is absurd, because that is not possible (think about it)
                            if candidate_card % 5 > lowest_card % 5:
                                lowest_card = candidate_card

                return (lowest_card, None)


            for move in moves: #Else try to find a stronger card of same suit
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

            for move in moves:
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


        # print state.get_deck().get_card_states()
        # Return a random choice
        return (lowest_card, None)