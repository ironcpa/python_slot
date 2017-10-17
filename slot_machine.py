# slot machine
from random import randrange
from enum import Enum
import unittest


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


class SlotSetting:
    def __init__(self):
        self.symbols = []
        self.layout = []
        self.paylines = []
        self.paytables = []
        self.scatters = []
        self.scatter_rewards = []
        self.abs_pos_paylines = []
        self.reels = []
        self.read_setting_file()

    def read_setting_file(self):
        infile = open('./machine_setting.txt', 'r')
        curr_section = Section.none
        for line in infile:
            s = line.rstrip()
            if len(s) == 0 or line.startswith('//'):
                continue
            section = self.resolve_section(s)
            if section != Section.none:
                curr_section = section
            else:
                self.read_section(s, curr_section)

        print('paylines', self.paylines)
        print('self.reels', self.reels)

    @staticmethod
    def resolve_section(line):
        if line == '[Symbols]':
            return Section.symbol
        elif line == '[Layout]':
            return Section.layout
        elif line == '[Paylines]':
            return Section.payline
        elif line == '[Paytables]':
            return Section.paytable
        elif line == '[Scatters]':
            return Section.scatter;
        elif line == '[Reels]':
            return Section.reels
        else:
            return Section.none

    def read_section(self, line, section):
        if section == Section.symbol:
            self.read_symbol(line)
        elif section == Section.layout:
            self.read_layout(line)
        elif section == Section.payline:
            self.read_paylines(line)
        elif section == Section.paytable:
            self.read_paytables(line)
        elif section == Section.scatter:
            self.read_scatter(line)
        elif section == Section.reels:
            self.read_reels(line)

    def read_symbol(self, line):
        key_val = line.split('=')
        code = key_val[0].rstrip()
        data_tokens = key_val[1].split()
        bitflag = data_tokens[0]
        desc = data_tokens[1]
        is_wild = int(data_tokens[2])
        self.symbols.append(Symbol(code, bitflag, desc, is_wild))

    def read_layout(self, line):
        print('readLayout', line, len(self.layout))
        assert (len(self.layout) == 0), 'already set layout data'
        tokens = line.split()
        for t in tokens:
            self.layout.append(int(t))
        print('layout result:', self.layout)

    def read_paylines(self, line):
        key_val = line.split('=')
        print(line)
        payline_id = int(key_val[0])
        reel_rows = []
        val_tokens = key_val[1].split()
        for t in val_tokens:
            reel_rows.append(int(t))
        self.paylines.append(Payline(payline_id, reel_rows))

    def read_paytables(self, line):
        symbol, val_list = self.read_key_val_line(line, '=', ' ')
        for reel, mul in enumerate(val_list):
            match = reel + 1
            if int(mul) > 0:
                self.paytables.append(Paytable(symbol, match, mul))
        print('readPaytable', len(self.paytables), self.paytables)

    def read_scatter(self, line):
        key, val_list = self.read_key_val_line(line, '=', ' ')
        scatter = self.find_symbol(key)
        if scatter is not None and scatter not in self.scatters:
            self.scatters.append(scatter)
        self.scatter_rewards.append(ScatterReward(scatter, val_list[0], val_list[1], val_list[2]))

    def read_key_val_line(self, line, keyDel, valDel):
        key_val = line.split(keyDel)
        key = key_val[0].rstrip()
        val_list = []
        val_tokens = key_val[1].split()
        for t in val_tokens:
            val_list.append(t.rstrip())
        return key, val_list

    def read_reels(self, line):
        reel = 0
        sym_code = ''
        multi = 0
        row = line.split()
        for n in range(0, len(row)):
            if n % 2 == 0:
                sym_code = row[n]
            else:
                reel = n // 2
                multi = row[n]
                if reel >= len(self.reels):
                    self.reels.append([])
                self.reels[reel].append((self.find_symbol(sym_code), multi))

    def conv_abs_pos(self, reel, row):
        prev_pos = 0
        for rl in range(0, reel):
            prev_pos += self.layout[rl]
        return prev_pos + row

    def find_symbol(self, symbol_code):
        # print('find_symbol', symbol_code, len(symbol_code))
        return next((x for x in self.symbols if x.code == symbol_code), None)

    def get_paytable(self, symbol_code, match):
        found = next((x for x in self.paytables if x.symbol_code == symbol_code and x.match == match), None)
        # print('getPaytable', symbol_code, match, found)
        if found is not None:
            return found.mul
        else:
            return 0

    def find_all_scatter_reward(self, symbol, match):
        return [x for x in self.scatter_rewards if x.symbol == symbol and x.match == match]


class PaylineWin:
    def __init__(self, line_id, symbol, match, multi):
        self.line_id = line_id
        self.symbol = symbol
        self.match = match
        self.multi = multi


class ScatterWin:
    def __init__(self, symbol, match, reward):
        self.symbol = symbol
        self.match = match
        self.reward = reward


