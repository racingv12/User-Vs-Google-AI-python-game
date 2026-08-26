import google.generativeai as genai
import random
import os
import sys
import time
genai.configure(api_key="YOUR_API_KEY_HERE")
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"





color_codes = {
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "purple": "\033[35m",
    "orange": "\033[38;5;214m",  # orange is not a standard ANSI color
    "reset": "\033[0m"
}





class Card:
    suits = [f'{color_codes["red"]}Hearts ♥{color_codes["reset"]}', 
    f'{color_codes["red"]}Diamonds ♦{color_codes["reset"]}', 
    'Clubs ♣ ', 
    'Spades ♠']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    def __init__ (self, suits, rank):
        # Innitializig all the cards in poker
        self.suits = suits
        self.rank = rank
    def __repr__(self):
        return f"{self.rank} of {self.suits} "

class Deck:
    def __init__(self,):
        
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        random.shuffle(self.cards) 
    
    def deal (self, num_cards):
        """ Deals cards"""
        dealt_cards = []
        
        for _ in range(num_cards): # removes from the cards list and adds it to dealt cards 
            if self.cards:
                dealt_cards.append(self.cards.pop()) 
        
        return dealt_cards
        
    def shuffle(self):
        random.shuffle(self.cards)
        
        
        
        
        
        
class Hand:
    def __init__(self, cards):
        # ensure proper hand management
        if not cards:
            raise ValueError (" A hand must Contain Cards") 
        if not all(isinstance(card, Card) for card in cards):
            raise ValueError ("All elements must be a real card )  ")
        self.cards = sorted(cards, key = lambda card: card.rank)
    
    def rank_counts(self):
        """ Returns a distionary of ranks (usefull for evaluating hands ) """
        count = {}
        for card in self.cards:
            count[card.rank] = count.get(card.rank, 0) + 1
        
        return count
        
    def suit_counts(self):
        """ Returns a dictionary of suits """
        count = {}
        for card in self.cards:
            count[card.rank] = count.get(card.rank, 0) + 1
        
        return count
    
    def is_straight(self):
        if len(self.cards) < 5:
            return False
        
        ranks = sorted(Card.ranks.index(card.rank) for card in self.cards)
        # Regular straight
        if ranks[-1] - ranks[0] == 4 and len(set(ranks)) == 5:
            return True

        # Ace-low straight (A, 2, 3, 4, 5)
        if set(ranks) == {0, 1, 2, 3, 12}:
            return True
        
        return False
        
    def is_flush(self):
        """Checks if the hand is a flush (5 equal suits )"""
        return len(self.suit_counts()) == 1
        
    def evaluate (self):
        """ Checks your hand and gives a ranking """
        counts = list(self.rank_counts().values())
        is_straight = self.is_straight()
        is_flush = self.is_flush()

        if is_straight and is_flush:
            # Check for Royal Flush (10, J, Q, K, A of same suit)
            if self.cards[-1].rank == 'A':
                return "Royal Flush"
            return "Straight Flush"
        if 4 in counts:
            return "Four of a Kind"
        if 3 in counts and 2 in counts:
            return "Full House"
        if is_flush:
            return "Flush"
        if is_straight:
            return "Straight"
        if 3 in counts:
            return "Three of a Kind"
            
        if counts.count(2) == 2:
            return "Two Pair"
            
        
        return "High Card"
        
        
class Player:
    def __init__ (self, name, stack = 10000):
        self.name = name
        self.hand = []
        self.stack = stack
        self.current_bet = 0 # amount user has on the table  
    
    def receive_cards(self, cards):
        self.hand.extend(cards)
    
    def show_hand(self):
        return ', '.join(str(card) for card in self.hand) 
    
    def bet (self, amount):
        """Placing a bet  """
        if amount > self.stack:
            raise ValueError(" not enough money ")
        self.stack -= amount
        self.current_bet += amount
    
    def call(self, amount):
        """ Calls the current stack """
        if self.stack < amount:
            raise ValueError(" not enough money ")
        self.stack -= amount
        self.current_bet = amount
    
    def raise_bet(self, amount):
        """Raise the current bet """
        if self.stack < amount:
             raise ValueError(" not enough money ")
        self.stack -= amount
        self.current_bet += amount
    
    def fold(self):
        """Fold, and exit the betting round"""
        self.hand = [] # dicarding the hand
        self.current_bet = 0
        
        
        
        
        
# ranking system 
def get_hand_rank(hand_type):
    """Convert hand type to numerical rank for comparison"""
    rankings = {
        "Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "One Pair": 2,
        "High Card": 1
    }
    return rankings.get(hand_type, 0)

