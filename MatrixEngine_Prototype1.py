import math
import re
math.cosec = lambda x: 1 / math.sin(x)
math.sec = lambda x: 1 / math.cos(x)
math.cot = lambda x: 1 / math.tan(x)

class Matrix:

    def __init__(self, data): #accepts a nested list
        if not self._validate(data):
            print("Cannot Construct Matrix!")
            return
        self.matrix = data
        self._row_count = len(data)
        self._column_count = len(data[0])
        self._construct_datadict()
        print("Matrix Constructed!")

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
        for row_no, row in enumerate(data,1):
            if len(row) != len_test_value:
                print(f"Matrix dimensions violated! Row-{row_no}, Expected: [no of columns = {len_test_value}]")
                return
        exp_dict = dict()
        temp_dict = dict()
        for row_no, row in enumerate(data,1):
            for col_no, element in enumerate(row,1):
                if isinstance(element, str) and element.startswith('exp(') and element.endswith(')'):
                    element = element[4:-1]
                    temp_dict[row_no, col_no] = Matrix.Exp(element, row_no, col_no)
                    if temp_dict[row_no, col_no].valid:
                        exp_dict[(row_no, col_no)] = temp_dict[row_no, col_no]
                    else:
                        print(f"Element Violated! Invalid expression at a{row_no}{col_no}")
                        return
                elif not isinstance(element, (int, float, complex)):
                    print(f'Element Violated! Element at ele{row_no}{col_no} is not a numeral value or an expression')
                    return
        for (row, col), value in exp_dict.items():
            data[row-1][col-1] = value
        return True

    def exp_solve(self):
        if hasattr(self, 'matrix'):
            solve_dict = dict()
            for row_index, row in enumerate(self.matrix):
                for col_index, element in enumerate(row):
                    if isinstance(element, Matrix.Exp):
                        solve_dict[(row_index, col_index)] = element.result
            for row_index, col_index in solve_dict.keys():
                self.matrix[row_index][col_index] = solve_dict[(row_index, col_index)]
            return self
        else:
            print("Invalid Matrix! Cannot Solve Expressions ")

    @property
    def fetcher(self):
        pass
    
    def transpose(self):
        if hasattr(self, 'matrix'):
            self._transpose = []
            for col_count in range(self._column_count):
                new_row = []
                for row in self.matrix:
                    new_row.append(row[col_count])
                self._transpose.append(new_row)
            return Matrix(self._transpose)

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


    class Exp:

        def __init__(self, element, row_no, col_no):
            self.valid = False
            self.row_no = row_no
            self.col_no = col_no
            search_pattern = re.compile(r'([a-zA-Z]+(?:10)?)\(([+-]?\d*\.?\d+)\)')
            match = search_pattern.fullmatch(element)
            if match:
                self.func_name = match.group(1)
                if hasattr(math, self.func_name):
                    self.function = getattr(math, self.func_name)
                    self.parameter = float(match.group(2))
                    trig_funcs = ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot']
                    if self.func_name in trig_funcs:
                        self.parameter = math.radians(self.parameter)
                    self.result = self.function(self.parameter)
                    self.valid = True
                else:
                    print(f"Element Violated! Invalid Expresion at ele{row_no}{col_no}")
                    return
            else:
                print(f"Element Violated! Invalid Expresion at ele{row_no}{col_no}")

        def __str__(self):
            return f'{self.func_name}({self.parameter})'
    

data = [
    [12, 5, 83, 41, 7, 29, 64],
    [91, 34, 16, 72, 8, 55, 20],
    [43, 67, 3, 88, 51, 14, 76],
    [25, 99, 38, 6, 47, 81, 32],
    [70, 11, 59, 23, 95, 40, 68]
]
mat = Matrix(data)
print(mat)
a = Matrix(mat.transpose())
print(a)
'''print()
solve_test_nlist = [
    [12, "exp(sin(30))", 7.5],
    ["exp(cos(60))", -4, "exp(sqrt(81))"],
    [3.14, "exp(tan(45))", "exp(log10(1000))"]
]
matrix_object = Matrix(solve_test_nlist)
print(matrix_object)
print(matrix_object.exp_solve())'''