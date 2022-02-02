class Quest():
    '''
    Defines quests and handles their activation, completion, rewards.

    Attributes:
    name : str
        Quest's name.
    description : str
        Quest's description.
    proposalText : str
        Text for when the quest is proposed.
    xpReward : int
        Amount of xp to give when quest is completed.
    goldReward : int
        Amount of gold to give when quest is completed.
    itemReward : Item
        Item to give when quest is completed.
    status : str
        Current quest's status
    event : Event
        Event the quest triggers.
    recommendedLvl : int
        Recommended level for this quest.
    '''
    def __init__(self, name, description, proposalText, xpReward, goldReward, itemReward, event, recommendedLvl) -> None:
        self.name = name
        self.description = description
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.itemReward = itemReward
        # TODO: Change way the quest's status is handled
        self.status = 'Not Active'
        self.event = event
        self.proposalText = proposalText
        self.recommendedLvl = recommendedLvl

    def activate_quest(self, player):
        '''
        Activates the quest and appends itself to player's active quests list.

        player : Player
            Player that activated the quest.
        '''
        if self.status == 'Not Active':
            self.status = 'Active'
            self.event.add_event_to_event_list()
            player.activeQuests.append(self)

    def complete_quest(self, player):
        '''
        Completes the quest, appends itself to player's completed quests list and removes itself from
        active quests list. Also gives rewards. 

        player : Player
            Player that completed the quest.
        '''
        if self.status == 'Active':
            self.status = 'Completed'
            player.activeQuests.remove(self)
            player.completedQuests.append(self)
            self.give_rewards(player)

    def show_info(self):
        '''
        Displays all info of this quest.
        '''
        print(f'\n - {self.name} - ')
        print(f'Recommended level: {self.recommendedLvl}')
        print(self.description)
        print('Rewards:')
        if self.xpReward > 0:
            print(f'XP: {self.xpReward}')
        if self.goldReward > 0:
            print(f'G: {self.goldReward}')
        if self.itemReward != None:
            print(f'Item: {self.itemReward.name}')
        print('')

    def give_rewards(self, player):
        '''
        Gives quest's rewards to a certain player.

        Parameters:
        player : Player
            Player to be rewarded.
        '''
        print(f'\"{self.name}\" quest completed. You earn {self.xpReward}xp and {self.goldReward}G')
        if self.xpReward > 0:
            player.add_exp(self.xpReward)
        if self.goldReward > 0:
            player.money += self.goldReward
        if self.itemReward != None:
            self.itemReward.add_to_inventory(player.inventory())
    
    def propose_quest(self, player):
        '''
        Proposes the quest to a certain player. They can accept it or decline it.

        Parameters:
        player : Player
            Player to propose the quest to.
        '''
        print(self.proposalText)
        print('Accept? [y/n] (Recommended level: {})'.format(self.recommendedLvl))
        option = input("> ").lower()
        while option not in ['y', 'n']:
            option = input("> ").lower()
        if option == 'y':
            self.activate_quest(player)