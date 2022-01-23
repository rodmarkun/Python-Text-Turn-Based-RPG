import inventory
import random

class Shop():
    def __init__(self, itemSet) -> None:
        self.itemSet = itemSet
        self.inventory = inventory.Inventory()
        self.add_items_to_inventory_shop()

    def add_items_to_inventory_shop(self):
        itemQuantity = random.randint(len(self.itemSet), len(self.itemSet) * 2)
        for _ in range(itemQuantity):
            random.choice(self.itemSet).add_to_inventory(self.inventory, 1)