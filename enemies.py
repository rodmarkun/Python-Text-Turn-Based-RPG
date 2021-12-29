import data

class Imp(data.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 20,
                    'hp' : 20,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 4,
                    'def' : 5,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 10
        }
        xpReward = 40
        super().__init__('Imp', stats, xpReward)

class Golem(data.Enemy):
    def __init__(self) -> None:
        stats = {'maxHp' : 60,
                    'hp' : 60,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 4,
                    'def' : 8,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 10
        }
        xpReward = 40
        super().__init__('Imp', stats, xpReward)