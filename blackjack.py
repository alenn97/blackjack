import random
import logging
import sys

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
cards_value_low = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
cards_value_high = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

class Player():
	def __init__(self, name, balance):
		self.name = name
		self.balance = balance
		self.cards = []
		self.bet = 0
		self.stop = False
	def __repr__(self):
		return "Player: {name} \nBalance:{balance}".format(name = self.name, balance = self.balance)

	def add_bet(self, bet):
		self.bet = bet

	def get_score(self):
		score_soft = 0
		score_hard = 0
		for card in self.cards:
			score_low += cards_value_low[cards.index(card)]
			score_high += cards_value_high[cards.index(card)]
		if score_high > 21 or score_high == score_low:
			return [score_low]
		else:
			return [score_low, score_high]

	def call(self):
		self.cards.append(random.choice(cards))

	def stay(self):
		self.stop = True

	def double_down(self):
		self.bet = self.bet * 2
		self.call()
		self.stay()

	def split(self):
		pass

	def win_hand(self):
		score = self.get_score()
		if len(self.cards)==2 and score[1]==21:
			self.balance += self.bet * 1.5
		else:
			self.balance += self.bet
		print("Winner! Winner! Chicken dinner!")

	def lose_hand(self):
		self.balance -= self.bet



class Game():
	def __init__(self, players, minimum_bet):
		self.players = players
		self.minimum_bet = minimum_bet
	def __repr__(self):
		output = "Currently playing:\n"
		for player in self.players:
			output = output + "\t {name}: {balance}\n".format(name = player.name, balance = player.balance)
		return output

	def add_player(self, player):
		self.players.append(player)
	def remove_player(self, player):
		self.players.remove(player)

	def start(self):
		# Betting
		for player in self.players:
			bet = 0
			while bet < self.minimum_bet:
				bet = input("{name}, insert your bet: ".format(player.name))
				if bet < self.minimum_bet:
					logger.warning("The bet must be more or equal than {min_bet}".format(min_bet = self.minimum_bet))
			player.add_bet(bet)
		# Distributing first cards
		for player in self.players:
			player.call()
		dealer.call()
		for player in self.players:
			player.call()
		self.covered_card = random.choice(cards)

		print("Dealer: {cards} ---> {score}".format(cards = dealer.cards, score = dealer.get_score()))
		for player in self.players:
			print("{name}: {cards} ---> {score}".format(name = player.name, cards = player.cards, score = player.get_score()))

	def players_hand(self, player):
		print("{name}, it's your turn.".format(name=self.name))
		player.stop = False
		score = self.get_score()
		moves = 0
		if score == 21:
			print("Your cards are: {cards}".format(cards=self.cards))
			print('BLACKJAK!')
			self.stay()
		else:
			while ~self.stop:
				print('Your cards are: {cards}'.format(cards=self.cards))
				print('Your score is: {score}'.format(score=score))
				if score >= 21:
					self.stay()
				else:
					if moves == 0:
						print("What do you want to do? (call - stay - double down)")
						answer = input('')
						if answer == "stay": self.stay()
						if answer == "call": self.call()
						if answer == "double down": self.double_down()
					else:
						print("What do you want to do? (call - stay)")
						answer = input('')
						if answer == "stay": self.stay()
						if answer == "call": self.call()
						if answer == "double down": logger.warning("You have more than 2 cards. You can not double down.")
					moves += 1


	def dealer_hand(self, dealer):
		dealer.cards.append(self.covered_card)
		stop = False
		while stop == False:
			score = dealer.get_score()
			if len(score) > 1:
				if score[1] >= 17:
					stop = True
				else:
					dealer.call()
			else:
				if score[0] >= 16:
					stop = True
				else:
					dealer.call()



###
print("Welcome to SPPL's casino!")
n_players = input("Please, enter the number of players at the table: ")
players = []
for i in range(n_players):
	print("Player number " + str(i+1))
	player_name = input("Please, insert your name: ")
	player_balance = input("Please, insert your current balance: ")
	vars(player_name) = Player(player_name, player_balance)
	players.append(vars(player_name))

print("Thank you, all players have been registered.")
minimum_bet = 0
while minimum_bet <= 0:
	minimum_bet = input("Please choose the minimum bet for this game: ")
	if minimum_bet <= 0:
		logger.warning("The minimum bet must be more than 0.")

print("Thank you, we are now ready to start playing.\nGood luck!")
print("\n\n\n")

dealer = Player('dealer', float('inf'))
game = Game(players, minimum_bet)
game.start()
end = True
while end == True:
	for player in players:
		game.player_hand(player)
	game.dealer_hand(dealer)

	# Terminate hand
	print("This hand is ended.")
	answer = input("Do you want to continue playing? (Yes/No)")
	if answer == "Yes":
		answer = input("Do you want to add a player? (Yes/No)")
		if answer == "Yes":
			print("Player number " + str(len(players)+1))
			player_name = input("Please, insert your name: ")
			player_balance = input("Please, insert your current balance: ")
			vars(player_name) = Player(player_name, player_balance)
			game.add_player(var(player_name))
		answer = input("Do you want to remove a player? (Yes/No)")
		if answer == "Yes":
			player_name = input("Which player would you like to remove? \n")
			game.remove_player(var(player_name))
	else:
		end = False

print("\n\n\n")
print("The game is ended.")
for player in players:
	print(player)
