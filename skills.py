'''
Skill is the parent class for Spells(matk) and Combos(atk)
'''
class Skill():
    def __init__(self, name, description, cost, isTargeted) -> None:
        self.name = name
        self.description = description
        self.cost = cost
        self.isTargeted = isTargeted

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
    def __init__(self, name, description, power, cost, isTargeted) -> None:
        super().__init__(name, description, cost, isTargeted)
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
    def __init__(self, name, description, cost, isTargeted) -> None:
        super().__init__(name, description, cost, isTargeted)
    
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
    def __init__(self, name, description, power, mpCost, isTargeted) -> None:
        super().__init__(name, description, power, mpCost, isTargeted)

    def effect(self, caster, target):
        if self.check_mp(caster):
            dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
        target.take_dmg(dmg)

class HealingSpell(Spell):
    def __init__(self, name, description, power, mpCost, isTargeted) -> None:
        super().__init__(name, description, power, mpCost, isTargeted)
    
    def effect(self, caster, target):
        amountToHeal = 0
        if self.check_mp(caster):
            amountToHeal = self.power + round(caster.stats['matk']/2)
        target.heal(amountToHeal)

class BuffDebuffSpell(Spell):
    def __init__(self, name, description, power, mpCost, isTargeted, statToChange, amountToChange, turns) -> None:
        super().__init__(name, description, power, mpCost, isTargeted)
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns

    def effect(self, caster, target):
        if self.check_mp(caster) and not self.check_already_has_buff(target):
            buff = BuffDebuff(self.name, target, self.statToChange, self.amountToChange, self.turns)
            buff.activate()

##### COMBOS #####

class SlashCombo(Combo):
    def __init__(self, name, description, comboCost, isTargeted, timesToHit) -> None:
        super().__init__(name, description, comboCost, isTargeted)
        self.timesToHit = timesToHit

    def effect(self, caster, target):
        if self.check_cp(caster):
            print('{} attacks {} {} times!'.format(caster.name, target.name, self.timesToHit))
            for _ in range(self.timesToHit):
                caster.normal_attack(target)

class ArmorBreakingCombo(Combo):
    def __init__(self, name, description, cost, isTargeted, armorDestroyed) -> None:
        super().__init__(name, description, cost, isTargeted)
        self.armorDestroyed = armorDestroyed
    
    def effect(self, caster, target):
        if self.check_cp(caster):
            print('{} pierces {}\'s armor!'.format(caster.name, target.name))
            if not self.check_already_has_buff(target):
                armorBreak = BuffDebuff('Armor Break', target, 'def', self.armorDestroyed, 4)
                armorBreak.activate()
                caster.normal_attack(target)
            
class VampirismCombo(Combo):
    def __init__(self, name, description, cost, isTargeted, percentHeal) -> None:
        super().__init__(name, description, cost, isTargeted)
        self.percentHeal = percentHeal

    def effect(self, caster, target):
        if self.check_cp(caster):
            amountToRecover = caster.normal_attack(target) * self.percentHeal
            caster.heal(round(amountToRecover))

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

fireball = DamageSpell('Fireball', '', 15, 3, True)
divineBlessing = HealingSpell('Divine Blessing', '', 8, 4, True)
benettFantasticVoyage = BuffDebuffSpell('Bennett\'s Fantastic Voyage', '', 0, 5, False, 'atk', 0.5, 3)

slashCombo1 = SlashCombo('Slash Combo I', '', 3, True, 3)
armorBreaker1 = ArmorBreakingCombo('Armor Break I', '', 2, True, -0.3)
vampireStab1 = VampirismCombo('Vampire Stab I', '', 2, True, 0.5)