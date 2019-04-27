import logging
import sys
from random import randint
from characters import barbazu, lucius

def dice(num, sides):
    return sum([randint(1, sides) for i in range(num)])

if __name__ == '__main__':
    # Logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # Roll initiative!
    if barbazu.Barbazu().initiative > lucius.Lucius().initiative:
        player_1, player_2 = barbazu.Barbazu(), lucius.Lucius()
    else:
        player_1, player_2 = lucius.Lucius(), barbazu.Barbazu()
    player_1.first = True

    # Battle start!
    turn = 1
    while True:
        logging.info(f'Round {turn}, fight!')
        player_1.turn = turn
        player_1.battle(player_2)
        if not player_2.is_alive:
            break
        player_2.turn = turn
        player_2.battle(player_1)
        if not player_1.is_alive:
            break
        turn += 1

    # Battle finished!
    if not player_1.is_alive:
        logging.info(f'{player_2.name} has defeated {player_1.name} with {player_2.hp} HP left!')
    else:
        logging.info(f'{player_1.name} has defeated {player_2.name} with {player_1.hp} HP left!')
