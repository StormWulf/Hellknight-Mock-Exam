import logging
from random import randint

class Lucius(object):
    def __init__(self, power_attack=True, bless=False, bane=True):
        self.name = 'Lucius Uthric'
        self.hp = 46  # Health
        self.ac = 24  # Armor check
        self.stamina = 7  # Stamina pool
        self.bleeding = False  # If suffering from the bleeding condition
        self.devil_chills = False  # If suffering from the Barbazu's devil chills
        self.fatigued = False  # If suffering from fatigued condition
        self.critical_hit = False  # If this character landed a critical hit
        self.power_attack = power_attack  # If this character will use Power Attack
        self.bless = bless  # If this character will use Oil of Bless Weapon
        self.bane = bane  # If this character will use Bane (devil)
        self.first = False  # Determines if this character had the first turn
        self.turn = 1  # The round number of the battle

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def initiative(self):
        return dice(1, 20) + 2

    @property
    def attack(self):
        roll = dice(1, 20)
        if roll == 20:
            self.critical_hit = True
        else:
            self.critical_hit = False
        mod = 13
        if self.power_attack:
            mod -= 3
        if self.fatigued:
            mod -= 2
        if self.bane:
            mod += 2
        return roll + mod

    @property
    def damage(self):
        roll = dice(1, 8)
        mod = 9
        if self.power_attack:
            mod += 4
        if not self.bless:
            mod -= 5
        if self.fatigued:
            mod -= 2
        if self.critical_hit and any([self.attack >= 19, self.bless]):
            logging.info('Critical hit!')
            roll += dice(1, 8)
            mod *= 2
        result = roll + mod
        if self.bane:
            result += dice(2, 6) + 2
        return result

    @property
    def fort_save(self):
        return dice(1, 20) + 6

    def battle(self, enemy):
        if self.bleeding:
            logging.info(f'{self.name} is bleeding!')
            self.hp -= 2
            if not self.is_alive:
                logging.info(f'{self.name} has bled to death')
                return
        if any([self.bless, self.bane]) and self.turn == 1:
            logging.info(f'{self.name} enhances his weapon!')
        else:
            # Bonus on foe's AC on first turn if the foe is charging
            attack = self.attack + 2 if self.turn == 1 and not self.first else self.attack
            # Lucius hits his enemy!
            if attack >= enemy.ac:
                damage = self.damage
                logging.info(f'{self.name} hits {enemy.name} for {damage}!')
                enemy.hp -= damage
            # Lucius spends stamina points to hit his enemy!
            elif all([5 >= enemy.ac - attack, any([self.stamina > enemy.ac - attack, self.stamina >= enemy.ac - attack and enemy.hp < 22])]):
                gap = enemy.ac - attack
                logging.info(f'{self.name} spends {gap} stamina point(s)!')
                self.stamina -= gap
                damage = self.damage
                logging.info(f'{self.name} hits {enemy.name} for {damage}!')
                enemy.hp -= damage
                if self.stamina == 0:
                    logging.info(f'{self.name} feels fatigued!')
                    self.fatigued = True
                    self.ac -= 2
            # Lucius misses!
            else:
                logging.info(f'{self.name} missed!')

def dice(num, sides):
    return sum([randint(1, sides) for i in range(num)])
