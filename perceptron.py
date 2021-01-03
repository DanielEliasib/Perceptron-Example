from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import math

import json

import os

from mpl_toolkits import mplot3d

import argparse

def MaxNorm(X):
    #! Expects X to be a np.array
    # dim = X.shape[1]
    # m = X.shape[0]

    max = -1

    for xi in X:
        norm = 0
        for v in xi:
            norm = norm + v*v
        norm = math.sqrt(norm)
        if norm > max:
            max = norm
    
    return max

def AproximatePerceptron(X: np.ndarray, Y: np.ndarray, maxIterations: int) -> Tuple[np.ndarray, float, int]:
    weights = np.zeros(X.shape[1])      #| Parameters
    bias = 0                            #| Bias, separated for implementation simplicity

    totalErrors = 0                     #| Total errors in the entire process, less or equal than R^2/delta^2
    currentErrors = -1                  #| Errors in the current iterations

    it = 0

    while currentErrors != 0 and it <= maxIterations:    #| Stops updating the weights when there are no more errors or until a maxIteration in case something goes wrong
        currentErrors = 0

        for xi, yi in zip(X, Y):
            if yi*(np.dot(weights, xi) + bias) <= 0:    #| Checks for an error
                totalErrors += 1
                currentErrors += 1

                weights += yi*xi                        #| Updating weights and bias
                bias += yi

        it += 1

    return (weights, bias, totalErrors) 

def RenderPointsAndSolution2D(X: np.ndarray, Y: np.ndarray, weights: np.ndarray, bias: float):
    X_1, X_2 = zip(*X)
    
    df = pd.DataFrame(dict(X1=X_1, X2=X_2, Y=Y))
    colors = {-1:'lightcoral', 1:'steelblue'}

    fig, ax = plt.subplots()
    ax.scatter(df['X1'], df['X2'], c=df['Y'].map(colors))

    solX = np.linspace(min(X_1), max(X_1), 10)
    solY = (-bias - solX*weights[0])/weights[1]

    plt.plot(solX, solY, '#9467bd')
    plt.savefig('result2D.png')
    plt.show()

def RenderPointsAndSolution3D(X: np.ndarray, Y: np.ndarray, weights: np.ndarray, bias: float):
    X_1, X_2, X_3 = zip(*X)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    df = pd.DataFrame(dict(X1=X_1, X2=X_2, X3=X_3, Y=Y))
    colors = {-1:'lightcoral', 1:'steelblue'}

    ax.scatter(df['X1'], df['X2'], df['X3'], c=df['Y'].map(colors))
    ax.view_init(elev=10., azim=-110)

    solX = np.linspace(min(X_1), max(X_1), 10)
    solY = np.linspace(min(X_2), max(X_2), 10)
    

    pX, pY = np.meshgrid(solX, solY)
    pZ = (-bias - pY*weights[1]- pX*weights[0])/weights[2]

    ax.contour3D(pX, pY, pZ, 50, cmap='binary')

    plt.savefig('result3D.png')
    plt.show()

def CheckDataIntegrity(points: list, labels: list) -> bool:
    if len(points) <= 0 or len(points) != len(labels):
        return False
    
    #| Check first element
    x1 = points[0]

    if type(x1) != list:
        return False

    isPointsValid = all(
        isinstance(x, list) and 
        len(x)== len(x1) and 
        all(isinstance(xi, (int, float)) for xi in x) 
        for x in points)    #| Probably not eficient but check if it's composed of list of the same size with numeric values

    isLabelsValid = all(
        isinstance(x, (int, float)) for x in labels     #| Allows floats for experimenting
    )

    return isPointsValid and isLabelsValid

def LoadData(fileName:str) -> Tuple[np.ndarray, np.ndarray, int]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fileDir = os.path.join(dir_path, 'Data', fileName)

    if not os.path.exists(fileDir):
        raise Exception("File doesn't exists!")

    f = open(fileDir)

    data = json.load(f)

    points = data['points']
    labels = data['labels']

    if not CheckDataIntegrity(points, labels):
        raise Exception("Data is not well organized")
    
    return (np.array(points), np.array(labels), len(points[0]))

if __name__ == "__main__":
    descText = 'This is a basic implementation of the Perceptron algorithm, it will load the labeld data from a .json and will calculate the hyperplane dividing the data.\nIt only generates a plot for 2D and 3D data.'

    parser = argparse.ArgumentParser(description=descText)

    parser.add_argument('-v', '--version', help='shows program version', action='store_true')
    parser.add_argument('-d', '--data', help='Specify the name of your .json file with your data.\nThe file must be inside the "Data" folder and should follow the same sintaxys as the examples given.')
    parser.add_argument('-it', '--iterations', help='Maximum number of iterations the program can do.')

    args = parser.parse_args()

    if args.version:
        print("Perceptron example version 0.1 by Daniel Eliasib")

    dataFile = ""
    maxIter = 1500

    if args.data:
        dataFile = str(args.data)
    else:
        dataFile = "example2D-1.json"
    
    if args.iterations:
        val = int(args.iterations)
        maxIter = 1 if val <= 1 else val

    print("Loading data example %s" % dataFile)
    print("Aproximating with maximum iterations %d" % maxIter)

    X, Y, dim = LoadData(dataFile)

    W, b, k = AproximatePerceptron(X, Y, maxIter)

    if dim == 2:
        RenderPointsAndSolution2D(X, Y, W, b)
    elif dim == 3:
        RenderPointsAndSolution3D(X, Y, W, b)
    else:
        print("The points have dimention %d, this programm will only render 2D and 3D data." % dim)

    print("Results: ")
    print("\tWeights: " + str(W))
    print("\tBias: " + str(b))
    print("\tTotal errors: " + str(k))
# RenderPointsAndSolution2D(X, Y, W, b)

