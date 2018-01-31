#!/usr/bin/env python
"""
This bot has basically two mode: (1) playing a card when it is the bot's turn and (2) playing a card when it is the
opponent's turn and a card has been played.

Let's first talk about mode 1. As we get into this mode, we first check if there is a possibility of a trump
exchange. If there is such a possibility, we simply return this move and the work of the bot ends. We then check for
any possibly marriage, and proceed in the same way as trump exchange. If none of the above is true, we try the
strategy that has been implemented by using Knowledge Base. The following is the strategy of the KB:

"Try to play a card of the suit given that all the cards of the same suit having higher value than this card have
already been played.For example, if we have a King of Clubs, we play that card if and only if 10 and Ace of Clubs
have been played."

When this KB is checked for satisfaction, this strategy is not evoked first. Before that, we check if that card is a
trump card, and if this is true, then we don't play that card. Remember, for a card to be played, we have to return
false instead of true as a card would only be played if the model is not satisfiable with negative of that card. We
then check if the card is an Ace, and if it is we play it. This is because the current strategy is not capable of
playing an Ace from any suit. After this, we apply the above mentioned strategy.

If all goes well, the message 'Strategy Applied' is printed on the console. If somehow these tests fail,
we play either the highest possible card or the lowest possible card. Multiple tournaments have shown that both these
strategies have similar results, hence any of these can be used to play a card.

Apart from this, there is check to see if the score of our bot has exceeded a particular threshold. From this point
on we can play with a strong bias towards gaining maximum points in minimum time. So we try to play maximum number of
trump cards onto the table, because they have a higher chance of winning.

Mode 2 is chosen when we have to reply to a card played by the opponent. This is a relatively simple strategy. We
first check if the played card is from the trump suit. If it is from the trump suit, we try to find a trump card with
value higher than the played card. If such a card is not found, we can predict that we loose that trick,
hence we play the lowest possible card. If the played card is not from the trump suit, we first check for a card
stronger than that card, then we look for a trump card to win that trick. If these conditions are not fulfilled,
it can be predicted that we loose that trick, hence we simply play the lowest non-trump card. Again, if we don't have
such a card, we play the lowest possible card.

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

    def get_move(self, state):
        whose_turn = state.whose_turn()
        leader = state.leader()
        trump_suit = state.get_trump_suit()

        if whose_turn == leader:
            global kb
            moves = state.moves()

            # We look for a possible trump exchange
            for move in moves:
                if move[0] is None:
                    return move

            # We look for a possible marriage
            for move in moves:
                if move[1] is not None:
                    return move

            # We compare the bot's points with the threshold value and decide on playing hard.
            if state.get_points(whose_turn) >= 45:
                for move in moves:
                    if Deck.get_suit(move[0]) == trump_suit:
                        return move


            random.shuffle(moves)
            for move in moves:
                if not self.kb_consistent(state, move):
                    print "Strategy Applied"
                    return move

            # We play the highest possible card if none of the cards in hand is entailed by the KB
            chosen_move = moves[0]
            for index, move in enumerate(moves):
                if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
                    chosen_move = move

            return chosen_move

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


    def returnMove(self, state):
        moves = state.moves()
        trump_suit = state.get_trump_suit()

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