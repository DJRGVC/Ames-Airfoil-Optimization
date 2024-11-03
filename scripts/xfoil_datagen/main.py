import os
import subprocess

# Define Mach and Reynolds values
mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]

# Request NACA number from the user
naca_number = input("Enter the NACA airfoil number (e.g., '2412'): ")

# Prepare the command to run the XFOIL execution script
command = ['python3', 'run_xfoil.py', naca_number] + [str(m) + ',' + str(r) for m in mach_values for r in reynolds_values]

# Ensure the output directory exists
output_dir = "../data/xfoil_dump"
os.makedirs(output_dir, exist_ok=True)

# Execute the XFOIL script
subprocess.run(command)

