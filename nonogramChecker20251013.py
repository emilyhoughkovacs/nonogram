# Checks if given example and solution match each other, given a set of hints and a solution

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
        parsed_sol = self.parse_solution()

        return parsed_input == parsed_sol


def main():
    solver = Solution()
    parsed_in = solver.parse_input()
    parsed_out = solver.parse_solution()
    pp = solver.print_solution()

    print(pp)

    with open('solution_first.txt', 'w') as f:
        f.write(pp)

    print("parsed_input: ", parsed_in)
    print("parsed_output:", parsed_out)
    print("solution: ", solver.solution())

if __name__ == '__main__':
    main()