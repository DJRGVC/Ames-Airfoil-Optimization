import os
import subprocess
from multiprocessing import Pool
from XfoilOutputParser import XParser

# Define Mach, Reynolds, and AoA values
mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]
aoa_values = list(range(-20, 21))

# Request NACA number once
naca_number = input("Enter the NACA airfoil number (e.g., '2412'): ")

# Ensure output directory exists
output_dir = "../data/xfoil_dump"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"polar_{naca_number}.txt")

# Function to run XFOIL for a specific Mach and Reynolds number
def run_xfoil(params):
    mach, reynolds = params
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
        {output_dir}/polar_tmp_save_{mach}_{reynolds}.txt
        {output_dir}/polar_tmp_dump_{mach}_{reynolds}.txt
        aseq -20 20 1

        quit
    """
    
    # Run XFOIL with the specified commands
    process = subprocess.Popen(['xfoil'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate(xfoil_cmds.encode())
    
    # Read data from the temporary file
    tmp_file_path = f"{output_dir}/polar_tmp_save_{mach}_{reynolds}.txt"
    try:
        with open(tmp_file_path, 'r') as tmp_file:
            data = tmp_file.read()
    finally:
        # Clean up temporary files
        os.remove(tmp_file_path)
        os.remove(f"{output_dir}/polar_tmp_dump_{mach}_{reynolds}.txt")

    return data

# Run simulations in parallel and gather results
params_list = [(mach, reynolds) for mach in mach_values for reynolds in reynolds_values]

# Use Pool to parallelize XFOIL simulations
with Pool() as pool:
    results = pool.map(run_xfoil, params_list)

# Write all results to the output file once pooling completes
with open(output_file, 'w') as file:
    for result in results:
        file.write(result)
        file.write("\n")

# Parse the final polar file
XParser.parse_xfoil_file(naca_number, output_file)
print(f"Polar data saved to {output_file}")

