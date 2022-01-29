class Quest():
    def __init__(self, name, description, proposalText, xpReward, goldReward, itemReward, event, recommendedLvl) -> None:
        self.name = name
        self.description = description
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.itemReward = itemReward
        self.status = 'Not Active'
        self.event = event
        self.proposalText = proposalText
        self.recommendedLvl = recommendedLvl

    def activate_quest(self, player):
        if self.status == 'Not Active':
            self.status = 'Active'
            self.event.add_event_to_event_list()
            player.activeQuests.append(self)

    def complete_quest(self, player):
        if self.status == 'Active':
            self.status = 'Completed'
            player.activeQuests.remove(self)
            player.completedQuests.append(self)
            self.give_rewards(player)

    def show_info(self):
        print('\n - {} - '.format(self.name))
        print('Recommended level: {}'.format(self.recommendedLvl))
        print(self.description)
        print('Rewards:')
        if self.xpReward > 0:
            print('XP: {}'.format(self.xpReward))
        if self.goldReward > 0:
            print('G: {}'.format(self.goldReward))
        if self.itemReward != None:
            print('Item: {}'.format(self.itemReward.name))
        print('')

    def give_rewards(self, player):
        print('\"{}\" quest completed. You earn {}xp and {}G'.format(self.name, self.xpReward, self.goldReward))
        if self.xpReward > 0:
            player.add_exp(self.xpReward)
        if self.goldReward > 0:
            player.money += self.goldReward
        if self.itemReward != None:
            self.itemReward.add_to_inventory(player.inventory())
    
    def propose_quest(self, player):
        print(self.proposalText)
        print('Accept? [y/n] (Recommended level: {})'.format(self.recommendedLvl))
        option = input("> ").lower()
        while option not in ['y', 'n']:
            option = input("> ").lower()
        if option == 'y':
            self.activate_quest(player)