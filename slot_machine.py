#slot machine
from random import randrange

class SlotMachine:
    def __init__(self):
        self.__loadReels()
        self.reelSize = len(self.reels)

    def __loadReels(self):
        self.reels = []
        infile = open('./machine_setting.txt', 'r')
        isInReelsSection = False
        for line in infile:
            if line.startswith('//'):
                continue
            s = line.rstrip()
            if isInReelsSection == False and s == '[Reels]':
                isInReelsSection = True
                continue
            if isInReelsSection:
                reel = 0
                symbol = ''
                multi = 0
                row = s.split()
                for n in range(0, len(row)):
                    if n % 2 == 0:
                        symbol = row[n]
                    else:
                        reel = n // 2
                        multi = row[n]
                        if reel >= len(self.reels):
                            self.reels.append([])
                        self.reels[reel].append((symbol, multi))
        print('self.reels', self.reels)
        
    def __rowLen(self, reel):
        return len(self.reels[reel])

    def createRndStop(self):
        randStop = []
        for r in range(0, self.reelSize):
            randStop.append(randrange(self.__rowLen(r)))

        print('reelstop', randStop)
        return randStop

    def createSymbolset(self, stops):
        symbolset = []
        for r in range(0, len(stops)):
            reelRow = []
            reelRow.append(self.reels[r][stops[r]][0])
            reelRow.append(self.reels[r][(stops[r] + 1) % self.__rowLen(r)][0])
            reelRow.append(self.reels[r][(stops[r] + 2) % self.__rowLen(r)][0])
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
