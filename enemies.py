import combat

class Imp(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 20,
                    'hp' : 20,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 4,
                    'def' : 6,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 5
        }
        xpReward = 7
        super().__init__('Imp', stats, xpReward)

class Golem(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 38,
                    'hp' : 38,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 3,
                    'def' : 9,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 0
        }
        xpReward = 14
        super().__init__('Golem', stats, xpReward)

class GiantSlime(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 200,
                    'hp' : 200,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 3,
                    'def' : 1,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 0
        }
        super().__init__('Giant Slime', stats, 20)