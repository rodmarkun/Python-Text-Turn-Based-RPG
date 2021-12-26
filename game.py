# Python Text-Based RPG
# Pablo Rodríguez Martín - @rodmarkun

import cmd
import textwrap
import sys
import os
import data

screen_width = 100

##### Title Screen #####
def title_screen_selections():
    option = int(input("> "))
    if option == (1):
        play()
    elif option == (2):
        help_menu()
    elif option == (3):
        sys.exit()
    while option not in [1,2,3]:
        print("Please enter a valid command")
        option = int(input("> "))

def title_screen():
    print('############################')
    print('# Welcome to the text RPG! #')
    print('############################')
    print('#         1 - Play         #')
    print('#         2 - Help         #')
    print('#         3 - Quit         #')
    print('############################')
    title_screen_selections()

def help_menu():
    os.system('clear')
    print("Do you really need help in here? LMAO")

def play():
    myPlayer = data.Player("Test Player")
    myEnemy = data.Imp()
    data.combat(myPlayer, myEnemy)

if __name__ == "__main__":
    title_screen()