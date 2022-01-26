class Quest():
    def __init__(self, name, text, xpReward, goldReward, itemReward, event, proposalText) -> None:
        self.name = name
        self.text = text
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.itemReward = itemReward
        self.status = 'Not Active'
        self.event = event
        self.proposalText = proposalText

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
        print('###################')
        print(' - {} - '.format(self.name))
        print(self.text)
        print('Rewards:')
        if self.xpReward > 0:
            print('XP: {}'.format(self.xpReward))
        if self.goldReward > 0:
            print('G: {}'.format(self.goldReward))
        if self.itemReward != None:
            print('Item: {}'.format(self.itemReward.name))

    def give_rewards(self, player):
        print('\"{}\" quest completed. You earn {}xp and {}G'.format(self.name, self.xpReward, self.goldReward))
        if self.xpReward > 0:
            player.addExp(self.xpReward)
        if self.goldReward > 0:
            player.money += self.goldReward
        if self.itemReward != None:
            self.itemReward.add_to_inventory(player.inventory())
    
    def propose_quest(self, player):
        print(self.proposalText)
        print('Accept? [y/n]')
        option = input("> ").lower()
        while option not in ['y', 'n']:
            option = input("> ").lower()
        if option == 'y':
            self.activate_quest(player)