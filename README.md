# Vision-Based Autonomous Path Tracking of a Mobile Robot using Fuzzy Logic

This repository contains the implementation of a vision-based autonomous path tracking system for a mobile robot using fuzzy logic. The project originated from our 2023 seminar, where we proposed and implemented a novel approach to track straight and curved paths in the environment.

## Abstract

In this work, we present an algorithm for autonomous path tracking of a mobile robot, aiming to follow both straight and curved paths within its environment. The algorithm employs a fuzzy logic-based approach to emulate human driving behavior in the mobile robot. It integrates a fuzzy steering controller responsible for controlling the steering angle and a fuzzy velocity controller regulating the forward linear velocity, ensuring safe path tracking.

The inputs to the fuzzy system are provided by the vision system of the mobile robot, which utilizes a camera to capture images of the path ahead. The vision system calculates the lateral offset, heading error, and path curvature. Experimental validation was conducted using a mobile robot platform (in the previous work) whilst we did it using Gazebo and ROS Noetic (videos haven't been uploaded yet). The robot successfully tracked straight paths in the initial experiment, demonstrating the efficacy of the fuzzy steering controller. Furthermore, experiments on paths with curved sections showcased the ability of the fuzzy velocity controller to adjust the speed for safe path tracking.

Additionally, we plan to enhance the visual system's robustness by implementing a deep learning approach based on image processing techniques (probably a Deep Reinforcement Learning Approach Given the Simulation environment that we used). This extension aims to improve the system's performance and adaptability in diverse environments.

The original work was inspired by a research paper ([link to the paper](https://ieeexplore.ieee.org/document/7053862)) and was reimplemented in Python and Gazebo. It is noteworthy that our project was recognized as the best seminar project among our peers.

<!--## Project Structure

- `src/`: Contains the source code for the autonomous path tracking system.
- `docs/`: Documentation related to the project, including technical specifications and guides.
- `data/`: Data files and datasets used in the experiments.
- `examples/`: Example scripts and notebooks demonstrating the usage of the system.

## How to Use

Detailed instructions on setting up and running the system can be found in the `docs/` directory.-->
## Environment
We present first the environment that we created on Gazebo to have some accurate representations for the simulation.


## Acknowledgments

We acknowledge the original research team for their pioneering work and inspiration for this project. This project was mainly a recreation of their work as our contribution was mainly in creating the simulation on ROS and Gazebo.

## Contact Information

For inquiries or collaboration opportunities, please contact:
- [Said GUERAZEM](mailto:said.guerazem@g.enp.edu.dz)
- [Zakaria Fakhri SASSI](mailto:zakaria_fakhri.sassi@g.enp.edu.dz )

