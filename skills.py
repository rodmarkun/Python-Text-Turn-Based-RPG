'''
Skill is the parent class for Spells(matk) and Combos(atk)
'''
class Skill():
    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        self.name = name
        self.description = description
        self.cost = cost
        self.isTargeted = isTargeted
        self.defaultTarget = defaultTarget

    def check_already_has_buff(self, target):
        for bd in target.buffsAndDebuffs:
            if bd.name == self.name:
                print('{} has their {}\'s duration restarted'.format(target.name, self.name))
                bd.restart()
                return True
        return False

'''
Spells consume mp (Magic Points), which are restored by leveling up, using items,
events... They also increment when upgrading the WIS (Wisdom) aptitude or equipping
certain items. They use matk (Magic Attack) and their own power to calculate the
damage done.
'''
class Spell(Skill):
    def __init__(self, name, description, power, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.power = power

    def check_mp(self, caster):
        if caster.stats['mp'] < self.cost:
            print('Not enough MP!')
            return False
        else:
            print('{} casts {}!'.format(caster.name, self.name))
            caster.stats['mp'] -= self.cost
            return True

'''
Combos consume cp (Combo Points), which counter is by default set to 0 when a battle
starts and increment as the Battler performs normal attacks. They can also increment
by using certain Skills. They usually have special effects and integrates normal
attacks within them.
'''
class Combo(Skill):
    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
    
    def check_cp(self, caster):
        if caster.comboPoints < self.cost:
            print('Not enough Combo Points!')
            return False
        else:
            print('{} uses {}!'.format(caster.name, self.name))
            caster.comboPoints -= self.cost
            return True

##### SPELLS #####

class DamageSpell(Spell):
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)

    def effect(self, caster, target):
        if self.check_mp(caster):
            if self.isTargeted:
                dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
                target.take_dmg(dmg)
            else:
                if self.defaultTarget == 'all_enemies':
                    for enemy in target:
                        dmg = self.power + (caster.stats['matk'] - enemy.stats['mdef'])
                        enemy.take_dmg(dmg)

class RecoverySpell(Spell):
    def __init__(self, name, description, power, mpCost, stat, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.stat = stat
    
    def effect(self, caster, target):
        amountToRecover = 0
        if self.check_mp(caster):
            amountToRecover = self.power + round(caster.stats['matk']/2)
        if self.stat == 'hp':
            target.heal(amountToRecover)
        elif self.stat == 'mp':
            target.recover_mp(amountToRecover)

class BuffDebuffSpell(Spell):
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget, statToChange, amountToChange, turns) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns

    def effect(self, caster, target):
        if self.check_mp(caster) and not self.check_already_has_buff(target):
            buff = BuffDebuff(self.name, target, self.statToChange, self.amountToChange, self.turns)
            buff.activate()

##### COMBOS #####

class SlashCombo(Combo):
    def __init__(self, name, description, comboCost, isTargeted, defaultTarget, timesToHit) -> None:
        super().__init__(name, description, comboCost, isTargeted, defaultTarget)
        self.timesToHit = timesToHit

    def effect(self, caster, target):
        if self.check_cp(caster):
            print('{} attacks {} {} times!'.format(caster.name, target.name, self.timesToHit))
            for _ in range(self.timesToHit):
                caster.normal_attack(target)

class ArmorBreakingCombo(Combo):
    def __init__(self, name, description, cost, isTargeted, defaultTarget, armorDestroyed) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.armorDestroyed = armorDestroyed
    
    def effect(self, caster, target):
        if self.check_cp(caster):
            print('{} pierces {}\'s armor!'.format(caster.name, target.name))
            if not self.check_already_has_buff(target):
                armorBreak = BuffDebuff('Armor Break', target, 'def', self.armorDestroyed, 4)
                armorBreak.activate()
                caster.normal_attack(target)
            
class VampirismCombo(Combo):
    def __init__(self, name, description, cost, isTargeted, defaultTarget, percentHeal) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.percentHeal = percentHeal

    def effect(self, caster, target):
        if self.check_cp(caster):
            amountToRecover = caster.normal_attack(target) * self.percentHeal
            caster.heal(round(amountToRecover))

class RecoveryCombo(Combo):
    def __init__(self, name, description, cost, stat, amountToChange, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.stat = stat
        self.amountToChange = amountToChange
    
    def effect(self, caster, target):
        if self.check_cp(caster):
            if self.stat == 'hp':
                target.heal(self.amountToChange)
            elif self.stat == 'mp':
                target.recover_mp(self.amountToChange)

##### MISC #####

class BuffDebuff():
    def __init__(self, name, target, statToChange, amountToChange, turns) -> None:
        self.name = name
        self.target = target
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns
        self.maxTurns = turns
        self.diference = 0

    def activate(self):
        self.target.buffsAndDebuffs.append(self)
        if self.amountToChange < 0:
            print('{} has their {} debuffed by {}% for {} turns'.format(self.target.name, 
                                        self.statToChange, self.amountToChange * 100, self.turns))
        else:
            print('{} has their {} buffed by {}% for {} turns'.format(self.target.name, 
                                        self.statToChange, self.amountToChange * 100, self.turns))
        self.difference = int(self.target.stats[self.statToChange] * self.amountToChange)
        self.target.stats[self.statToChange] += self.difference

    def restart(self):
        self.turns = self.maxTurns

    def check_turns(self):
        self.turns -= 1
        if self.turns <= 0:
            self.deactivate()

    def deactivate(self):
        print('The effect of {} has ended'.format(self.name))
        self.target.buffsAndDebuffs.remove(self)
        self.target.stats[self.statToChange] -= self.difference

##### SPELL & COMBO INSTANCES #####

spellFireball = DamageSpell('Fireball', '', 15, 3, True, None)
spellDivineBlessing = RecoverySpell('Divine Blessing', '', 8, 4, 'hp', True, None)
spellEnhanceWeapon = BuffDebuffSpell('Enhance Weapon', '', 0, 5, False, 'self', 'atk', 0.5, 3)
spellInferno = DamageSpell('Inferno', '', 14, 7, False, 'all_enemies')

comboSlash1 = SlashCombo('Slash Combo I', '', 3, True, None, 3)
comboSlash2 = SlashCombo('Slash Combo II', '', 3, True, None, 4)
comboArmorBreaker1 = ArmorBreakingCombo('Armor Break I', '', 2, True, None, -0.3)
comboVampireStab1 = VampirismCombo('Vampire Stab I', '', 2, True, None, 0.5)
comboVampireStab2 = VampirismCombo('Vampire Stab II', '', 2, True, None, 0.75)
comboMeditation1 = RecoveryCombo('Meditation I', '', 1, 'mp', 5, False, 'self')
comboMeditation2 = RecoveryCombo('Meditation II', '', 2, 'mp', 15, False, 'self')