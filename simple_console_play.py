#!/usr/bin/env python3

import argparse
import time
import re

from game.core import GameState, GameException, EndGameException


# player view
# info of non rainbow color has to include rainbow colors
# action history (visible?) (undo move possible?)


ACTION_RE = re.compile(
    '(?P<action>[bit])'
    '('
        '(?<=[bt])(?P<card>\d)'
        '|'
        '(?<=i)(?P<to_player>\d)(?P<type>[cn])(?P<type_value>\d)'
    ')'
)
INPUT_TO_ACTION = {
    'b': 'build',
    'i': 'info',
    't': 'throw',
}
INPUT_TO_TYPE = {
    'n': 'number',
    'c': 'color',
}

COLOR_START_CONSOLE = {
    0: u'\x1b[1m\x1b[31m',  # red
    1: u'\x1b[1m\x1b[32m',  # green
    2: u'\x1b[1m\x1b[34m',  # blue
    3: u'\x1b[1m\x1b[37m',  # white
    4: u'\x1b[1m\x1b[33m',  # yellow
    5: u'\x1b[1m\x1b[35m',  # rainbow (magenta)
}
COLOR_END_CONSOLE = u'\x1b[0m'



def parse_args():
    parser = argparse.ArgumentParser()
    player_choices = set(GameState.CARDS_COUNT.keys())
    parser.add_argument(
        'players',
        metavar='PLAYERS',
        type=int,
        choices=player_choices,
        help=f'Number of players. Choices: {player_choices}',
    )
    args = parser.parse_args()
    return args


def match_to_params(match):
    data = match.groupdict()
    action = INPUT_TO_ACTION[data['action']]

    kwargs = dict()
    to_player = data.get('to_player')
    if to_player is not None:
        kwargs['to_player'] = int(to_player)
        type_ = INPUT_TO_TYPE[data['type']]
        kwargs[type_] = int(data['type_value'])

    card = data.get('card')
    if card is not None:
        kwargs['card'] = int(card)

    return action, kwargs


def print_game_state(game_state, color_on=False):
    if not color_on:
        print(game_state)
        return

    colors = ', '.join([
        f'{COLOR_START_CONSOLE[color]}{color_name}: {color}{COLOR_END_CONSOLE}'
        for color, color_name in game_state.COLORS.items()
    ])

    players = ']   ['.join([
        ' '.join([
            f'{COLOR_START_CONSOLE[color]}({number}){COLOR_END_CONSOLE}'
            for color, number in player_cards
        ])
        for player_cards in game_state.players
    ])

    built = '  ---  '.join([
        f'{COLOR_START_CONSOLE[color]}({built}){COLOR_END_CONSOLE}'
        for color, built in game_state.built.items()
    ])
    print('\n - '.join([
        f' -         Colors: {{{colors}}}',
        f'    Deck count: {len(game_state.deck)}',
        f'       Garbage: {game_state.garbage}',
        f'         Built:  {built}',
        f'    Lightnings: {game_state.lightnings}',
        f'         Tempo: {game_state.tempo}{" "*(3+game_state.tempo*24)}\u2193\u2193\u2193\u2193\u2193\u2193\u2193\u2193\u2193\u2193\u2193',
        f'       Players: [{players}]',
        f'Info Available: {game_state.info_available}',
        f'    Game Ended: {game_state.game_ended}',
        f'        Points: {game_state.points}',
    ]))


def get_user_action(game_state):
    while True:
        print_game_state(game_state, True)
        user_input = input('Choose your action (e.g.: i1c1, i0n3, b2, t4): ')
        match = ACTION_RE.match(user_input)
        if not match:
            print(f'Invalid action: \'{user_input}\'')
            continue
        action, kwargs = match_to_params(match)

        # print(f'action: {action}, kwargs: {kwargs}')
        try:
            game_state.action(action, **kwargs)
            break
        except EndGameException as e:
            raise
        except GameException as e:
            print(e)
    return user_input


def main():
    args = parse_args()
    game_state = GameState(players_count=args.players)
    history = []
    while True:
        print(f' ===>     History: {history}')
        try:
            user_action = get_user_action(game_state)
        except EndGameException as e:
            print("Game Over!")
            return
        history.append(user_action)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n... forcefully exited ...')
