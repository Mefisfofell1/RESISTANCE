import random


class Player:
    def __init__(self, nickname):
        self.nick = nickname
        self.is_spy = False


class Game:
    def __init__(self):
        self.round_number = 0
        self.players_number = 0
        self.spies_number = 0
        self.host = Player('')
        self.game_set = []
        self.nicks_list = []
        self.players_list = []
        self.spies_list = []
        self.rebels_list = []

    def add_player(self, gamer):
        if self.players_number == 0:
            self.host = gamer
        self.nicks_list.append(gamer.nick)
        print('i wrote')
        self.players_list.append(gamer)
        self.rebels_list.append(gamer)
        self.players_number += 1

    def remove_player(self, gamer):
        self.players_list.remove(gamer)
        self.players_number -= 1
        if self.host.nick == gamer.nick:
            if self.players_number == 0:
                print('All players left')
            else:
                self.host = self.players_list[0]

    def distribution_of_spies(self):
        while len(self.spies_list) < self.spies_number:
            spy = random.choice(self.rebels_list)
            self.rebels_list.remove(spy)
            self.spies_list.append(spy)
            spy.is_spy = True


# def rounds_passing:


def lobby_assemble(game, players_max, players_min, playing_sets, spies_numbers):
    # Resetting parameters without changing nicknames
    game.spies_list = []
    game.rebels_list = []
    for element in game.players_list:
        game.rebels_list.append(element)

    while game.players_number <= players_max:
        request = input()

        # Unique control of nicks
        if request[0:4] == 'nick':
            if game.nicks_list.count(request.replace("nick.", "", 1)) == 0:
                game.add_player(Player(request.replace("nick.", "", 1)))
                print(game.players_number)
                print('Hello,', game.players_list[game.players_number - 1].nick)
            else:
                print("Someone's already using this nickname")
                continue

        # Start before reaching max amount of players
        elif request.find('start') != -1:
            if game.players_number < players_min:
                print('You need', players_min - game.players_number,
                      'more players to start')
            else:
                game.round_number += 1
                game.game_set = playing_sets[game.players_number - players_min]
                game.spies_number = spies_numbers[game.players_number -
                                                  players_min]
                if game.players_number == players_min:
                    print("You're perverts")
                break

        # Error in lobby creating
        else:
            print('ERROR ', request)
            break

            # Reaching max amount of players
        if game.players_number == players_max:
            game.round_number += 1
            game.game_set = playing_sets[game.players_number - players_min]
            game.spies_number = spies_numbers[game.players_number - players_min]
            print("You've reached maximum amount of players")

    game.distribution_of_spies()


# Started values
min_players_number = 5
max_players_number = 10
victory_score = 3
spies_sets = [2, 2, 3, 3, 3, 4]
game_sets = [[2, 3, 2, 3, 3], [2, 3, 3, 3, 4], [2, 3, 3, 4, 4],
             [3, 4, 4, 5, 5], [3, 4, 4, 5, 5], [3, 4, 4, 5, 5]]
game1 = Game()
lobby_assemble(game1, max_players_number, min_players_number, game_sets, spies_sets)
for man in game1.players_list:
    print(man.nick, "Is he a spy?", man.is_spy)
# print(game1.host.nick)
# print(game1.nicks_list)
# print(game1.players_number)
print(game1.players_list)
print(len(game1.players_list))
print(game1.game_set)
print(game1.spies_number)

