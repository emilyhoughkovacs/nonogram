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

    def solution(self):

        # def parse_solution(args):
        #     file = args[1] if len(args) >= 2 and os.path.isfile(args[1]) else 'solution.txt'
        #     f = open(file, 'r')
        #     solution = f.read().splitlines()
        #     f.close()

        #     # transpose solution and check in opposite direction
        #     transposed = [[char for char in row] for row in solution]

        #     for i in range(len(solution)):
        #         for j in range(i, len(solution[0])):
        #             transposed[i][j], transposed[j][i] = solution[j][i], solution[i][j]

        #     transposed = [''.join(row) for row in transposed]
        #     columns = [[x for x in row if x!=''] for row in [re.split(r'x+', line) for line in transposed]]
        #     columns = [[len(x) for x in row] for row in columns]

        #     rows = [[x for x in row if x!=''] for row in [re.split(r'x+', line) for line in solution]]
        #     rows = [[len(x) for x in row] for row in rows]

        #     return [columns, rows]

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

        # assert(parse_solution(self.args) == parse_input(self.args))
        # print("assertion passed")
        # print("parse_solution(self.args): ", parse_solution(self.args))

        parsed_input = self.parse_input()
        # print("parsed_input:", parsed_input)

        solution = [solve_row_or_column(row, len(parsed_input[0])) for row in parsed_input[1]]

        # print("solution: ", solution)

        # col = parsed_input[0][0]
        # row = parsed_input[1][0]
        # print(solve_row_or_column(row, len(parsed_input[0])))
        # print(solve_row_or_column(col, len(parsed_input[0])))
        return solution

    def check_solution(self, solution):
        # test = [[' ', ' ', '.', ' ', '.'], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', '.', '.', '.', ' ']]
        blah = [''.join(x).split() for x in solution]
        nums = [[len(i) for i in x] if len(x)>=1 else [0] for x in blah]
        return nums


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