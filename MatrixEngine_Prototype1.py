import math
import re


class Matrix:

    def __init__(self, data): #accepts a nested list
        if not self._validate(data):
            print("Cannot Construct Matrix!")
            return
        self.matrix = data
        self._row_count = len(data)
        self._column_count = len(data[0])
        print("Matrix Constructed!")

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
        if not (data and isinstance(data, list)):
            print(f"TypeError: The data should be in the form of nested Lists only!")
            return
        for i in data:
            if not isinstance(i, list):
                print(f"TypeError: The row data should be in the form of Lists only!")
                return
            if not i:
                print("ValueError: Given Data must atleast contain one column!")
                return
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
            exp_solved_matrix = [[element.result if isinstance(element, Matrix.Exp) else element for element in row] for row in self.matrix]
            return Matrix(exp_solved_matrix)
        else:
            print("Invalid Matrix! Cannot Solve Expressions ")

    def get(self, row, col):
        return self.matrix[row-1][col-1]
    
    def transpose(self):
        if hasattr(self, 'matrix'):
            transpose = []
            for col_count in range(self._column_count):
                new_row = []
                for row in self.matrix:
                    new_row.append(row[col_count])
                transpose.append(new_row)
            return Matrix(transpose)

    def __str__(self):
        print_str = '\n'
        body_str = ''
        #column specific max lens
        col_len = []
        for col in range(self._column_count):
            current_col_len = []
            for row in self.matrix:
                current_col_len.append(len(str(row[col])))
            col_len.append(max(current_col_len)+2)
        #prepping print_strs
        for rno, row in enumerate(self.matrix):
            body_str += '| '
            for cno, element in enumerate(row):
                body_str += str(element) + ' '*(col_len[cno] - len(str(element)))
            body_str += '|\n'
        horizontal_len = len(body_str.split('\n')[0])
        dashcount = max(round(horizontal_len*0.1), 1)
        head = '\n ' + '_'*dashcount + ' '*(horizontal_len-(2*dashcount)-2) + '_'*dashcount + '\n'
        foot = ' ' + '‾'*dashcount + ' '*(horizontal_len-(2*dashcount)-2) + '‾'*dashcount + '\n'
        print_str = head + body_str + foot
        return print_str


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
                    trig_funcs = ['sin', 'cos', 'tan']
                    if self.func_name in trig_funcs:
                        self.parameter = round(math.radians(self.parameter), 4)
                    self.result = round(self.function(self.parameter), 4)
                    self.valid = True
                elif self.func_name in ['cosec', 'sec', 'cot']:
                    self.function = getattr(Matrix.Exp, self.func_name)
                    self.parameter = round(math.radians(float(match.group(2))),4)
                    self.result = round(self.function(self.parameter),4)
                    self.valid = True

                else:
                    print(f"Element Violated! Invalid Expresion at ele{row_no}{col_no}")
                    return
            else:
                print(f"Element Violated! Invalid Expresion at ele{row_no}{col_no}")

        def __str__(self):
            return f'{self.func_name}({self.parameter})'

        @staticmethod
        def cosec(parameter):
            return 1/(math.sin(parameter))
        @staticmethod
        def sec(parameter):
            return 1/(math.cos(parameter))
        @staticmethod
        def cot(parameter):
            return 1/(math.tan(parameter))

    

data = [
    [12, 5, 83, 41, 7, 29, 64],
    [91, 34, 16, 72, 8, 55, 20],
    [43, 67, 3, 88, 51, 14, 76],
    [25, 99, 38, 6, 47, 81, 32],
    [70, 11, 59, 23, 95, 40, 68]
]
print()
mat = Matrix(data)
print(mat)
a = mat.transpose()
print(a)
print()
solve_test_nlist = [
    [12, "exp(sin(30))", 7.5],
    ["exp(cos(60))", -4, "exp(sqrt(81))"],
    [3.14, "exp(cot(45))", "exp(log10(1000))"]
]
matrix_object = Matrix(solve_test_nlist)
print(matrix_object)
print(matrix_object.exp_solve())