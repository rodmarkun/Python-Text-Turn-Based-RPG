# Python Text-Based RPG
# Pablo Rodríguez Martín - @rodmarkun

import cmd
import textwrap
import sys
import os
import random
import combat, enemies, text, player, inventory, items

##### Title Screen #####
def title_screen_selections():
    text.title_screen()
    option = int(input("> "))
    if option == 1:
        play()
    elif option == 2:
        text.help_menu()
    elif option == 3:
        sys.exit()
    while option not in [1,2,3]:
        print("Please enter a valid command")
        option = int(input("> "))

def inventory_selections(player):
    option = input("> ")
    while option.lower() != 'q':
        if option.lower() == 's':
            player.money += player.inventory.sell_item()
        elif option.lower() == 'd':
            player.inventory.drop_item()
        elif option.lower() == 'e':
            player.equip_item(player.inventory.equip_item())
        else:
            pass
        option = input("> ")

def play():
    myPlayer = player.Player("Test Player")
    potions = inventory.Item('Health Potion', 'a', 4, 10)
    potions.add_to_inventory(myPlayer.inventory)
    items.debug_sword.add_to_inventory(myPlayer.inventory)
    items.dagger.add_to_inventory(myPlayer.inventory)

    while myPlayer.alive:
        text.play_menu()
        option = int(input("> "))
        if option == 1:
            randomChosenEnemy = random.randint(1, 2)
            if randomChosenEnemy == 1:
                enemy = enemies.Imp()
            elif randomChosenEnemy == 2:
                enemy = enemies.Golem()
            combat.combat(myPlayer, enemy)
        elif option == 2:
            text.showStats(myPlayer)
        elif option == 3:
            myPlayer.assign_aptitude_points()
        elif option == 4:
            text.inventory_menu()
            myPlayer.inventory.show_inventory()
            inventory_selections(myPlayer)
        elif option == 5:
            combat.fully_heal(myPlayer)
        else:
            pass

if __name__ == "__main__":
    title_screen_selections()