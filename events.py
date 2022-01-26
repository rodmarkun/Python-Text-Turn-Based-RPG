import combat
import random
import text
import shops
import items
import enemies
import quest

# Handles events (Enemy encounters, shops, healing places...)
class Event():
    def __init__(self, name, successChance, isUnique) -> None:
        self.name = name
        self.successChance = successChance
        self.isUnique = isUnique

    def check_success(self):
        if self.successChance < random.randint(0, 100):
            return False
        return True

    def add_event_to_event_list(self):
        if type(self) == FixedCombatEvent:
            event_type_list[0].append(self)
        elif type(self) == ShopEvent:
            event_type_list[1].append(self)
        elif type(self) == HealingEvent:
            event_type_list[2].append(self)

class RandomCombatEvent(Event):
    def __init__(self, name) -> None:
        super().__init__(name, 100, False)
    
    def effect(self, player):
        enemies = combat.create_enemy_group(player.lvl)
        combat.combat(player, enemies)

class FixedCombatEvent(Event):
    def __init__(self, name, enemyList) -> None:
        super().__init__(name, 10, True)
        self.enemyList = enemyList

    def effect(self, player):
        combat.combat(player, self.enemyList)


class ShopEvent(Event):
    def __init__(self, name, isUnique, encounterText, enterText, talkText, exitText, itemSet, quest) -> None:
        super().__init__(name, 100, isUnique)
        self.encounter = encounterText
        self.enter = enterText
        self.exit = exitText
        self.talk = talkText
        self.itemSet = itemSet
        self.quest = quest
    
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
                    if self.quest != None and self.quest.status == 'Not Active':
                        self.quest.propose_quest(player)
                    else:
                        print(self.talk)
                text.shop_menu(player)
                option = input ("> ").lower()
        print(self.exit)

class HealingEvent(Event):
    def __init__(self, name, encounterText, successText, failText, refuseText, successChance, isUnique, healingAmount) -> None:
        super().__init__(name, successChance, isUnique)
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

# Quests
# -> Caesarus
caesarus_bandit_combat = FixedCombatEvent('Caesarus and his bandits', enemies.enemy_list_caesarus_bandit)
quest_caesarus_bandit = quest.Quest('Caesarus and his bandits.', text.quest_caesarus_bandit_text, 100, 100, None, caesarus_bandit_combat, text.shop_quest_caesarus_bandits)

# Event Instances
random_combat = RandomCombatEvent('Random Combat')
shop_rik_armor = ShopEvent('Rik\'s Armor Shop', False, text.rik_armor_shop_encounter, text.rik_armor_shop_enter, text.rik_armor_shop_talk, text.rik_armor_shop_exit, items.rik_armor_shop_item_set, quest_caesarus_bandit)
shop_itz_magic = ShopEvent('Itz Magic', False, text.itz_magic_encounter, text.itz_magic_enter, text.itz_magic_talk, text.itz_magic_exit, items.itz_magic_item_set, None)
heal_medussa_statue = HealingEvent('Medussa\'s Statue', text.medussa_statue_encounter, text.medussa_statue_success,
                                text.medussa_statue_fail, text.medussa_statue_refuse, 70, False, 50)
# Grouped events
combat_event_list = [random_combat]
shop_event_list = [shop_itz_magic, shop_rik_armor]
heal_event_list = [heal_medussa_statue]

# List of all events, divided by type
event_type_list = [combat_event_list, shop_event_list, heal_event_list]