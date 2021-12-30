import random
import text
import inventory

class Battler():
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True

class Player(Battler):

    def __init__(self, name) -> None:
        stats = {'maxHp' : 25,
                    'hp' : 25,
                    'maxMp' : 10,
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
        self.inventory = inventory.Inventory()

class Enemy(Battler):

    def __init__(self, name, stats, xpReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward


def takeDmg(attacker, defender):
    dmg = round(attacker.stats['atk'] * (100/(100 + defender.stats['def'])))
    if attacker.stats['critCh'] > random.randint(0, 100):
        print('Critical blow!')
        dmg *= 2
    if dmg < 0: dmg = 0
    defender.stats['hp'] -= dmg
    print('{} takes {} damage!'.format(defender.name, dmg))
    if defender.stats['hp'] <= 0:
        print('{} has been slain.'.format(defender.name))
        defender.alive = False
    else:
        print('{} now has {} hp'.format(defender.name, defender.stats['hp']))

def combat(player, enemy):
    print('#######################')
    print('A wild {} has appeared!'.format(enemy.name))
    while player.alive and enemy.alive:
        cmd = input('Attack? (yes): ').lower()
        if 'yes' in cmd:
            print('{} takes the opportunity to attack!'.format(player.name))
            takeDmg(player, enemy)
            if enemy.alive == True:
                print('{} takes the opportunity to attack!'.format(enemy.name))
                takeDmg(enemy, player)
        else:
            pass
    if player.alive:
        addExp(player, enemy.xpReward)

def addExp(player, exp):
    player.xp += exp
    print("You earn {}xp".format(exp))
    while(player.xp >= player.xpToNextLvl):
        player.xp -= player.xpToNextLvl
        player.lvl += 1
        player.xpToNextLvl = round(player.xpToNextLvl * 1.5)
        fullyHeal(player)
        for stat in player.stats:
            player.stats[stat] += 1
        print("Level up! You are now level {}.".format(player.lvl))


def assignAptitudePoints(player):
    text.showAptitudes(player)
    option = int(input("> "))
    optionsDictionary = {1 : 'str',
                        2 : 'dex',
                        3 : 'int',
                        4 : 'wis',
                        5 : 'const'}
    while option != 6:
        if option in range(1, 7):
            if player.aptitudePoints >=1:
                aptitudeToAssign = optionsDictionary[option]
                player.aptitudes[aptitudeToAssign] += 1
                print('{} is now {}!'.format(aptitudeToAssign, player.aptitudes[aptitudeToAssign]))
                updateStatsToAptitudes(player, aptitudeToAssign)
                player.aptitudePoints -= 1
            else:
                print('Not enough points!')
        else:
            print('Not a valid character!')
        option = int(input("> "))

'''
When an aptitude is leveled up, certain stats also increase:
STR -> ATK + 1
DEX -> SPD + 1, CRIT + 1
INT -> MATK + 1
WIS -> MP + 5
CONST -> MAXHP + 5
'''
def updateStatsToAptitudes(player, aptitude):
    if aptitude == 'str':
        player.stats['atk'] += 1
    elif aptitude == 'dex':
        player.stats['speed'] += 1
        player.stats['critCh'] += 1
    elif aptitude == 'int':
        player.stats['matk'] += 1
    elif aptitude == 'wis':
        player.stats['mp'] += 3
    elif aptitude == 'const':
        player.stats['maxHp'] += 3

def fullyHeal(target):
    target.stats['hp'] = target.stats['maxHp']