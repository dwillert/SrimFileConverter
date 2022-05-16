
def unit_removal(unit):
    pass

def ion_energy_conv(prefix: (str), value, line: (str)) -> str:
    unit = '{}eV'.format(prefix)
    print(unit)
    if unit != 'keV':
        conv_value = unit_conversion(prefix, value)
        line = line.replace(" "+value, str(conv_value))
    new_line = line.replace(unit, '    ')
    return new_line

def unit_conversion(prefix, value):
    print(value)
    print(type(value))
    float_value = round(float(value), 2)
    if prefix == 'M':
        conv_value = float_value * 1000
    return conv_value

def file_helper(line: (str)) -> str:
    line = str(line)
    finder = line.find("eV")
    if finder != -1:
        splitter = line[finder]
        splitter_list = line.split(splitter)
        splitter_str= splitter_list[0]
        unit_split = splitter_str.split(" ")
        print(unit_split)
        prefix = unit_split[-1]
        value = unit_split[-2]
        print(prefix, value)
        new_line = ion_energy_conv(prefix, value, line)
        return new_line
    else:
        print("Not Present")
        return line


def table_check(line, transform):
    print(line)
    starter = "--------------  ---------- ---------- ----------  ----------  ----------"
    end = "-----------------------------------------------------------"
    if starter in line:
        transform = True
    elif end in line:
        transform = False
    return transform

def save_file(new_line):
    with open('output_files/output.txt', 'a') as f:
        f.write(new_line)

def read_file():
    with open('./srim_files/Hydrogen_in_Copper.txt') as f:
        lines = f.readlines()
    transform = False
    for line in lines:
        transform = table_check(line, transform)
        print(transform)
        if transform:
            new_line = file_helper(line)
            save_file(new_line)
        else:
            save_file(line)

        # ion_energy_conv('', line)
        # print(line)

    
if __name__ == '__main__':
    read_file()
    print("DONE")