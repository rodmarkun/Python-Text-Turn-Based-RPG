import math
import random
import skills
import text

'''
Parent class for all instances that can enter in combat.
A Battler will always be either an Enemy, a Player's ally or the Player himself
'''
class Battler():
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True
        self.buffsAndDebuffs = []
        self.isAlly = False

class Enemy(Battler):

    def __init__(self, name, stats, xpReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward


# Normal attack all battlers have
def normal_attack(attacker, defender):
    print('{} attacks!'.format(attacker.name))
    dmg = round(attacker.stats['atk'] * (100/(100 + defender.stats['def'])))
    if attacker.stats['critCh'] > random.randint(0, 100):
        print('Critical blow!')
        dmg *= 2
    if not check_miss(attacker, defender):
        take_dmg(defender, dmg)

# Taking damage from a certain source
def take_dmg(defender, dmg):
    if dmg < 0: dmg = 0
    defender.stats['hp'] -= dmg
    print('{} takes {} damage!'.format(defender.name, dmg))
    if defender.stats['hp'] <= 0:
        print('{} has been slain.'.format(defender.name))
        defender.alive = False

'''
Main combat loop
'''
def combat(player, enemies):
    # All battlers are inserted into the Battlers list and ordered by speed (turn order)
    battlers = enemies.copy()
    battlers.append(player)
    battlers.sort(key=lambda b: b.stats['speed'], reverse=True)

    print('############################')
    for enemy in enemies:
        print('A wild {} has appeared!'.format(enemy.name))
    while player.alive and len(enemies) > 0:
        for battler in battlers:
            if battler.isAlly:
                text.combat_menu(player, enemies)
                cmd = input('> ').lower()
                while cmd not in ['a', 'c', 's']:
                    cmd = input('> ').lower()
                if 'a' in cmd:
                    targeted_enemy = select_target(enemies)
                    normal_attack(player, targeted_enemy)
                    if targeted_enemy.alive == False:
                        battlers.remove(targeted_enemy)
                        enemies.remove(targeted_enemy)
                elif 's' in cmd:
                    # TODO: This needs more control
                    text.spell_menu(player)
                    option = int(input("> "))
                    if option != 0:
                        targeted_enemy = select_target(battlers)
                        skill_effect(player.spells[option - 1], player, targeted_enemy)
                        if targeted_enemy.alive == False:
                            battlers.remove(targeted_enemy)
                            enemies.remove(targeted_enemy)
            else:
                normal_attack(battler, player)

        # A turn has passed
        # Check turns for buffs and debuffs
        for bd in player.buffsAndDebuffs:
            bd.check_turns()
        for bd in enemy.buffsAndDebuffs:
            bd.check_turns()
    if player.alive:
        # Deactivate all existent buffs and debuffs
        for bd in player.buffsAndDebuffs:
            bd.deactivate()
        # Add experience to players
        player.add_exp(enemy.xpReward)

# Select a certain target from the battlefield
def select_target(targets):
    text.select_objective(targets)
    i = int(input("> "))
    if i <= len(targets):
        target = targets[i-1]
        return target

# Returns True if attack misses, false if it doesn't
def check_miss(attacker, defender):
    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))
    if chance > random.randint(0, 100):
        print('{}\'s attack missed!'.format(attacker.name))
        return True
    return False

# Target recovers a certain amount of mp
def recover_mp(target, amount):
    if target.stats['mp'] + amount > target.stats['maxMp']:
        target.stats['mp'] = target.stats['maxMp']
    else:
        target.stats['mp'] += amount
    print('{} recovers {} mp!'.format(target.name, amount))

# Target recovers a certain amount of hp
def heal(target, amount):
    if target.stats['hp'] + amount > target.stats['maxHp']:
        target.stats['hp'] = target.stats['maxHp']
    else:
        target.stats['hp'] += amount
    print('{} heals {} hp!'.format(target.name, amount))

# Activates the effect of a certain skill
def skill_effect(skill, caster, target):
    if type(skill) == skills.SimpleOffensiveSpell:
        amount = skill.effect(caster, target)
        take_dmg(target, amount)
    elif type(skill) == skills.SimpleHealingSpell:
        # TODO: Change for target when multi-character combat is ready
        amount = skill.effect(caster, target)
        heal(caster, amount)
    elif type(skill) == skills.BuffDebuffSpell:
        skill.effect(caster, caster)

# Fully heal a target (debug)
def fully_heal(target):
    target.stats['hp'] = target.stats['maxHp']