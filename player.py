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

        self.lvl = 1 # Player Lvl
        self.xp = 0 # Current xp
        self.xpToNextLvl = 25 # Amount of xp to reach next lvl is multiplied by 1.5 per level
        self.aptitudes = {'str' : 5,
                    'dex' : 5,
                    'int' : 5,
                    'wis' : 5,
                    'const' : 5
        }
        '''
        When an aptitude is leveled up, certain stats also increase:
        STR -> ATK + 1
        DEX -> SPD + 1, CRIT + 1
        INT -> MATK + 1
        WIS -> MP + 5
        CONST -> MAXHP + 5
        '''

        self.aptitudePoints = 0 # Points for upgrading aptitudes
        self.inventory = inventory.Inventory() # Player's inventory
        self.equipment = {'Weapon' : None,
                            'Armor' : None} # Player's equipment, can be further expanded
        self.money = 999 # Current money
        self.combos = [skills.slashCombo1, skills.armorBreaker1, skills.vampireStab1] # Player's selection of combos (atk, cp)
        self.spells = [skills.fireball, skills.divineBlessing, skills.benettFantasticVoyage] # Player's selection of spells (matk, mp)
        self.isAlly = True # Check if battler is an ally or not
    
    # Equip an item (must be of type 'Equipment')
    def equip_item(self, equipment):
        if type(equipment) == inventory.Equipment:
            actualEquipment = self.equipment[equipment.objectType]
            if actualEquipment != None:
                print('{} has been unequiped.'.format(actualEquipment.name))
                actualEquipment.add_to_inventory(self.inventory)
                for stat in actualEquipment.statChangeList:
                    self.stats[stat] -= actualEquipment.statChangeList[stat]
            for stat in equipment.statChangeList:
                self.stats[stat] += equipment.statChangeList[stat]
            self.equipment[equipment.objectType] = equipment
            print('{} has been equipped.'.format(equipment.name))
            print(equipment.show_stats())
        else:
            print('{} is not equipable.'.format(equipment.name))
        text.inventory_menu()
        self.inventory.show_inventory()

    # Use an item
    def use_item(self, item):
        usable_items = [inventory.Potion]
        if type(item) in usable_items:
            item.activate(self)
        text.inventory_menu()
        self.inventory.show_inventory()

    # Adds a certain amount of exp to the player
    def add_exp(self, exp):
        self.xp += exp
        print("You earn {}xp".format(exp))
        # Level up:
        while(self.xp >= self.xpToNextLvl):
            self.xp -= self.xpToNextLvl
            self.lvl += 1
            self.xpToNextLvl = round(self.xpToNextLvl * 1.5)
            for stat in self.stats:
                self.stats[stat] += 1
            self.aptitudePoints += 1
            combat.fully_heal(self)
            combat.fully_recover_mp(self)
            print("Level up! You are now level {}. You have {} aptitude points".format(self.lvl, self.aptitudePoints))

    # Adds a certain amount of money to the player
    def add_money(self, money):
        self.money += money
        print("You earn {} coins".format(money))

    # Loop for upgrading aptitudes with aptitude points
    def assign_aptitude_points(self):
        optionsDictionary = {'1' : 'str',
                            '2' : 'dex',
                            '3' : 'int',
                            '4' : 'wis',
                            '5' : 'const'}
        text.showAptitudes(self)
        option = input("> ")
        while option.lower() != 'q':
            try:
                if self.aptitudePoints >= 1:
                    aptitudeToAssign = optionsDictionary[option]
                    self.aptitudes[aptitudeToAssign] += 1
                    print('{} is now {}!'.format(aptitudeToAssign, self.aptitudes[aptitudeToAssign]))
                    self.update_stats_to_aptitudes(aptitudeToAssign)
                    self.aptitudePoints -= 1
                else:
                    print('Not enough points!')
            except:
                print('Please enter a valid number')
            option = input("> ")


    '''
    Updates stats when an aptitude is leveled up
    
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

    def buy_from_vendor(self, vendor):
        text.shop_buy(self)
        vendor.inventory.show_inventory()
        i = int(input("> "))
        while i != 0:
            if i <= len(vendor.inventory.items) and i > 0:
                vendor.inventory.items[i-1].buy(self)
                if vendor.inventory.items[i-1].amount <= 0:
                    vendor.inventory.items.pop(i - 1)
                vendor.inventory.show_inventory()
                i = int(input("> "))
            