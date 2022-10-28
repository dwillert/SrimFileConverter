from types import DynamicClassAttribute
import pandas as pd
import re
import argparse

def unit_removal(unit):
    pass

def angstrom_conv(prefix: (str), value: (int), line: (str)) -> str:
    print("1: ",value)
    unit = 'A'
    conv_value = float(value) * 10000
    print("2: ", conv_value)

    line = line.replace(" "+value, str(conv_value))
    new_line = line.replace(unit, '    ')
    return new_line

def meter_conv(prefix: (str), value: (int), line: (str)) -> str:
    unit = '{}m'.format(prefix)
    print(unit)
    conv_value = unit_conversion(prefix, value)
    line = line.replace(" "+value, str(conv_value))
    new_line = line.replace(unit, '    ')
    return new_line

def ion_energy_conv(prefix: (str), value: (int), line: (str), conv_value: (int)) -> str:
    unit = '{}eV'.format(prefix)
    print(unit)
    line = line.replace(" "+value, str(conv_value))
    new_line = line.replace(unit, '    ')
    return new_line

def create_csv(data_obj: (list)) -> None:
    del data_obj[0]
    df = pd.DataFrame.from_dict(data_obj)
    df.to_csv("./output_files/output.csv", index=False)

def unit_conversion(prefix, value, desired_prefix):
    '''
    create dict of conversion values and loop
    '''

    metric_conv = {
        "G": 1000000000,
        "M": 1000000,
        "k": 1000,
        "d": .1,
        "c": .01,
        "m": .001,
        "u": .000001,
        "n": .000000001,
        "p": .000000000001
    }
    print("PREFIX: ", desired_prefix)
    print(value)
    print(type(prefix))
    float_value = round(float(value), 2)

    
    if prefix and desired_prefix in metric_conv:
        conv_value = float_value * metric_conv[prefix] / metric_conv[desired_prefix]
    elif prefix in metric_conv and desired_prefix == "":
        conv_value = float_value * metric_conv[prefix]
    elif desired_prefix in metric_conv and prefix == "":
        conv_value = float_value / metric_conv[desired_prefix]
    else:
        print("SI UNIT {}: Not Available".format(prefix))
        conv_value = "N/A"
    return conv_value

def unit_manager(prefix, unit, value, desired_unit):
    if unit == "eV":
        actual_unit = "{}{}".format(prefix, unit)
        if actual_unit != desired_unit["ion_energy"]:
            desired_prefix = desired_unit["ion_energy"].replace("eV", "")
            converted_value = unit_conversion(prefix, value, desired_prefix)
            return converted_value
    if unit == "A":




def file_helper(line: (str), desired_unit_dict: (dict)) -> str:
    line = str(line)
    print("START LINE: ", line)
    unit_map = ["eV", "m", "mm", "A"] 
    for unit in unit_map:
        print("UNIT: ", unit)
        finder = line.find(unit)
        if finder != -1:
            if unit == "m" and (line[finder + 1]) == "m":
                unit = "mm"
                finder +=1
            splitter = line[finder]
            splitter_list = line.split(splitter)
            splitter_str= splitter_list[0]
            unit_split = splitter_str.split(" ")
            prefix = unit_split[-1]
            value = unit_split[-2]
            conv_value = unit_manager(prefix, unit, value, desired_unit_dict)
            if unit == "eV":
                line = ion_energy_conv(prefix, value, line, conv_value)
            elif unit == "A" and desired_unit_dict[]:
                line = angstrom_conv(prefix, value, line, desired_unit)
            # elif unit == "m":
            #     line = meter_conv(prefix, value, line, desired_unit)    
            # elif unit == "mm":
            #     prefix = "m"
            #     line = meter_conv(prefix, value, line, desired_unit)  
            # else:
            #     print("Unexpected Unit") 
        else:
            print("Not Present")
    print("NEW LINE: ", line)
    value_list = data_dict(line, desired_unit_dict)
    print('VALUES:', value_list)

    return line, value_list

def data_dict(line: (str), desired_unit: (dict)) -> list:
    value_list = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
    data_dict = {}
    try:
        data_dict = {
        "Ion Energy ({})".format(desired_unit_dict["ion_energy"]): value_list[0], 
        "dE/dx Elec.": value_list[1], 
        "dE/dx Nuclear": value_list[2], 
        "Projected Range ({})".format(desired_unit_dict["pro_range"]): value_list[3], 
        "Longitudinal Straggling ({})".format(desired_unit_dict["long_strag"]): value_list[4], 
        "Lateral Straggling ({})".format(desired_unit_dict["lat_strag"]): value_list[5]
        }
    except:
        print(line)
    print(data_dict)
    return data_dict

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
    with open('output_files/output.txt', 'a+') as f:
        f.write(new_line)

def read_file(desired_unit_dict):
    with open('./srim_files/Hydrogen_in_Copper.txt') as f:
        lines = f.readlines()
    transform = False
    data_obj = []
    for line in lines:
        transform = table_check(line, transform)
        print(transform)
        if transform:
            new_line, data_dict = file_helper(line, desired_unit_dict)
            save_file(new_line)
            data_obj.append(data_dict)
        else:
            save_file(line)

        # ion_energy_conv('', line)
        # print(line)
    print("DATA: ", data_obj)
    create_csv(data_obj)

def desired_units():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ion", "--ion_energy_unit", dest="ion_unit", default= "keV", help="Ion Energy Desired Unit - Default: keV")
    parser.add_argument("-pr", "--projected_range_unit", dest="pr_unit", default= "um", help="Projected Range Desired Unit - Default: um")
    parser.add_argument("-long", "--longitudinal_straggling_unit", dest="long_unit", default= "um", help="Longitudinal Straggling Desired Unit - Default: um")
    parser.add_argument("-lat", "--lateral_straggling_unit", dest="lat_unit", default= "um",help="Lateral Straggling Desired Unit - Default: um")
    units = parser.parse_args()
    print("Standardized Units: Ion Energy: {}, Projected Range: {}, Longitudinal Straggling: {}, Lateral Straggling: {}".format(units.ion_unit, units.pr_unit, units.long_unit, units.lat_unit))
    return units.ion_unit.strip(), units.pr_unit.strip(), units.long_unit.strip(), units.lat_unit.strip()

if __name__ == '__main__':
    ion_unit, pr_unit, long_unit, lat_unit = desired_units()
    print(ion_unit, pr_unit, long_unit, lat_unit)
    desired_unit_dict = {"ion_energy": ion_unit, "pro_range": pr_unit, "lat_strag": long_unit, "long_strag": lat_unit}
    print(desired_unit_dict)
    read_file(desired_unit_dict)
    print("DONE")