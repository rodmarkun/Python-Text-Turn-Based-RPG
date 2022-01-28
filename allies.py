import combat

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