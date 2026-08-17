class Matrix:

    def __init__(self, data): #accepts a nested list
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