import random

class Battler():
    def __init__(self, name, lvl, stats) -> None:
        self.name = name
        self.lvl = lvl
        self.stats = stats

class Player(Battler):

    def __init__(self, name) -> None:
        stats = {'hp' : 20,
                    'mp' : 10,
                    'atk' : 10,
                    'def' : 10,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 10
        }

        super().__init__(name, 1, stats)

        self.xp = 0
        self.xpToNextLvl = 25
        self.aptitudes = {'str' : 5,
                    'dex' : 5,
                    'int' : 5,
                    'wis' : 5,
                    'const' : 5
        }

class Imp(Battler):

    def __init__(self) -> None:
        stats = {'hp' : 200,
                    'mp' : 5,
                    'atk' : 5,
                    'def' : 5,
                    'matk' : 5,
                    'mdef' : 5,
                    'speed' : 5,
                    'critCh' : 5
        }
        super().__init__('Imp', 1, stats)

def takeDmg(attacker, defender):
    dmg = attacker.stats['atk'] - defender.stats['def']
    if dmg < 0: dmg = 0
    defender.stats['hp'] -= dmg
    if defender.stats['hp'] <= 0:
        print('{} has been slain.'.format(defender.name))
    else:
        print('{} takes {} damage!'.format(defender.name, dmg))

def combat(player, enemy):
    while True:
        print('#######################')
        cmd = input('Attack? yes/no: ').lower()
        if 'yes' in cmd:
            print('{} takes the opportunity to attack!'.format(player.name))
            takeDmg(player, enemy)
        elif 'no' in cmd:
            print('{} takes the opportunity to attack!'.format(enemy.name))
            takeDmg(enemy, player)
        else:
            pass