def get_high_card(cards):
    """Get the highest card value for tie-breaking"""
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                  '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return max(rank_values[card.rank] for card in cards)





class Game:
    def __init__(self, players):
        self.players = players 
        self.deck = Deck()
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []
    
    
    def start_game(self):
        """ Starting Game and handling game flow"""
        os.environ["GRPC_VERBOSITY"] = "ERROR"
        os.environ["GLOG_minloglevel"] = "2"
        
        os.system("cls")

        print('Welcome To POKER AI ')
        
        intro = input("press ENTER to play or 'g' for a guide ").lower().strip()
        
        if intro == 'g':
            os.system("cls")
            
            print(f"{color_codes['blue']}Poker is a game where players bet on the strength of their hands, with the goal of winning chips or money from other players. To start, each player is dealt two private cards (known as hole cards). Then, five community cards are dealt face-up in the center of the table in stages: three cards are dealt together (the flop), followed by one card (the turn), and finally one more card (the river). Players make the best five-card hand they can using their hole cards and the community cards. The hand rankings from highest to lowest are: Royal Flush, Straight Flush, Four of a Kind, Full House, Flush, Straight, Three of a Kind, Two Pair, One Pair, and High Card. Players take turns betting in rounds, with options to check, bet, raise, or fold, depending on the strength of their hand and strategy. The winner is the player with the best hand at the showdown, or the last player remaining after all others have folded.You are playing as Alice .However, you are playing againts two other players that are both being controlled by gemini AI! Make humans proud...{color_codes['reset']} ")
            ex_user = input("press Enter to play or 'q ' to quit: ")
            
            if ex_user == 'q':
                os.system("cls")
                sys.exit()
            else:
                self.gameplay()
            
        else:
            self.gameplay()
            
            
            
    
    def gameplay(self):
        os.system("cls")
            
        self.deal_hands()
        self.betting_round()
        
        # Deal community cards
        time.sleep(1)
        print(" !!Community Cards Incoming!! ")
        time.sleep(2.5)
        os.system("cls")
        self.deal_community_cards(3)  # Flop
        self.betting_round()
        
        
        self.deal_community_cards(1)  # Turn
        self.betting_round()
        
        self.deal_community_cards(1)  # River
        self.betting_round()
        
        # Evaluate hands and determine the winner
        
        
        
    
        
        
        print("Evaluating Hands...")
        time.sleep(2)
        os.system("cls")
        self.deal_community_cards(0)  # River

        self.evaluate_hands()
        
        
    def deal_hands (self):
        """Deal two hole cards to each player."""
        for player in self.players:
            player.receive_cards(self.deck.deal(2))
            if player.name == f"{playername}":
                print(f"{player.name} has {player.show_hand()}")
            else:
                print(f"{player.name} has recieved their cards")
    
                
    
                
    
    def deal_community_cards(self, num_cards):
        
        new_cards = self.deck.deal(num_cards)
        self.community_cards.extend(new_cards)
        print(f"Community cards: {', '.join(str(card) for card in self.community_cards)}")
    
    

    
        
    def betting_round(self):
        """handles the betting round"""
        active_players = [player for player in self.players if player.hand]
        if len(active_players) <= 1:
            return  # Round ends if only 1 or 0 players remain
        
        # Track the highest bet and which players have acted since last raise
        highest_bet = 0
        players_acted = set()
        
        while True:
            for player in active_players:
                
                if not player.hand: # skipping folded players 
                    continue 
                    
                    
                # If everyone has acted since last raise and bets are equal, end round
                if len(players_acted) == len([p for p in active_players if p.hand]) and \
                   all(p.current_bet == highest_bet for p in active_players if p.hand):
                   return
                
                amount_to_call = highest_bet
                
                options = ['fold']
                
                if amount_to_call > 0:
                    options.append('call')
                    
                if amount_to_call < player.stack:
                    options.append('raise')
                if amount_to_call == 0:
                    options.append('check')
                    options.append('bet')
                
                
                if player.name == 'Bob' or player.name == 'Charlie':
                    try:
                        # AI logic for Bob
                        hand_description = (f"Your cards are {player.show_hand()}, "
                                         f"community cards: {', '.join(str(card) for card in self.community_cards)}. "
                                         f"Current pot: {self.pot}, amount to call: {amount_to_call}, "
                                         f"stack: {player.stack}.")
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        prompt = f"You are playing poker. {hand_description} What action will you take(one word answer)? Options: {', '.join(options)} (you can't check)" # This Prompt is used to give the AI an undrestanding of what's happening, and makes a one word decision based of what it knows 
                        response = model.generate_content(prompt)
                        action = response.text.lower().strip()
                        print(f"{player.name} chose: {action}")
                    except:
                        print("AI response timeout. Defaulting to 'fold'.")
                        action = "fold"
                else:
                    # Human Player Logic
                    
                    print(f"\n{player.name}")
                    print(f" You have {player.show_hand()}")
                    print(f"Your stack: {player.stack}")
                    print(f"Your current bet ; {player.current_bet}")
                    print(f"Current Pot : {self.pot}")
                    print(f"Avaible actions : {', '.join(options)}")
                    action = input("Choose your action: ").lower()
                
                #handling actions
                try:
                    if action == 'fold':
                        player.fold()
                        active_players.remove(player)
                        if len(active_players) <= 1:
                            return
                    elif action == 'check':
                        if amount_to_call == 0:
                            players_acted.add(player)
                        else:
                            print("Invalid action")
                    
                    elif action == 'call':
                        if amount_to_call > 0:
                            player.call(amount_to_call)
                            self.pot += amount_to_call
                            player.stack -= amount_to_call
                        players_acted.add(player)
                    
                    elif action == 'bet':
                        if amount_to_call == 0:
                            if player.name == 'Bob' or player.name == 'Charlie':  # AI players
                                try:
                                    # AI betting logic
                                    hand_description = (
                                            f"Your cards are {player.show_hand()}, "
                                            f"community cards: {', '.join(str(card) for card in self.community_cards)}. "
                                            f"Current pot: {self.pot}, amount to call: {amount_to_call}, "
                                            f"stack: {player.stack}."
                                    )
                                    model = genai.GenerativeModel("gemini-1.5-flash")
                                    prompt = (f" you are player poker. {hand_description}.  How much do you want t bet (only write the number, nothig else )?") # Allows AI to choose the about it wants to bet
                                    response = model.generate_content(prompt)
                                    bet_amount = response.text.strip()
                                    
                                    try:
                                        bet_amount = int(bet_amount)
                                    except ValueError:
                                        print(f"Invalid response: {bet_amount}")
                                        bet_amount = 0 
                                        
                                    print(f"{player.name} will bet {bet_amount}")
                                    
                                    
                                except Exception as e:
                                    print(f"AI response error: {e}. Defaulting to 'fold'.")
                                    bet_amount = 0  # Default to no bet


                            else:
                                try:
                                    bet_amount = int(input("How much would you like to bet? "))
                                except ValueError:
                                    print("Invalid input. Please enter a numeric value.")
                                    continue
                            
                            
                            
                            if bet_amount <= player.stack and bet_amount > 0:
                                player.bet(bet_amount)
                                self.pot += bet_amount
                                highest_bet = player.current_bet
                                players_acted.clear()
                                players_acted.add(player)
                            else:
                                print("Not enough money")
                                continue
                        else:
                            print("Invalid action - cannot bet when there's already a bet")
                            continue
                            

                            
                        
                    
                    elif action == "raise" :
                        if player.name == 'Bob' or player.name == 'Charlie':
                            try:
                                # AI logic for Bob and Charlie
                                hand_description = (
                                    f"Your cards are {player.show_hand()}, "
                                    f"community cards: {', '.join(str(card) for card in self.community_cards)}. "
                                    f"Current pot: {self.pot}, amount to call: {amount_to_call}, "
                                    f"stack: {player.stack}."
                                )
                                model = genai.GenerativeModel("gemini-1.5-flash")
                                prompt = (
                                    f"You are playing poker. {hand_description} "
                                    f"How much would you like to raise(one word answer )? (You must raise at least double the pot.)"
                                )
                                response = model.generate_content(prompt)
                                raise_amount = response.text.strip()
                    
                                # Attempt to parse raise amount
                                try:
                                    raise_amount = int(raise_amount)
                                except ValueError:
                                    print(f"Invalid AI response: '{raise_amount}'. Defaulting to 'fold'.")
                                    raise_amount = 0  # Treat invalid raise as fold
                    
                                print(f"{player.name} will raise: {raise_amount}")
                    
                            except Exception as e:
                                print(f"AI response error: {e}. Defaulting to 'fold'.")
                                raise_amount = 0  # Default to no raise
                        else:
                            # Human player input for raise amount
                            try:
                                raise_amount = int(input("How much would you like to raise to? "))
                            except ValueError:
                                print("Invalid input. Please enter a numeric value.")
                                continue
                    
                        # Validate raise amount
                        min_raise = max(highest_bet * 2, self.pot * 2)  # Minimum is double the pot or the current highest bet
                        if raise_amount >= min_raise and raise_amount <= player.stack + player.current_bet:
                            additional_amount = raise_amount - player.current_bet
                            player.raise_bet(additional_amount)
                            self.pot += additional_amount
                            highest_bet = raise_amount
                            players_acted.clear()  # Reset because the action has changed
                            players_acted.add(player)
                        else:
                            print(f"Invalid raise amount. Must be at least {min_raise} and no more than your stack.")
                            continue
                                            

                    elif action not in options:
                        print("Invalid Input")
                    
                    
                    else:
                        print('Invalid Action')
                        continue
                    
                    print(f"POT : {self.pot}")
                
                except ValueError as e:
                    print(f"Error : {e}")
                    continue
            
                    
                        
                    
                    
    def perform_action(self,player, action):
        """ Performing the action wanted from the user"""
        try:
            if action == "bet":
                bet_amount = int(input("How much would you like to bet? "))
                player.bet(bet_amount)
                self.pot += bet_amount
                self.current_bet = bet_amount
            elif action == "call":
                player.call(self.current_bet)
                self.pot += self.current_bet
            elif action == "raise":
                raise_amount = int(input("How much would you like to raise? "))
                player.raise_bet(raise_amount)
                self.pot += raise_amount
                self.current_bet += raise_amount
            elif action == "fold":
                player.fold()
            else:
                print("Inavild Input (fold)")
                player.fold()
        except ValueError as e:
            print(f"Error: {e}. Try again.")
    
    def evaluate_hands(self):
        """Evaluate all hands and decide the final winner """
        active_players = [player for player in self.players if player.hand]
        if not active_players:
            print("No active players remaining.")
            
            return

        # Store player hands and their evaluations
        player_hands = []
        for player in active_players:
            full_hand = player.hand + self.community_cards
            hand = Hand(full_hand)
            hand_type = hand.evaluate()
            hand_rank = get_hand_rank(hand_type)
            high_card = get_high_card(full_hand)
            player_hands.append((player, hand_type, hand_rank, high_card))

        # Sort by hand rank (primary) and high card (secondary)
        player_hands.sort(key=lambda x: (x[2], x[3]), reverse=True)

        # Print all hands
        print("\nFinal hands:")
        for player, hand_type, _, _ in player_hands:
            print(f"{player.name}: {player.show_hand()} - {hand_type}")

        # Determine winner(s)
        winners = []
        best_rank = player_hands[0][2]
        best_high_card = player_hands[0][3]

        for player, hand_type, rank, high_card in player_hands:
            if rank == best_rank and high_card == best_high_card:
                winners.append(player)

        # Award pot
        if len(winners) == 1:
            winner = winners[0]
            winner.stack += self.pot
            print(f"\n{winner.name} wins pot of {self.pot} with {player_hands[0][1]}")
        else:
            split_amount = self.pot // len(winners)
            print(f"\nSplit pot of {self.pot} between {len(winners)} players:")
            for winner in winners:
                winner.stack += split_amount
                print(f"{winner.name} receives {split_amount}")

        # Reset pot and community cards for next hand
        self.pot = 0
        self.community_cards = []
        for player in self.players:
            player.hand = []
            player.current_bet = 0
    
    


        
        
        
if __name__ == "__main__":
    
    #Loading Screen 
    width = 30
    loading_text = "Loading..."
    
    for i in range(width + 1):
        filled = '#' * i
        empty = ' ' * (width - i)
        sys.stdout.write(f"{color_codes['blue']}\r[{filled}{empty}] {loading_text}{color_codes['reset']}")
        sys.stdout.flush()
        
        # Simulate delay with a busy wait (reduce the number for faster loading)
        for _ in range(1000000):  
            pass
    
    # Clear the loading bar by overwriting it with spaces
    sys.stdout.write(f"\r{' ' * (width + len(loading_text) + 4)}\r")
    sys.stdout.flush()
    
    # Continue with the rest of the script
    print("\n")
    os.system('cls')

    
    # Game initialization
    playername = input("Give me your name to begin: ")
    player1 = Player(f"{playername}", stack = 10000)
    player2 = Player("Bob", stack = 10000)
    player3 = Player("Charlie", stack = 10000)
    
    
    game = Game([player1,player2,player3])
    game.start_game()