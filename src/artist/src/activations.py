import numpy

# Note: All activation functions here are dynamically added to numpy_image_nn during construction
#   To add a new activation function write a function here that takes a numpy array 
#   and returns the new activated array. 

def tanh(matrix):
    return numpy.tanh(matrix)

def sigmoid(matrix):
    return 1.0 / (1 + numpy.exp(-matrix))

def relu(matrix):
    return numpy.maximum(matrix, 0, matrix)

def softmax(matrix):
    expo = numpy.exp(matrix)
    expo_sum = numpy.sum(numpy.exp(matrix))
    return expo/expo_sum

def sech(matrix):
    return 1.0 / numpy.cosh(matrix)
