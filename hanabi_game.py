#!/usr/bin/env python3

import time
import random
import argparse


COLORS = {
    0: 'red',
    1: 'green',
    2: 'blue',
    3: 'while',
    4: 'yellow',
    5: 'rainbow',
}


class GameState:
    DECK_BASE = [(c, n) for c in range(len(COLORS)) for n in (1,1,1,2,2,3,3,4,4,5)]
    CARDS_COUNT = {
        2: 5,
        3: 5,
        4: 4,
        5: 4,
    }
    MAX_LIGHTNINGS = 2
    MAX_INFO_AVAILABLE = 8

    @classmethod
    def generate_deck(cls):
        return random.sample(cls.DECK_BASE, k=len(cls.DECK_BASE))

    def __init__(self, players_count=2):
        if players_count not in self.CARDS_COUNT:
            raise Exception('Wrong number of players!')

        self._players_count = players_count
        self.tempo = random.randrange(players_count)
        self._cards_count = self.CARDS_COUNT[players_count]
        self.lightnings = 0
        self.info_available = self.MAX_INFO_AVAILABLE
        self.built = dict([(c, 0) for c in COLORS])
        self.garbage = []
        self.deck = GameState.generate_deck()
        self.players = []
        self.deal_cards()

    def deal_cards(self):
        for player in range(self._players_count):
            self.players.append([])
            for _ in range(self._cards_count):
                self.players[player].append(self.get_deck_card())

    def lightning(self):
        self.lightnings += 1
        if self.lightnings > self.MAX_LIGHTNINGS:
            raise Exception('Max lightnings exceeded!')

    def get_deck_card(self):
        if not self.deck:
            raise Exception('No more cards in the deck!')
        return self.deck.pop()

    def get_player_card(self, player, card):
        if player >= len(self.players) or player < 0:
            raise Exception('Such player does not exist!')
        elif card >= self._cards_count or card < 0:
            raise Exception('Such card does not exist!')
        return self.players[player].pop(card)

    def give_player_card(self):
        try:
            self.players[self.tempo].append(self.get_deck_card())
        except Exception as e:
            if len(self.players[self.tempo]) != self._cards_count:
                raise

    def shift_tempo(self):
        self.tempo = (self.tempo + 1) % self._players_count

    def build(self, card):
        card_color, card_number = self.get_player_card(self.tempo, card)
        if (self.built[card_color] + 1) == card_number:
            self.built[card_color] = card_number
            if card_number == 5 and self.info_available < self.MAX_INFO_AVAILABLE:
                self.info_available += 1
        else:
            self.garbage.append((card_color, card_number))
            self.lightning()
        self.give_player_card()
        self.shift_tempo()

    def throw_card(self, card):
        card_color, card_number = self.get_player_card(self.tempo, card)
        if self.info_available < self.MAX_INFO_AVAILABLE:
            self.info_available += 1
        self.garbage.append((card_color, card_number))
        self.give_player_card()
        self.shift_tempo()

    def give_hint(self, to_player, color=None, number=None):
        if self.tempo == to_player:
            raise Exception('Can not give hint to oneself!')
        elif not self.info_available:
            raise Exception('No info available!')
        elif color is not None and number is not None:
            raise Exception('Can hint either color or number, not both!')
        elif color is None and number is None:
            raise Exception('Must give precisely one hint!')
        # TODO: check with rules:
        # Can we give info about color/number that player does not have?
        self.info_available -= 1
        self.shift_tempo()

    def __str__(self):
        return '\n - '.join([
            # f' - Deck: {self.deck}',
            f' - Deck count: {len(self.deck)}',
            f'Players: {self.players}',
            f'Tempo: {self.tempo}',
            f'Garbage: {self.garbage}',
            f'Built: {self.built}',
            f'Lightnings: {self.lightnings}',
            f'Info_available: {self.info_available}',
        ])


def main():
    while True:
        game_state = GameState()
        print(game_state)
        print()
        game_state.build(0)
        print(game_state)
        print()
        game_state.give_hint((game_state.tempo + 1) % 2, 0)
        print(game_state)
        print()
        game_state.give_hint((game_state.tempo + 1) % 2, number=1)
        print(game_state)
        print()
        game_state.throw_card(1)
        print(game_state)
        print()
        # Action = {hint / throw / build}
        # actions = []
        # action = input('Action (t1, b1, h1n1): ')
        print('x'*80)
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n... forcefully exited ...')
