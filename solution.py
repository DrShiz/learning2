from tempfile import gettempdir
import os
path_myfile1 = 'myfile.txt'


class File:

    def __init__(self, path_file):
        self.path_file = path_file
        if not os.path.exists(self.path_file):
            with open(self.path_file, 'w') as f:
                pass

    def __str__(self):
        return self.path_file

    def read(self):
        with open(self.path_file, 'r') as f:
            if f.read() != '':
                with open(self.path_file, 'r') as f:
                    return print(str(f.read()))
            else:
                return ''

    def write(self, data):
        with open(self.path_file, 'w') as f:
            f.write(data)

    def __iter__(self):
        self.i = 0
        with open(self.path_file, 'r') as f:
            self.count_lines = sum(1 for line in f)
        return self

    def __next__(self):
        if self.i < self.count_lines:
            with open(self.path_file, 'r') as f:
                line = f.readlines()[self.i]
                self.i += 1
            return line
        else:
            raise StopIteration

    def __add__(self, other):
        with open(self.path_file, 'r') as f:
            data1 = f.read()
        with open(other.path_file, 'r') as f:
            data2 = f.read()
        data3 = data1 + data2
        result = File(os.path.join(gettempdir(), 'temp_file.txt'))
        with open(result.path_file, 'w') as f:
            f.write(data3)
        return result


# print(path.exists(path_myfile1))
myfile1 = File(path_myfile1  + '_3')
# # print(myfile1)
# # print(path.exists(path_myfile1))
myfile2 = File(path_myfile1  + '_2')
# myfile1.write('Hello\nPrivet\n')
myfile1.read()
print()
myfile1.write('a\n')
myfile2.write('b\nc')
myfile2.read()
print()
myfile3 = myfile1 + myfile2
# myfile3.read()
# for line in myfile3:
#     print(line.strip('\n'))
# # myfile2.read()
# # myfile1.read()
for line in myfile3:
    print(ascii(line))
