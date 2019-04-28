import logging
import sys
from random import randint
from characters import barbazu, lucius

if __name__ == '__main__':
    # Logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    results = {
        'Lucius Uthric': 0,
        'Devil, Barbazu': 0,
        'bleeding': 0,
        'devil_chills': 0,
    }
    for i in range(1000):
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
                logging.info(f'{player_1.name} has defeated {player_2.name} with {player_1.hp} HP left!')
                results[player_1.name] += 1
                break
            player_2.turn = turn
            player_2.battle(player_1)
            if not player_1.is_alive:
                logging.info(f'{player_2.name} has defeated {player_1.name} with {player_2.hp} HP left!')
                results[player_2.name] += 1
                break
            turn += 1

        # Battle finished!
        if player_1.name == 'Lucius Uthric':
            lucius_status = player_1
        else:
            lucius_status = player_2
        results['bleeding'] += 1 if lucius_status.bleeding else 0
        results['devil_chills'] += 1 if lucius_status.devil_chills else 0
    logging.info(results)
