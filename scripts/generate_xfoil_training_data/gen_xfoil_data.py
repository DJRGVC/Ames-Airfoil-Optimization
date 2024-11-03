import subprocess
from XfoilOutputParser import XParser
from tqdm import tqdm

# Define the Mach numbers, Reynolds numbers, and Angles of Attack as per the provided table
mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]
aoa_values = list(range(-20, 21))

# Request NACA airfoil number from user
naca_number = input("Enter the NACA airfoil number (e.g., '2412'): ")

# Output file for polar data
output_file = f"../../data/xfoil_dump/polar_{naca_number}.txt"

# Create and open a file to store the polar data
with open(output_file, 'w') as file:
    # Total number of iterations for progress tracking
    total_iterations = len(mach_values) * len(reynolds_values)
    
    # Loop over Mach and Reynolds number values with a progress bar
    with tqdm(total=total_iterations, desc="Processing XFOIL Simulations") as pbar:
        for mach in mach_values:
            for reynolds in reynolds_values:
                # Prepare commands for XFOIL
                xfoil_cmds = f"""
                    naca {naca_number}
                    pane
                    ppar
                    n 100
                    p 0.75



                    oper
                    iter 600
                    mach {mach}
                    visc {reynolds}
                    pacc
                    ../../data/xfoil_dump/polar_tmp_save.txt
                    ../../data/xfoil_dump/polar_tmp_dump.txt
                    aseq -20 20 1

                    quit

                """
                
                # Run XFOIL with the specified commands
                process = subprocess.Popen(['xfoil'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, errors = process.communicate(xfoil_cmds.encode())
                
                # Append output to the main file
                with open("../../data/xfoil_dump/polar_tmp_save.txt", 'r') as tmp_file:
                    file.write(tmp_file.read())
                file.write("\n")
                
                # Remove tmp files
                subprocess.run(['rm', '../../data/xfoil_dump/polar_tmp_save.txt'])
                subprocess.run(['rm', '../../data/xfoil_dump/polar_tmp_dump.txt'])
                
                # Update progress bar
                pbar.update(1)

# Parse the final polar file
XParser.parse_xfoil_file(naca_number, f"../../data/xfoil_dump/polar_{naca_number}.txt")
print(f"Polar data saved to {output_file}")

