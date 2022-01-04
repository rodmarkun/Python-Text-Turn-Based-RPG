class Skill():
    def __init__(self, name, description, power, mpCost) -> None:
        self.name = name
        self.description = description
        self.power = power
        self.mpCost = mpCost
    
    def check_mp(self, caster):
        if caster.stats['mp'] < self.mpCost:
            print('Not enough MP!')
            return False
        else:
            print('{} casts {}!'.format(caster.name, self.name))
            caster.stats['mp'] -= self.mpCost
            return True

class SimpleOffensiveSpell(Skill):
    def __init__(self, name, description, power, mpCost) -> None:
        super().__init__(name, description, power, mpCost)

    def effect(self, caster, target):
        if self.check_mp(caster):
            dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
            return dmg
        return 0

class SimpleHealingSpell(Skill):
    def __init__(self, name, description, power, mpCost) -> None:
        super().__init__(name, description, power, mpCost)
    
    def effect(self, caster, target):
        if self.check_mp(caster):
            amountToHeal = self.power + round(caster.stats['matk']/2)
            return amountToHeal
        return 0

class BuffDebuffSpell(Skill):
    def __init__(self, name, description, power, mpCost, statToChange, amountToChange, turns) -> None:
        super().__init__(name, description, power, mpCost)
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns

    def effect(self, caster, target):
        if self.check_mp(caster) and not self.check_already_has_buff(target):
            buff = BuffDebuff(self.name, target, self.statToChange, self.amountToChange, self.turns)
            buff.activate()

    def check_already_has_buff(self, target):
        for bd in target.buffsAndDebuffs:
            if bd.name == self.name:
                print('{} already has {}'.format(target.name, self.name))
                return True
        return False

class BuffDebuff():
    def __init__(self, name, target, statToChange, amountToChange, turns) -> None:
        self.name = name
        self.target = target
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns
        self.diference = 0

    def activate(self):
        self.target.buffsAndDebuffs.append(self)
        if self.amountToChange < 0:
            print('{} has their {} debuffed by {} for {} turns'.format(self.target.name, 
                                        self.statToChange, self.amountToChange, self.turns))
        else:
            print('{} has their {} buffed by {}% for {} turns'.format(self.target.name, 
                                        self.statToChange, self.amountToChange * 100, self.turns))
        self.difference = int(self.target.stats[self.statToChange] * self.amountToChange)
        self.target.stats[self.statToChange] += self.difference
        
    def check_turns(self):
        self.turns -= 1
        if self.turns <= 0:
            self.deactivate()

    def deactivate(self):
        print('The effect of {} has ended'.format(self.name))
        self.target.buffsAndDebuffs.remove(self)
        self.target.stats[self.statToChange] -= self.difference

fireball = SimpleOffensiveSpell('Fireball', '', 15, 3)
divineBlessing = SimpleHealingSpell('Divine Blessing', '', 8, 4)
benettFantasticVoyage = BuffDebuffSpell('Bennett\'s Fantastic Voyage', '', 0, 5, 'atk', 0.5, 3)