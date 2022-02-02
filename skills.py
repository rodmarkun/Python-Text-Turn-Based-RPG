import allies

class Skill():
    '''
    Skill is the parent class for Spells and Combos.

    Attributes:
    name : str
        Name of the skill.
    description : str
        Skill's description.
    cost : int
        Cost of MP or CP.
    isTargeted : bool
        True if a target must be chosen, False if there is a default target.
    defaultTarget : str
        Default target if spell is not targeted.
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        self.name = name
        self.description = description
        self.cost = cost
        self.isTargeted = isTargeted
        self.defaultTarget = defaultTarget

    def check_already_has_buff(self, target):
        '''
        Checks if target Battler already has a buff from this skill.
        Skill's name bust be equal to buff's.

        Parameters:
        target : Battler
            Target to check if already has this buff.

        Returns:
        True/False : bool
            True if Battler already had buff. False if it didn't.
        '''
        for bd in target.buffsAndDebuffs:
            if bd.name == self.name:
                print(f'{target.name} has their {self.name}\'s duration restarted')
                bd.restart()
                return True
        return False

class Spell(Skill):
    '''
    Spells consume mp (Magic Points), which are restored by leveling up, using items,
    events... They also increment when upgrading the WIS (Wisdom) aptitude or equipping
    certain items. They use matk (Magic Attack) and their own power to calculate the
    damage done. Inherits from Skill.

    Attributes:
    power : int
        Power this spell has.
    '''
    def __init__(self, name, description, power, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.power = power

    def check_mp(self, caster):
        '''
        Checks if caster has enough MP to cast the spell.

        Parameters:
        caster : Battler
            Caster of the spell.
        
        Returns:
        True/False : bool
            True if spell was casted succesfully. False if it didn't.
        '''
        if caster.stats['mp'] < self.cost:
            print('Not enough MP!')
            return False
        else:
            print(f'{caster.name} casts {self.name}!')
            caster.stats['mp'] -= self.cost
            return True

class Combo(Skill):
    '''
    Combos consume cp (Combo Points), which counter is by default set to 0 when a battle
    starts and increment as the Battler performs normal attacks. They can also increment
    by using certain Skills. They usually have special effects and integrates normal
    attacks within them. Inherits from Skill.
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
    
    def check_cp(self, caster):
        '''
        Checks if caster has enough CP to perform the combo.

        Parameters:
        caster : Battler
            Performer of the combo.
        
        Returns:
        True/False : bool
            True if combo was performed succesfully. False if it didn't.
        '''
        if caster.comboPoints < self.cost:
            print('Not enough Combo Points!')
            return False
        else:
            print(f'{caster.name} uses {self.name}!')
            caster.comboPoints -= self.cost
            return True

##### SPELLS #####

class DamageSpell(Spell):
    '''
    Standard damaging Spell class. Inherits from Spell.
    '''
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)

    # TODO: Change target to always be a list.
    def effect(self, caster, target):
        '''
        Deals damage based on spell's power to target.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_mp(caster):
            if self.isTargeted:
                dmg = self.power + (caster.stats['matk'] - target.stats['mdef'])
                target.take_dmg(dmg)
            else:
                if self.defaultTarget == 'all_enemies':
                    for enemy in target:
                        dmg = self.power + (caster.stats['matk'] - enemy.stats['mdef'])
                        enemy.take_dmg(dmg)

class RecoverySpell(Spell):
    '''
    Standard recovery Spell class. Inherits from Spell.

    Attributes:
    stat : str
        Stat to recover (mp/hp)
    '''
    def __init__(self, name, description, power, mpCost, stat, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.stat = stat
    
    def effect(self, caster, target):
        '''
        Recovers a certain amount of target's stat.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        amountToRecover = 0
        if self.check_mp(caster):
            amountToRecover = self.power + round(caster.stats['matk']/2)
        if self.stat == 'hp':
            target.heal(amountToRecover)
        elif self.stat == 'mp':
            target.recover_mp(amountToRecover)

