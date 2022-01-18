# Python Text-Based RPG
# Pablo Rodríguez Martín - @rodmarkun

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
        elif option.lower() == 's':
            player.money += player.inventory.sell_item()
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

    debug_add_test_items(myPlayer)

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
        else:
            print("Please enter a valid command")

# DEBUG
def debug_add_test_items(myPlayer):
    # Adding some testing items
    items.hpPotions.add_to_inventory(myPlayer.inventory)
    items.mpPotions.add_to_inventory(myPlayer.inventory)
    items.longsword.add_to_inventory(myPlayer.inventory)
    items.dagger.add_to_inventory(myPlayer.inventory)
    items.staff.add_to_inventory(myPlayer.inventory)
    items.clothArmor.add_to_inventory(myPlayer.inventory)
    items.warhammer.add_to_inventory(myPlayer.inventory)
    items.ironArmor.add_to_inventory(myPlayer.inventory)

def generate_event(myPlayer):
    # Event chances (in %)
    combat_chance = 60
    shop_chance = 10
    heal_chance = 30

    eventList = random.choices(events.event_type_list, weights=(combat_chance, shop_chance, heal_chance), k=1)
    # random.choices returns a list so we need to use eventList[0]
    random.choice(eventList[0]).effect(myPlayer)


if __name__ == "__main__":
    title_screen_selections()