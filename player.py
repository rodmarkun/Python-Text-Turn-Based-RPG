import inventory
import text
import combat
import skills

class Player(combat.Battler):

    def __init__(self, name) -> None:
        stats = {'maxHp' : 25,
                    'hp' : 25,
                    'maxMp' : 10,
                    'mp' : 10,
                    'atk' : 10,
                    'def' : 10,
                    'matk' : 10,
                    'mdef' : 10,
                    'speed' : 10,
                    'critCh' : 10
        }

        super().__init__(name, stats)

        self.lvl = 1
        self.xp = 0
        self.xpToNextLvl = 25
        self.aptitudes = {'str' : 5,
                    'dex' : 5,
                    'int' : 5,
                    'wis' : 5,
                    'const' : 5
        }
        self.aptitudePoints = 5
        self.inventory = inventory.Inventory()
        self.equipment = {'Weapon' : None,
                            'Armor' : None}
        self.money = 0
        self.combos = []
        self.spells = [skills.fireball]
    
    def equip_item(self, equipment):
        if equipment != None:
            if type(equipment) == inventory.Equipment:
                actualEquipment = self.equipment[equipment.equipmentType]
                if actualEquipment != None:
                    actualEquipment.add_to_inventory(self.inventory)
                    for stat in actualEquipment.statChangeList:
                        self.stats[stat] -= actualEquipment.statChangeList[stat]
                self.equipment[equipment.equipmentType] = equipment
                print('{} has been equipped.'.format(equipment.name))
                statChangeList = equipment.statChangeList
                for stat in statChangeList:
                    self.stats[stat] += statChangeList[stat]
                    print('{} +{}'.format(stat, statChangeList[stat]))
            else:
                print('{} is not equipable.'.format(equipment.name))
        text.inventory_menu()
        self.inventory.show_inventory()

    def add_exp(self, exp):
        self.xp += exp
        print("You earn {}xp".format(exp))
        while(self.xp >= self.xpToNextLvl):
            self.xp -= self.xpToNextLvl
            self.lvl += 1
            self.xpToNextLvl = round(self.xpToNextLvl * 1.5)
            for stat in self.stats:
                self.stats[stat] += 1
            self.aptitudePoints += 1
            combat.fully_heal(self)
            self.stats['mp'] = self.stats['maxMp']
            print("Level up! You are now level {}.".format(self.lvl))

    def assign_aptitude_points(self):
        text.showAptitudes(self)
        option = int(input("> "))
        optionsDictionary = {1 : 'str',
                            2 : 'dex',
                            3 : 'int',
                            4 : 'wis',
                            5 : 'const'}
        while option != 6:
            if option in range(1, 7):
                if self.aptitudePoints >=1:
                    aptitudeToAssign = optionsDictionary[option]
                    self.aptitudes[aptitudeToAssign] += 1
                    print('{} is now {}!'.format(aptitudeToAssign, self.aptitudes[aptitudeToAssign]))
                    self.update_stats_to_aptitudes(aptitudeToAssign)
                    self.aptitudePoints -= 1
                else:
                    print('Not enough points!')
            else:
                print('Not a valid character!')
            option = int(input("> "))

    '''
    When an aptitude is leveled up, certain stats also increase:
    STR -> ATK + 1
    DEX -> SPD + 1, CRIT + 1
    INT -> MATK + 1
    WIS -> MP + 5
    CONST -> MAXHP + 5
    '''
    def update_stats_to_aptitudes(self, aptitude):
        if aptitude == 'str':
            self.stats['atk'] += 1
        elif aptitude == 'dex':
            self.stats['speed'] += 1
            self.stats['critCh'] += 1
        elif aptitude == 'int':
            self.stats['matk'] += 1
        elif aptitude == 'wis':
            self.stats['mp'] += 3
        elif aptitude == 'const':
            self.stats['maxHp'] += 3