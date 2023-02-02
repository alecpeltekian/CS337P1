class FrameByAward:
    def __init__(self,awardName, winnerName = None, nomineeList = []):
        self.awardName = awardName
        self.winnerName = winnerName
        self.nomineeList = nomineeList

    def addNominee(self, nomineeName):
        self.nomineeList.append(nomineeName)

    def addWinner(self,winnerName):
        self.winnerName = winnerName

    def visualize(self):
        print("Award Name: ")
        print(self.awardName)
        print("Winner Name: ")
        print(self.winnerName)
        print("Nominees")
        print(self.nomineeList)




