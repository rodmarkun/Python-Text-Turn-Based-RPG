from constants import VERSION

def title_screen():
    print('############################')
    print('# Welcome to the text RPG! #')
    print('############################')
    print('#         1 - Play         #')
    print('#         2 - About        #')
    print('#         3 - Quit         #')
    print('############################')

def about_menu():
    print(f'Python Text Turn-Based RPG System v{VERSION}')
    print('Made by Pablo Rodríguez Martín (@rodmarkun)')
    print('\nHello there! What lies before your eyes is an attempt of making a functional\
\nturn-based RPG completely in Python. Keep in mind that it is more about making a system rather than a whole game.')
    print('You can battle enemies, purchase items from shops, complete quests, learn spells\
\nand combos...')
    print('\nI highly recommend checking the code and modifying whatever you want. Have fun!')

def play_menu():
    print('############################')   
    print('#        1 - Walk          #')
    print('#      2 - See stats       #')
    print('#      3 - Aptitudes       #')
    print('#      4 - Inventory       #')
    print('#        5 - Quests        #')
    print('############################')

def showStats(player):
    print('############################')
    print('#          STATS           #')
    print('############################')
    print('HP: {}/{}'.format(player.stats['hp'], player.stats['maxHp']))
    print('MP: {}/{}'.format(player.stats['mp'],  player.stats['maxMp']))
    print('ATK: {}'.format(player.stats['atk']))
    print('DEF: {}'.format(player.stats['def']))
    print('MATK: {}'.format(player.stats['matk']))
    print('MDEF: {}'.format(player.stats['mdef']))
    print('SPD: {}'.format(player.stats['speed']))
    print('CRIT: {}'.format(player.stats['critCh']))
    print('############################')
    print('#        APTITUDES         #')
    print('############################')
    print('STR: {}'.format(player.aptitudes['str']))
    print('DEX: {}'.format(player.aptitudes['dex']))
    print('INT: {}'.format(player.aptitudes['int']))
    print('WIS: {}'.format(player.aptitudes['wis']))
    print('CONST: {}'.format(player.aptitudes['const']))
    print('############################')
    print('MONEY: {}'.format(player.money))
    print('############################')
    print('#        EQUIPMENT         #')
    print('############################')
    for equipment in player.equipment:
        if player.equipment[equipment] is not None:
            print('{}: {}'.format(equipment, player.equipment[equipment].name))
        else:
            print('{}:'.format(equipment))

def showAptitudes(player):
    print('############################')
    print('#        POINTS: {}        #'.format(player.aptitudePoints))
    print('#    SELECT AN APTITUDE    #')
    print('############################')
    print('1 - STR (Current: {})'.format(player.aptitudes['str']))
    print('2 - DEX (Current: {})'.format(player.aptitudes['dex']))
    print('3 - INT (Current: {})'.format(player.aptitudes['int']))
    print('4 - WIS (Current: {})'.format(player.aptitudes['wis']))
    print('5 - CONST (Current: {})'.format(player.aptitudes['const']))
    print('Q - Quit menu')
    print('############################')

def inventory_menu():
    print('############################')
    print('#    U - Use an item       #')
    print('#    D - Drop an item      #')
    print('#    E - Equip an item     #')
    print('#        Q - Quit          #')
    print('############################')

def combat_menu(player, allies, enemies):
    print('############################')
    print('{} - HP: {}/{} - MP: {}/{} - CP: {}'.format(player.name, player.stats['hp'], player.stats['maxHp'],
                                                player.stats['mp'], player.stats['maxMp'], player.comboPoints))
    for ally in allies:
        if ally != player:
            print('{} - HP: {}/{}'.format(ally.name, ally.stats['hp'], ally.stats['maxHp']))
    print('-----------------------------')
    for enemy in enemies:
        print('{} - HP: {}/{}'.format(enemy.name, enemy.stats['hp'], enemy.stats['maxHp']))
    print('############################')
    print('#       A - Attack         #')
    print('#       C - Combos         #')
    print('#       S - Spells         #')
    print('############################')

