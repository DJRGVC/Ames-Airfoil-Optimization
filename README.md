# Ames Airfoil Optimization Project

<p align="center">
  <img src="updates/images/NAS_logo.png" alt="NASA Logo" width="200"/>
</p>

**Author**: Daniel Grant  

**Date Begun**: October 15, 2024  

**Institution**: NASA Advanced Supercomputing, Ames Research Center  

**Advisors**: David Garcia Perez & Patricia Ventura Diaz  

**Contact**: [daniel@jrgvc.com](mailto:daniel@jrgvc.com)  


## Project Overview

The Ames Airfoil Optimization project aims to create a streamlined pipeline for optimizing airfoil design with reduced computational overhead compared to traditional high-fidelity computational fluid dynamics (CFD) simulations. The project seeks to quickly and accurately predict airfoil performance characteristics, allowing for iterative design improvements.

The workflow involves training a predictive model on XFOIL simulation data, which will serve as a performance reward for a neural network tasked with optimizing airfoil shape. By leveraging this generator, we aim to produce high-performing airfoil designs efficiently. The project’s long-term goal is to extend this 2D optimization approach to a 3D context, enabling performance evaluations and optimizations for entire wing structures.


## Recent Updates

- [Update 1: Placeholder for Future Updates](updates/reports/placeholder.md)


## Objectives

1. **Tool Development**: Develop a rapid airfoil design optimization tool to advance NASA’s mission objectives.
2. **Optimization and Performance Prediction**: Implement models that accurately and efficiently predict airfoil performance, enabling a faster design cycle.
3. **3D Expansion**: Extend the optimization framework from individual airfoils to entire wings, incorporating three-dimensional aerodynamic factors.


## Roadmap

- [x] Generate XFOIL training data for arbitrary 4- and 5-digit NACA airfoils using automated scripts.
- [] Design a reward system for airfoil optimization based on XFOIL outputs.
- [] Train neural networks on the generated data to predict airfoil performance metrics.
- [] Develop an iterative generator capable of producing optimized airfoil shapes.
- [] Scale the system to handle 3D simulations for entire wing designs.


## Tools and Technologies

- **Simulation**: XFOIL, Overflow2
- **Programming & ML**: Python, PyTorch


## Workflow

1. **Data Collection**: Gather XFOIL simulation data for a range of 4- and 5-digit NACA airfoils.
2. **Model Training**: Train machine learning models on this data to predict key performance characteristics.
3. **Reward Optimization**: Utilize the predictive model as a reward signal within a neural network, optimizing airfoil designs iteratively.
4. **Design Generation**: Implement an iterative generator to produce optimized airfoil shapes.
5. **3D Expansion**: Develop methods to evaluate and optimize entire wing structures using the established framework.


## Acknowledgments

Special thanks to Seokkwan Yoon, David Garcia Perez, Patricia Ventura Diaz, and Denis-Gabriel Caprace, all at the NASA Advanced Supercomputing Division, Ames Research Center, Mountain View, CA, for their guidance and support throughout this project.


## Contribution Guidelines

This project is currently open to collaboration. If you are interested in contributing or learning more about the project, please reach out via the contact information provided above.

