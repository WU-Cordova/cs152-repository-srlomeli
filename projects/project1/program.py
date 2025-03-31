import copy
import random
from datastructures.bag import Bag
from projects.project1.card import Card, Face, Suit

class MultiDeck:
    """Represents a deck of multiple shuffled decks."""
    def __init__(self):
        self.deck_count = random.choice([2, 4, 6, 8])  # Random multi-deck count
        one_deck_list = [Card(face, suit) for suit in Suit for face in Face]
        self.cards = Bag(*(copy.deepcopy(one_deck_list) * self.deck_count))
    
    def deal_card(self):
        """Removes and returns a card from the deck."""
        card = random.choice(list(self.cards.distinct_items()))
        self.cards.remove(card)
        return card
    
class Game:
    """Handles the Blackjack game logic."""
    def __init__(self):
        self.deck = MultiDeck()
        self.player_cards = []
        self.dealer_cards = []
    
    def calculate_score(self, cards):
        """Calculates the best possible score for a given set of cards."""
        score = sum(card.face.face_value() for card in cards)
        num_aces = sum(1 for card in cards if card.face == Face.ACE)
        while score > 21 and num_aces > 0:
            score -= 10  # Convert an Ace from 11 to 1
            num_aces -= 1
        return score

    def deal_initial_cards(self):
        """Deals two cards to both the player and the dealer."""
        self.player_cards = [self.deck.deal_card(), self.deck.deal_card()]
        self.dealer_cards = [self.deck.deal_card(), self.deck.deal_card()]
    
    def display_game_state(self, show_dealer=False):
        """Displays the current state of the game."""
        player_score = self.calculate_score(self.player_cards)
        dealer_score = self.calculate_score(self.dealer_cards)
        print("\nYour cards:", ' '.join(str(card) for card in self.player_cards), f"(Score: {player_score})")
        if show_dealer:
            print("Dealer's cards:", ' '.join(str(card) for card in self.dealer_cards), f"(Score: {dealer_score})")
        else:
            print("Dealer's cards:", str(self.dealer_cards[0]), "[Hidden]")
    
    def player_turn(self):
        """Handles the player's turn."""
        while True:
            player_score = self.calculate_score(self.player_cards)
            if player_score > 21:
                print("Bust! You exceeded 21. Dealer wins.")
                return False  # Ends turn if 21 exceeded
            choice = input("Do you want to (H)it or (S)tand? ").strip().lower()
            if choice == 'h':
                new_card = self.deck.deal_card()
                self.player_cards.append(new_card)
                self.display_game_state()
            elif choice == 's':
                break
        return True
    
    def dealer_turn(self):
        """Handles the dealer's turn."""
        print("\nDealer's turn...")
        self.display_game_state(show_dealer=True)  # Reveal dealer's full hand before hitting
        while self.calculate_score(self.dealer_cards) < 17:
            new_card = self.deck.deal_card()
            self.dealer_cards.append(new_card)
            self.display_game_state(show_dealer=True)
            
            if self.calculate_score(self.dealer_cards) > 21:
                print("Dealer busts! You win!")
                return False  # Immediately end dealer's turn if they bust
    
    def determine_winner(self):
        """Determines the winner based on final scores."""
        player_score = self.calculate_score(self.player_cards)
        dealer_score = self.calculate_score(self.dealer_cards)
        print("\nFinal Results:")
        self.display_game_state(show_dealer=True)
        if player_score > 21:
            print("Bust! You exceeded 21. Dealer wins.")
        elif dealer_score > 21 or player_score > dealer_score:
            print("Congratulations! You win!")
        elif dealer_score > player_score:
            print("Dealer wins. Better luck next time.")
        else:
            print("It's a tie.")
    
    def play(self):
        """Main game loop."""
        while True:
            print("\nWelcome to Blackjack!")
            self.deck = MultiDeck()
            self.deal_initial_cards()
            self.display_game_state()
            
            if self.player_turn():
                if self.dealer_turn():
                    self.determine_winner()
            
            user_input = input("Would you like to play again? (Y/N): ").strip().upper()
            if user_input != 'Y':
                print("Thanks for playing!")
                break

if __name__ == '__main__':
    game = Game()
    game.play()
