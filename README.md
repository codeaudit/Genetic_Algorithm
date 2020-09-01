# Genetic Algorthim
A simple evolutionary-genetic algorithm (Simultaneous update of all the weights) implemented both in python and C++.
The algorithm is very simple conceptually. it competes between two networks: father (f) & child (c) network and simultaneously mutates all the weights of the child network then chooses the better network to become the father of the next generation. For low dimensional data, this algorithm can be as efficient as naive gradient decent and that is because it doesn't require the backward pass (back-propagtion), instead it requires 2 forward passes (which are less intensive computationally than the backward pass). Also, if the loss function is not convex or the local minima hides in a narrow and elongated ridge, then this algorithm can be more efficient than the naive gradient decent which produces a zigzagged path towards the minima.

For a detailed comparision between this GA method vs SGD methods please refer to this article:
https://

**Files:**
*very_simple_GA.py:* This file contains a very simple GA implemenation using numpy (few lines of code). It solves the XOR problem.
*Solve_Xor_and_Cartople.py:* This file implements GA from scratch using object oriented principles which give more flexibility to structure the network and It has been showcased to solve clasififcation problems (Xor) and reinforcement learning (Cartople) using the same code base.
*Solve_Xor.cpp:* a C++ implentation of the same code.



visit us at: https://www.brainxyz.com/ 
License: MIT
