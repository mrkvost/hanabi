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
        self.info_available = 8
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

    def shift_tempo(self):
        self.tempo = (self.tempo + 1) % self._players_count

    def build(self, player, card):
        card_color, card_number = self.get_player_card(player, card)
        if (self.built[card_color] + 1) == card_number:
            self.built[card_color] = card_number
            try:
                self.players[player].append(self.get_deck_card())
            except Exception as e:
                print(e)
                # TODO: fix if this is the last round, otherwise raise...
                pass
        else:
            self.garbage.append((card_color, card_number))
            self.lightning()
        self.shift_tempo()

    def __str__(self):
        return '\n - '.join([
            f' - Deck: {self.deck}',
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
        game_state.build(0, 0)
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
