from random import randint
import combat

class Imp(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 18,
                    'hp' : 18,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 3,
                    'def' : 6,
                    'matk' : 1,
                    'mdef' : 2,
                    'speed' : 9,
                    'critCh' : 5
        }
        super().__init__('Imp', stats, xpReward=8, goldReward=randint(3, 6))

class Slime(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 30,
                    'hp' : 30,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 2,
                    'def' : 1,
                    'matk' : 1,
                    'mdef' : 1,
                    'speed' : 3,
                    'critCh' : 0
        }
        super().__init__('Slime', stats, xpReward=6, goldReward=randint(1, 6))

class Golem(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 38,
                    'hp' : 38,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 3,
                    'def' : 12,
                    'matk' : 5,
                    'mdef' : 4,
                    'speed' : 4,
                    'critCh' : 0
        }
        super().__init__('Golem', stats, xpReward=15, goldReward=randint(2, 15))

class GiantSlime(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 100,
                    'hp' : 100,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 3,
                    'def' : 1,
                    'matk' : 10,
                    'mdef' : 1,
                    'speed' : 2,
                    'critCh' : 0
        }
        super().__init__('Giant Slime', stats, xpReward=30, goldReward=randint(3, 15))

class Bandit(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 30,
                    'hp' : 30,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 6,
                    'def' : 4,
                    'matk' : 10,
                    'mdef' : 2,
                    'speed' : 10,
                    'critCh' : 15
        }
        super().__init__('Bandit', stats, xpReward=30, goldReward=randint(10, 15))

class CaesarusBandit(combat.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 50,
                    'hp' : 50,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 10,
                    'def' : 5,
                    'matk' : 10,
                    'mdef' : 2,
                    'speed' : 14,
                    'critCh' : 15
        }
        super().__init__('Caesarus, bandit leader', stats, xpReward=200, goldReward=randint(40, 60))

# Possible Enemy : (LowestPlayerLevelForAppearing, HighestPlayerLevelForAppearing)
possible_enemies = {Slime: (1, 2),
                    Imp : (1, 4),
                    Golem : (2, 10),
                    GiantSlime : (3, 100),
                    Bandit : (4, 100)}

# Fixed Combat Enemies
enemy_list_caesarus_bandit = [CaesarusBandit(), Bandit(), Bandit()]