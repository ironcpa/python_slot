#slot machine
import random

def createRndStop(reels):
    randStop = []
    for r in range(0, len(reels)):
        randStop.append(random.randrange(len(reels[r])))

    assert (len(randStop) == len(reels)), "reel size mismatch"

    print('reelstop', randStop)
    return randStop

def createSymbolset(reels, stops):
    symbolset = []
    for r in range(0, len(stops)):
        rowLen = len(reels[r])
        reelRow = []
        reelRow.append(reels[r][stops[r]][0])
        reelRow.append(reels[r][(stops[r] + 1) % rowLen][0])
        reelRow.append(reels[r][(stops[r] + 2) % rowLen][0])
        symbolset.append(reelRow)

    print('symbolset', symbolset)

    return symbolset
    
def spin():
    reels = [ [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
              [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
              [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
              [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ],
              [ ('H1', 1), ('M1', 1), ('M2', 1), ('L1', 1), ('L2', 2) ] ]

    reelLen = len(reels)
    randStop = createRndStop(reels)
    symbolset = createSymbolset(reels, randStop)

    return symbolset

if __name__ == '__main__':
    spin()
