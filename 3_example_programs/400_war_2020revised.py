"""
Card game of WAR
Uses several global variables to track card values but decks and players built
up during game execution.
There are 7 functions in total that allow the game play to be condensed into
a smaller logical unit towards the end of the file.
The actual game play is between lines 218 and 302 (and that's the short version).
Imagine how long that one loop would be if you tried to include ALL of the functionality
into a single giant loop and how confusing it would be if something went wrong!
"""

# Made a small improvment to this so that the cards would be displayed as the color they are; red for diamond and hearts, black for spades and clovers

import random

# Face value of cards
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
# Clubs, Diamonds, Spades, Hearts
card_suit = ['\u2663', '\u2666', '\u2660', '\u2665']

# Indexes to player list
PLAYER_1 = 0
PLAYER_2 = 1

# Indexes to card list
CARD_WEIGHT = 0
CARD_FACE = 1
CARD_SUIT = 2

# Maximum number of allowed turns before game ends
MAX_TURN_COUNT = 400


def build_deck(shuffle_count=7):
    """
        Build a deck of 52 cards and shuffle them
        for a game.
        Parameters:
        shuffle_count:
            int - Number of times to shuffle
        Returns:
            List of cards where a card is a list of
                [weight, face, suit]
    """
    # Build the deck by adding in each value with each suit
    deck = []
    for suit in range(len(card_suit)):
        for value in range(len(card_values)):
            card = [value, card_values[value], card_suit[suit], '\033[39m']
            deck.append(card)

    # Now loop through the number of shuffles to mix them up
    for unused_var in range(shuffle_count):
        random.shuffle(deck)

    # Return the deck
    return deck


def deal_cards(deck):
    """
        Provide a full deck (52 cards), and divvy them
        up into two player decks.
        Parameters:
            deck - List of cards
        Returns:
            A list of lists (one for each player)
    """
    # List of lists to hold player cards
    players = [[], []]

    # Split all the cards in the deck between each player
    for card_num in range(len(deck)):
        players[card_num % 2].append(deck[card_num])

    # Return the players decks
    return players


def game_over(player_decks):
    """
        Determines if either of the player decks are empty
        and if so, game is over.
        Parameters:
            player_decks -
                Decks for each player
        Returns:
            True if either deck is empty, False otherwise
    """
    return_value = False

    for deck in player_decks:
        if len(deck) == 0:
            print("GAME OVER")
            return_value = True
            break

    return return_value


def compare_cards(risk_cards):
    """
        Return index of winning card or -1 if tied
        Parameters:
        risk_cards -
            Cards that are in play
        Returns:
            Index of winning card, -1 in case of tie (war)
    """
    return_value = -1

    if risk_cards[PLAYER_1][CARD_WEIGHT] > risk_cards[PLAYER_2][CARD_WEIGHT]:
        return_value = PLAYER_1
    elif risk_cards[PLAYER_1][CARD_WEIGHT] < risk_cards[PLAYER_2][CARD_WEIGHT]:
        return_value = PLAYER_2

    return return_value


def prepend_cards(deck, cards):
    """
        Add cards to a deck. Insert at 0 so it's at the
        bottom of the deck.
        Parameters:
        deck -
            Player list of cards
        cards -
            List of cards to prepend to deck
    """
    for card in cards:
        deck.insert(0, card)


def format_risk_cards(risk_cards):
    return "(P1) {}{} vs. (P2) {}{}".format(
        ('\033[31m' if card_suit.index(risk_cards[PLAYER_1][CARD_SUIT]) % 2 else '\033[30m') + risk_cards[PLAYER_1][CARD_FACE], risk_cards[PLAYER_1][CARD_SUIT] + '\033[39m',
        ('\033[31m' if card_suit.index(risk_cards[PLAYER_2][CARD_SUIT]) % 2 else '\033[30m') + risk_cards[PLAYER_2][CARD_FACE], risk_cards[PLAYER_2][CARD_SUIT] + '\033[39m'
    )


