import random


class Player:
    def __init__(self, nickname):
        self.nick = nickname
        self.is_spy = False
        self.is_leader = False


class Game:
    def __init__(self):
        self.round_number = 0
        self.players_number = 0
        self.spies_number = 0
        self.host = Player('')
        self.current_leader = Player('')
        self.set = []
        self.nicks_list = []
        self.players_list = []
        self.spies_list = []
        self.rebels_list = []

    def add_player(self, gamer):
        # Host's appointment
        if self.players_number == 0:
            self.host = gamer
            self.current_leader = gamer
            gamer.is_leader = True

        # Adding player to the game
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

            # Cleaning rebels list from spies and adding spies to spies list
            self.rebels_list.remove(spy)
            self.spies_list.append(spy)
            spy.is_spy = True

        # Writing to spies of other spies nicknames
        for spy in self.spies_list:
            for spy_name in self.spies_list:
                print(spy_name.nick)


def take_vote(gamer):
    print(gamer.nick, "do you agree with the group composition")
    request = input()
    if request == 'Yes':
        return 1
    elif request == 'No':
        return 0
    else:
        print('ERROR IN TAKE_VOTE')


def group_creating(game):
    print(game.current_leader.nick, 'need to choose group of',
          game.set[game.round_number-1], 'members')
    squad = []
    while len(squad) < game.set[game.round_number-1]:
        request = input()

        # Control of nicknames correctness
        if request[0:4] == 'nick':
            if request.replace("nick", "", 1) in game.nicks_list:
                squad.append(request.replace("nick", "", 1))
            else:
                print("Which nickname is correct? Think,",
                      game.current_leader.nick, "think!")

        # Error in group creating
        else:
            print(request)
            print('ERROR IN GROUP_CREATING', request)
            break

    return squad


def voting(game):
    squad = group_creating(game)
    print("Leader's choice", ', '.join(squad))

    # Counting of voting results
    voting_result = 1

    for gamer in game.players_list:
        voting_result += take_vote(gamer)
    print(voting_result, "players voted for and",
          game.players_list-voting_result, "players voted against")


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
            if game.nicks_list.count(request.replace("nick", "", 1)) == 0:
                game.add_player(Player(request.replace("nick", "", 1)))
                print(game.players_number)
                print('Hello,', game.players_list[game.players_number - 1].nick)
            else:
                print("Someone's using this nickname")
                continue

        # Start before reaching max amount of players
        elif request.find('start') != -1:
            if game.players_number < players_min:
                print('You need', players_min - game.players_number,
                      'more players to start')
            else:
                game.round_number += 1
                game.set = playing_sets[game.players_number - players_min]
                game.spies_number = spies_numbers[game.players_number -
                                                  players_min]
                if game.players_number == players_min:
                    print("You're perverts")
                break

        # Error in lobby creating
        else:
            print(request)
            print('ERROR in lobby_assemble', request)
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
print(game1.set)
print(game1.spies_number)
print(group_creating(game1))