class BuffDebuffSpell(Spell):
    '''
    Standard Spell that inflicts a buff/debuff on certain target.

    Attributes:
    statToChange : str
        Stat to buff/debuff.
    amountToChange : float
        Percentage for stat to be changed (from 0 to 1).
    turns : int
        Amount of turns the buff/debuff is active.
    '''
    def __init__(self, name, description, power, mpCost, isTargeted, defaultTarget, statToChange, amountToChange, turns) -> None:
        super().__init__(name, description, power, mpCost, isTargeted, defaultTarget)
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns

    def effect(self, caster, target):
        '''
        Casts a buff/debuff on target.
        
        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_mp(caster) and not self.check_already_has_buff(target):
            buff = BuffDebuff(self.name, target, self.statToChange, self.amountToChange, self.turns)
            buff.activate()

class SummonSpell(Spell):
    '''
    Standard Spell that summons a certain ally.

    Attributes:
    summoning : Battler
        Battler to summon.
    '''
    def __init__(self, name, description, power, cost, isTargeted, defaultTarget, summoning) -> None:
        super().__init__(name, description, power, cost, isTargeted, defaultTarget)
        self.summoning = summoning

    def effect(self, caster, allies):
        '''
        Summons a battler to help in battler.

        Parameters:
        caster : Battler
            Caster of the spell.
        target : Battler/List
            Target of the spell.
        '''
        if self.check_mp(caster):
            summoningInst = self.summoning()
            allies.append(summoningInst)
            print(f'You summoned {summoningInst.name}')

##### COMBOS #####

class SlashCombo(Combo):
    '''
    Standard slashing Combo (Performs X normal attacks). Inherits from Combo.

    Attributes:
    timesToHit : int
        Number of normal attacks performed.
    '''
    def __init__(self, name, description, comboCost, isTargeted, defaultTarget, timesToHit) -> None:
        super().__init__(name, description, comboCost, isTargeted, defaultTarget)
        self.timesToHit = timesToHit

    def effect(self, caster, target):
        '''
        Caster performs X normal attacks against target.

        Parameters:
        caster : Battler
            Caster of the combo.
        target : Battler/List
            Target of the combo.
        '''
        if self.check_cp(caster):
            print(f'{caster.name} attacks {target.name} {self.timesToHit} times!')
            for _ in range(self.timesToHit):
                caster.normal_attack(target)

class ArmorBreakingCombo(Combo):
    '''
    Standard armor debuff Combo. Inherits from Combo.

    Attributes:
    armorDestroyed : float
        Percentage of destroyed armor (from -1 to 1, for it being a debuff should be -1 < armorDestroyed < 0)
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget, armorDestroyed) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.armorDestroyed = armorDestroyed
    
    def effect(self, caster, target):
        '''
        Caster performs a normal attack and debuffs target's armor. Inherits from Combo.

        Parameters:
        caster : Battler
            Caster of the combo.
        target : Battler/List
            Target of the combo.
        '''
        if self.check_cp(caster):
            print(f'{caster.name} pierces {target.name}\'s armor!')
            if not self.check_already_has_buff(target):
                armorBreak = BuffDebuff('Armor Break', target, 'def', self.armorDestroyed, 4)
                armorBreak.activate()
                caster.normal_attack(target)
            
class VampirismCombo(Combo):
    '''
    Standard life-draining Combo. Inherits from Combo.

    Attributes:
    percentHeal : float
        Percentage of healed hp based of damage dealt. (From 0 to 1)
    '''
    def __init__(self, name, description, cost, isTargeted, defaultTarget, percentHeal) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.percentHeal = percentHeal

    def effect(self, caster, target):
        '''
        Caster performs a normal attack and heals some hp based of damage dealt.

        Parameters:
        caster : Battler
            Caster of the combo.
        target : Battler/List
            Target of the combo.
        '''
        if self.check_cp(caster):
            amountToRecover = caster.normal_attack(target) * self.percentHeal
            caster.heal(round(amountToRecover))

