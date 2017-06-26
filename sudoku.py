from __future__ import division, print_function


class Sudoku:

    def __init__(self, s):
        self.s = [int(v) for v in s]
        self.empty = len([v for v in self.s if v == 0])
        # print "Suduko with", 81-self.empty, "filled entries"
        self.opts_row = {}
        self.opts_col = {}
        self.opts_block = {}
        self.init_opts()

    def init_opts(self):
        full = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for i in range(9):
            diff = full.difference(self.get_row_entries(i))
            if diff:
                self.opts_row[i] = diff

            diff = full.difference(self.get_col_entries(i))
            if diff:
                self.opts_col[i] = diff

            diff = full.difference(self.get_block_entries(i))
            if diff:
                self.opts_block[i] = diff

    def get_row_entries(self, i):
        """ get all filled entries of the i-th row"""
        e = set(self.s[i*9:(i+1)*9])
        if 0 in e:
            e.remove(0)
        return e

    def get_col_entries(self, i):
        """ get all filled entries of the i-th column"""
        c = i % 9
        e = set([self.s[c+j*9] for j in range(9)])
        if 0 in e:
            e.remove(0)
        return e

    def get_block_entries(self, i):
        """ get all filled entries of the i-th block"""
        b = 27*(i//3) + (i % 3)*3
        e = set([self.s[b+i+j*9] for i in range(3) for j in range(3)])
        if 0 in e:
            e.remove(0)
        return e

    def get_position(self, i):
        """ get the row, column and block index of the i-th entry"""
        r = i//9
        c = i % 9
        # b = 3*(i//27) +
        b = 3*(r//3) + c//3
        return r, c, b

    def check(self):
        """ walk through the entries and check possible entries"""
        n_found = 0
        min_opt = (9, 0)
        for i, v in enumerate(self.s):
            if v == 0:
                r, c, b = self.get_position(i)
                opts = self.opts_row[r] & self.opts_col[c] & self.opts_block[b]
                if len(opts) < min_opt[0]:
                    min_opt = (len(opts), i)
                if len(opts) == 1:
                    v = opts.pop()
                    self.s[i] = v
                    self.opts_row[r].remove(v)
                    self.opts_col[c].remove(v)
                    self.opts_block[b].remove(v)
                    n_found += 1
        self.empty -= n_found
        return n_found, min_opt

    def solve(self, verbose=True):
        while(True):
            found, m = self.check()
            if found == 0:
                if self.empty == 0:
                    if verbose:
                        print("Sudoku solved")
                    return True
                else:
                    if verbose:
                        print("Sudoku not solved, "
                              "{} entries left".format(self.empty))
                        print("minimal number of possibilities "
                              "is {} at {}".format(*m))
                    return False

    def set(self, i, v):
        r, c, b = self.get_position(i)
        self.opts_row[r].remove(v)
        self.opts_col[c].remove(v)
        self.opts_block[b].remove(v)
        self.s[i] = v

    def __str__(self):
        s = ""
        n = 0
        for i in range(9):
            s += "{v[0]} {v[1]} {v[2]} | {v[3]} {v[4]} {v[5]} | "\
                 "{v[6]} {v[7]} {v[8]}\n".format(v=self.s[i*9:(i+1)*9])
            if i == 2 or i == 5:
                s += "- - - + - - - + - - -\n"
        return s


def test_1():
    s = Sudoku("00000001040000000002000000000005040700800"
               "0300001090000300400200050100000000806000")
    s.solve()
    print(s)


def test_2():
    s = Sudoku("24030000078050600093047005850790001001000"
               "0090090007504470015089000803072000004035")
    s.solve()
    print(s)


def read_from_file_and_solve():
    solved = 0
    not_solved = 0

    with open("sudokus.txt") as f:
        for l in f.readlines():
            s = Sudoku(l.strip())
            if s.solve(False):
                solved += 1
            else:
                not_solved += 1
    print("Solved {} from {} Sudokus".format(solved, solved+not_solved))


if __name__ == "__main__":
    test_1()
    test_2()
