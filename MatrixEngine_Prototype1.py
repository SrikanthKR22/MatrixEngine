import math
import re

class Matrix:

    def __init__(self, data): #accepts a nested list
        if not self._validate(data):
            return
        self.matrix = data
        self._row_count = len(data)
        self._column_count = len(data[0])
        self._construct_datadict()

    def _construct_datadict(self):
        self._datadict = dict()
        row_count = 1
        for row in self.matrix:
            col_count = 1
            for element in row:   
                self._datadict[f'ele{row_count}{col_count}'] = element
                col_count += 1
            row_count += 1

    @classmethod
    def from_inputs(cls):
        _row_count = int(input("Number of rows: "))
        _col_count = int(input("Number of cols: "))
        data = []

        for row in range(_row_count):
            current_row = []
            for col in range(_col_count):
                element = input(f"Enter element ele{row+1}{col+1}: ")
                current_row.append(element)
            data.append(current_row)

        return(cls(data))

    @staticmethod
    def _validate(data):
        len_test_value = len(data[0])
        row_num = -1
        for i in data:
            row_num += 1
            col_num = -1
            if len(i) != len_test_value:
                print(f"Matrix dimensions violated! Row-{row_num+1}, Expected: [no of columns = {len_test_value}]")
                return False
            for j in i:
                col_num += 1
                if isinstance(j, str) and j.startswith('exp(') and j.endswith(')'):
                    data[row_num][col_num] = j[4:-1]
                elif not isinstance(j, (int, float, complex)):
                    print(f'Element Violated! Element at ele{row_num+1}{col_num+1} is not a numeral value')
                    return False
        return True

    def exp_solve(self):
        solve_dict = dict()
        search_pattern = re.compile(r'([a-zA-Z]+)\(([+-]?\d*\.?\d+)\)')
        for row_count, row in enumerate(self.matrix):
            for col_count, element in enumerate(row):
                if isinstance(element,str):
                    match = search_pattern.fullmatch(element)
                    if match:
                        func = match.group(1)
                        parameter = float(match.group(2))
                        func_math = getattr(math, func)
                        result = func_math(parameter)
                        index = (row_count, col_count)
                        solve_dict[index] = result

        for index, value in solve_dict.items():
            rindex, cindex = index
            self.matrix[rindex][cindex] = value

        return self.matrix
                                            

    @property
    def fetcher(self):
        pass

    def __str__(self):
        len_list = []
        for row in self.matrix:
            for element in row:
                len_list.append(len(str(element)))
        len_maxxer = max(len_list)

        displaystr = '\n ' + '_'*(len_maxxer+1) + ' '*(len_maxxer*(self._column_count+1)) + '_'*(len_maxxer+1) +  '\n'
        for row in self.matrix:
            displaystr += '| '
            for element in row:
                displaystr += str(element) + ' '*(len_maxxer - len(str(element))+1)
            displaystr += '|\n'
        displaystr += ' ' + '¯'*(len_maxxer+1) + ' '*(len_maxxer*(self._column_count+1)) + '¯'*(len_maxxer+1) +  '\n'
        return displaystr

data = [
    [12, 5, 83, 41, 7, 29, 64],
    [91, 34, 16, 72, 8, 55, 20],
    [43, 67, 3, 88, 51, 14, 76],
    [25, 99, 38, 6, 47, 81, 32],
    [70, 11, 59, 23, 95, 40, 68]
]
mat = Matrix(data)
print(mat)

solve_test_nlist = [
    [12, "exp(sin(30))", 7.5],
    ["exp(cos(60))", -4, "exp(sqrt(81))"],
    [3.14, "exp(tan(45))", "exp(log10(1000))"]
]

solve_test_matrix = Matrix(solve_test_nlist)
print('Sucess!!!')
print(solve_test_matrix)