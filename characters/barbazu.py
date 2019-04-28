import logging
from random import randint

class Barbazu(object):
    def __init__(self):
        self.name = 'Devil, Barbazu'
        self.hp = 57  # Health
        self.ac = 19  # Armor check
        self.critical_hit = False  # If this character landed a critical hit
        self.first = False  # Determines if this character had the first turn
        self.turn = 1  # The round number of the battle

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def initiative(self):
        return dice(1, 20) + 6

    @property
    def glaive_attack(self):
        roll = dice(1, 20)
        if roll == 20:
            self.critical_hit = True
        else:
            self.critical_hit = False
        return roll + 11
    
    @property
    def glaive_damage(self):
        roll = dice(1, 10)
        mod = 6
        if self.critical_hit and self.glaive_attack > 24:
            logging.info('Critical hit!')
            roll += dice(2, 10)
            mod *= 3
        return roll + mod

    def glaive(self, enemy):
        # First glaive attack (assuming charge on first turn)
        attack = self.glaive_attack + 2 if self.turn == 1 and self.first else self.glaive_attack
        if attack >= enemy.ac:
            damage = self.glaive_damage
            logging.info(f'{self.name} hits {enemy.name} with the first glaive attack for {damage}!')
            enemy.hp -= damage
            enemy.bleeding = True
        else:
            logging.info(f'{self.name} missed with the first glaive attack!')

        # Second glaive attack (can't FRA on first turn)
        if not self.turn == 1:
            if self.glaive_attack - 5 >= enemy.ac:
                damage = self.glaive_damage
                logging.info(f'{self.name} hits {enemy.name} with a second glaive attack for {damage}!')
                enemy.hp -= damage
                enemy.bleeding = True
            else:
                logging.info(f'{self.name} missed with the second glaive attack!')

    @property
    def claws_attack(self):
        roll = dice(1, 20)
        if roll == 20:
            self.critical_hit = True
        else:
            self.critical_hit = False
        return roll + 10

    @property
    def claws_damage(self):
        roll = dice(1, 6)
        mod = 4
        if self.critical_hit and self.claws_attack > 24:
            logging.info('Critical hit!')
            roll += dice(1, 6)
            mod *= 2
        return roll + mod
    
    def claws(self, enemy):
        hit = 0
        for i in range(2):
            if self.claws_attack >= enemy.ac:
                damage = self.claws_damage
                logging.info(f'{self.name} hits {enemy.name} with claw for {damage}!')
                enemy.hp -= damage
                hit += 1
            else:
                logging.info(f'{self.name} missed with claw!')
        if hit == 2:
            damage = dice(1, 8) + 2
            logging.info(f'{self.name} attacks with its beard, inflicting {damage}!')
            enemy.hp -= damage
            if enemy.fort_save < 17:
                logging.info(f'{enemy.name} contracts Devil Chills!')
                enemy.devil_chills = True

    def battle(self, enemy):
        if self.turn == 1 and self.first:
            self.glaive(enemy)
        else:
            self.claws(enemy)

def dice(num, sides):
    return sum([randint(1, sides) for i in range(num)])