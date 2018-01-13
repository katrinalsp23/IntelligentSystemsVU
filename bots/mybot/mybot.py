"""
MyBot --
"""

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
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # All legal moves
        moves = state.moves()
        chosen_move = moves[0]

        # If the opponent has played a card
        if state.get_opponents_played_card() is not None:
            moves_same_suit = []

            # Get all moves of the same suit as the opponent's played card
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
                    moves_same_suit.append(move)

            # If mybot has cards of the same suit as opponent's card
            if len(moves_same_suit) > 0:
                # Take out the first higher card, if there is one
                higher_ranked_same_suit = False
                for index, move in enumerate(moves_same_suit):
                    if move[0] is not None and moves_same_suit[0][0] % 5 <= state.get_opponents_played_card() % 5:
                        chosen_move = move
                        higher_ranked_same_suit = True
                # Take out the first card with the same suit, if none are bigger than opponent's
                if not higher_ranked_same_suit:
                    chosen_move = moves_same_suit[0]
                return chosen_move
            # If mybot does not have cards of the same suit
            else:
                moves_trump_suit = []
                for index, move in enumerate(moves):
                    if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                        moves_trump_suit.append(move)
                # Choose any trump, if mybot has any
                if len(moves_trump_suit) > 0:
                    chosen_move = moves_trump_suit[0]
                    return chosen_move

            # If mybot does not have the same suit and has not trumps
            # Get move with lowest rank available, of any suit
            for index, move in enumerate(moves):
                if move[0] is not None and move[0] % 5 >= chosen_move[0] % 5:
                    chosen_move = move

        # If opponent has not played a card
        else:
            # Get move with highest rank available, of any suit
            for index, move in enumerate(moves):
                if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
                    chosen_move = move

        # Return the choice
        return chosen_move