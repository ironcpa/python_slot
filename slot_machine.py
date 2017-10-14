#slot machine
from random import randrange
from enum import Enum

class Section(Enum):
    none = 0
    symbol = 1
    layout = 2
    payline = 3
    reels = 4

class Symbol:
    def __init__(self, code, bitflag, desc):
        self.code = code
        self.bitflag = bigflag
        self.desc = desc

class Payline:
    def __init__(self, id, *reelRows):
        self.id = 0;
        self.reelRows = reelRows
        
    def __str__(self):
        return "Payline"
    
    def __repr__(self):
        return str(self.id) + str(self.reelRows)

class AbsPosPayline:
    def __init__(self, id, *positions):
        self.id = 0
        self.positions = positions

class SlotSetting:
    def __init__(self):
        self.symbols = []
        self.layout = []
        self.paylines = []
        self.absPosPaylines = []
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
        elif line == '[Layout]':
            return Section.layout
        elif line == '[Paylines]':
            return Section.payline
        elif line == '[Reels]':
            return Section.reels
        else:
            return Section.none

    def readSection(self, line, section):
        if section == Section.symbol:
            self.readSymbol(line)
        elif section == Section.layout:
            self.readLayout(line)
        elif section == Section.payline:
            self.readPaylines(line)
        elif section == Section.reels:
            self.readReels(line)
    
    def readSymbol(self, line):
        keyVal = line.split('=')
        code = keyVal[0]
        dataTokens = keyVal[1].split()
        bitflag = dataTokens[0]
        desc = dataTokens[1]
        self.symbols.append(Symbol(code, bitflag, desc))

    def readLayout(self, line):
        print('readLayout', line, len(self.layout))
        assert (len(self.layout) == 0), 'already set layout data'
        self.layout = line.split()
        
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

    def convAbsPos(self, reel, row):
        prevPos = 0
        if reel > 0:
            for rl in range(0, reel - 1):
                prevPos += layout[rl]
        return prevPos + row
            
        
class PaylineWin:
    def __init__(self):
        self.line_id = 0
        self.symbol = 0
        self.match = 0
        self.multi = 0
        
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

        #payout
        # line, symbol, match, multi
        paylineWins = self.resolvePayout(symbolset)

        return symbolset

    def resolvePayout(self, symbolset):
        paylineWins = []
        for pl in paylines:
           #check match for reelRow's symbol 
           #최대 영역 레이아웃 돌면서 layout바운더리 넘지 않게 하고
           #절대페이라인 위치를 비트플래그로 검사
           #비트플래그 검사 방법
           #H1, H1, H1 인 경우 첫번째 심볼 기준, 
        for reel, r in enumerate(symbolset):
            for row, s in enumerate(r):
                print('>>', reel, row, s)
        return paylineWins

if __name__ == '__main__':
    machine = SlotMachine()
    machine.spin()

