import combat
'''
Manages player's inventory and items. Can be modified to have a certain capacity.
'''
class Inventory():

    def __init__(self) -> None:
        self.items = []

    # Show all items in the inventory
    def show_inventory(self):
        index = 1
        for item in self.items:
            print(str('{} - {}'.format(index, item.show_info())))
            index += 1

    # Drop an item from the inventory
    def drop_item(self):
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
            self.show_inventory()

    # Sell a certain item from inventory
    def sell_item(self):
        print('\nWhich item do you want to sell? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('Closing inventory...')
        elif i <= len(self.items):
            item = self.items[i-1]
            moneyForItem = item.sell()
            if item.amount <= 0:
                self.items.pop(i - 1)
            return moneyForItem

    # Equip a certain item from inventory (must be type 'Equipment')
    def equip_item(self):
        print('\nWhich item do you want to equip? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        if i == 0:
            print('Closing inventory...')
            return None
        elif i <= len(self.items):
            item = self.items[i-1]
            if type(item) == Equipment:
                self.items.pop(i - 1)
                return item
            else:
                print('Please choose an equipable object.')
                return None

    # Use a certain item of type 'Consumable'
    def use_item(self):
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
            
class Item():

    def __init__(self, name, description, amount, individual_value, objectType) -> None:
        self.name = name
        self.description = description
        self.amount = amount
        self.individual_value = individual_value
        self.objectType = objectType

    def drop(self):
        if self.amount == 1:
            print('You dropped 1 {}.\nNow your inventory looks like this:'.format(
                self.name))
            self.amount -= 1
        else:
            print('You have {} of this item, how many do you want to drop?'.format(self.amount))
            amountToDrop = int(input("> "))
            if amountToDrop > self.amount:
                print('You don\'t have that many!')
            else:
                self.amount -= amountToDrop
                print('You dropped {} {}.\nNow your inventory looks like this:'.format(amountToDrop,
                    self.name))

    def sell(self):
        if self.amount >= 1:
            print('How many do you want to sell?')
            amountToSell = int(input("> "))
            if amountToSell <= self.amount and amountToSell > 0:
                moneyToReceive = self.individual_value * amountToSell
                print('Are you sure you want to sell {} {} for {}? [y/n]'.format(amountToSell, 
                    self.name, moneyToReceive))
                confirmation = input("> ")
                if confirmation == 'y':
                    self.amount -= amountToSell
                    print('{} {} sold for {}'.format(amountToSell, self.name, 
                        moneyToReceive))
                    return moneyToReceive
                else:
                    pass
            else:
                print('You don\'t have that many {}!'.format(self.name))
        return 0

    def add_to_inventory(self, inventory):
        alreadyInInventory = False
        for item in inventory.items:
            if self.name == item.name:
                item.amount += self.amount
                alreadyInInventory = True
        if not alreadyInInventory:
            inventory.items.append(self)
        print('{} {} was added to your inventory!'.format(self.amount, self.name))
    
    def show_info(self):
        return '[x{}] {} ({})'.format(self.amount, self.name, self.objectType)

'''
Equipment shall be items but with an added dictionary statChangeList with stats to change
and a number with the amount of points that stat changes, like:
{'hp' : 3
    'atk' : 2
    'speed' : -2
}
This would increase hp by 3, atk by 2 and decrease speed by 2.
'''

# TODO: It could be interesting to add skills to some weapons
class Equipment(Item):
    def __init__(self, name, description, amount, individual_value, objectType, statChangeList) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.statChangeList = statChangeList
    
    def show_info(self):
        return '[x{}] {} ({}) {}'.format(self.amount, self.name, self.objectType, self.show_stats())
    
    def show_stats(self):
        statsString = '[ '
        for stat in self.statChangeList:
            sign = '+'
            if self.statChangeList[stat] < 0:
                sign = ''
            statsString += '{} {}{} '.format(stat, sign, self.statChangeList[stat])
        statsString += ']'
        return statsString

class Potion(Item):
    def __init__(self, name, description, amount, individual_value, objectType, stat, amountToChange) -> None:
        super().__init__(name, description, amount, individual_value, objectType)
        self.stat = stat
        self.amountToChange = amountToChange

    def activate(self, caster):
        print('{} uses a {}!'.format(caster.name, self.name))
        if self.stat == 'hp':
            caster.heal(self.amountToChange)
        elif self.stat == 'mp':
            caster.recover_mp(self.amountToChange)