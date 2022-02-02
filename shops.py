import inventory
import random

class Shop():
    '''
    Handles shop management.

    Attributes:
    itemSet : List
        Item pool the shop can have.
    inventory : Inventory
        Shop's inventory
    '''
    def __init__(self, itemSet) -> None:
        self.itemSet = itemSet
        self.inventory = inventory.Inventory()
        self.add_items_to_inventory_shop()

    def add_items_to_inventory_shop(self):
        '''
        Adds new items to the shop's inventory.
        '''
        itemQuantity = random.randint(len(self.itemSet)//2, len(self.itemSet))
        for _ in range(itemQuantity):
            random.choice(self.itemSet).add_to_inventory(self.inventory, 1)