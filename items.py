import inventory

# Basic Items
longsword = inventory.Equipment('Longword', '', 1, 20, 'Weapon', {'atk' : 6})
dagger = inventory.Equipment('Dagger', '', 1, 15, 'Weapon', {'atk' : 3, 'critCh' : 10, 'speed': 3})
staff = inventory.Equipment('Staff', '', 1, 18, 'Weapon', {'matk' : 3, 'maxMp' : 2})

clothArmor = inventory.Equipment('Cloth Armor', '', 1, 10, 'Armor', {'maxHp' : 2, 'def' : 2})

# Advanced Items
warhammer = inventory.Equipment('Warhammer', '', 1, 62, 'Weapon', {'atk' : 13, 'speed' : -2})
ironArmor = inventory.Equipment('Iron Armor', '', 1, 102, 'Armor', {'maxHp' : 8, 'def' : 10})

# Consumables
hpPotions = inventory.Potion('Health Potion', 'a', 4, 10, 'Consumable', 'hp', 15)
mpPotions = inventory.Potion('Mana Potion', 'a', 4, 10, 'Consumable', 'mp', 15)