

import subprocess
from XfoilOutputParser import XParser

# Define the Mach numbers, Reynolds numbers, and Angles of Attack as per the provided table
mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]
aoa_values = list(range(-20, 21))

# Request NACA airfoil number from user
naca_number = input("Enter the NACA airfoil number (e.g., '2412'): ")

# Output file for polar data
output_file = f"../data/xfoil_dump/polar_{naca_number}.txt"

# Create and open a file to store the polar data
with open(output_file, 'w') as file:
    # Loop over Mach, Reynolds number, and angle-of-attack ranges
    for mach in mach_values:
        for reynolds in reynolds_values:
            # Prepare commands for XFOIL
            xfoil_cmds = f"""
                NACA {naca_number}
                oper
                iter 200
                Mach {mach}
                visc {reynolds}
                PACC
                ../data/xfoil_dump/polar_tmp_save.txt
                ../data/xfoil_dump/polar_tmp_dump.txt
                ASEQ -20 20 1

                quit

                """
            # Run XFOIL with the specified commands
            process = subprocess.Popen(['xfoil'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate(xfoil_cmds.encode())
            
            # Append output to the main file
            with open("../data/xfoil_dump/polar_tmp_save.txt", 'r') as tmp_file:
                file.write(tmp_file.read())
            file.write("\n")


            # remove tmp files
            subprocess.run(['rm', '../data/xfoil_dump/polar_tmp_save.txt'])
            subprocess.run(['rm', '../data/xfoil_dump/polar_tmp_dump.txt'])

XParser.parse_xfoil_file(naca_number, f"../data/xfoil_dump/polar_{naca_number}.txt")
print(f"Polar data saved to {output_file}")


