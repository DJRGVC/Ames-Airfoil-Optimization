import sys
import subprocess
import os

def main(naca_number, mach, reynolds):
    output_dir = "../data/xfoil_dump"
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

    # Read data from the temporary file
    tmp_file_path = f"{output_dir}/polar_tmp_save_{mach}_{reynolds}.txt"
    data = ""
    try:
        with open(tmp_file_path, 'r') as tmp_file:
            data = tmp_file.read()
    finally:
        # Clean up temporary files
        os.remove(tmp_file_path)
        os.remove(f"{output_dir}/polar_tmp_dump_{mach}_{reynolds}.txt")

    print(data)  # Print the data to stdout to capture it in the main script

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_xfoil.py <naca_number> <mach> <reynolds>")
        sys.exit(1)

    naca_number = sys.argv[1]
    mach = float(sys.argv[2])
    reynolds = float(sys.argv[3])

    main(naca_number, mach, reynolds)

