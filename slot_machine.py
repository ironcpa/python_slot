#slot machine
from random import randrange
from enum import Enum

class Section(Enum):
    none = 0
    symbol = 1
    layout = 2
    payline = 3
    paytable = 4
    reels = 5

class Symbol:
    def __init__(self, code, bitflag, desc):
        self.code = code
        self.bitflag = bitflag
        self.desc = desc

class Payline:
    def __init__(self, id, reelRows):
        self.id = 0;
        self.reelRows = reelRows
        print('in payline constructor', self.reelRows)
        
    def __str__(self):
        return "Payline"
    
    def __repr__(self):
        return str(self.id) + str(self.reelRows)

class Paytable:
    def __init__(self, symbol, match, mul):
        self.symbol = symbol
        self.match = int(match)
        self.mul = int(mul)
    
    def __str__(self):
        return "Paytable"
    
    def __repr__(self):
        return '{} {} {}'.format(self.symbol, self.match, self.mul)

class AbsPosPayline:
    def __init__(self, id, *positions):
        self.id = 0
        self.positions = positions

class SlotSetting:
    def __init__(self):
        self.symbols = []
        self.layout = []
        self.paylines = []
        self.paytables = []
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
        elif line == '[Paytables]':
            return Section.paytable
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
        elif section == Section.paytable:
            self.readPaytables(line)
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
        tokens = line.split()
        for t in tokens:
            self.layout.append(int(t))
        print('layout result:', self.layout)
        
    def readPaylines(self, line):
        keyVal = line.split('=')
        print(line)
        paylineId = int(keyVal[0])
        reelRows = []
        valTokens = keyVal[1].split()
        for t in valTokens:
            reelRows.append(int(t))
        self.paylines.append(Payline(paylineId, reelRows))

    def readPaytables(self, line):
        key, valList = self.readKeyValLine(line, '=', ' ')
        symbol = key.rstrip()
        for reel, mul in enumerate(valList):
            match = reel + 1
            print('mul', match, mul)
            if int(mul) > 0:
                self.paytables.append(Paytable(symbol, match, mul))
        print('readPaytable', len(self.paytables), self.paytables)
         
    def readKeyValLine(self, line, keyDel, valDel):
        keyVal = line.split(keyDel)
        key = keyVal[0]
        valList = []
        valTokens = keyVal[1].split()
        for t in valTokens:
            valList.append(t)
        return key, valList
    
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
        for rl in range(0, reel):
            prevPos += self.layout[rl]
        return prevPos + row

    def getPaytable(self, symbol, match):
        #found = next((x for x in self.paytables if x.symbol == symbol and x.match == match), None)
        found = next((x for x in self.paytables if x.symbol == symbol), None)
        print('getPaytable', symbol, match, found)
        if found != None:
            return found.mul
        else:
            return 0
        
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
        print('paylineWins')
        print(paylineWins)

        return symbolset

    def resolvePayout(self, symbolset):
        #test symbolset
        symbolset = [['H1','H2','M1'], ['H1','H2','M1'], ['H1','H2','M1'], ['H1','H2','M1'], ['H1','H2','M1']]
        paylineWins = []
        startSymbol = None
        matchCnt = 0
        wildBeforeStartSymbol = 0
        for line in self.settings.paylines:
            for reel, row in enumerate(line.reelRows):
                s = symbolset[reel][row]
                print('line symbols', reel, row, symbolset[reel][row])
                if s != 'WI':
                    startSymbol = s
                if startSymbol == None and s == 'WI':
                    wildBeforeStartSymbol += 1
                if startSymbol != None and s == startSymbol:
                    matchCnt += 1
            if startSymbol == None:
                startSymbol = 'WI'
            matchCnt += wildBeforeStartSymbol

            payout = self.settings.getPaytable(startSymbol, matchCnt)

            print('line check:', startSymbol, matchCnt)
            if payout > 0:
                paylineWins.append((startSymbol, matchCnt, payout))

        return paylineWins

if __name__ == '__main__':
    machine = SlotMachine()
    machine.spin()

