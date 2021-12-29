# Python Text-Based RPG
# Pablo Rodríguez Martín - @rodmarkun

import cmd
import textwrap
import sys
import os
import data
import random
import enemies, text

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

def play():
    myPlayer = data.Player("Test Player")

    while myPlayer.alive:
        text.play_menu()
        option = int(input("> "))
        if option == 1:
            randomChosenEnemy = random.randint(1, 2)
            if randomChosenEnemy == 1:
                enemy = enemies.Imp()
            elif randomChosenEnemy == 2:
                enemy = enemies.Golem()
            data.combat(myPlayer, enemy)
        elif option == 2:
            text.showStats(myPlayer)
        elif option == 3:
            data.assignAptitudePoints(myPlayer)
        elif option == 4:
            data.fullyHeal(myPlayer)
        else:
            pass

if __name__ == "__main__":
    title_screen_selections()