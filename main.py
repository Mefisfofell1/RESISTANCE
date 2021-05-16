import random


class Player:
    def __init__(self, nickname):
        self.nick = nickname
        self.is_spy = False
        self.is_leader = False


class Game:
    def __init__(self):
        self.leader_changes_to_stop = 5
        self.min_players = 5
        self.max_players = 10
        self.rebels_lucky_mission = 4
        self.spies_to_sabotage_lucky_mission = 2
        self.spies_sets = [2, 2, 3, 3, 3, 4]
        self.game_sets = [[2, 3, 2, 3, 3], [2, 3, 3, 3, 4], [2, 3, 3, 4, 4],
                          [3, 4, 4, 5, 5], [3, 4, 4, 5, 5], [3, 4, 4, 5, 5]]
        self.points_to_win = 3
        self.round_number = 0
        self.players_number = 0
        self.leader_changing_count = 0
        self.spies_number = 0
        self.spies_points = 0
        self.rebels_points = 0
        self.host = Player('')
        self.leaders_index = 0
        self.set = []
        self.nicks_list = []
        self.players_list = []
        self.spies_list = []
        self.rebels_list = []

    def add_player(self, gamer):
        # Host's appointment
        if self.players_number == 0:
            self.host = gamer
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

    def add_points(self, to_spies):
        if to_spies:
            self.spies_points += 1
            if self.spies_points == self.points_to_win:
                print('Spies won the game. Try not to be toxic after game')
                print('or not')

                # OPTION FOR HOST ONLY
                print('Do you want to play one more game?')
                if input() == 'YES':
                    lobby_assemble(self)
                else:
                    quit()
        else:
            self.rebels_points += 1
            if self.rebels_points == self.points_to_win:
                print("Spies won the game.")

                # OPTION FOR HOST ONLY
                print("Do you want to play one more game?")
                if input() == 'YES':
                    lobby_assemble(self)
                else:
                    quit()

    def distribution_of_spies(self):
        while len(self.spies_list) < self.spies_number:
            spy = random.choice(self.rebels_list)

            # Cleaning rebels list from spies and adding spies to spies list
            self.rebels_list.remove(spy)
            self.spies_list.append(spy)
            spy.is_spy = True

        # Writing spies nicknames to other spies
        for spy in self.spies_list:
            for spy_name in self.spies_list:
                print(spy_name.nick)

    def change_leader(self):
        # Changing index, if we passed all players
        if self.leaders_index == self.players_number - 1:
            self.leaders_index = 0
        else:
            self.leaders_index += 1

        # Resetting to zero leader_changing_count
        # if leader was changed too many times
        if self.leader_changing_count == self.leader_changes_to_stop:
            self.leader_changing_count = 0
        else:
            self.leader_changing_count += 1


def take_vote(gamer, is_mission):
    if is_mission:
        print(gamer.nick, "do you want to sabotage the mission?")
    else:
        print(gamer.nick, "do you agree with the group composition?")

    # Taking player's answer
    request = input()
    if request == 'Yes':
        return 1
    elif request == 'No':
        return 0
    else:
        print('ERROR IN TAKE_VOTE')


def group_creating(game):
    print(game.nicks_list[game.leaders_index], 'need to choose group of',
          game.set[game.round_number - 1], 'members')
    squad = []
    while len(squad) < game.set[game.round_number - 1]:
        request = input()

        # Control of nicknames correctness
        if request[0:4] == 'nick':
            if request.replace("nick", "", 1) in game.nicks_list \
                    and request.replace("nick", "", 1) not in squad:
                squad.append(request.replace("nick", "", 1))
            else:
                print("Which nickname is correct? Think,",
                      game.nicks_list[game.leaders_index], "think!")

        # Error in group creating
        else:
            print(request)
            print('ERROR IN GROUP_CREATING', request)
            break

    return squad


def lobby_assemble(game):
    # Resetting parameters without changing nicknames
    game.leader_changing_count = 0
    game.round_number = 1
    game.spies_points = 0
    game.rebels_points = 0
    game.spies_list = []
    game.rebels_list = []
    for element in game.players_list:
        game.rebels_list.append(element)

    while game.players_number <= game.max_players:
        request = input()

        # Unique control of nicks
        if request[0:4] == 'nick':
            # Reaching max amount of players
            if game.players_number == game.max_players:
                print("You've reached maximum amount of players")
                continue

            # Adding player to lobby
            if game.nicks_list.count(request.replace("nick", "", 1)) == 0:
                game.add_player(Player(request.replace("nick", "", 1)))
                print(game.players_number)
                print('Hello,', game.nicks_list[game.players_number - 1])
            else:
                print("Someone's using this nickname")
                continue

        # Start before reaching max amount of players
        elif request.find('start') != -1:
            if game.players_number < game.min_players:
                print('You need', game.min_players - game.players_number,
                      'more players to start')
            else:
                if game.players_number == game.min_players:
                    print("You're perverts")
                break

        # Error in lobby creating
        else:
            print(request)
            print('ERROR in lobby_assemble', request)

            # Need to change 'break' to 'quit'
            break

    game.set = game.game_sets[game.players_number - game.min_players]
    game.spies_number = game.spies_sets[game.players_number - game.min_players]
    game.distribution_of_spies()
    voting(game)


def voting(game):
    # OPTION FOR LEADER ONLY
    # Time to discuss the group
    while input() != 'start':
        continue

    # Creating group and writing about it
    squad = group_creating(game)
    print("Leader's choice", ', '.join(squad))

    # Counting of voting results
    voting_result = 0
    for gamer in game.players_list:
        voting_result += take_vote(gamer, False)
    yes_votes = voting_result
    no_votes = game.players_number - voting_result
    print(yes_votes, "players voted for and",
          no_votes, "players voted against")

    # Processing the results of voting
    if yes_votes > no_votes:
        game.change_leader()
        mission(game, squad)

    # Failing mission because leader was changed too many times
    elif game.leader_changing_count == game.leader_changes_to_stop:
        game.round_number += 1
        game.add_points(True)
        game.change_leader()
        voting(game)

    # Need to create another group
    else:
        game.change_leader()
        voting(game)


def mission(game, group):
    mission_result = 0
    for nick in group:
        mission_result += take_vote(game.players_list[game.nicks_list.index(nick)], True)

    # Adding points to the command, which won the round
    if game.round_number == game.rebels_lucky_mission:
        game.add_points(mission_result >= game.spies_to_sabotage_lucky_mission)
    else:
        game.add_points(mission_result > 0)

    game.round_number += 1
    game.leader_changing_count = 0
    voting(game)


game1 = Game()
lobby_assemble(game1)

