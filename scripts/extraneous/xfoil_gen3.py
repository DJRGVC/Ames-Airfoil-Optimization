import os
import subprocess
from multiprocessing import Pool
from XfoilOutputParser import XParser

# Define Mach and Reynolds values
mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]

# Request NACA number once
naca_number = input("Enter the NACA airfoil number (e.g., '2412'): ")

# Ensure output directory exists
output_dir = "../data/xfoil_dump"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"polar_{naca_number}.txt")

# Function to run XFOIL for a specific Mach and Reynolds number
def run_xfoil(params):
    mach, reynolds = params
    cmd = ['python3', 'run_xfoil.py', naca_number, str(mach), str(reynolds)]
    output = subprocess.check_output(cmd, text=True)
    return output

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