def spell_menu(player):
    print('############################')
    print('     SPELLS ["0" to Quit]   ')
    print('############################')
    index = 1
    for s in player.spells:
            print(str('{} - {} - {}MP'.format(index, s.name, s.cost)))
            index += 1

def combo_menu(player):
    print('############################')
    print('     COMBOS ["0" to Quit]   ')
    print('############################')
    index = 1
    for c in player.combos:
            print(str('{} - {} - {}CP'.format(index, c.name, c.cost)))
            index += 1

def select_objective(targets):
    print('############################')
    print('    Select an objective:    ')
    print('############################')
    index = 1
    for t in targets:
        print('{} - {} - HP: {}/{}'.format(index, t.name, t.stats['hp'], t.stats['maxHp']))
        index += 1
    print('############################')

def shop_menu(player):
    print('############################')
    print('      SHOP - Money: {}      '.format(player.money))
    print('############################')
    print('       B - Buy Items        ')
    print('       S - Sell Items       ')
    print('         T - Talk           ')
    print('         E - Exit           ')
    print('############################')

def shop_buy(player):
    print('############################')
    print('      SHOP - Money: {}      '.format(player.money))
    print('       ["0" to Quit]        ')
    print('############################')

def enter_shop(name):
    if name == 'Rik\'s Armor Shop':
        print(rik_armor_shop_encounter)
    elif name == 'Itz Magic':
        print(itz_magic_encounter)
    
### Events' text

# Initial event
initial_event_text = 'This is finally the day. You have registered your name in the Adventurers Guild.\n\
As a gift, they let you choose between three sets of gear. Which one do you choose?\n\
1 - Warrior Set\n\
2 - Rogue Set\n\
3 - Magic Set'

## Shops

# Rik's armor shop
rik_armor_shop_encounter = 'Wandering around a small village, you find yourself in front of a shop.\n \
There is a sign on the door. It says: <Rik\'s Armor Shop>. \n\
Enter? [y/n]'
rik_armor_shop_enter = '\"Hello there, friend! What do you need?\" a big and strong man asks.'
rik_armor_shop_talk = '' # Talk dialogue
rik_armor_shop_exit = 'You leave the village in search for more adventures.'

#Itz Magic
itz_magic_encounter = 'You stumble upon a swamp. Looking around, you find a small hut.\n\
There is a sign on the door. It says <Itz\'s Magic Shop>\n\
Enter? [y/n]'
itz_magic_enter = 'Inside is a short woman with big glasses. She seems to be a witch. \n\
She whispers:\"Well, well, what do we have here?... Come, take a look!\"'
itz_magic_talk = '' # Talk dialogue
itz_magic_exit = 'You leave the swamp, continuing your journey.'

## Healing

# Medussa Statue
medussa_statue_encounter = 'On the top of a hill, you find what seems to be a small shrine. \n\
There is a statue of a goddess forgotten long ago. \n\
Not knowing exactly why, you feel the urge to pay respects. \n\
Kneel before it? [y/n]'
medussa_statue_success = 'You feel a pleasant warmth inside you.'
medussa_statue_fail = 'Nothing happens. It was probably just your imagination.'
medussa_statue_refuse = 'You decide not to kneel.'

# Inn encounter
inn_event_encounter = 'While travelling across a forest, you find an Inn.\n\
You can rest here, but it won\'t be free.\n\
Pay 15G for one night? [y/n]'
inn_event_success = 'You rest in a comfortable bed tonight.'
inn_event_fail = 'You do not have enough money.'
inn_event_refuse = 'You decide not to pay.'

## Quests
quest_caesarus_bandit_text = 'That Caesarus and his bandits have been causing\n\
trouble to nearby villages. Take care of them.'
shop_quest_caesarus_bandits = 'Have you heard about the bandits? They have been terrorizing\n\
villages from around here. A guy named Caesarus leads them. If you take care of them,\n\
maybe the villagers would reward you or something. '