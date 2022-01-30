import combat
import random
import text
import shops
import items
import enemies
import quest

class Event():
    '''
    Handles events (Enemy encounters, shops, healing places...)

    Attributes: 
    name : str
        Name of the event
    successChance : int
        Chance of event succeding
    isUnique : bool
        True if event is unique and can only be played once. False if doesn't.
    '''
    def __init__(self, name, successChance, isUnique) -> None:
        self.name = name
        self.successChance = successChance
        self.isUnique = isUnique

    def check_success(self):
        '''
        Checks if event is successful or not

        Returns:
        True/False : bool
            True if event is successful, False if fail
        '''
        if self.successChance < random.randint(0, 100):
            return False
        return True

    def add_event_to_event_list(self):
        '''
        Adds event to a certain event-type list
        '''
        if type(self) == FixedCombatEvent:
            event_type_list[0].append(self)
        elif type(self) == ShopEvent:
            event_type_list[1].append(self)
        elif type(self) == HealingEvent:
            event_type_list[2].append(self)

class RandomCombatEvent(Event):
    '''
    Inherits Event. Used for basic random combats.

    Attributes:
    enemy_quantity_for_level : Dictionary
        Dictionary of number of enemies to appear based on level,
        follows this syntax: {levelUpToThisQuantityToAppear, Quantity}
        for example, {3 : 1} means that up to level 3, only 1 enemy will appear.
    '''
    def __init__(self, name) -> None:
        super().__init__(name, 100, False)
        self.enemy_quantity_for_level = {3 : 1,
                                        5 : 2, 
                                        10 : 3, 
                                        100 : 4}
    
    def effect(self, player):
        '''
        Triggers effect of the event.

        Parameters:
        player : Player
            Player for which the event happens
        '''
        enemy_group = combat.create_enemy_group(player.lvl, enemies.possible_enemies, self.enemy_quantity_for_level)
        combat.combat(player, enemy_group)

class FixedCombatEvent(Event):
    '''
    Inherits Event. Used for fixed combats (boss fights, quests...)

    Attributes:
    enemyList : List
        List of enemies to fight with
    '''
    def __init__(self, name, enemyList) -> None:
        super().__init__(name, 10, True)
        self.enemyList = enemyList

    def effect(self, player):
        '''
        Triggers effect of the event.

        Parameters:
        player : Player
            Player for which the event happens
        '''
        combat.combat(player, self.enemyList)


class ShopEvent(Event):
    '''
    Inherits Event. Used for shop events.

    Attributes:
    encounter : str
        Text when encountering the shop
    enter : str
        Text when entering the shop
    talk : str
        Text when talking with the shop owner
    exit : str
        Text when exiting the shop
    itemSet : List
        List of possible item classes to be sold in the shop
    quest : Quest
        Quest to be given when talking to the owner
    '''
    def __init__(self, name, isUnique, encounterText, enterText, talkText, exitText, itemSet, quest) -> None:
        super().__init__(name, 100, isUnique)
        self.encounter = encounterText
        self.enter = enterText
        self.exit = exitText
        self.talk = talkText
        self.itemSet = itemSet
        self.quest = quest
    
    def effect(self, player):
        '''
        Triggers effect of the event.

        Parameters:
        player : Player
            Player for which the event happens
        '''
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
    '''
    Inherits Event. Used for events where you're healed.

    Attributes:
    encounter : str
        Text when encountering the shop
    success : str
        Text when the event is successful
    fail : str
        Text when the event fails
    refuse : str
        Text when the player refuses to take part in the event
    healingAmount : str
        Amount to heal the player if successful
    '''
    def __init__(self, name, encounterText, successText, failText, refuseText, successChance, isUnique, healingAmount) -> None:
        super().__init__(name, successChance, isUnique)
        self.encounter = encounterText
        self.success = successText
        self.fail = failText
        self.refuse = refuseText
        self.healingAmount = healingAmount

    def effect(self, player):
        '''
        Triggers effect of the event.

        Parameters:
        player : Player
            Player for which the event happens
        '''
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

class InnEvent(HealingEvent):
    '''
    Inherits HealingEvent. Is always successful but comes at a cost.

    Attributes:
    cost : int
        Monetary cost of healing
    '''
    def __init__(self, name, encounterText, successText, failText, refuseText, healingAmount, cost) -> None:
        super().__init__(name, encounterText, successText, failText, refuseText, 100, False, healingAmount)
        self.cost = cost

    def effect(self, player):
        '''
        Triggers effect of the event.

        Parameters:
        player : Player
            Player for which the event happens
        '''
        print(self.encounter)
        accept = input("> ").lower()
        while accept not in ['y', 'n']:
            accept = input("> ").lower()
        if accept == 'y':
            if player.money >= self.cost:
                print(self.success)
                player.heal(self.healingAmount)
                player.money -= self.cost
            else:
                print(self.fail)
        elif accept == 'n':
            print(self.refuse)

# Quests
# -> Caesarus
caesarus_bandit_combat = FixedCombatEvent('Caesarus and his bandits', enemies.enemy_list_caesarus_bandit)
quest_caesarus_bandit = quest.Quest('Caesarus and his bandits.', text.quest_caesarus_bandit_text, text.shop_quest_caesarus_bandits, 100, 100, None, caesarus_bandit_combat, 5)

# Event Instances
random_combat = RandomCombatEvent('Random Combat')
shop_rik_armor = ShopEvent('Rik\'s Armor Shop', False, text.rik_armor_shop_encounter, text.rik_armor_shop_enter, text.rik_armor_shop_talk, text.rik_armor_shop_exit, items.rik_armor_shop_item_set, quest_caesarus_bandit)
shop_itz_magic = ShopEvent('Itz Magic', False, text.itz_magic_encounter, text.itz_magic_enter, text.itz_magic_talk, text.itz_magic_exit, items.itz_magic_item_set, None)
heal_medussa_statue = HealingEvent('Medussa\'s Statue', text.medussa_statue_encounter, text.medussa_statue_success,
                                text.medussa_statue_fail, text.medussa_statue_refuse, 70, False, 20)
inn_event = InnEvent('Inn', text.inn_event_encounter, text.inn_event_success, text.inn_event_fail, text.inn_event_refuse, 50, 15)
# Grouped events
combat_event_list = [random_combat]
shop_event_list = [shop_itz_magic, shop_rik_armor]
heal_event_list = [heal_medussa_statue, inn_event]

# List of all events, divided by type
event_type_list = [combat_event_list, shop_event_list, heal_event_list]