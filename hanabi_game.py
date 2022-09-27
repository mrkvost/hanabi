#!/usr/bin/env python3

import random
import json


class GameException(Exception):
    pass


class EndGameException(GameException):
    pass


class GameState:
    COLORS = {
        0: 'red',
        1: 'green',
        2: 'blue',
        3: 'while',
        4: 'yellow',
        5: 'rainbow',
    }

    DECK_BASE = [(c, n) for c in range(len(COLORS)) for n in (1,1,1,2,2,3,3,4,4,5)]
    CARDS_COUNT = {
        2: 5,
        3: 5,
        4: 4,
        5: 4,
    }
    MAX_LIGHTNINGS = 2
    MAX_INFO_AVAILABLE = 8
    MAX_POINTS = 5 * len(COLORS)

    @classmethod
    def generate_deck(cls):
        return random.sample(cls.DECK_BASE, k=len(cls.DECK_BASE))

    def __init__(self, players_count=2):
        if players_count not in self.CARDS_COUNT:
            raise GameException('Wrong number of players!')

        self._players_count = players_count
        self.tempo = random.randrange(players_count)
        self._cards_count = self.CARDS_COUNT[players_count]
        self.lightnings = 0
        self.game_ended = False
        self.info_available = self.MAX_INFO_AVAILABLE
        self.built = dict([(c, 0) for c in self.COLORS])
        self.garbage = []
        self.deck = GameState.generate_deck()
        self.players = []
        self.deal_cards()
        self.points = 0

    def deal_cards(self):
        for player in range(self._players_count):
            self.players.append([])
            for _ in range(self._cards_count):
                self.players[player].append(self.get_deck_card())

    def lightning(self):
        self.lightnings += 1
        if self.lightnings > self.MAX_LIGHTNINGS:
            self.points = 0
            self.game_ended = True
            raise EndGameException('Max lightnings exceeded!')

    def get_deck_card(self):
        if not self.deck:
            raise GameException('No more cards in the deck!')
        return self.deck.pop()

    def get_player_card(self, player, card):
        if player >= len(self.players) or player < 0:
            raise GameException('Such player does not exist!')
        elif card >= self._cards_count or card < 0:
            raise GameException('Such card does not exist!')
        return self.players[player].pop(card)

    def give_player_card(self):
        try:
            self.players[self.tempo].append(self.get_deck_card())
        except GameException as e:
            if len(self.players[self.tempo]) != self._cards_count:
                raise

    def shift_tempo(self):
        self.tempo = (self.tempo + 1) % self._players_count

    def _build(self, card=None):
        if card is None:
            raise GameException('Must specify a card to build with!')
        card_color, card_number = self.get_player_card(self.tempo, card)
        if (self.built[card_color] + 1) == card_number:
            self.built[card_color] = card_number
            self.points += 1
            if card_number == 5:
                if self.info_available < self.MAX_INFO_AVAILABLE:
                    self.info_available += 1
                if self.points == self.MAX_POINTS:
                    self.game_ended = True
                    raise EndGameException('Max lightnings exceeded!')
        else:
            self.garbage.append((card_color, card_number))
            self.lightning()
        self.give_player_card()
        self.shift_tempo()

    def _throw(self, card=None):
        if card is None:
            raise GameException('Must specify a card to throw away!')
        card_color, card_number = self.get_player_card(self.tempo, card)
        if self.info_available < self.MAX_INFO_AVAILABLE:
            self.info_available += 1
        self.garbage.append((card_color, card_number))
        self.give_player_card()
        self.shift_tempo()

    def _info(self, to_player=None, color=None, number=None):
        if to_player is None:
            raise GameException('Must specify a player receiving info!')
        elif self.tempo == to_player:
            raise GameException('Can not give info to oneself!')
        elif not self.info_available:
            raise GameException('No info available!')
        elif color is not None and number is not None:
            raise GameException('Can info either color or number, not both!')
        elif color is None and number is None:
            raise GameException('Must give precisely one info!')
        # TODO: check with rules:
        # Can we give info about color/number that player does not have?
        self.info_available -= 1
        self.shift_tempo()

    def action(self, action, **kwargs): # to_player=None, card=None, color=None, number=None
        actions = {
            'build': self._build,
            'throw': self._throw,
            'info': self._info,
        }
        if self.game_ended:
            raise EndGameException(f'Game Ended! (Points: {self.points})')
        elif action not in actions:
            raise GameException(f'Unknown action: \'{action}\'!')
        actions[action](**kwargs)

    def __str__(self):
        return '\n - '.join([
            # f' - Deck: {self.deck}',
            f' -     Deck count: {len(self.deck)}',
            f'       Players: {self.players}',
            f'         Tempo: {self.tempo}',
            f'       Garbage: {self.garbage}',
            f'         Built: {self.built}',
            f'    Lightnings: {self.lightnings}',
            f'Info Available: {self.info_available}',
            f'    Game Ended: {self.game_ended}',
            f'        Points: {self.points}',
        ])

    def json(self):
        return json.dumps({
            'deck': self.deck,
            'players': self.players,
            'tempo': self.tempo,
            'garbage': self.garbage,
            'built': self.built,
            'lightnings': self.lightnings,
            'info_available': self.info_available,
            'game_ended': self.game_ended,
            'points': self.points,
        })


def _main():
    # This is just for simple testing of the game state:
    import time
    while True:
        game_state = GameState()
        # print(game_state.json())
        print(game_state)
        print('-'*30)
        for i in range(10):
            rnd = random.randint(0, 10)
            try:
                if rnd < 3:
                    game_state.action('info', to_player=((game_state.tempo + 1) % 2), color=0)
                elif rnd < 5:
                    game_state.action('throw', card=0)
                else:
                    game_state.action('build', card=0)
            except EndGameException as e:
                break
            except GameException as e:
                pass
        print(game_state)
        print('x'*80)
        time.sleep(1)


if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        print('\n... forcefully exited ...')