class SlotMachine:
    def __init__(self):
        self.settings = SlotSetting()
        self.reel_size = len(self.settings.reels)

    def __row_len(self, reel):
        return len(self.settings.reels[reel])

    def create_rnd_stop(self):
        rand_stop = []
        for r in range(0, self.reel_size):
            rand_stop.append(randrange(self.__row_len(r)))

        print('reelstop', rand_stop)
        return rand_stop

    def create_symbolset(self, stops):
        symbolset = []
        for r in range(0, len(stops)):
            reel_row = [self.settings.reels[r][stops[r]][0],
                        self.settings.reels[r][(stops[r] + 1) % self.__row_len(r)][0],
                        self.settings.reels[r][(stops[r] + 2) % self.__row_len(r)][0]]
            symbolset.append(reel_row)

        print('symbolset', symbolset)
        print(self.str_symbolset(symbolset))

        return symbolset

    def spin(self):
        rand_stop = self.create_rnd_stop()
        symbolset = self.create_symbolset(rand_stop)

        # payout
        # line, symbol, match, multi
        payline_wins = self.resolve_payout(symbolset)
        print('paylineWins')
        print(payline_wins)

        return symbolset

    def resolve_payout(self, symbolset):
        payline_wins = []
        for line in self.settings.paylines:
            start_symbol = None
            match_cnt = 0
            wild_before_start_symbol = 0
            for reel, row in enumerate(line.reel_rows):
                s = symbolset[reel][row]
                # print('line symbols', reel, row, symbolset[reel][row])
                if s is None:
                    continue

                if s.is_wild:
                    if start_symbol is None:
                        wild_before_start_symbol += 1
                    else:
                        match_cnt += 1
                else:
                    if start_symbol is None:
                        start_symbol = s
                        match_cnt += 1
                    else:
                        if s == start_symbol:
                            match_cnt += 1
                        else:
                            break

            match_cnt += wild_before_start_symbol

            multi = self.settings.get_paytable(start_symbol.code, match_cnt)

            # print('line check:', start_symbol, match_cnt)
            if multi > 0:
                payline_wins.append(PaylineWin(line.id, start_symbol, match_cnt, multi))

        return payline_wins

    def resolve_scatter_rewards(self, symbolset):
        scatter_wins = []
        match_cnt = 0
        for scatter in self.settings.scatters:
            for reel in symbolset:
                for sym in reel:
                    if sym == scatter:
                        match_cnt += 1
            if match_cnt > 0:
                rewards = self.settings.find_all_scatter_reward(scatter, match_cnt)
                if rewards is not None:
                    for reward in rewards:
                        scatter_wins.append(ScatterWin(scatter, match_cnt, reward))
        return scatter_wins

    def str_symbolset(self, symbolset):
        s_str = ''
        reel_size = len(self.settings.layout)
        max_row = 3
        for row in range(0, max_row):
            for reel in range(0, reel_size):
                s = symbolset[reel][row]
                if s is not None:
                    s_str += s.code + ","
            s_str += "\n"
        return s_str


class UnitTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def fs(self, machine, code):
        return machine.settings.find_symbol(code)

    @staticmethod
    def create_symbolset(machine, symbol_codes):
        reel_size = len(machine.settings.layout)
        max_row = 3
        symbolset = []
        cur_pos = 0
        for reel in range(0, reel_size):
            symbolset.append([])
            for row in range(0, max_row):
                if row >= machine.settings.layout[reel]:
                    continue
                symbol = machine.settings.find_symbol(symbol_codes[cur_pos])
                assert (symbol is not None), "Unknown symbol"
                symbolset[reel].append(symbol)
                cur_pos += 1
        print('create_symbolset')
        return symbolset

    def test001_resolve_payout(self):
        m = SlotMachine()
        test_symbolset = self.create_symbolset(m, ['H1', 'H1', 'H1', 'H1', 'H1',
                                                   'H1', 'H1', 'H1', 'H1', 'H1',
                                                   'H1', 'H1', 'H1', 'H1', 'H1'])
        wins = m.resolve_payout(test_symbolset)
        total_payout = 0
        for w in wins:
            total_payout += w.multi
        print(total_payout)
        self.assertTrue(total_payout == 150)

    def test002_resolve_scatter(self):
        m = SlotMachine()
        test_symbolset = self.create_symbolset(m, ['SC', 'H1', 'H1', 'H1', 'H1',
                                                   'H1', 'SC', 'SC', 'H1', 'H1',
                                                   'H2', 'SC', 'H1', 'H1', 'SC'])
        print(m.str_symbolset(test_symbolset))
        wins = m.resolve_scatter_rewards(test_symbolset)
        self.assertTrue(len(wins) == 1)


if __name__ == '__main__':
    # machine = SlotMachine()
    # machine.spin()

    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
