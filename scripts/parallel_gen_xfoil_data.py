import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from XfoilOutputParser import XParser
from tqdm import tqdm

# Define the Mach numbers, Reynolds numbers, and Angles of Attack as per the provided table
mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]
aoa_values = list(range(-20, 21))

# Request NACA airfoil number once in the main process
naca_number = input("Enter the NACA airfoil number (e.g., '2412'): ")

# Output file for polar data
output_file = f"../data/xfoil_dump/polar_{naca_number}.txt"

# Function to run XFOIL for a specific Mach and Reynolds number
def run_xfoil(mach, reynolds, naca_number):
    # Prepare commands for XFOIL
    xfoil_cmds = f"""
        naca {naca_number}
        ppar
        n 160
        t 2

        oper
        iter 600
        mach {mach}
        visc {reynolds}
        pacc
        ../data/xfoil_dump/polar_tmp_save_{mach}_{reynolds}.txt
        ../data/xfoil_dump/polar_tmp_dump_{mach}_{reynolds}.txt
        aseq -20 20 1

        quit
    """
    
    # Run XFOIL with the specified commands
    process = subprocess.Popen(['xfoil'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate(xfoil_cmds.encode())
    
    # Read and return the data from the temporary output file
    tmp_file_path = f"../data/xfoil_dump/polar_tmp_save_{mach}_{reynolds}.txt"
    with open(tmp_file_path, 'r') as tmp_file:
        data = tmp_file.read()

    # Clean up temporary files
    os.remove(tmp_file_path)
    os.remove(f"../data/xfoil_dump/polar_tmp_dump_{mach}_{reynolds}.txt")

    return data

# Create the output directory if it does not exist
os.makedirs("../data/xfoil_dump", exist_ok=True)

# Parallel processing with ProcessPoolExecutor
with open(output_file, 'w') as file, ProcessPoolExecutor() as executor:
    futures = [
        executor.submit(run_xfoil, mach, reynolds, naca_number)
        for mach in mach_values
        for reynolds in reynolds_values
    ]
    
    # Using tqdm to track progress of completed tasks
    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing XFOIL Simulations"):
        # Write the results of each future as it completes
        file.write(future.result())
        file.write("\n")

# Parse the final polar file
XParser.parse_xfoil_file(naca_number, output_file)
print(f"Polar data saved to {output_file}")

