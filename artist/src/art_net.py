import argparse
import numpy
import src.activations as activation_funcs
import os
import random

from inspect import getmembers, isfunction

class NumpyArtGenerator:
    """ Generates imagery using randomness and a fully connected forward propagation network """

    def __init__(self, resolution, seed, num_layers, layer_width, activation_name):
        """Initialize the network.

            resolution          -- tuple resolution of the output network 
            seed                -- seed value used by numpy random 
            num_layers          -- the number of hidden layers in the neural network
            layer_width         -- the number of perceptrons in each hidden layer 
            activation_name     -- name of the activation function used in each hidden layer
        """
        self.resolution = resolution

        self.seed = seed
        numpy.random.seed(self.seed)

        self.num_layers = num_layers
        self.layer_width = layer_width
        self.output_layer = 3

        self.__set_activation(activation_name)


    def __str__(self):
        """String representation of the network. """

        activation_string = self.activation[0]
        return "-".join([str(self.seed), str(activation_string), str(self.num_layers), str(self.layer_width)])


    def __set_activation(self, activation_name):
        """Set the activation functions for the network. """

        activations_dict = {}
        for func_name, func in getmembers(activation_funcs, isfunction):
            activations_dict[func_name] = func

        if activation_name not in activations_dict:
            raise KeyError("Invalid activation function: " + activation_name + ". Supported activation functions can be found in numpy_activation.py.")

        activation_func = activations_dict[activation_name]
        self.activation = (activation_name, activation_func)


    def __generate_input(self):
        """Generate the x,y coordinate matrices used as input for the network. """
        (ncols, nrows) = self.resolution

        rowmat = (numpy.tile(numpy.linspace(0, nrows-1, nrows, dtype=numpy.float32), ncols).reshape(ncols, nrows).T - nrows/2.0)/(min(nrows, ncols)/2.0)
        colmat = (numpy.tile(numpy.linspace(0, ncols-1, ncols, dtype=numpy.float32), nrows).reshape(nrows, ncols)   - ncols/2.0)/(min(nrows, ncols)/2.0)

        inputs = [rowmat, colmat, numpy.sqrt(numpy.power(rowmat, 2)+numpy.power(colmat, 2))]
        return numpy.stack(inputs).transpose(1, 2, 0).reshape(-1, len(inputs))


    def forward_prop(self, inputs):
        """Run forward propagation on the network"""
        results = inputs

        (ncols, nrows) = self.resolution

        for layer in range(0, self.num_layers):
            print("Current neural layer: " + str(layer+1) + "/" + str(self.num_layers), end='\r')

            if layer == self.num_layers - 1:
                W = numpy.random.randn(results.shape[1], self.output_layer)
            else:
                W = numpy.random.randn(results.shape[1], self.layer_width)

            activation_func = self.activation[1]
            results = activation_func(numpy.matmul(results, W))

        results = (255.0 * results.reshape(nrows, ncols, results.shape[-1])).astype(numpy.uint8)
        return results


    def print_details(self):
        """Print details of the generator"""

        print("Generator Settings:")
        print(f"    Resolution: {self.resolution}")
        print(f"    Seed: {self.seed}")
        print(f"    Number of Layers: {self.num_layers}")
        print(f"    Hidden Layer Width: {self.layer_width}")
        print(f"    Activation Function: {self.activation[0]}")


    def run(self, verbose):
        """ Run the generator. This includes generating inputs and running the forward propagation network"""

        if verbose:
            self.print_details()

        inputs = self.__generate_input()
        return self.forward_prop(inputs)




