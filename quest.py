class Quest():
    def __init__(self, name, text, xpReward, goldReward, itemReward) -> None:
        self.name = name
        self.text = text
        self.xpReward = xpReward
        self.goldReward = goldReward
        self.itemReward = itemReward
        self.status = 'Not Active'

    def activate_quest(self, player):
        if self.status == 'Not Active':
            self.status = 'Active'
            player.activeQuests.append(self)

    def complete_quest(self, player):
        if self.status == 'Active':
            self.status = 'Completed'
            player.completedQuests.append(self)

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