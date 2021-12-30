class Inventory():

    def __init__(self) -> None:
        self.items = []

    def show_inventory(self):
        index = 1
        for item in self.items:
            print(str('{} - [x{}] {}'.format(index, item.amount, item.name)))
            index += 1

    def drop_item(self):
        print('\nWhich item do you want to drop? ["0" to Quit]')
        self.show_inventory()
        i = int(input("> "))
        # TODO: Control out of range dropping
        if i == 0:
            print('Closing inventory...')
        else:
            item = self.items[i-1]
            if item.amount == 1:
                self.items.pop(i - 1)
                print('You dropped 1 {}.\nNow your inventory looks like this:'.format(
                    item.name))
            else:
                print('You have {} of this item, how many do you want to drop?'.format(item.amount))
                amountToDrop = int(input("> "))
                # TODO: Control amount to drop
                item.amount -= amountToDrop
                print('You dropped {} {}.\nNow your inventory looks like this:'.format(amountToDrop,
                    item.name))
            self.show_inventory()

    @property
    def total_worth(self):
        totalWorth = 0
        for item in self.items:
            totalWorth += item.amount * item.individual_value
        print('Total inventory worth is: {}'.format(totalWorth))
            
class Item():

    def __init__(self, name, description, amount, individual_value) -> None:
        self.name = name
        self.description = description
        self.amount = amount
        self.individual_value = individual_value

    @property
    def total_worth(self):
        return self.amount * self.individual_value

    def sell(self):
        if self.amount >= 1:
            print('How many do you want to sell?')
            amountToSell = int(input("> "))
            if amountToSell <= self.amount:
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