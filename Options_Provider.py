__author__ = 'joschka'

# this is a class which is supposed to deal with all the options, reading, writing, and providing them, to be specific.

import os


class OptionsProvider:
    # it loads all the options from 'options.prop' or creates the file if it dosen't exist.
    def __init__(self):
        self.options = []
        self.values = []
        if os.path.isfile('options.prop'):
            file = open('options.prop', 'r')
            for line in file.read().splitlines():
                if '#' != line[0]:
                    j = line.split(' = ')
                    self.options.append(j[1])
                    if j[0] == 's':
                        self.values.append(j[2])
                    elif j[0] == 'i':
                        self.values.append(int(j[2]))
                    elif j[0] == 'b':
                        if j[2] == 'True':
                            self.values.append(True)
                        elif j[2] == 'False':
                            self.values.append(False)
                        else:
                            del self.options[-1]
                            print('option.prop seems to be corrupt skipping...')
                    elif j[0] == 'l':
                        self.values.append(j[2].split(','))
            file.close()
        #print(self.options)
        #print(self.values)

    # creates new options or passes if the option already exists
    def new_option(self, name, value):
        if name not in self.options:
            self.options.append(name)
            self.values.append(value)

    def get(self, name):
        return self.values[self.options.index(name)]

    def set(self, name, value):
        self.values[self.options.index(name)] = value

    # writes 'options.prop' on closing of the program
    def __del__(self):
        file = open('options.prop', 'w')
        file.write('#Options for jajo_11 Schematic to java converter\n'
                        '#first char is the type after a \' = \' is the name and after that the value\n'
                        '#"s" = string, "i" = int, "b" = boolean, "l" = list of strings\n')
        for option in self.options:
            index = self.options.index(option)
            if type(self.values[index]) is str:
                file.write('s = ' + option + ' = ' + self.values[index] + '\n')
            elif type(self.values[index]) is int:
                file.write('i = ' + option + ' = ' + str(self.values[index]) + '\n')
            elif type(self.values[index]) is bool:
                file.write('b = ' + option + ' = ' + str(self.values[index]) + '\n')
            elif type(self.values[index]) is list:
                j = ''
                for i in self.values[index]:
                    j = j + i + ','
                j = j[:-1]
                file.write('l = ' + option + ' = ' + j + '\n')
        file.close()