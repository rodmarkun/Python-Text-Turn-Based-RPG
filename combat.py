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

    # Taking damage from a certain source
    def take_dmg(self, dmg):
        if dmg < 0: dmg = 0
        self.stats['hp'] -= dmg
        print('{} takes {} damage!'.format(self.name, dmg))
        # Defender dies
        if self.stats['hp'] <= 0:
            print('{} has been slain.'.format(self.name))
            self.alive = False

    # Normal attack all battlers have
    def normal_attack(self, defender):
        print('{} attacks!'.format(self.name))
        dmg = round(self.stats['atk'] * (100/(100 + defender.stats['def'])))
        # Check for critical attack
        if self.stats['critCh'] > random.randint(0, 100):
            print('Critical blow!')
            dmg *= 2
        # Check for missed attack
        if not check_miss(self, defender):
            defender.take_dmg(dmg)

    # Target recovers a certain amount of mp
    def recover_mp(self, amount):
        if self.stats['mp'] + amount > self.stats['maxMp']:
            fully_recover_mp(self)
        else:
            self.stats['mp'] += amount
        print('{} recovers {} mp!'.format(self.name, amount))

    # Target recovers a certain amount of hp
    def heal(self, amount):
        if self.stats['hp'] + amount > self.stats['maxHp']:
            fully_heal(self)
        else:
            self.stats['hp'] += amount
        print('{} heals {} hp!'.format(self.name, amount))

class Enemy(Battler):
    
    def __init__(self, name, stats, xpReward, goldReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward
        self.goldReward = goldReward


'''
Main combat loop
'''
# TODO: Change "player" for "allies". There will be other characters aside from the player
# for the user to control.
def combat(player, enemies):
    # All battlers are inserted into the Battlers list and ordered by speed (turn order)
    battlers = define_battlers(player, enemies)

    print('############################')
    for enemy in enemies:
        print('A wild {} has appeared!'.format(enemy.name))
    # The battle will go on while the player is still alive and there are still enemies to defeat
    while player.alive and len(enemies) > 0:
        # Battlers should be updated for speed changes (buffs/debuffs)
        battlers = define_battlers(player, enemies)
        for battler in battlers:
            # If the battler is an ally, the user has control over its actions
            if battler.isAlly:
                text.combat_menu(player, enemies)
                cmd = input('> ').lower()
                while cmd not in ['a', 'c', 's']:
                    print('Please enter a valid command')
                    cmd = input('> ').lower()
                if 'a' in cmd:
                    targeted_enemy = select_target(enemies)
                    battler.normal_attack(targeted_enemy)
                    check_if_dead(targeted_enemy, enemies, battlers)
                elif 's' in cmd:
                    text.spell_menu(player)
                    option = int(input("> "))
                    while option not in range(len(player.spells)+1):
                        print('Please enter a valid number')
                        option = int(input("> "))
                    if option != 0:
                        spellChosen = player.spells[option - 1]
                        if spellChosen.isTargeted:
                            target = select_target(battlers)
                            spellChosen.effect(player, target)
                            check_if_dead(target, enemies, battlers)
                        else:
                            spellChosen.effect(player, player)
            else:
                # For now, enemies will perform a normal attack against the player.
                # This can be expanded to work as a functional AI
                battler.normal_attack(player)

        # A turn has passed
        # Check turns for buffs and debuffs
        for battler in battlers:
            check_turns_buffs_and_debuffs(battler, False)
    if player.alive:
        # Deactivate all existent buffs and debuffs
        check_turns_buffs_and_debuffs(player, True)
        # Add experience to players
        player.add_exp(enemy.xpReward)

# Returns the battlers list, ordered by speed (turn order)
# This should be changed to when the change from "player" to "allies" is made.
def define_battlers(player, enemies):
    battlers = enemies.copy()
    battlers.append(player)
    battlers.sort(key=lambda b: b.stats['speed'], reverse=True)
    return battlers

# Select a certain target from the battlefield
def select_target(targets):
    text.select_objective(targets)
    i = int(input("> "))
    while i not in range(len(targets)+1):
        print('Select a valid target')
        i = int(input("> "))
    target = targets[i-1]
    return target

# Returns True if attack misses, False if it doesn't
def check_miss(attacker, defender):
    chance = math.floor(math.sqrt(max(0, (5 * defender.stats['speed'] - attacker.stats['speed'] * 2))))
    if chance > random.randint(0, 100):
        print('{}\'s attack missed!'.format(attacker.name))
        return True
    return False

# Checks if buffs and debuffs should still be active
# If deactivate = True they will inmediately deactivate
def check_turns_buffs_and_debuffs(target, deactivate):
    if deactivate:
        for bd in target.buffsAndDebuffs:
            bd.deactivate()
    else:
        for bd in target.buffsAndDebuffs:
            bd.check_turns()

# Checks if a battler is dead and removes it from the appropiate lists
def check_if_dead(target, enemies, battlers):
    if target.isAlly:
        # Here it should be removed of the "Allies" list
        # Player doesnt use this function for now
        pass
    else:
        if target.alive == False:
            battlers.remove(target)
            enemies.remove(target)

# Fully heal a target
def fully_heal(target):
    target.stats['hp'] = target.stats['maxHp']

def fully_recover_mp(target):
    target.stats['mp'] = target.stats['maxMp']