# This file is your entry point:
# - add you Python files and folder inside this 'flows' folder
# - add your imports
# - just don't change the name of the function 'run()' nor this filename ('convertgslibfileforjointsonecode.py')
#   and everything is gonna be ok.
#
# Remember: everything is gonna be ok in the end: if it's not ok, it's not the end.
# Alternatively, ask for help at https://github.com/deeplime-io/onecode/issues

import onecode

from flows.plot_3d_scatter import plot_3d_scatter


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

    # Create lists to store coordinates and color values
    x_coords = []
    y_coords = []
    z_coords = []
    color_values = []

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
            # Store coordinates and color value
            x_coords.append(x_coord)
            y_coords.append(y_coord)
            z_coords.append(z_coord)
            color_values.append(values[6])

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

        # Call the plotting function
        plot_3d_scatter(x_coords, y_coords, z_coords, color_values,
                        title='3D Point Cloud - Color Coded by P-Velocity',
                        color_label='P-Velocity',
                        cmap='viridis',
                        point_size=50,
                        alpha=0.6)


def run():
    my_input_file = onecode.file_input(
        key="input_gslib_file",
        value="input.gslib",
        label="Select a GSLib file",
        types=[("GSLib", ".gslib")])
    my_output_file = onecode.file_output(
        key="output_gslib_file",
        value="output.gslib",
        make_path=True)
    my_i_offset = onecode.number_input(key="i_offset", value=0, label="I offset", min=0, max=None, step=1)
    my_j_offset = onecode.number_input(key="j_offset", value=0, label="J offset", min=0, max=None, step=1)
    my_k_offset = onecode.number_input(key="k_offset", value=0, label="K offset", min=0, max=None, step=1)
    my_dip_angle = onecode.slider(key="dip_angle", value=0, label="Dip angle", min=0, max=90, step=0.1)
    my_strike_angle = onecode.slider(key="strike_angle", value=0, label="Strike angle", min=0, max=360, step=0.1)
    my_kn = onecode.number_input(key="KN", value=8000000, label="KN", min=0, max=None, step=0.1)
    my_ks = onecode.number_input(key="KS", value=4000000, label="KS", min=0, max=None, step=0.1)

    modify_gslib(my_input_file, my_output_file,
                 my_i_offset, my_j_offset, my_k_offset,
                 my_dip_angle, my_strike_angle, my_kn, my_ks)