def do_war(player_decks, turn_cards=3):
    """
    Do war happens when both players turn equally weighted cards
    and have to "war". War consists of turn_cards cards being played
    face down, then flipping again.
    This continues until someone wins or someone runs out of cards and
    has to forfeit.
    Parameters:
    player_decks -
        Player card decks
    turn_cards -
        Number of cards to play face down before continuing.
    Returns:
        Index of winner
    """
    return_value = []
    all_risk_cards = []
    current_risk_cards = []

    if len(player_decks[PLAYER_1]) < (turn_cards + 1):
        print("Player 1 forfiets WAR due to lack of cards.")
        player_decks[PLAYER_2].extend(player_decks[PLAYER_1])
        player_decks[PLAYER_1] = []
        return_value = PLAYER_2
    elif len(player_decks[PLAYER_2]) < (turn_cards + 1):
        print("Player 2 forfiets WAR due to lack of cards.")
        player_decks[PLAYER_1].extend(player_decks[PLAYER_2])
        player_decks[PLAYER_2] = []
        return_value = PLAYER_1
    else:
        # Each have enough to add to the risk cards, first collect face down
        for unused_counter in range(turn_cards):
            all_risk_cards.append(player_decks[PLAYER_1].pop())
            all_risk_cards.append(player_decks[PLAYER_2].pop())

        # Now get the final turn card
        current_risk_cards = [player_decks[PLAYER_1].pop(), player_decks[PLAYER_2].pop()]

        # Add these to the bounty as whomever wins gets all cards, face down and up
        all_risk_cards.extend(current_risk_cards)

        # Tell user what the war flip is (good reuse of format_risk_cards)
        print("WAR FLIP : {}".format(format_risk_cards(current_risk_cards)))

        # See who won... status is -1 for tie, otherwise index to players list for winner
        return_value = compare_cards(current_risk_cards)

        if return_value == -1:
            # In a tie AGAIN, we have to do it again...
            print("CONTINUE WAR.....")
            return_value = do_war(player_decks)

        # If we get here we know return value has a value that is NOT -1 and hence can
        # continue to move cards to winners pile.
        player_id = "Player1" if return_value == 0 else "Player2"

        print("{} won the war with {}{}".format(player_id, ('\033[31m' if card_suit.index(risk_cards[PLAYER_1][CARD_SUIT]) % 2 else '\033[30m') + current_risk_cards[return_value][CARD_FACE], current_risk_cards[return_value][CARD_SUIT]) + '\033[39m')
        prepend_cards(player_decks[return_value], all_risk_cards)

    # Return the index of whomever won the war so they can take original risk cards
    return return_value


"""
    Game starts below.......
"""
# Create a deck (shuffled)
playing_deck = build_deck()

# Deal the cards out
player_decks = deal_cards(playing_deck)

# General statistics to print at the end
game_turn = 0
war_count = 0
win_stats = [0, 0]

# Game ends when someone is out of cards....
while not game_over(player_decks):

    # Each loop through increment game count
    game_turn += 1

    # Current face up cards to compare
    risk_cards = [player_decks[PLAYER_1].pop(), player_decks[PLAYER_2].pop()]

    # String representation of risk cards
    played_cards = format_risk_cards(risk_cards)

    # Status is -1 for tie, otherwise index to players list for winner
    status = compare_cards(risk_cards)

    if status == -1:
        # War - Tie, have to break tie...
        print("{} : WAR! with {}".format(game_turn, played_cards))

        # Run the war, guaranteed a winner before it returns
        war_winner = do_war(player_decks)

        # Whoever won the war gets the initial risk cards
        prepend_cards(player_decks[war_winner], risk_cards)

        # Update stats
        war_count += 1
        win_stats[war_winner] += 1
    else:

        # Show results of round as we have a winner
        print("{} : {} - {}{} wins round".format(
            game_turn,
            played_cards,
            ('\033[31m' if card_suit.index(risk_cards[status][CARD_SUIT]) % 2 else '\033[30m') + risk_cards[status][CARD_FACE],
            risk_cards[status][CARD_SUIT] + '\033[39m'
        ))

        # Give winner the cards
        prepend_cards(player_decks[status], risk_cards)

        # Update stats
        win_stats[status] += 1

    if game_turn > MAX_TURN_COUNT:
        # At MAX_TURN_COUNT turns, just bail out or it may run too long
        print("Game exceeded {} turns! Auto quit....".format(MAX_TURN_COUNT))
        break

    if game_turn % 10 == 0:
        # Every 10th turn, show how many cards each player has
        print("P1 card count: {} , P2 card count: {}".format(len(player_decks[PLAYER_1]), len(player_decks[PLAYER_2])))


# Game has ended or aborted on MAX_TURN_COUNT so show general stats
print(f"STATS:\nP1 card count : {len(player_decks[PLAYER_1])}\nP2 card count {len(player_decks[PLAYER_2])}\nTurn Count: {game_turn}\nWar Count: {war_count}\nWin Stats [P1, P2]: {war_count}\nWINNER: {'P1' if len(player_decks[PLAYER_1]) > len(player_decks[PLAYER_2]) else 'P2' if len(player_decks[PLAYER_2]) > len(player_decks[PLAYER_1]) else 'No one.'}")
