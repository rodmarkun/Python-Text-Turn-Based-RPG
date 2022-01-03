class Skill():
    def __init__(self, name, description, power, mpCost) -> None:
        self.name = name
        self.description = description
        self.power = power
        self.mpCost = mpCost

class SimpleOffensiveSpell(Skill):
    def __init__(self, name, description, power, mpCost) -> None:
        super().__init__(name, description, power, mpCost)

    def effect(self, caster, target):
        if caster.stats['mp'] < self.mpCost:
            print('Not enough MP!')
            return 0
        else:
            dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
            print('{} casts {}!'.format(caster.name, self.name))
            caster.stats['mp'] -= self.mpCost
            return dmg

fireball = SimpleOffensiveSpell('Fireball', '', 20, 3)