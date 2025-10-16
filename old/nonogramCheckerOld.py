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
        file = args[0] if args and os.path.isfile(args[0]) else 'example.txt'
        f = open(file, 'r')
        nonogram = f.read().splitlines()
        f.close()

        nonogram = [[[int(num) for num in x.split(' ')] for x in line.split(', ')] for line in nonogram]

        return nonogram


    def parse_solution(self):
        args = self.args

        file = args[1] if len(args) >= 2 and os.path.isfile(args[1]) else 'solution.txt'
        f = open(file, 'r')
        solution = f.read().splitlines()
        f.close()

        # transpose solution and check in opposite direction
        transposed = [[char for char in row] for row in solution]

        for i in range(len(solution)):
            for j in range(i, len(solution[0])):
                transposed[i][j], transposed[j][i] = solution[j][i], solution[i][j]

        transposed = [''.join(row) for row in transposed]
        columns = [[x for x in row if x!=''] for row in [re.split(r'x+', line) for line in transposed]]
        columns = [[len(x) for x in row] for row in columns]

        rows = [[x for x in row if x!=''] for row in [re.split(r'x+', line) for line in solution]]
        rows = [[len(x) for x in row] for row in rows]

        return [columns, rows]

    def solution(self):

        parsed_input = self.parse_input()
        parsed_sol = self.parse_solution()

        return parsed_input == parsed_sol


def main():
    solver = Solution()
    parsed_in = solver.parse_input()
    parsed_out = solver.parse_solution()

    print(len(parsed_in))

    print("parsed_input: ", parsed_in)
    print("parsed_output:", parsed_out)
    print("solution: ", solver.solution())

if __name__ == '__main__':
    main()