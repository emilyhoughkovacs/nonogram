import sys
import os
import re

class Solution(object):
    def __init__(self):
        self.args = [arg for arg in sys.argv[1:]]

    def parse_input(self):
        args = self.args

        # uses first command line arg if exists else inputfile.txt
        file = args[0] if args and os.path.isfile(args[0]) else 'nonograms_5x5_first.csv'
        f = open(file, 'r')
        nonograms = f.read().splitlines()[1:]
        f.close()

        rows = [[[int(num) for num in line.split('-')] for line in nonogram.split(',')[0:5]] for nonogram in nonograms]
        cols = [[[int(num) for num in line.split('-')] for line in nonogram.split(',')[5:]] for nonogram in nonograms]

        nons = [list(pair) for pair in zip(rows, cols)]

        return nons

    def transpose(self, sol):
        transposed = [[None for _ in range(len(sol))] for _ in range(len(sol[0]))]
        for i in range(len(sol)):
            for j in range(i, len(sol[0])):
                transposed[i][j], transposed[j][i] = sol[j][i], sol[i][j]
        return transposed

    def solution(self):

        parsed_input = self.parse_input()
        rowlength = len(parsed_input[0][0])
        collength = len(parsed_input[0][1])

        board = [['.' for _ in range(rowlength)] for _ in range(collength)]

        print(board)
        print(self.transpose(board))

        # def solve_from_left(row_or_col, grid_size):
        #     if len(row_or_col) == 1 and row_or_col[0] > grid_size / 2:
        #         return range(row_or_col[0])
        #     elif sum(row_or_col) + len(row_or_col) - 1 > grid_size / 2:
        #         xs = list()
        #         for i, chunk in enumerate(row_or_col):
        #             xs.append([num for num in range(len(xs)+i, len(xs)+i+chunk)])
        #         return xs
        #     else:
        #         return []

        # def solve_from_right(row_or_col, grid_size):
        #     if len(row_or_col) == 1 and row_or_col[0] > grid_size / 2:
        #         return range(grid_size - row_or_col[0], grid_size)
        #     elif sum(row_or_col) + len(row_or_col) - 1 > grid_size / 2:
        #         xs = list()
        #         for i, chunk in zip(range(len(row_or_col)), reversed((row_or_col))):
        #             xs.append([num for num in range(grid_size-i-len(xs)-chunk, grid_size-i-len(xs))])
        #         return xs
        #     else:
        #         return []

        # def solve_row_or_column(row_or_col, grid_size):
        #     left = solve_from_left(row_or_col, grid_size)
        #     right = solve_from_right(row_or_col, grid_size)
        #     return ['x' if x in left and x in right else ' ' for x in range(grid_size) ]

        return ['xxxxx,x    , xxxx,x    ,x    ']

    def parse_solution(self):
        solutions = self.solution()

        solutions = [solution.split(',') for solution in solutions]
        solutions = [[[char for char in row] for row in solution] for solution in solutions]

        trans = [self.transpose(x) for x in solutions]

        rows = [[[len(r) for r in ''.join(row).split()] for row in s] for s in solutions]
        cols = [[[len(c) for c in ''.join(col).split()] for col in s] for s in trans]

        return [list(pair) for pair in zip(rows, cols)]

    def print_solution(self):
        solutions = self.solution()

        solutions = [solution.split(',') for solution in solutions]
        solutions = '\n'.join('\n'.join(sol) for sol in solutions)

        return solutions

    def check_solution(self):

        parsed_input = self.parse_input()
        parsed_sol = self.parse_solution()

        return parsed_input == parsed_sol


def main():
    solver = Solution()
    parsed = solver.parse_input()
    sol = solver.parse_solution()
    # pp = solver.print_solution()

    # print(pp)
    print("parsed_input: ", parsed)
    print("parsed_output:", sol)
    # print("solution:", solver.check_solution())


    # print("solution: ", s.solution(s.args))

if __name__ == '__main__':
    main()