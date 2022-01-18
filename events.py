import combat
import random
import text

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
    def __init__(self, name, encounterText, enterText, exitText, itemSet) -> None:
        super().__init__(name, 100)
        self.encounter = encounterText
        self.enter = enterText
        self.exit = exitText
        self.itemSet = itemSet
    
    def effect(self, player):
        print(self.encounter)
        enter = input("> ").lower()
        while enter not in ['y', 'n']:
            enter = input("> ").lower()
        if enter == 'y':
            print(self.enter)
            text.shop_menu(player)
            # Buy stuff
        elif enter == 'n':
            print(self.exit)
        print(self.exit)

class HealingEvent(Event):
    def __init__(self, name, encounterText, successText, failText, successChance, healingAmount) -> None:
        super().__init__(name, successChance)
        self.encounter = encounterText
        self.success = successText
        self.fail = failText
        self.healingAmount = healingAmount

    def effect(self, player):
        print(self.encounter)
        if self.check_success():
            print(self.success)
            player.heal(self.healingAmount)
        else:
            print(self.fail)

# Event Instances
random_combat = RandomCombatEvent('Random Combat')
shop_rik_armor = ShopEvent('Rik\'s Armor Shop', text.rik_armor_shop_encounter, text.rik_armor_shop_enter, text.rik_armor_shop_exit, None)
shop_itz_magic = ShopEvent('Itz Magic', text.itz_magic_encounter, text.itz_magic_enter, text.itz_magic_exit, None)
heal_medussa_statue = HealingEvent('Medussa\'s Statue', text.medussa_statue_encounter, text.medussa_statue_success,
                                text.medussa_statue_fail, 70, 50)

# Grouped events
combat_event_list = [random_combat]
shop_event_list = [shop_itz_magic, shop_rik_armor]
heal_event_list = [heal_medussa_statue]

# List of all events, divided by type
event_type_list = [combat_event_list, shop_event_list, heal_event_list]