import inventory
import skills

# Starting Items
# -> Starting Weapons
rustySword = inventory.Equipment('Rusty Sword', '', 1, 6, 'Weapon', {'atk' : 2}, None)
brokenDagger = inventory.Equipment('Broken Dagger', '', 1, 6, 'Weapon', {'atk' : 1, 'critCh': 5, 'speed' : 1}, None)
oldStaff = inventory.Equipment('Old Staff', '', 1, 6, 'Weapon', {'matk' : 1, 'maxMp' : 2}, None)
# -> Starting Armor
noviceArmor = inventory.Equipment('Novice Armor', '', 1, 10, 'Armor', {'maxHp' : 1, 'def' : 2, 'speed' : 1}, None)
oldRobes = inventory.Equipment('Old Robes', '', 1, 10, 'Armor', {'def' : 1, 'mdef' : 2, 'maxMp' : 2}, None)

# Basic Items
# -> Basic Weapons
longsword = inventory.Equipment('Longsword', '', 1, 19, 'Weapon', {'atk' : 5}, skills.comboSlash1)
dagger = inventory.Equipment('Dagger', '', 1, 15, 'Weapon', {'atk' : 3, 'critCh' : 10, 'speed': 2}, skills.comboVampireStab1)
staff = inventory.Equipment('Staff', '', 1, 18, 'Weapon', {'matk' : 3, 'maxMp' : 3}, skills.comboMeditation1)
# -> Basic Armor
clothArmor = inventory.Equipment('Cloth Armor', '', 1, 18, 'Armor', {'maxHp' : 2, 'def' : 3, 'speed' : 1}, None)
bronzeArmor = inventory.Equipment('Bronze Armor', '', 1, 25, 'Armor', {'maxHp' : 4, 'def' : 5}, None)
studentRobes = inventory.Equipment('Student Robes', '', 1, 25, 'Armor', {'maxHp' : 2, 'def' : 1, 'mdef' : 3, 'maxMp' : 4}, None)

# Advanced Items
# -> Advanced Weapons
warhammer = inventory.Equipment('Warhammer', '', 1, 72, 'Weapon', {'atk' : 11, 'speed' : -2}, skills.comboArmorBreaker1)
zweihander = inventory.Equipment('Zweihander', '', 1, 75, 'Weapon', {'atk' : 9, 'def' : 2}, skills.comboSlash2)
sageStaff = inventory.Equipment('Sage Staff', '', 1, 70, 'Weapon', {'matk' : 9, 'maxMp' : 5}, skills.comboMeditation2)
sai = inventory.Equipment('Sai', '', 1, 70, 'Weapon', {'atk' : 6, 'critCh' : 20, 'speed' : 3}, skills.comboVampireStab2)

# -> Advanced Armor
ironArmor = inventory.Equipment('Iron Armor', '', 1, 85, 'Armor', {'maxHp' : 8, 'def' : 10}, None)
sageTunic = inventory.Equipment('Sage Tunic', '', 1, 85, 'Armor', {'maxHp' : 3, 'def': 4, 'mdef':7, 'maxMp': 10}, None)
thiefArmor = inventory.Equipment('Thief Armor', '', 1, 80, 'Armor', {'maxHp' : 4, 'def' : 6, 'speed' : 3}, None)

# Consumables
hpPotion = inventory.Potion('Health Potion', 'a', 1, 10, 'Consumable', 'hp', 15)
mpPotion = inventory.Potion('Mana Potion', 'a', 1, 10, 'Consumable', 'mp', 15)

# Grimoires
grimoireFireball = inventory.Grimoire('Grimoire: Fireball', '', 1, 20, 'Consumable', skills.spellFireball)
grimoireDivineBlessing = inventory.Grimoire('Grimoire: Divine Blessing', '', 1, 20, 'Consumable', skills.spellDivineBlessing)
grimoireEnhanceWeapon = inventory.Grimoire('Grimoire: Enhance Weapon', '', 1, 25, 'Consumable', skills.spellEnhanceWeapon)
grimoireInferno = inventory.Grimoire('Grimoire: Inferno', '', 1, 50, 'Consumable', skills.spellInferno)

# Shop Item Sets

rik_armor_shop_item_set = [ longsword, 
                            dagger, 
                            warhammer, 
                            ironArmor,
                            zweihander,
                            clothArmor,
                            bronzeArmor,
                            sai, 
                            thiefArmor ]

itz_magic_item_set = [ staff,
                        clothArmor,
                        hpPotion,
                        mpPotion,
                        sageTunic,
                        sageStaff,
                        studentRobes,
                        grimoireFireball,
                        grimoireEnhanceWeapon,
                        grimoireDivineBlessing,
                        grimoireInferno ]