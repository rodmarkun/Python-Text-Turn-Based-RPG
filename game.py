# Python Text-Based RPG
# Pablo Rodríguez Martín - @rodmarkun

from re import M
from ssl import MemoryBIO
import sys
import random
import text, player, items, events

##### Title Screen #####
def title_screen_selections():
    text.title_screen()
    option = input("> ")
    while option not in ['1','2','3']:
        print("Please enter a valid command")
        option = input("> ")
    if option == '1':
        play()
    elif option == '2':
        text.help_menu()
    elif option == '3':
        sys.exit()

##### Inventory menu #####
def inventory_selections(player):
    option = input("> ")
    while option.lower() != 'q':
        if option.lower() == 'u':
            player.use_item(player.inventory.use_item())
        elif option.lower() == 'd':
            player.inventory.drop_item()
        elif option.lower() == 'e':
            player.equip_item(player.inventory.equip_item())
        else:
            pass
        option = input("> ")

##### Initializing function #####
def play():
    # Player instantiation
    myPlayer = player.Player("Test Player")

    give_initial_items(myPlayer)

    while myPlayer.alive:
        text.play_menu()
        option = input("> ")
        if option == '1':
            generate_event(myPlayer)
        elif option == '2':
            text.showStats(myPlayer)
        elif option == '3':
            myPlayer.assign_aptitude_points()
        elif option == '4':
            text.inventory_menu()
            myPlayer.inventory.show_inventory()
            inventory_selections(myPlayer)
        elif option == '5':
            myPlayer.show_quests()
        else:
            print("Please enter a valid command")

def give_initial_items(myPlayer):
    print(text.initial_event_text)
    option = str(input("> "))
    while option not in ['1', '2', '3']:
        option = str(input("> "))
    if option == '1':
        items.rustySword.add_to_inventory_player(myPlayer.inventory)
        items.noviceArmor.add_to_inventory_player(myPlayer.inventory)
    elif option == '2':
        items.brokenDagger.add_to_inventory_player(myPlayer.inventory)
        items.noviceArmor.add_to_inventory_player(myPlayer.inventory)
    elif option == '3':
        items.oldStaff.add_to_inventory_player(myPlayer.inventory)
        items.oldRobes.add_to_inventory_player(myPlayer.inventory)
    print('[ Remember to equip these items in Inventory > Equip Items ]')

def generate_event(myPlayer):
    # Event chances (in %)
    combat_chance = 70
    shop_chance = 20
    heal_chance = 10

    eventList = random.choices(events.event_type_list, weights=(combat_chance, shop_chance, heal_chance), k=1)
    # random.choices returns a list so we need to use eventList[0]
    event = random.choice(eventList[0])
    event.effect(myPlayer)
    if event.isUnique:
        events.event_type_list.eventList.remove(event)


if __name__ == "__main__":
    title_screen_selections()