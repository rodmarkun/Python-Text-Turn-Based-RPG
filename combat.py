import random
import skills
import text

class Battler():
    def __init__(self, name, stats) -> None:
        self.name = name
        self.stats = stats
        self.alive = True
        self.buffsAndDebuffs = []

class Enemy(Battler):

    def __init__(self, name, stats, xpReward) -> None:
        super().__init__(name, stats)
        self.xpReward = xpReward

def normal_attack(attacker, defender):
    print('{} attacks!'.format(attacker.name))
    dmg = round(attacker.stats['atk'] * (100/(100 + defender.stats['def'])))
    if attacker.stats['critCh'] > random.randint(0, 100):
        print('Critical blow!')
        dmg *= 2
    take_dmg(attacker, defender, dmg)

def take_dmg(attacker, defender, dmg):
    if dmg < 0: dmg = 0
    defender.stats['hp'] -= dmg
    print('{} takes {} damage!'.format(defender.name, dmg))
    if defender.stats['hp'] <= 0:
        print('{} has been slain.'.format(defender.name))
        defender.alive = False

def combat(player, enemy):
    print('############################')
    print('A wild {} has appeared!'.format(enemy.name))
    while player.alive and enemy.alive:
        text.combat_menu(player, enemy)
        cmd = input('> ').lower()
        while cmd not in ['a', 'c', 's']:
            cmd = input('> ').lower()
        if 'a' in cmd:
            normal_attack(player, enemy)
            if enemy.alive == True:
                normal_attack(enemy, player)
        elif 's' in cmd:
            # TODO: This needs more control
            text.spell_menu(player)
            option = int(input("> "))
            if option != 0:
                skill_effect(player.spells[option - 1], player, enemy)
                if enemy.alive == True:
                    normal_attack(enemy, player)

        # A turn has passed
        for buffdebuff in player.buffsAndDebuffs:
            buffdebuff.turns -= 1
        for buffdebuff in enemy.buffsAndDebuffs:
            buffdebuff.turns -= 1
    if player.alive:
        player.buffsAndDebuffs.clear()
        player.add_exp(enemy.xpReward)

def heal(target, amount):
    if target.stats['hp'] + amount > target.stats['maxHp']:
        target.stats['hp'] = target.stats['maxHp']
    else:
        target.stats['hp'] += amount
    print('{} heals {} hp!'.format(target.name, amount))

def skill_effect(skill, caster, target):
    if type(skill) == skills.SimpleOffensiveSpell:
        amount = skill.effect(caster, target)
        take_dmg(caster, target, amount)
    elif type(skill) == skills.SimpleHealingSpell:
        # TODO: Change for target when multi-character combat is ready
        amount = skill.effect(caster, target)
        heal(caster, amount)
    elif type(skill) == skills.BuffDebuffSpell:
        skill.effect(caster, caster)

def fully_heal(target):
    target.stats['hp'] = target.stats['maxHp']