#!/usr/bin/env python3

import argparse

from game_core import GameState, GameException, EndGameException


# game creation for x players input
# player view
# player actions input
# info of non rainbow color has to include rainbow colors
# action history (visible?) (undo move possible?)


def parse_args():
    parser = argparse.ArgumentParser()
    player_choices = set(GameState.CARDS_COUNT.keys())
    parser.add_argument(
        'players',
        metavar='PLAYERS',
        choices=player_choices,
        help=f'Number of players. Choices: {player_choices}',
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n... forcefully exited ...')
