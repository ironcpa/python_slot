from enum import Enum


class Section(Enum):
    none = 0
    symbol = 1
    layout = 2
    payline = 3
    paytable = 4
    scatter = 5
    reels = 6


class RewardType(Enum):
    none = 0
    payout = 1
    bonus_game = 2
    freespin = 3


class Symbol:
    def __init__(self, code, bitflag, desc, is_wild):
        self.code = code
        self.bitflag = int(bitflag)
        self.desc = desc
        self.is_wild = True if is_wild == 1 else False

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code


class Payline:
    def __init__(self, id, reel_rows):
        self.id = 0;
        self.reel_rows = reel_rows
        print('in payline constructor', self.reel_rows)

    def __str__(self):
        return "Payline"

    def __repr__(self):
        return str(self.id) + str(self.reel_rows)


class Paytable:
    def __init__(self, symbol_code, match, mul):
        self.symbol_code = symbol_code
        self.match = int(match)
        self.mul = int(mul)

    def __str__(self):
        return "Paytable"

    def __repr__(self):
        return '{} {} {}'.format(self.symbol_code, self.match, self.mul)


class ScatterReward:
    def __init__(self, symbol, match, reward_type, reward_val):
        self.symbol = symbol
        self.match = int(match)
        self.reward_type = int(reward_type)
        self.reward_val = int(reward_val)


class AbsPosPayline:
    def __init__(self, id, *positions):
        self.id = 0
        self.positions = positions


class PaylineWin:
    def __init__(self, line_id, symbol, match, multi):
        self.line_id = line_id
        self.symbol = symbol
        self.match = match
        self.multi = multi

    def __repr__(self):
        return "line={} {}x{} x{}".format(self.line_id, self.symbol, self.match, self.multi)

    def __str__(self):
        return self.__repr__()


class ScatterWin:
    def __init__(self, symbol, match, reward_type, reward):
        self.symbol = symbol
        self.match = match
        self.reward_type = RewardType(reward_type)
        self.reward = reward

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{}: x{} rwd={}".format(self.symbol, self.match, self.reward)


class ResultType(Enum):
    base = 0
    bonus_game = 1
    free = 3


class SpinResult:
    def __init__(self, rtype, line_bet):
        self.rtype = rtype
        self.line_bet = line_bet
        self.symbolset = None
        self.payline_wins = []
        self.scatter_wins = []
        self.sub_results = []

    def add_sub_result(self, spin_result):
        self.sub_results.append(spin_result)

    def base_payout(self):
        payout = 0
        for pw in self.payline_wins:
            payout += self.line_bet * pw.multi
        for sw in self.scatter_wins:
            if sw.reward_type == RewardType.payout:
                payout += self.line_bet * sw.reward
        return payout

    def payout(self):
        sub_payout = 0
        for sw in self.sub_results:
            print(sw.payout())
            if hasattr(sw, 'payout') == False:
                print('xxxxxx', sw)
            sub_payout += sw.payout()
        return self.base_payout() + sub_payout


class BonusResult:
    def __init__(self, line_bet):
        self.rtype = ResultType.bonus_game
        self.line_bet = line_bet
        self.bonus_payout = 0

    def payout(self):
        return self.bonus_payout


class Stat:
    def __init__(self):
        self.total_reward = 0
        self.total_spins = 0
        self.total_freespins = 0


class BonusGame:
    def __init__(self):
        pass

    def run(self, base_spin_result):
        result = BonusResult(base_spin_result.line_bet)
        result.bonus_payout = 999  # test
        return result


class Freespin:
    def __init__(self):
        self.remain_spins = 0
