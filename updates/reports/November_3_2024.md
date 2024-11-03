# Update 1: XFOIL Optimization Progress

**Date**: November 3, 2024  
**Author**: Daniel Grant  
**Institution**: NASA Advanced Supercomputing, Ames Research Center  

## Summary

This week, I successfully got XFOIL running on my Mac and compiled a CSV with the airfoil parameters from the Cornelius paper for simulation. I created a script to compile XFOIL output into a single text file based on the input NACA number (e.g., 3415), followed by another script to parse this output into a CSV format for training purposes.

I am currently facing challenges with XFOIL parameters and convergence issues at high Mach and Reynolds number configurations.

## XFOIL Configuration Details

Here are the input settings used for XFOIL, with varying Mach and Reynolds numbers for each run. Comments have been added for clarity:

```bash
naca {naca_number}
 pane # Activates the paneled surface representation of the airfoil, creating a boundary outline for simulation.
 ppar
 n 100 # Sets the number of panels (surface points) along the airfoil to 100
 p 0.5 # Sets the leading edge panel density factor to 0.5. (.5 -> more refinement along tail)

 oper
 iter 600 # Specifies a maximum of 600 iterations for the XFOIL solver to converge to a solution
 mach {mach}
 visc {reynolds}
 pacc
 ../data/xfoil_dump/polar_tmp_save.txt
 ../data/xfoil_dump/polar_tmp_dump.txt
 aseq -20 20 1 # variation of aoa from -20 to 20 by increments of 1

 quit
```


Despite various attempts to adjust the number of panels and density settings, I have not yet found a configuration that consistently works across all parameters.

## Future Work

I plan to develop a script to check the validity of the converged solutions, as XFOIL sometimes reports inaccurate drag coefficients (e.g., 1e15). Additionally, I am considering a script that identifies the best settings for a range of input parameters. 

## Literature Review

I have not yet conducted a thorough literature review of similar work, as my focus has been on generating the training data with XFOIL. I will prioritize this following an initial training phase with the XFOIL data once I have a more stable configuration.

## Additional Notes

Once I have my NASA device activated, I would like to start running OVERFLOW simulations for the NACA 3415 airfoil to compare with my XFOIL simulation data.

## Images

![XFOIL Optimization Data 1](../images/xfoil_output_1.png)
![XFOIL Optimization Data 2](../images/xfoil_output_2.png)

## Video

[View XFOIL Simulation Video](../videos/xfoil_simulation.mp4)


