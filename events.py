import combat
import random
import text
import shops
import items

# Handles events (Enemy encounters, shops, healing places...)
class Event():
    def __init__(self, name, successChance) -> None:
        self.name = name
        self.successChance = successChance

    def check_success(self):
        if self.successChance < random.randint(0, 100):
            return False
        return True

class RandomCombatEvent(Event):
    def __init__(self, name) -> None:
        super().__init__(name, 100)
    
    def effect(self, player):
        enemies = combat.create_enemy_group(player.lvl)
        combat.combat(player, enemies)

class ShopEvent(Event):
    def __init__(self, name, encounterText, enterText, talkText, exitText, itemSet) -> None:
        super().__init__(name, 100)
        self.encounter = encounterText
        self.enter = enterText
        self.exit = exitText
        self.talk = talkText
        self.itemSet = itemSet
    
    def effect(self, player):
        print(self.encounter)
        enter = input("> ").lower()
        while enter not in ['y', 'n']:
            enter = input("> ").lower()
        if enter == 'y':
            print(self.enter)
            vendor = shops.Shop(self.itemSet)
            text.shop_menu(player)
            option = input ("> ").lower()
            while option != 'e':
                if option == 'b':
                    player.buy_from_vendor(vendor)
                elif option == 's':
                    player.money += player.inventory.sell_item()
                elif option == 't':
                    print(self.talk)
                text.shop_menu(player)
                option = input ("> ").lower()
        print(self.exit)

class HealingEvent(Event):
    def __init__(self, name, encounterText, successText, failText, refuseText, successChance, healingAmount) -> None:
        super().__init__(name, successChance)
        self.encounter = encounterText
        self.success = successText
        self.fail = failText
        self.refuse = refuseText
        self.healingAmount = healingAmount

    def effect(self, player):
        print(self.encounter)
        accept = input("> ").lower()
        while accept not in ['y', 'n']:
            accept = input("> ").lower()
        if accept == 'y':
            if self.check_success():
                print(self.success)
                player.heal(self.healingAmount)
            else:
                print(self.fail)
        elif accept == 'n':
            print(self.refuse)

# Event Instances
random_combat = RandomCombatEvent('Random Combat')
shop_rik_armor = ShopEvent('Rik\'s Armor Shop', text.rik_armor_shop_encounter, text.rik_armor_shop_enter, text.rik_armor_shop_talk, text.rik_armor_shop_exit, items.rik_armor_shop_item_set)
shop_itz_magic = ShopEvent('Itz Magic', text.itz_magic_encounter, text.itz_magic_enter, text.itz_magic_talk, text.itz_magic_exit, items.itz_magic_item_set)
heal_medussa_statue = HealingEvent('Medussa\'s Statue', text.medussa_statue_encounter, text.medussa_statue_success,
                                text.medussa_statue_fail, text.medussa_statue_refuse, 70, 50)

# Grouped events
combat_event_list = [random_combat]
shop_event_list = [shop_itz_magic, shop_rik_armor]
heal_event_list = [heal_medussa_statue]

# List of all events, divided by type
event_type_list = [combat_event_list, shop_event_list, heal_event_list]