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
    print('#       1 - Battle         #')
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
    print('#    S - Sell an item      #')
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