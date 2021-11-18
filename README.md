# TorchFoam
A package to run OpenFOAM simulations, extract and process the data for use in PyTorch.

## Interfacing with OpenFOAM:
The `PyFoam` library is used to interface with openFOAM. This library includes useful classes which introduce an intuitive way to set up parameters for an OpenFOAM simulation from within a python script. 

## Interfacing with PyTorch:
Solver results files from OpenFOAM are given in ASCII text format, from which the numerical data may be extracted for conversion to a `torch` tensor.
