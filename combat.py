import math
import random
import player
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
        self.comboPoints = 0

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
        dmg = round(self.stats['atk'] * (100/(100 + defender.stats['def']*1.5)))
        # Check for critical attack
        if self.stats['critCh'] > random.randint(0, 100):
            print('Critical blow!')
            dmg *= 2
        # Check for missed attack
        if not check_miss(self, defender):
            defender.take_dmg(dmg)
        else:
            dmg = 0
        return dmg

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
    
    # Adds a certain amount of combo points
    def addComboPoints(self, points):
        self.comboPoints += points

class Enemy(Battler):
    
    def __init__(self, name, stats, xpReward, goldReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward
        self.goldReward = goldReward


'''
Main combat loop
'''

def combat(myPlayer, enemies):
    # All battlers are inserted into the Battlers list and ordered by speed (turn order)
    allies = [myPlayer]
    battlers = define_battlers(allies, enemies)
    enemy_exp = 0 
    enemy_money = 0

    print('############################')
    for enemy in enemies:
        print('A wild {} has appeared!'.format(enemy.name))
        enemy_exp += enemy.xpReward
        enemy_money += enemy.goldReward
    # The battle will go on while the player is still alive and there are still enemies to defeat
    while myPlayer.alive and len(enemies) > 0:
        # Battlers should be updated for speed changes (buffs/debuffs)
        battlers = define_battlers(allies, enemies)
        for battler in battlers:
            if type(battler) == player.Player:
                text.combat_menu(myPlayer, allies, enemies)
                cmd = input('> ').lower()
                while cmd not in ['a', 'c', 's']:
                    print('Please enter a valid command')
                    cmd = input('> ').lower()
                # Perform a normal attack
                if 'a' in cmd:
                    targeted_enemy = select_target(enemies)
                    battler.normal_attack(targeted_enemy)
                    battler.addComboPoints(1)
                    check_if_dead(allies, enemies, battlers)
                # Cast a spell
                elif 's' in cmd:
                    text.spell_menu(battler)
                    option = int(input("> "))
                    while option not in range(len(myPlayer.spells)+1):
                        print('Please enter a valid number')
                        option = int(input("> "))
                    if option != 0:
                        spellChosen = myPlayer.spells[option - 1]
                        if spellChosen.isTargeted:
                            target = select_target(battlers)
                            spellChosen.effect(myPlayer, target)
                            check_if_dead(allies, enemies, battlers)
                        else:
                            if spellChosen.defaultTarget == 'self':
                                spellChosen.effect(myPlayer, myPlayer)
                            elif spellChosen.defaultTarget == 'all_enemies':
                                spellChosen.effect(myPlayer, enemies)
                                check_if_dead(allies, enemies, battlers)
                            elif spellChosen.defaultTarget == 'allies':
                                spellChosen.effect(myPlayer, allies)
                # Use a combo
                elif 'c' in cmd:
                    text.combo_menu(battler)
                    option = int(input("> "))
                    while option not in range(len(myPlayer.combos)+1):
                        print('Please enter a valid number')
                        option = int(input("> "))
                    if option != 0:
                        comboChosen = myPlayer.combos[option - 1]
                        if comboChosen.isTargeted:
                            target = select_target(battlers)
                            comboChosen.effect(myPlayer, target)
                            check_if_dead(allies, enemies, battlers)
                        else:
                            if comboChosen.defaultTarget == 'self':
                                comboChosen.effect(myPlayer, myPlayer)
                            elif comboChosen.defaultTarget == 'all_enemies':
                                comboChosen.effect(myPlayer, enemies)
                                check_if_dead(allies, enemies, battlers)
            else:
                if battler.isAlly:
                    if len(enemies) > 0:
                        randomEnemy = random.choice(enemies)
                        battler.normal_attack(randomEnemy)
                        check_if_dead(allies, enemies, battlers)
                else:
                    # For now, enemies will just perform a normal attack against the player.
                    # This can be expanded to work as a functional AI
                    randomAlly = random.choice(allies)
                    battler.normal_attack(randomAlly)
                    check_if_dead(allies, enemies, battlers)

        # A turn has passed
        # Check turns for buffs and debuffs
        for battler in battlers:
            check_turns_buffs_and_debuffs(battler, False)
    if myPlayer.alive:
        # Deactivate all existent buffs and debuffs
        check_turns_buffs_and_debuffs(myPlayer, True)
        # Add experience to players
        myPlayer.add_exp(enemy_exp)
        myPlayer.add_money(enemy_money)
        # Restart Combo Points
        myPlayer.comboPoints = 0

# Returns the battlers list, ordered by speed (turn order)
# This should be updated to when the change from "player" to "allies" is made.
def define_battlers(allies, enemies):
    battlers = enemies.copy()
    for ally in allies:
        battlers.append(ally)
    battlers.sort(key=lambda b: b.stats['speed'], reverse=True)
    return battlers

# Select a certain target from the battlefield
def select_target(targets):
    text.select_objective(targets)
    valid_target = False
    while not valid_target:
        valid_int = False
        while not valid_int:
            i = input("> ")
            try:
                i = int(i)
                valid_int = True
            except:
                print('Please enter a number')
        if i not in range(len(targets)+1):
            print('Select a valid target')
            valid_target = False
        else:
            valid_target = True
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
def check_if_dead(allies, enemies, battlers):
    dead_bodies = []
    for ally in allies:
        if ally.alive == False:
            dead_bodies.append(ally)
    for target in enemies:
        if target.alive == False:
            dead_bodies.append(target)
    for dead in dead_bodies:
        if dead in battlers:
            battlers.remove(dead)
        if dead in enemies:
            enemies.remove(dead)
        elif dead in allies:
            allies.remove(dead)

# Fully heal a target
def fully_heal(target):
    target.stats['hp'] = target.stats['maxHp']

def fully_recover_mp(target):
    target.stats['mp'] = target.stats['maxMp']

def create_enemy_group(lvl):
    from enemies import possible_enemies
    enemies_to_appear = []
    for enemy in possible_enemies:
        lowlvl, highlvl = possible_enemies[enemy]
        if lowlvl <= lvl <= highlvl:
            enemies_to_appear.append(enemy)
    
    # Dictionary for quantity of enemies to battle.
    # If lvl < 5 -> up to 3 enemies
    # If lvl < 10 -> up to 4 enemies
    # ...
    enemy_quantity_for_level = {3 : 1,
                                5 : 2, 
                                10 : 3, 
                                100 : 4}
    
    max_enemies = 1
    for max_level in enemy_quantity_for_level:
        if lvl < max_level:
            max_enemies = enemy_quantity_for_level[max_level]
            break

    enemy_group = []
    # Select x enemies, being x a random number between 1 and max_enemies
    for i in range(random.randint(1, max_enemies)):
        enemy_instance = random.choice(enemies_to_appear)()
        enemy_group.append(enemy_instance)
    return enemy_group