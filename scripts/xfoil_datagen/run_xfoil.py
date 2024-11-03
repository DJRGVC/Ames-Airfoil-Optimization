import sys
import subprocess
import os
from multiprocessing import Pool

def run_xfoil(params):
    naca_number, mach, reynolds = params
    output_dir = "../data/xfoil_dump"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

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
        {output_dir}/polar_tmp_save_{mach}_{reynolds}.txt
        {output_dir}/polar_tmp_dump_{mach}_{reynolds}.txt
        aseq -20 20 1

        quit
    """

    # Run XFOIL with the specified commands
    process = subprocess.Popen(['xfoil'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate(xfoil_cmds.encode())

    # Log the output and errors
    print(output.decode())  # Print standard output
    if errors:
        print(f"XFOIL error for Mach {mach}, Reynolds {reynolds}:\n{errors.decode()}")

    # Read data from the temporary file
    tmp_file_path = f"{output_dir}/polar_tmp_save_{mach}_{reynolds}.txt"
    data = ""
    try:
        with open(tmp_file_path, 'r') as tmp_file:
            data = tmp_file.read()
    except FileNotFoundError:
        print(f"Error: The expected file {tmp_file_path} was not created.")
    finally:
        # Clean up temporary files if they exist
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if os.path.exists(f"{output_dir}/polar_tmp_dump_{mach}_{reynolds}.txt"):
            os.remove(f"{output_dir}/polar_tmp_dump_{mach}_{reynolds}.txt")

    return data

def main(naca_number):
    # Define Mach and Reynolds values
    mach_values = [0.25, 0.35, 0.45, 0.55, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
    reynolds_values = [75000, 125000, 250000, 500000, 1000000, 2000000, 4000000, 8000000]

    # Prepare parameter list for all combinations of Mach and Reynolds numbers
    params_list = [(naca_number, m, r) for m in mach_values for r in reynolds_values]

    # Use Pool to parallelize XFOIL simulations
    with Pool() as pool:
        results = pool.map(run_xfoil, params_list)

    # Write all results to the output file once pooling completes
    output_file = os.path.join("../data/xfoil_dump", f"polar_{naca_number}.txt")
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result)
            file.write("\n")

    print(f"Polar data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_xfoil.py <naca_number>")
        sys.exit(1)

    naca_number = sys.argv[1]
    main(naca_number)

