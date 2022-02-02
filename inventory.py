class Inventory():
    '''
    Manages player's inventory and items. Can be modified to have a certain capacity.
    It is also used for shops.

    Attributes:
    items : List
        List of current items in the inventory
    '''
    def __init__(self) -> None:
        self.items = []

    def show_inventory(self):
        '''
        Shows all items from the inventory (indexed).
        '''
        index = 1
        for item in self.items:
            print(str(f'{index} - {item.show_info()}'))
            index += 1

    def drop_item(self):
        '''
        Selects and drops an item from the inventory.
        '''
        print('\nWhich item do you want to drop? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('Closing inventory...')
        elif i <= len(self.items):
            item = self.items[i-1]
            item.drop()
            if item.amount <= 0:
                self.items.pop(i - 1)
            print('Now your inventory looks like this:')
            self.show_inventory()

    def sell_item(self):
        '''
        Selects and sells an item from the inventory.

        Returns:
        moneyForItem : int
            Amount of money for item(s) sold.
        '''
        print('\nWhich item do you want to sell? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('Closing inventory...')
            return 0
        elif i <= len(self.items):
            item = self.items[i-1]
            moneyForItem, amountToSell = item.sell()
            self.decrease_item_amount(item, amountToSell)
            return moneyForItem

    def equip_item(self):
        '''
        Selects and equips a certain item from inventory (must be type 'Equipment').

        Returns:
        item : Item
            Returns the item for the player to equip. Returns None if it chose
            a non-equipable object.
        '''
        print('\nWhich item do you want to equip? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('Closing inventory...')
            return None
        elif i <= len(self.items):
            item = self.items[i-1]
            if type(item) == Equipment:
                return item
            else:
                print('Please choose an equipable object.')
                return None

    def use_item(self):
        '''
        Selects and uses a certain item from inventory (must be type 'Consumable').

        Returns:
        item : Item
            Returns the item for the player to use. Returns None if it chose
            a non-consumable object
        '''
        print('\nWhich item do you want to use? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('Closing inventory...')
            return None
        elif i <= len(self.items):
            item = self.items[i-1]
            if item.objectType == 'Consumable':
                item.amount -= 1
                if item.amount <= 0:
                    self.items.pop(i - 1)
                return item
            else:
                print('Please choose a consumable object.')
                return None

    def decrease_item_amount(self, item, amount):
        '''
        Decreases a certain amount of a certain item in this inventory.
        This was made because of the shop system.

        Parameters:
        item : Item
            Item to decrease the amount from
        amount : int
            Amount to decrease
        '''
        for actualItem in self.items:
            if item.name == actualItem.name:
                actualItem.amount -= amount
                if actualItem.amount <= 0:
                    self.items.remove(actualItem)
            
class Item():
    '''
    Items are always stored in a certain inventory. They can be either:
    - Equipment (Weapons & Armor)
    - Consumables (Potions & Grimoires)

    Attributes:
    name : str
        Name of the item
    description : str
        Description of the item
    amount : int
        Amount of this item in this inventory
    individualValue : int
        Amount of gold one of this item is worth
    objectType : str
        Object type
    '''
    # TODO: Change Object Type to inheritance
    def __init__(self, name, description, amount, individualValue, objectType) -> None:
        self.name = name
        self.description = description
        self.amount = amount
        self.individualValue = individualValue
        self.objectType = objectType

    def drop(self):
        '''
        Drops a certain amount of this item. Dropped items can never be recovered.
        '''
        if self.amount == 1:
            print(f'You dropped 1 {self.name}.')
            self.amount -= 1
        else:
            print(f'You have {self.amount} of this item, how many do you want to drop?')
            amountToDrop = int(input("> "))
            if amountToDrop > self.amount:
                print('You don\'t have that many!')
            else:
                self.amount -= amountToDrop
                print(f'You dropped {amountToDrop} {self.name}.')

    def sell(self):
        '''
        Sells a certain amount of this item. Sold items can never be recovered.

        Returns:
        moneyToReceive : int
            Amount of money to receive for selling X amount of this item.
        amountToSell : int
            Amount of this item to be sold.
        '''
        if self.amount >= 1:
            print('How many do you want to sell?')
            amountToSell = int(input("> "))
            if amountToSell <= self.amount and amountToSell > 0:
                # Items sell for 50% the value they are worth for
                moneyToReceive = int(round(self.individualValue * 0.5 * amountToSell))
                print(f'Are you sure you want to sell {amountToSell} {self.name} for {moneyToReceive}G? [y/n]')
                confirmation = input("> ")
                if confirmation == 'y':
                    print(f'{amountToSell} {self.name} sold for {moneyToReceive}')
                    return moneyToReceive, amountToSell
                else:
                    pass
            else:
                print(f'You don\'t have that many {self.name}!')
        return 0, 0

    def buy(self, player):
        '''
        Buys a certain amount of this item.

        Parameters:
        player : Player
            Player which buys the item.    
        '''
        if self.amount > 1:
            print('How many do you want to buy?')
            amountToBuy = int(input("> "))
            price = self.individualValue * amountToBuy
            if amountToBuy > self.amount:
                print(f'The vendor does not have that many {self.name}')
            elif price > player.money:
                print('Not enough money!')
            else:
                itemForPlayer = self.create_item(amountToBuy)
                self.amount -= amountToBuy
                itemForPlayer.add_to_inventory_player(player.inventory)
                player.money -= price
        elif self.amount == 1 and self.individualValue <= player.money:
            itemForPlayer = self.create_item(1)
            itemForPlayer.add_to_inventory_player(player.inventory)
            player.money -= self.individualValue
            self.amount = 0

    def create_item(self, amount):
        '''
        Creates a copy of this item with a custom "amount".
        This was added for the shop system.

        Parameters:
        amount : int
            Amount for the created item to have.
        '''
        return Item(self.name, self.description, amount, self.individualValue, self.objectType)

    def add_to_inventory_player(self, inventory):
        '''
        Adds the item to the player's inventory.

        Parameters:
        inventory : Inventory
            Inventory of the player.
        '''
        amountAdded = self.amount
        self.add_to_inventory(inventory, amountAdded)
        print(f'{amountAdded} {self.name} was added to your inventory!')

    def add_to_inventory(self, inventory, amount):
        '''
        Adds certain amount of this item to an inventory.
        Made specially for the shop system.

        Parameters:
        inventory : Inventory
            Inventory in which the item will be added.
        amount : int
            Amount of the item to add
        '''
        alreadyInInventory = False
        for item in inventory.items:
            if self.name == item.name:
                item.amount += amount
                alreadyInInventory = True
                break
        if not alreadyInInventory:
            self.amount = amount
            inventory.items.append(self)


    def show_info(self):
        '''
        Shows the info of this specific object.

        Returns:
        info : str
            String with amount, name, objectType and individual value of this object.
        '''
        return f'[x{self.amount}] {self.name} ({self.objectType}) - {self.individualValue}G'


class Equipment(Item):
    '''
    Items player can equip for increased stats and unique abilities (combos).

    Parameters:
    statChangeList : Dictionary
        Dictionary that defines the changes in stats after equipping this item.
        Example:
        {'hp' : 3,
        'atk' : 2,
        'speed' : -2
        }
        This would increase hp by 3, atk by 2 and decrease speed by 2.
    combo : Combo
        Combo this equipment gives access to.
    '''
    def __init__(self, name, description, amount, individual_value, objectType, statChangeList, combo) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.statChangeList = statChangeList
        self.combo = combo
    
    def show_info(self):
        return f'[x{self.amount}] {self.name} ({self.objectType}) [{self.show_stats()}] - {self.individualValue}G'

    def show_stats(self):
        '''
        Shows this equipment stats.

        Returns:
        statsString : str
            String which contains all the stat changes of this equipment.
        '''
        statsString = ' '
        for stat in self.statChangeList:
            sign = '+'
            if self.statChangeList[stat] < 0:
                sign = ''
            statsString += f'{stat} {sign}{self.statChangeList[stat]} '
        return statsString
    
    def create_item(self, amount):
        return Equipment(self.name, self.description, amount, self.individualValue, self.objectType, self.statChangeList, self.combo)

class Potion(Item):
    '''
    Players use potions for recovering either MP or HP.

    Attributes:
    stat : str
        Stat to recover
    amountToChange : int
        Amount to recover
    '''
    def __init__(self, name, description, amount, individual_value, objectType, stat, amountToChange) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.stat = stat
        self.amountToChange = amountToChange

    def activate(self, caster):
        '''
        Activates the use of this object. (Recovers HP/MP)

        Parameters:
        caster : Player
            Player to recover.
        '''
        print('{} uses a {}!'.format(caster.name, self.name))
        if self.stat == 'hp':
            caster.heal(self.amountToChange)
        elif self.stat == 'mp':
            caster.recover_mp(self.amountToChange)
    
    def create_item(self, amount):
        return Potion(self.name, self.description, amount, self.individualValue, self.objectType, self.stat, self.amountToChange)

class Grimoire(Item):
    '''
    Grimoires are items the player can use for learning new spells.

    Attributes:
    spell : Spell
        Spell the player will learn.
    '''
    def __init__(self, name, description, amount, individual_value, objectType, spell) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.spell = spell

    def activate(self, caster):
        '''
        Activates the use of this object. (Learns a new spell)

        Parameters:
        caster : Player
            Player which learns the spell.
        '''
        alreadyLearnt = False
        for skill in caster.spells:
            if skill.name == self.spell.name:
                alreadyLearnt = True
                break
        if alreadyLearnt:
            print('You already know this spell.')
        else:
            print(f'Using a \"{self.name}\" you have learnt to cast: \"{self.spell.name}\"!')
            caster.spells.append(self.spell)

    def create_item(self, amount):
        return Grimoire(self.name, self.description, amount, self.individualValue, self.objectType, self.spell)