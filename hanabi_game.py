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
    DEALT_CARDS = {
        2: 5,
        3: 5,
        4: 4,
        5: 4,
    }
    MAX_LIGHTNINGS = 2

    @classmethod
    def generate_deck(cls):
        return random.sample(cls.DECK_BASE, k=len(cls.DECK_BASE))

    def deal_cards(self):
        for player in range(self._players_count):
            self.players.append([])
            for _ in range(self.DEALT_CARDS[self._players_count]):
                self.players[player].append(self.deck.pop())

    def __init__(self, players_count=2):
        if players_count not in self.DEALT_CARDS:
            raise Exception('Wrong number of players!')

        self._players_count = players_count
        self.lightnings = 0
        self.info_available = 8
        self.built = dict([(c, 0) for c in COLORS])
        self.garbage = []
        self.deck = GameState.generate_deck()
        self.players = []
        self.deal_cards()

    def __str__(self):
        return '\n - '.join([
            f' - Deck: {self.deck}',
            f'Players: {self.players}',
            f'Garbage: {self.garbage}',
            f'Built: {self.built}',
            f'Lightnings: {self.lightnings}',
            f'Info_available: {self.info_available}',
        ])


def main():
    while True:
        game_state = GameState()
        print(game_state)
        # Action = {hint / throw / build}
        # actions = []
        action = input('Action (t1, b1, h1n1): ')
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n... forcefully exited ...')
