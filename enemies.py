import data

class Imp(data.Enemy):

    def __init__(self) -> None:
        stats = {'hp' : 20,
                    'mp' : 10,
                    'atk' : 5,
                    'def' : 5,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 10
        }
        xpReward = 40
        super().__init__('Imp', stats, xpReward)