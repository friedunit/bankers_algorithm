# This is a Python script for implementing the Banker's Algorithm for resource allocation and deadlock avoidance. It was originally written in Java for my Operating Systems class, but I wanted to convert it to Python for practice.

The program asks for a filename where the format is:
resources m, processes n
total number of resource units
next n lines, resource needs for each process
next n lines, resources allocated to each process
Example:
5,7
8,6,9,5,7
1,2,1,2,1
2,0,1,0,2
0,0,1,0,1
1,2,1,2,0
2,0,1,0,1
1,1,0,1,2
2,3,2,2,1
2,1,0,1,0
0,2,3,1,1
1,0,2,0,1
1,0,1,0,1
0,0,1,0,2
1,0,0,1,1
2,3,1,2,0

This program not only finds the greedy sequence, but finds all possible safe sequences for the given values.
