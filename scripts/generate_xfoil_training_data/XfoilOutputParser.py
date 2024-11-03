import os
import re
from tqdm import tqdm

class XParser:
    @staticmethod
    def parse_xfoil_file(naca_number, input_file, output_dir="../../data/airfoil_training_data"):
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Read the file content
        with open(input_file, "r") as file:
            lines = file.readlines()
        
        # Set up patterns to match relevant data lines
        data_pattern = re.compile(r"(-?\d+\.\d{3,4})\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)")
        meta_pattern = re.compile(r"Mach\s+=\s+(\d+\.\d+)\s+Re\s+=\s+(\d+\.\d+)\s+e\s+6")
        results = []
        mach_number, reynolds_number = None, None
        
        # Parse file lines with progress bar
        for line in tqdm(lines, desc="Parsing XFOIL Data"):
            # Check for Mach and Reynolds number information
            if "Mach =" in line:
                meta_match = meta_pattern.search(line)
                if meta_match:
                    mach_number = float(meta_match.group(1))
                    reynolds_number = float(meta_match.group(2)) * 1e6
            
            # Extract alpha, CL, CD, and CM values from data lines
            data_match = data_pattern.search(line)
            if data_match and mach_number is not None and reynolds_number is not None:
                alpha = float(data_match.group(1))
                cl = float(data_match.group(2))
                cd = float(data_match.group(3))
                cm = float(data_match.group(5))
                results.append((mach_number, reynolds_number, alpha, cl, cd, cm))
        
        # Write output file in the specified format
        output_file = os.path.join(output_dir, f"{naca_number}.csv")
        with open(output_file, "w") as outfile:
            # Write header
            outfile.write("Mach Number,Reynolds Number,Angle of Attack,CL,CD,CM\n")
            for result in results:
                outfile.write(",".join(map(str, result)) + "\n")
        
        print(f"Data has been successfully saved to {output_file}")

