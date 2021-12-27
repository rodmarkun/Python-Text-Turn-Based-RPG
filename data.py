import random

class Battler():
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True

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

        super().__init__(name, stats)

        self.lvl = 1
        self.xp = 0
        self.xpToNextLvl = 25
        self.aptitudes = {'str' : 5,
                    'dex' : 5,
                    'int' : 5,
                    'wis' : 5,
                    'const' : 5
        }
        self.aptitudePoints = 5

class Enemy(Battler):

    def __init__(self, name, stats, xpReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward


def takeDmg(attacker, defender):
    dmg = round(attacker.stats['atk'] * (100/(100 + defender.stats['def'])))
    if dmg < 0: dmg = 0
    defender.stats['hp'] -= dmg
    print('{} takes {} damage!'.format(defender.name, dmg))
    if defender.stats['hp'] <= 0:
        print('{} has been slain.'.format(defender.name))
        defender.alive = False
    else:
        print('{} now has {} hp'.format(defender.name, defender.stats['hp']))

def combat(player, enemy):
    while player.alive and enemy.alive:
        print('#######################')
        print('A wild {} has appeared!'.format(enemy.name))
        cmd = input('Attack? yes/no: ').lower()
        if 'yes' in cmd:
            print('{} takes the opportunity to attack!'.format(player.name))
            takeDmg(player, enemy)
        elif 'no' in cmd:
            print('{} takes the opportunity to attack!'.format(enemy.name))
            takeDmg(enemy, player)
        else:
            pass
    if player.alive:
        addExp(player, enemy.xpReward)

def addExp(player, exp):
    player.xp += exp
    while(player.xp >= player.xpToNextLvl):
        player.xp -= player.xpToNextLvl
        player.lvl += 1
        player.xpToNextLvl = round(player.xpToNextLvl * 1.5)
        for stat in player.stats:
            player.stats[stat] += 2
        print("Level up! You are now level {}.".format(player.lvl))

def showStats(player):
    print('############################')
    print('#          STATS           #')
    print('############################')
    print('HP: {}'.format(player.stats['hp']))
    print('MP: {}'.format(player.stats['mp']))
    print('ATK: {}'.format(player.stats['atk']))
    print('DEF: {}'.format(player.stats['def']))
    print('MATK: {}'.format(player.stats['matk']))
    print('MDEF: {}'.format(player.stats['mdef']))
    print('SPD: {}'.format(player.stats['speed']))
    print('CRIT: {}'.format(player.stats['critCh']))
    print('############################')
    print('#        APTITUDES         #')
    print('############################')
    print('STR: {}'.format(player.aptitudes['str']))
    print('DEX: {}'.format(player.aptitudes['dex']))
    print('INT: {}'.format(player.aptitudes['int']))
    print('WIS: {}'.format(player.aptitudes['wis']))
    print('CONST: {}'.format(player.aptitudes['const']))
    print('############################')