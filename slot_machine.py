#slot machine
from random import randrange

class SlotMachine:
    def __init__(self):
        self.reels = [ [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
                       [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
                       [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
                       [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
                       [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ] ]
        self.reelSize = len(self.reels)

    def createRndStop(self):
        randStop = []
        for r in range(0, self.reelSize):
            randStop.append(randrange(len(self.reels[r])))

        assert (len(randStop) == len(self.reels)), "reel size mismatch"

        print('reelstop', randStop)
        return randStop

    def createSymbolset(self, stops):
        symbolset = []
        for r in range(0, len(stops)):
            rowLen = len(self.reels[r])
            reelRow = []
            reelRow.append(self.reels[r][stops[r]][0])
            reelRow.append(self.reels[r][(stops[r] + 1) % rowLen][0])
            reelRow.append(self.reels[r][(stops[r] + 2) % rowLen][0])
            symbolset.append(reelRow)

        print('symbolset', symbolset)

        return symbolset
        
    def spin(self):
        randStop = self.createRndStop()
        symbolset = self.createSymbolset(randStop)

        return symbolset

if __name__ == '__main__':
    machine = SlotMachine()
    machine.spin()
