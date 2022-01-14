from random import randint
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
                    'speed' : 9,
                    'critCh' : 5
        }
        super().__init__('Imp', stats, xpReward=8, goldReward=randint(1, 6))

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
                    'speed' : 4,
                    'critCh' : 0
        }
        super().__init__('Golem', stats, xpReward=15, goldReward=randint(2, 15))

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
        super().__init__('Giant Slime', stats, xpReward=30, goldReward=randint(3, 15))

possible_enemies = {Imp : (1, 3),
                    Golem : (2, 4),
                    GiantSlime : (3, 6)}