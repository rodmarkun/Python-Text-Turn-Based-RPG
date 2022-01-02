import random

class Battler():
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True

class Enemy(Battler):

    def __init__(self, name, stats, xpReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward

def take_dmg(attacker, defender):
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
            take_dmg(player, enemy)
            if enemy.alive == True:
                print('{} takes the opportunity to attack!'.format(enemy.name))
                take_dmg(enemy, player)
        else:
            pass
    if player.alive:
        player.addExp(enemy.xpReward)

def heal(target, amount):
    if target.stats['hp'] + amount > target.stats['maxHp']:
        target.stats['hp'] = target.stats['maxHp']
    else:
        target.stats['hp'] += amount

def fully_heal(target):
    target.stats['hp'] = target.stats['maxHp']