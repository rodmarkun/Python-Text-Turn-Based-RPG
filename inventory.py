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
            return 0
        elif i <= len(self.items):
            item = self.items[i-1]
            # TODO: Control both of these vars to avoid crash when selling items:
            moneyForItem, amountToSell = item.sell()
            self.decrease_item_amount(item, amountToSell)
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

    def decrease_item_amount(self, item, amount):
        for actualItem in self.items:
            if item.name == actualItem.name:
                actualItem.amount -= amount
                if actualItem.amount <= 0:
                    self.items.remove(actualItem)
            
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
                # Items sell for 50% the value they are worth for
                moneyToReceive = int(round(self.individual_value * 0.5 * amountToSell))
                print('Are you sure you want to sell {} {} for {}G? [y/n]'.format(amountToSell, 
                    self.name, moneyToReceive))
                confirmation = input("> ")
                if confirmation == 'y':
                    print('{} {} sold for {}'.format(amountToSell, self.name, 
                        moneyToReceive))
                    return moneyToReceive, amountToSell
                else:
                    pass
            else:
                print('You don\'t have that many {}!'.format(self.name))
        return 0

    def buy(self, player):
        if self.amount > 1:
            print('How many do you want to buy?')
            amountToBuy = int(input("> "))
            price = self.individual_value * amountToBuy
            if amountToBuy > self.amount:
                print('The vendor does not have that many {}'.format(self.name))
            elif price > player.money:
                print('Not enough money!')
            else:
                itemForPlayer = self.create_item(amountToBuy)
                self.amount -= amountToBuy
                itemForPlayer.add_to_inventory_player(player.inventory)
                player.money -= price
        elif self.amount == 1 and self.individual_value <= player.money:
            itemForPlayer = self.create_item(1)
            itemForPlayer.add_to_inventory_player(player.inventory)
            self.amount = 0

    def create_item(self, amount):
        return Item(self.name, self.description, amount, self.individual_value, self.objectType)

    def add_to_inventory_player(self, inventory):
        amountAdded = self.amount
        self.add_to_inventory(inventory, amountAdded)
        print('{} {} was added to your inventory!'.format(amountAdded, self.name))

    def add_to_inventory(self, inventory, amount):
        alreadyInInventory = False
        for item in inventory.items:
            if self.name == item.name:
                item.amount += amount
                alreadyInInventory = True
        if not alreadyInInventory:
            self.amount = amount
            inventory.items.append(self)


    def show_info(self):
        return '[x{}] {} ({}) - {}G'.format(self.amount, self.name, self.objectType, self.individual_value)

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
        return '[x{}] {} ({}) {} - {}G'.format(self.amount, self.name, self.objectType, self.show_stats(), self.individual_value)
    
    def show_stats(self):
        statsString = '[ '
        for stat in self.statChangeList:
            sign = '+'
            if self.statChangeList[stat] < 0:
                sign = ''
            statsString += '{} {}{} '.format(stat, sign, self.statChangeList[stat])
        statsString += ']'
        return statsString
    
    def create_item(self, amount):
        return Equipment(self.name, self.description, amount, self.individual_value, self.objectType, self.statChangeList)

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
    
    def create_item(self, amount):
        return Potion(self.name, self.description, amount, self.individual_value, self.objectType, self.stat, self.amountToChange)