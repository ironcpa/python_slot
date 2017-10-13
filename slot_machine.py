#slot machine
from random import randrange
from enum import Enum

class Section(Enum):
    none = 0
    symbol = 1
    payline = 2
    reels = 3

class Payline():
    def __init__(self, id, *reelRows):
        self.id = 0;
        self.reelRows = reelRows
    def __str__(self):
        return "Payline"
    def __repr__(self):
        return str(self.id) + str(self.reelRows)

class SlotSetting:
    def __init__(self):
        self.paylines = []
        self.reels = []
        self.readSettingFile()
        
    def readSettingFile(self):
        infile = open('./machine_setting.txt', 'r')
        currSection = Section.none
        for line in infile:
            s = line.rstrip()
            if len(s) == 0 or line.startswith('//'):
                continue
            section = self.resolveSection(s)
            if section != Section.none:
                currSection = section
            else:
                self.readSection(s, currSection)

        print('paylines', self.paylines)
        print('self.reels', self.reels)

    def resolveSection(self, line):
        if line == '[Symbols]':
            return Section.symbol
        elif line == '[Paylines]':
            return Section.payline
        elif line == '[Reels]':
            return Section.reels
        else:
            return Section.none

    def readSection(self, line, section):
        if section == Section.symbol:
            pass
        elif section == Section.payline:
            self.readPaylines(line)
        elif section == Section.reels:
            self.readReels(line)
        
    def readPaylines(self, line):
        keyVal = line.split('=')
        paylineId = keyVal[0]
        reelRows = keyVal[1]
        self.paylines.append(Payline(paylineId, reelRows))
        
    def readReels(self, line):
        reel = 0
        symbol = ''
        multi = 0
        row = line.split()
        for n in range(0, len(row)):
            if n % 2 == 0:
                symbol = row[n]
            else:
                reel = n // 2
                multi = row[n]
                if reel >= len(self.reels):
                    self.reels.append([])
                self.reels[reel].append((symbol, multi))
        
class SlotMachine:
    def __init__(self):
        self.settings = SlotSetting()
        self.reelSize = len(self.settings.reels)
        
    def __rowLen(self, reel):
        return len(self.settings.reels[reel])

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
            reelRow.append(self.settings.reels[r][stops[r]][0])
            reelRow.append(self.settings.reels[r][(stops[r] + 1) % self.__rowLen(r)][0])
            reelRow.append(self.settings.reels[r][(stops[r] + 2) % self.__rowLen(r)][0])
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
