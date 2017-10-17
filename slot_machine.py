# slot machine
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
    def __init__(self, id, reel_rows):
        self.id = 0;
        self.reel_rows = reel_rows
        print('in payline constructor', self.reel_rows)

    def __str__(self):
        return "Payline"

    def __repr__(self):
        return str(self.id) + str(self.reel_rows)


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
        elif section == Section.reels:
            self.read_reels(line)

    def read_symbol(self, line):
        key_val = line.split('=')
        code = key_val[0]
        data_tokens = key_val[1].split()
        bitflag = data_tokens[0]
        desc = data_tokens[1]
        self.symbols.append(Symbol(code, bitflag, desc))

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
        key, val_list = self.read_key_val_line(line, '=', ' ')
        symbol = key.rstrip()
        for reel, mul in enumerate(val_list):
            match = reel + 1
            print('mul', match, mul)
            if int(mul) > 0:
                self.paytables.append(Paytable(symbol, match, mul))
        print('readPaytable', len(self.paytables), self.paytables)

    def read_key_val_line(self, line, keyDel, valDel):
        key_val = line.split(keyDel)
        key = key_val[0]
        val_list = []
        val_tokens = key_val[1].split()
        for t in val_tokens:
            val_list.append(t)
        return key, val_list

    def read_reels(self, line):
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

    def conv_abs_pos(self, reel, row):
        prev_pos = 0
        for rl in range(0, reel):
            prev_pos += self.layout[rl]
        return prev_pos + row

    def get_paytable(self, symbol, match):
        # found = next((x for x in self.paytables if x.symbol == symbol and x.match == match), None)
        found = next((x for x in self.paytables if x.symbol == symbol), None)
        print('getPaytable', symbol, match, found)
        if found is not None:
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
            reel_row = []
            reel_row.append(self.settings.reels[r][stops[r]][0])
            reel_row.append(self.settings.reels[r][(stops[r] + 1) % self.__row_len(r)][0])
            reel_row.append(self.settings.reels[r][(stops[r] + 2) % self.__row_len(r)][0])
            symbolset.append(reel_row)

        print('symbolset', symbolset)

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
        # test symbolset
        symbolset = [['H1', 'H2', 'M1'], ['H1', 'H2', 'M1'], ['H1', 'H2', 'M1'], ['H1', 'H2', 'M1'], ['H1', 'H2', 'M1']]
        payline_wins = []
        start_symbol = None
        match_cnt = 0
        wild_before_start_symbol = 0
        for line in self.settings.paylines:
            for reel, row in enumerate(line.reel_rows):
                s = symbolset[reel][row]
                print('line symbols', reel, row, symbolset[reel][row])
                if s != 'WI':
                    start_symbol = s
                if start_symbol is None and s == 'WI':
                    wild_before_start_symbol += 1
                if start_symbol is not None and s == start_symbol:
                    match_cnt += 1
            if start_symbol is None:
                start_symbol = 'WI'
            match_cnt += wild_before_start_symbol

            payout = self.settings.get_paytable(start_symbol, match_cnt)

            print('line check:', start_symbol, match_cnt)
            if payout > 0:
                payline_wins.append((start_symbol, match_cnt, payout))

        return payline_wins


if __name__ == '__main__':
    machine = SlotMachine()
    machine.spin()
