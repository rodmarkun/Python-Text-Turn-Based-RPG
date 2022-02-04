import inventory
import text
import combat

class Player(combat.Battler):
    '''
    Main class for player handling. Includes all information about stats
    and progression made throughout the game.

    Attributes:
    lvl : int
        Player's current level. Starts in 1 by default.
    xp : int
        Player's current xp (Experience Points).
    xpToNextLvl : int
        Necessary amount of xp to reach next level.
    comboPoints : int
        Amount of current Combo Points (CP).
    aptitudes : Dictionary
        Dictionary for handling the aptitude system. Each aptitude grants
        stat bonuses:
            STR -> ATK + 1
            DEX -> SPD + 1, CRIT + 1
            INT -> MATK + 1
            WIS -> MP + 5
            CONST -> MAXHP + 5
    aptitudePoints : int
        Amount of points for upgrading aptitudes.
    inventory : Inventory
        Player's inventory.
    equipment : Dictionary
        Dictionary that defines current player's equipment.
    money : int
        Current amount of money (gold/coins).
    combos : List
        List of combos the user is capable to use.
    spells : List
        List of spells the user is capable to use.
    activeQuests : List
        List of active Quests.
    completedQuests : List
        List of completed Quests
    '''
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
        self.xpToNextLvl = 35 # Amount of xp to reach next lvl is multiplied by 1.5 per level
        self.comboPoints = 0
        self.aptitudes = {'str' : 5,
                    'dex' : 5,
                    'int' : 5,
                    'wis' : 5,
                    'const' : 5
        }

        self.aptitudePoints = 0 # Points for upgrading aptitudes
        self.inventory = inventory.Inventory() # Player's inventory
        self.equipment = {'Weapon' : None,
                            'Armor' : None} # Player's equipment, can be further expanded
        self.money = 20 # Current money
        self.combos = [] # Player's selection of combos (atk, cp)
        self.spells = [] # Player's selection of spells (matk, mp)

        self.activeQuests = []
        self.completedQuests = []
        
        self.isAlly = True # Check if battler is an ally or not
    
    def normal_attack(self, defender):
        self.addComboPoints(1)
        return super().normal_attack(defender)

    def equip_item(self, equipment):
        '''
        Player equips certain item. Must be of type 'Equipment'.

        Parameters:
        equipment : Equipment
            Item to equip.
        '''
        if type(equipment) == inventory.Equipment:
            actualEquipment = self.equipment[equipment.objectType]
            if actualEquipment != None:
                print(f'{actualEquipment.name} has been unequiped.')
                actualEquipment.add_to_inventory(self.inventory, 1)
                # Remove the combo from previous combo
                if actualEquipment.combo != None:
                    self.combos.remove(actualEquipment.combo)
                    print(f'You can no longer use the combo: {actualEquipment.combo.name}')
                # Remove stats from previous equipment
                for stat in actualEquipment.statChangeList:
                    self.stats[stat] -= actualEquipment.statChangeList[stat]
            # Adds stats to player
            for stat in equipment.statChangeList:
                self.stats[stat] += equipment.statChangeList[stat]
            self.equipment[equipment.objectType] = equipment.create_item(1)
            # Adds equipment's combo
            if equipment.combo != None and equipment.combo not in self.combos:
                self.combos.append(equipment.combo)
                print(f'You can now use the combo: {equipment.combo.name}')
            self.inventory.decrease_item_amount(equipment, 1)
            print(f'{equipment.name} has been equipped.')
            print(equipment.show_stats())
        else:
            if equipment != None:
                print('{} is not equipable.'.format(equipment.name))
        text.inventory_menu()
        self.inventory.show_inventory()

    def use_item(self, item):
        '''
        Uses a certain item. Item must be in the "usable_items" list
        to be used.

        Parameters:
        item : Item
            Item to be used.
        '''
        usable_items = [inventory.Potion, inventory.Grimoire]
        if type(item) in usable_items:
            item.activate(self)
        text.inventory_menu()
        self.inventory.show_inventory()

    def add_exp(self, exp):
        '''
        Adds a certain amount of exp to the player and also handles leveling up.
        When leveling up, player also recovers hp/mp fully and has a +1 to all stats.

        Parameters:
        exp : int
            Amount of exp points to add.
        '''
        self.xp += exp
        print(f"You earn {exp}xp")
        # Level up:
        while(self.xp >= self.xpToNextLvl):
            self.xp -= self.xpToNextLvl
            self.lvl += 1
            # You can change this formula for different exp progression
            self.xpToNextLvl = round(self.xpToNextLvl * 1.5 + 10 * self.lvl * self.lvl)
            for stat in self.stats:
                self.stats[stat] += 1
            self.aptitudePoints += 1
            combat.fully_heal(self)
            combat.fully_recover_mp(self)
            print(f"Level up! You are now level {self.lvl}. You have {self.aptitudePoints} aptitude points")

    def add_money(self, money):
        '''
        Adds a certain amount of money to the player.

        Parameters:
        money : int
            Amount of money to be added.
        '''
        self.money += money
        print(f"You earn {money} coins")

    def assign_aptitude_points(self):
        '''
        Menu for upgrading aptitudes.
        '''
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
                    print(f'{aptitudeToAssign} is now {self.aptitudes[aptitudeToAssign]}!')
                    self.update_stats_to_aptitudes(aptitudeToAssign)
                    self.aptitudePoints -= 1
                else:
                    print('Not enough points!')
            except:
                print('Please enter a valid number')
            option = input("> ")

    def update_stats_to_aptitudes(self, aptitude):
        '''
        Assigns the corresponding stat points when upgrading aptitudes.

        Parameters:
        aptitude : str
            Aptitude to be upgraded.
        '''
        if aptitude == 'str':
            self.stats['atk'] += 1
        elif aptitude == 'dex':
            self.stats['speed'] += 1
            self.stats['critCh'] += 1
        elif aptitude == 'int':
            self.stats['matk'] += 1
        elif aptitude == 'wis':
            self.stats['maxMp'] += 3
        elif aptitude == 'const':
            self.stats['maxHp'] += 3

    def buy_from_vendor(self, vendor):
        '''
        Buys an item from a vendor.

        Parameters:
        vendor : Shop
            Shop where the player is going to buy.
        '''
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
        
    def show_quests(self):
        '''
        Shows current quests, active and completed.
        '''
        print('/// ACTIVE ///')
        for actq in self.activeQuests:
            actq.show_info()
        print('/// COMPLETED ///')
        for cmpq in self.completedQuests:
            cmpq.show_info()

    def addComboPoints(self, points):
        '''
        Adds a certain amount of combo points.

        Parameters:
        points : int
            Amount of points to be added.
        '''
        self.comboPoints += points