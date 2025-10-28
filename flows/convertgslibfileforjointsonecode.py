
# This file is your entry point:
# - add you Python files and folder inside this 'flows' folder
# - add your imports
# - just don't change the name of the function 'run()' nor this filename ('convertgslibfileforjointsonecode.py')
#   and everything is gonna be ok.
#
# Remember: everything is gonna be ok in the end: if it's not ok, it's not the end.
# Alternatively, ask for help at https://github.com/deeplime-io/onecode/issues

import onecode

def modify_gslib(input_file, output_file, i_offset=0, j_offset=0, k_offset=0,
                 dip_angle=0.0, strike_angle=0.0, KN=8000000, KS=4000000):
    """
    Modify a gslib file by:
    - Adding offsets to i_index, j_index, k_index
    - Keeping x_coord, y_coord, z_coord unchanged
    - Removing extra columns
    - Adding 4 new columns: dip_angle, strike_angle, KN, KS

    Parameters:
    -----------
    input_file : str
        Path to the input gslib file
    output_file : str
        Path to the output gslib file
    i_offset : int
        Constant to add to i_index
    j_offset : int
        Constant to add to j_index
    k_offset : int
        Constant to add to k_index
    dip_angle : float or list
        Constant value(s) for dip_angle column
    strike_angle : float or list
        Constant value(s) for strike_angle column
    KN : int or list
        Constant value(s) for KN column
    KS : int or list
        Constant value(s) for KS column
    """

    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Read header information
    title = lines[0].strip()
    num_variables_old = int(lines[1].strip())

    # New number of variables (3 indices + 3 coords + 4 new columns = 10)
    num_variables_new = 10

    # Read data (skip title, num_variables, and variable names)
    data_start = 2 + num_variables_old
    data_lines = [line.strip() for line in lines[data_start:] if line.strip()]

    # Write modified file
    with open(output_file, 'w') as f:
        # Write header
        f.write(f"{title}\n")
        f.write(f"{num_variables_new}\n")

        # Write new variable names
        f.write("i_index\n")
        f.write("j_index\n")
        f.write("k_index\n")
        f.write("x_coord\n")
        f.write("y_coord\n")
        f.write("z_coord\n")
        f.write("dip_angle\n")
        f.write("strike_angle\n")
        f.write("KN\n")
        f.write("KS\n")

        # Process and write data
        for idx, data_line in enumerate(data_lines):
            values = data_line.split()

            # Parse original values
            i_index = int(values[0]) + i_offset
            j_index = int(values[1]) + j_offset
            k_index = int(values[2]) + k_offset
            x_coord = float(values[3])
            y_coord = float(values[4])
            z_coord = float(values[5])
            # values[6] is P-Velocity - we skip it

            # Get new column values (can be constant or vary per row)
            dip = dip_angle[idx] if isinstance(dip_angle, list) else dip_angle
            strike = strike_angle[idx] if isinstance(strike_angle, list) else strike_angle
            kn = KN[idx] if isinstance(KN, list) else KN
            ks = KS[idx] if isinstance(KS, list) else KS

            # Write modified data line with proper formatting
            f.write(f"{int(i_index):6d} {int(j_index):6d} {int(k_index):6d} "
                    f"{x_coord:18.7f} {y_coord:18.7f} {z_coord:18.7f} "
                    f"{dip:13.7f} {strike:13.7f} "
                    f"{kn:14.0f} {ks:14.0f}\n")

def run():
    my_input_file = onecode.file_input(
        key="input_gslib_file",
        value="*.gslib",
        label="Select a GSLib file",
        types=[onecode.FileFilter.CSV])

    modify_gslib(my_input_file,
                 'C:\\Users\\phili\\OneDrive - Ephesia Consult\\Downloads\\output.gslib',
                 i_offset=55,
                 j_offset=94,
                 k_offset=137,
                 dip_angle=65.0,
                 strike_angle=45.0,
                 KN=8000000,
                 KS=4000000)