class RecoveryCombo(Combo):
    '''
    Standard recovery Combo class. Inherits from Combo.

    Attributes:
    stat : str
        Stat to recover (mp/hp)
    '''
    def __init__(self, name, description, cost, stat, amountToChange, isTargeted, defaultTarget) -> None:
        super().__init__(name, description, cost, isTargeted, defaultTarget)
        self.stat = stat
        self.amountToChange = amountToChange
    
    def effect(self, caster, target):
        '''
        Recovers a certain amount of target's stat.

        Parameters:
        caster : Battler
            Caster of the combo.
        target : Battler/List
            Target of the combo.
        '''
        if self.check_cp(caster):
            if self.stat == 'hp':
                target.heal(self.amountToChange)
            elif self.stat == 'mp':
                target.recover_mp(self.amountToChange)

##### MISC #####

class BuffDebuff():
    '''
    Class that handles buffs and debuffs for a certain stat.

    Attributes:
    name : str
        Name of the buff/debuff (should be the same as Skill that triggered it).
    target : Battler
        Battler affected by the buff/debuff.
    statToChange : str
        Stat affected by the buff/debuff
    amountToChange : float
        Percentage for stat to change. (From -1 to 1).
    turns : int
        Current turns left for the buff/debuff to be disappear.
    maxTurns : int
        Maximum number of turns the buff/debuff can be active (default durations)
    '''
    def __init__(self, name, target, statToChange, amountToChange, turns) -> None:
        self.name = name
        self.target = target
        self.statToChange = statToChange
        self.amountToChange = amountToChange
        self.turns = turns
        self.maxTurns = turns

    def activate(self):
        '''
        Activates the effect of the buff/debuff.
        '''
        self.target.buffsAndDebuffs.append(self)
        if self.amountToChange < 0:
            print(f'{self.target.name} has their {self.statToChange} debuffed by {self.amountToChange * 100}% for {self.turns} turns')
        else:
            print(f'{self.target.name} has their {self.statToChange} buffed by {self.amountToChange * 100}% for {self.turns} turns')
        self.difference = int(self.target.stats[self.statToChange] * self.amountToChange)
        self.target.stats[self.statToChange] += self.difference

    def restart(self):
        '''
        Restarts the duration/turn count of this buff/debuff.
        '''
        self.turns = self.maxTurns

    def check_turns(self):
        '''
        Subtracts 1 to the turn count the buff/debuff is still active and checks if it should deactivate.
        '''
        self.turns -= 1
        if self.turns <= 0:
            self.deactivate()

    def deactivate(self):
        '''
        Deactivates buff/debuff.
        '''
        print(f'The effect of {self.name} has ended')
        self.target.buffsAndDebuffs.remove(self)
        self.target.stats[self.statToChange] -= self.difference

##### SPELL & COMBO INSTANCES #####

spellFireball = DamageSpell('Fireball', '', 15, 3, True, None)
spellDivineBlessing = RecoverySpell('Divine Blessing', '', 8, 4, 'hp', True, None)
spellEnhanceWeapon = BuffDebuffSpell('Enhance Weapon', '', 0, 5, False, 'self', 'atk', 0.5, 3)
spellInferno = DamageSpell('Inferno', '', 14, 7, False, 'all_enemies')
spellSkeletonSummoning = SummonSpell('Summon Skeleton', '', 0, 4, False, 'allies', allies.SummonedSkeleton)
spellFireSpiritSummonning = SummonSpell('Summon Fire Spirit', '', 0, 12, False, 'allies', allies.SummonedFireSpirit)

comboSlash1 = SlashCombo('Slash Combo I', '', 3, True, None, 3)
comboSlash2 = SlashCombo('Slash Combo II', '', 3, True, None, 4)
comboArmorBreaker1 = ArmorBreakingCombo('Armor Break I', '', 2, True, None, -0.3)
comboVampireStab1 = VampirismCombo('Vampire Stab I', '', 2, True, None, 0.3)
comboVampireStab2 = VampirismCombo('Vampire Stab II', '', 2, True, None, 0.5)
comboMeditation1 = RecoveryCombo('Meditation I', '', 1, 'mp', 5, False, 'self')
comboMeditation2 = RecoveryCombo('Meditation II', '', 2, 'mp', 15, False, 'self')