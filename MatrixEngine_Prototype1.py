#_____________________________________________________________________________________________IMPORTS_____________________________________________________________________________________________#
import math
import re
import copy
import timeit
#_____________________________________________________________________________________________CLASSES_____________________________________________________________________________________________#

class Matrix:

    #____________________________________________________________________________________INPUT-CONTRUCT-OUTPUT____________________________________________________________________________________#

    def __init__(self, data): #accepts a nested list
        if not self._validate(data):
            print("Cannot Construct Matrix!")
            return
        self.matrix = data
        self._row_count = len(data)
        self._column_count = len(data[0])

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
            print(data)
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
        for row_no, row in enumerate(data,1):
            for col_no, element in enumerate(row,1):
                if isinstance(element, str) and element.startswith('exp(') and element.endswith(')'):
                    element = element[4:-1]
                    temp_exp  = Matrix.Exp(element, row_no, col_no)
                    if temp_exp.valid:
                        exp_dict[(row_no, col_no)] = temp_exp
                    else:
                        print(f"Element Violated! Invalid expression at a{row_no}{col_no}")
                        return
                elif not isinstance(element, (int, float, Matrix.Exp, Matrix.Compound_Exp)):
                    print(f'Element Violated! Element at ele{row_no}{col_no} is not a numeral value or an expression')
                    return
        for (row, col), value in exp_dict.items():
            data[row-1][col-1] = value
        return True

    def validate_rc(self, row_index, col_index):
        if hasattr(self, 'matrix'):
            if (1 <= row_index <= self._row_count) and (1 <= col_index <= self._column_count):
                return True
            else:
                print(f"Indices {row_index},{col_index} do not exist in Matrix")
        else:
            print("MatrixError: Matrix does not Exist!")

    def is_mat(self):
        if hasattr(self, 'matrix'):
            return True
        else:
            print("MatrixError: Matrix does not Exist!")

    def is_square(self):
        if self.is_mat():
            if self._row_count == self._column_count:
                return True
    def is_22(self):
        if self.is_mat():
            if (self._row_count == 2) and (self._column_count == 2):
                return True
            
    def has_exp(self):
        return any((isinstance(element, (Matrix.Exp, Matrix.Compound_Exp)) for element in row) for row in self.matrix)

    def get(self, row, col):
        return self.matrix[row-1][col-1]

    @property
    def dimensions(self):
        return (self._row_count, self._column_count)

    def __str__(self):
        if self.is_mat():
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
            for row in self.matrix:
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
        else:
            return 'PrintError'


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
            return f'{self.func_name}({round(math.degrees(self.parameter))})' if self.func_name in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot'] else f'{self.func_name}({self.parameter})'

        def __add__(self, other):
            a = self.result if isinstance(self, Matrix.Exp) else self
            b = other.result if isinstance(other, Matrix.Exp) else other
            result = a + b
            return(Matrix.Compound_Exp(self, other, ' + ', result))

        def __radd__(self, other):
            return self + other

        def __sub__(self, other):
            a = self.result if isinstance(self, Matrix.Exp) else self
            b = other.result if isinstance(other, Matrix.Exp) else other
            result = a - b
            return(Matrix.Compound_Exp(self, other, ' - ', result))

        def __rsub__(self, other):
            a = self.result if isinstance(self, Matrix.Exp) else self
            b = other.result if isinstance(other, Matrix.Exp) else other
            result = b - a
            return Matrix.Compound_Exp(other, self, ' - ', result)

        def __mul__(self, other):
            a = self.result if isinstance(self, Matrix.Exp) else self
            b = other.result if isinstance(other, Matrix.Exp) else other
            result = a * b
            return(Matrix.Compound_Exp(self, other, ' * ', result))

        def __rmul__(self, other):
            return self*other

        def __truediv__(self, other):
            try:
                a = self.result if isinstance(self, Matrix.Exp) else self
                b = other.result if isinstance(other, Matrix.Exp) else other
                result = a / b
                return(Matrix.Compound_Exp(self, other, ' / ', result))
            except ZeroDivisionError:
                print(f"Zero Division Error at exp: {self}/{other}")

        def __rtruediv__(self, other):
            try:
                a = self.result if isinstance(self, Matrix.Exp) else self
                b = other.result if isinstance(other, Matrix.Exp) else other
                result = b / a
                return(Matrix.Compound_Exp(other, self, ' / ', result))
            except ZeroDivisionError:
                print(f"Zero Division Error at exp: {other}/{self}")

        def __floordiv__(self, other):
            try:
                a = self.result if isinstance(self, Matrix.Exp) else self
                b = other.result if isinstance(other, Matrix.Exp) else other
                result = a // b
                return(Matrix.Compound_Exp(self, other, ' // ', result))
            except ZeroDivisionError:
                print(f"Zero Division Error at exp: {self}//{other}")

        def __rfloordiv__(self, other):
            try:
                a = self.result if isinstance(self, Matrix.Exp) else self
                b = other.result if isinstance(other, Matrix.Exp) else other
                result = b // a
                return(Matrix.Compound_Exp(other, self, ' // ', result))
            except ZeroDivisionError:
                print(f"Zero Division Error at exp: {other}//{self}")
        
        @staticmethod
        def cosec(parameter):
            return 1/(math.sin(parameter))
        @staticmethod
        def sec(parameter):
            return 1/(math.cos(parameter))
        @staticmethod
        def cot(parameter):
            return 1/(math.tan(parameter))


    class Compound_Exp():

        def __init__(self, operand1, operand2, operator, result):
            self.operand1 = operand1
            self.operand2 = operand2
            self.operator = operator
            self.result = result

        def __str__(self):
            return '[' + str(self.operand1) + self.operator + str(self.operand2) + ']'
            
    #____________________________________________________________________________________LOCAL_OPERATIONS____________________________________________________________________________________#

    def exp_solve(self):
        if self.is_mat():
            exp_solved_matrix = [[element.result if isinstance(element, (Matrix.Exp, Matrix.Compound_Exp)) else element for element in row] for row in self.matrix]
            return Matrix(exp_solved_matrix)

    def transpose(self):
        if self.is_mat():
            return Matrix([[(row[col_count]) for row in self.matrix] for col_count in range(self._column_count)])

    def determinant_laplace(self):
        if self.is_mat():
            if self.is_square():
                if self.has_exp():
                    self = self.exp_solve()
                if self._row_count == 1:
                    return self.get(1,1)
                if self.is_22():
                    return (self.get(1,1) * self.get(2,2)) - (self.get(1,2) * self.get(2,1))
                else:
                    return sum(((-1)**no * top_row_element * self.minor_of_ele_Mat(1,no+1).determinant_laplace()) for no, top_row_element in enumerate(self.matrix[0]))
            else:
                print("ValueError: Cannot calculate determinant for a non square Matrix!")

    def determinant_gaussian(self):
        if self.is_mat():
            if self.is_square():
                gauss = copy.deepcopy(self.exp_solve().matrix)
                result = 1
                for rno in range(self._row_count): #pivot-by-pivot
                    pivot = gauss[rno][rno]
                    if pivot == 0:
                        for pivot_search in range(rno+1, self._row_count):
                            if gauss[pivot_search][rno] != 0:
                                pivot = gauss[pivot_search][rno]
                                gauss[rno],gauss[pivot_search] = gauss[pivot_search],gauss[rno]
                                result *= -1
                                break
                        else:
                            continue
                    for to_zero in range(rno+1, self._row_count): #row-by-row, eliminating zeros
                        factor = gauss[to_zero][rno] / pivot
                        gauss[to_zero] = list(map(lambda r1,r2: r2 - factor*r1, gauss[rno],gauss[to_zero]))
                for i in range(self._row_count): # product of diagonal entries of triangular matrix
                    result *= gauss[i][i]
                print(round(result))
                return round(result,4)
            else:
                print('Cannot calculate determinant for a non sqaure matrix!')

    def det_comp(self):
        ltime = timeit.timeit(lambda: self.determinant_laplace(), number=10) / 10
        gtime = timeit.timeit(lambda: self.determinant_gaussian(), number=10) / 10
        return f"Laplace:\nDeterminant = {self.determinant_laplace()}\nTime = {ltime}\n\nGaussian:\nDeterminant = {self.determinant_gaussian()}\nTime = {gtime}\n\n"
    
    def inverse(self): #-> Matrix
        if self.is_mat():
            if self.is_square():
                try:
                    return (1/self.determinant_gaussian()) * self.adj()
                except ZeroDivisionError:
                    print("Non-Invertible and Singular Matrix!")
            else:
                print("ValueError: Cannot Invert a non-square Matrix!")

    def minor_of_ele_Mat(self, row, col): #-> MinorMatrix of a particular element
        if self.validate_rc(row, col):
            return Matrix([[element for cno, element in enumerate(row_iter,1) if cno!=col] for rno, row_iter in enumerate(self.matrix,1) if rno!=row])

    def minor_of_ele_Val(self, row, col): #-> MinorValue of a particular element
        if self.is_square():
            if self.validate_rc(row, col):
                if self.has_exp():
                    solved_self = self.exp_solve()
                    return solved_self.minor_of_ele_Mat(row,col).determinant_gaussian()
                return self.minor_of_ele_Mat(row,col).determinant_gaussian()
        else:
            print("ValueError: Cannot calculate determinant for a non square Matrix!")

    def minor_matrix(self): #-> Matrix Of Minor Values of the entire Original Matrix
        return Matrix([[self.minor_of_ele_Val(rno+1, cno+1) for cno in range(self._column_count)] for rno in range(self._row_count)])

    def cofac_of_ele_Mat(self, row, col): #-> CofacMatrix of a particular element
        if self.validate_rc(row,col):
            return Matrix([[ (element * (-1)**(rno+cno)) for cno, element in enumerate(rowval,1)] for rno,rowval in enumerate(self.minor_of_ele_Mat(row,col).matrix,1)])

    def cofac_of_ele_Val(self, row, col): #-> CofacValue of a particular element
        if self.validate_rc(row, col):
            return self.minor_of_ele_Val(row,col) * (-1)**(row+col)

    def cofac_matrix(self): #-> Matrix Of Cofactor Values of the entire Original Matrix
        if self.is_mat():
            return Matrix([[(element * (-1)**(rno+cno)) for cno,element in enumerate(row,1)] for rno,row in enumerate(self.minor_matrix().matrix,1)])
        
    def adj(self):
        if self.is_mat():
            return self.cofac_matrix().transpose()

    def rank(self):
        if self.is_mat():
            rank = 0
            gauss = copy.deepcopy(self.matrix)
            rno = 0
            for cno in range(self._column_count):
                if rno >= self._row_count:
                    break
                pivot = gauss[rno][cno]
                if pivot == 0:
                    for pivot_search in range(rno+1, self._row_count):
                        if gauss[pivot_search][cno] != 0:
                            pivot = gauss[pivot_search][cno]
                            gauss[rno], gauss[pivot_search] = gauss[pivot_search], gauss[rno]
                            break
                    else:
                        continue
                for to_zero in range(rno+1, self._row_count):
                    factor = gauss[to_zero][cno] / pivot
                    gauss[to_zero] = list(map(lambda r1, r2: r2 - factor*r1, gauss[rno], gauss[to_zero]))
                rno += 1
                rank += 1
            return rank

    #____________________________________________________________________________________INTER_OPERATIONS____________________________________________________________________________________#

    def __add__(self, other):
        if self.is_mat() and other.is_mat():
            if (self._row_count == other._row_count) and (self._column_count == other._column_count):
                return Matrix([[element + other.matrix[rno][cno] for cno,element in enumerate(row)] for rno,row in enumerate(self.matrix)])
            else:
                print("Cannot Add Matrices! Matrix Dimensions do not match!")

    def __sub__(self, other):
        if self.is_mat() and other.is_mat():
            if (self._row_count == other._row_count) and (self._column_count == other._column_count):
                return Matrix([[element - other.matrix[rno][cno] for cno,element in enumerate(row)] for rno,row in enumerate(self.matrix)])
            else:
                print("Cannot Subtract Matrices! Matrix Dimensions do not match!")

    def __mul__(self, other):
        if self.is_mat() and isinstance(other, (int, float)):
            return Matrix([[(element * other) for element in row] for row in self.matrix])
        elif self.is_mat() and other.is_mat():
            if self._column_count == other._row_count:
                result = []
                solved_self = self.exp_solve().matrix if self.has_exp() else self.matrix
                solved_other = other.exp_solve().matrix if other.has_exp() else other.matrix
                for row in solved_self:
                    current_result_row = []
                    for cno in range(other._column_count):
                        elemental_result = sum((row[i]*solved_other[i][cno]) for i in range(other._row_count))
                        current_result_row.append(elemental_result)
                    result.append(current_result_row)
                return Matrix(result)
            else:
                print(f"ValueError: dimensional mismatch, cannot multiply matrices with dimensions {self._row_count}x{self._column_count} and {other._row_count}x{other._column_count}!")
        else:
            print("TypeError: Cannot multiply terms!")

    def __rmul__(self, other):
        if self.is_mat() and isinstance(other, (int, float)):
            return self*other

    def ele_wise_mul(self, other):
        if self.is_mat() and other.is_mat():
            if (self._row_count == other._row_count) and (self._column_count == other._column_count):
                return Matrix([[element * other.matrix[rno][cno] for cno,element in enumerate(row)] for rno,row in enumerate(self.matrix)])
            else:
                print("Cannot Multiply Matrices! Matrix Dimensions do not match!")

    def __truediv__(self, other):
        if self.is_mat() and other.is_mat():
            return self * other.inverse()
        if self.is_mat and isinstance(other, (int, float)):
            return Matrix([[element/other for element in row] for row in self.matrix])

    def __rtruediv__(self, other):
        return other*self.inverse()
    
    def ele_wise_div(self, other):
        if self.is_mat() and other.is_mat():
            if (self._row_count == other._row_count) and (self._column_count == other._column_count):
                return Matrix([[element / other.matrix[rno][cno] for cno,element in enumerate(row)] for rno,row in enumerate(self.matrix)])
            else:
                print("Cannot Divide Matrices! Matrix Dimensions do not match!")

    def ele_wise_floor_div(self, other):
        if self.is_mat() and other.is_mat():
            if (self._row_count == other._row_count) and (self._column_count == other._column_count):
                return Matrix([[element // other.matrix[rno][cno] for cno,element in enumerate(row)] for rno,row in enumerate(self.matrix)])
            else:
                print("Cannot Floor Divide Matrices! Matrix Dimensions do not match!")

    def __neg__(self):
        if self.is_mat():
            return self*(-1)
#________________________________________________________________________________________________END_______________________________________________________________________________________________#
#________________________________________________________________________________________________===_______________________________________________________________________________________________#


'''data = [
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
print(a + mat)
print(a + a)
print(mat.minor_of_ele_Mat(3,4))
print(mat.determinant())

data2 = [
    [2, 1, 3, 0, 4],
    [1, 0, 2, 5, 1],
    [3, 2, 1, 1, 0],
    [0, 4, 2, 1, 3],
    [5, 1, 0, 2, 2]
]
mat2 = Matrix(data2)
print(mat2)
print(mat2.rank())
print(Matrix([[1,2],[3,4]]).rank())
print(mat2.determinant_laplace())
print(mat2.determinant_gaussian())

M5 = [

    [[2, 1, 3, 0, 4],
     [1, 3, 2, 5, 1],
     [3, 2, 1, 1, 0],
     [0, 4, 2, 1, 3],
     [5, 1, 0, 2, 2]],

    [[4, 2, 0, 1, 3],
     [1, 5, 2, 0, 4],
     [3, 1, 6, 2, 0],
     [0, 2, 1, 7, 5],
     [2, 0, 4, 3, 6]],

    [[1, -2, 3, 4, 0],
     [5, 1, 0, -1, 2],
     [2, 3, 4, 0, 1],
     [0, 5, 2, 3, 4],
     [3, 0, 1, 2, 5]],

    [[0, 2, 1, 4, 3],
     [5, 0, 2, 1, 6],
     [1, 3, 0, 2, 4],
     [2, 5, 1, 0, 3],
     [4, 1, 3, 2, 0]],

    [[1, 2, 3, 4, 5],
     [2, 4, 6, 8, 10],
     [3, 6, 9, 12, 15],
     [4, 8, 12, 16, 20],
     [5, 10, 15, 20, 25]]
]
for no, i in enumerate(M5):
    print(Matrix(i).det_comp())

A = Matrix([
    ['exp(sin(90))',      "exp(sin(30))",  5],
    ["exp(cos(60))", 4,       1],
    [3,      "exp(tan(45))",  6]
])

B = Matrix([
    ["exp(cos(0))",   3,   2],
    ['exp(sin(30))',  4,   1],
    [7,               5,   "exp(cos(60))"]
])

print()
print(A)
print(B)
print()

print(A+B)
print((A+B).exp_solve())

print(A-B)
print((A-B).exp_solve())

print(A*B)
print((A*B).exp_solve())
print(A.minor_of_ele_Mat(2,3))
print(B.cofac_matrix())
print(A.determinant_gaussian(), A.determinant_laplace())
print(A.inverse() + B.cofac_matrix())
print(Matrix([[1,2],[3,4]]) * Matrix([[5,6],[7,8]]))
print(Matrix([["exp(sin(30))"]]) * Matrix([[2]]))'''
print(Matrix([
    [1, 2],
    [3, 4]
]).rank())  # 2

print(Matrix([
    [1, 2],
    [2, 4]
]).rank())  # 1

print(Matrix([
    [0, 0],
    [0, 0]
]).rank())  # 0

print(Matrix([
    [1, 0, 0],
    [0, 2, 0],
    [0, 0, 3]
]).rank())  # 3

print(Matrix([
    [1, 2, 3],
    [2, 4, 6],
    [1, 1, 1]
]).rank())  # 2

print(Matrix([
    [1, 2, 3],
    [2, 4, 6],
    [3, 6, 9]
]).rank())  # 1

print(Matrix([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]).rank())  # 0

print(Matrix([
    [1, 2, 3],
    [4, 5, 6]
]).rank())  # 2

print(Matrix([
    [1, 2, 3],
    [2, 4, 6]
]).rank())  # 1

print(Matrix([
    [1, 0],
    [0, 1],
    [1, 1]
]).rank())  # 2

print(Matrix([
    [1, 2],
    [2, 4],
    [3, 6]
]).rank())  # 1

print(Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]).rank())  # 2

print(Matrix([
    [1, 2, 3, 4],
    [2, 4, 6, 8],
    [3, 6, 9, 12]
]).rank())  # 1

print(Matrix([
    [1, 2, 3, 4],
    [0, 1, 2, 3],
    [1, 3, 5, 7]
]).rank())  # 2

print(Matrix([
    [1, 2, 3, 4],
    [2, 4, 6, 8],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
]).rank())  # 3

print(Matrix([
    [2, 1, 3, 0, 4],
    [1, 0, 2, 5, 1],
    [3, 2, 1, 1, 0],
    [0, 4, 2, 1, 3],
    [5, 1, 0, 2, 2]
]).rank())  # 5