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

    def parse_solution(self):
        args = self.args

        file = args[1] if len(args) >= 2 and os.path.isfile(args[1]) else 'solution_first_oneline.txt'
        f = open(file, 'r')
        solutions = f.read().splitlines()
        f.close()

        solutions = [solution.split(',') for solution in solutions]
        solutions = [[[char for char in row] for row in solution] for solution in solutions]

        def transpose(sol):
            transposed = [[None for _ in range(len(sol))] for _ in range(len(sol[0]))]
            for i in range(len(sol)):
                for j in range(i, len(sol[0])):
                    transposed[i][j], transposed[j][i] = sol[j][i], sol[i][j]
            return transposed

        trans = [transpose(x) for x in solutions]

        rows = [[[len(r) for r in ''.join(row).split()] for row in s] for s in solutions]
        cols = [[[len(c) for c in ''.join(col).split()] for col in s] for s in trans]

        return [list(pair) for pair in zip(rows, cols)]

    def print_solution(self):
        args = self.args

        file = args[1] if len(args) >= 2 and os.path.isfile(args[1]) else 'solution_first_oneline.txt'
        f = open(file, 'r')
        solutions = f.read().splitlines()
        f.close()

        solutions = [solution.split(',') for solution in solutions]
        solutions = '\n'.join('\n'.join(sol) for sol in solutions)

        return solutions


    def solution(self):

        parsed_input = self.parse_input()

        def solve_from_left(row_or_col, grid_size):
            if len(row_or_col) == 1 and row_or_col[0] > grid_size / 2:
                return range(row_or_col[0])
            elif sum(row_or_col) + len(row_or_col) - 1 > grid_size / 2:
                xs = list()
                for i, chunk in enumerate(row_or_col):
                    xs.append([num for num in range(len(xs)+i, len(xs)+i+chunk)])
                return xs
            else:
                return []

        def solve_from_right(row_or_col, grid_size):
            if len(row_or_col) == 1 and row_or_col[0] > grid_size / 2:
                return range(grid_size - row_or_col[0], grid_size)
            elif sum(row_or_col) + len(row_or_col) - 1 > grid_size / 2:
                xs = list()
                for i, chunk in zip(range(len(row_or_col)), reversed((row_or_col))):
                    xs.append([num for num in range(grid_size-i-len(xs)-chunk, grid_size-i-len(xs))])
                return xs
            else:
                return []

        def solve_row_or_column(row_or_col, grid_size):
            left = solve_from_left(row_or_col, grid_size)
            right = solve_from_right(row_or_col, grid_size)
            return ['.' if x in left and x in right else ' ' for x in range(grid_size) ]

    def check_solution(self):

        parsed_input = self.parse_input()
        parsed_sol = self.parse_solution()

        return parsed_input == parsed_sol


def main():
    solver = Solution()
    parsed = solver.parse_input()
    sol = solver.solution()
    print("parsed_input:", parsed)
    print(sol)
    print("solution:", solver.check_solution(sol))
    print("solution is valid:", solver.check_solution(sol)==parsed)


    # print("solution: ", s.solution(s.args))

if __name__ == '__main__':
    main()