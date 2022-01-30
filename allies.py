import combat
# Imports combat for inheriting Battler's data

'''
Allies help the player in battle. For now all the ones detailed here
are summoned by spells, though allies granted by an event or any
other reason can also be defined here. There are mainly their stats.
'''

class SummonedSkeleton(combat.Battler):
    def __init__(self) -> None:
        stats = {'maxHp' : 15,
                    'hp' : 15,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 5,
                    'def' : 3,
                    'matk' : 1,
                    'mdef' : 2,
                    'speed' : 7,
                    'critCh' : 5
        }
        super().__init__('Skeleton', stats)
        self.isAlly = True

class SummonedFireSpirit(combat.Battler):
    def __init__(self) -> None:
        stats = {'maxHp' : 20,
                    'hp' : 20,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 12,
                    'def' : 3,
                    'matk' : 4,
                    'mdef' : 5,
                    'speed' : 9,
                    'critCh' : 5
        }
        super().__init__('Fire Spirit', stats)
        self.isAlly = True