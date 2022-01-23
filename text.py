def title_screen():
    print('############################')
    print('# Welcome to the text RPG! #')
    print('############################')
    print('#         1 - Play         #')
    print('#         2 - Help         #')
    print('#         3 - Quit         #')
    print('############################')

def help_menu():
    print("Do you really need help in here? LMAO")

def play_menu():
    print('############################')   
    print('#        1 - Walk          #')
    print('#      2 - See stats       #')
    print('#3 - Assign aptitude points#')
    print('#      4 - Inventory       #')
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

def combat_menu(player, enemies):
    print('############################')
    print('{} - HP: {}/{} - MP: {}/{} - CP: {}'.format(player.name, player.stats['hp'], player.stats['maxHp'],
                                                player.stats['mp'], player.stats['maxMp'], player.comboPoints))
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
            print(str('{} - {}'.format(index, s.name)))
            index += 1

def combo_menu(player):
    print('############################')
    print('     COMBOS ["0" to Quit]   ')
    print('############################')
    index = 1
    for c in player.combos:
            print(str('{} - {}'.format(index, c.name)))
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