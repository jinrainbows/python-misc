# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def makeDistanceMatrix(data):
    distanceTriangle = [] #This will look like a lower diagnol matrix
    for i in range(1,len(data)): #for each instance but the first
        distances = [] #this will be a list of distances to location i
        for j in range(0,i): #only need to measure distance for objects before i
            distances.append(np.abs(data[i] - data[j]))
        distanceTriangle.append(distances)
    return distanceTriangle
        

def updateMatrix_Single(distances, i, j):
    #create a new row
    row = []
    n = len(distances)+1
    for col in range(n):
        if col == i+1 or col == j:
            continue
        if col > i+1:
            row.append(min(distances[col - 1][i+1], distances[col-1][j]))
        elif col > j:
            row.append(min(distances[i][col], distances[col-1][j]))
        else:
            row.append(min(distances[i][col], distances[j-1][col]))        
    
    #delete old cols
    for r in range(i+1,n-1):
        del distances[r][i+1]
    for r in range(j,n-1):
        del distances[r][j]
    #delete old rows
    del distances[i]
    del distances[max(j-1,0)]
    
    #Add row to Table
    distances.append(row)
    return distances
        

def updateGroups(groups, i, j):
    #Combine two groups
    #because table excludes first row add one to i when accessing groups which doesn't exclude first row
    newGroup = groups[i+1]+groups[j]
    #remove the old groups, start with higher number
    del groups[i+1]
    del groups[j]
    #add in the new group
    groups.append(newGroup)
    return groups
        
        
### Four clustering methods.
def findMaximum(data, groups):
    maximums = []
    for group in groups:
        values = []
        for name in group:
            values.append(data[name])
        maximum = max(values)
        maximums.append(maximum)
    return maximums
        
def findMinimum(data, groups):
    minimums = []
    for group in groups:
        values = []
        for name in group:
            values.append(data[name])
        minimum = min(values)
        minimums.append(minimum)
    return minimums

def singleLinkage1D(data, k):
    data = data.sort_values()
    groups = [[name] for name in data.index]
    
    while len(groups) > k:
        maximums = findMaximum(data, groups)
        minimums = findMinimum(data, groups)
        distances = []
        for i in range(len(groups)-1):
            distances.append(minimums[i+1] - maximums[i])
        i = 0
        
        minValue = min(distances)
        i = distances.index(minValue)
        
        groups[i].extend(groups[i+1])
        
        groups.pop(i+1)
        
    return groups
        
        
def completeLinkage1D(data, k):
    data = data.sort_values()
    groups = [[name] for name in data.index]
    
    while len(groups) > k:
        maximums = findMaximum(data, groups)
        minimums = findMinimum(data, groups)
        distances = []
        for i in range(len(groups)-1):
            distances.append(maximums[i+1] - minimums[i])
        i = 0
        
        minValue = min(distances)
        i = distances.index(minValue)
        
        groups[i].extend(groups[i+1])
        
        groups.pop(i+1)
        
    return groups
    

def calculateAverages(data, groups):
    averages = []
    for group in groups:
        total = 0
        for name in group:
            total += data[name]
        if len(group) == 0:
            print("Uh oh! You can't divide by zero! Try again.")
        else:
            average = total / len(group)
        averages.append(average)
    return averages

def averageLinkage1D(data, k):
    
    data = data.sort_values()
    groups = [[name] for name in data.index]
    
    while len(groups) > k:
        averages = calculateAverages(data, groups)
        distances = []
        for i in range(len(averages)-1):
            distances.append(averages[i+1] - averages[i])
        i = 0
        
        minValue = min(distances)
        i = distances.index(minValue)
        
        groups[i].extend(groups[i+1])
        
        groups.pop(i+1)

    return groups        


def closestCentroid(i, centroids):
    distances = []
    for j in range(len(centroids)):
        distance = abs(centroids[j] - data[i])
        distances.append(distance)
    minvalue = min(distances)
    return distances.index(minvalue)

def divideClusters(data, centroids):
    clusters = [[] for i in range(len(centroids))] 
    for i in data.index:
        clusters[closestCentroid(i, centroids)].append(i)
    return clusters

def same(centroids, newcentroids):
    centroidsRounded = [round(i, 2) for i in centroids]
    newcentroidsRounded = [round(j, 2) for j in newcentroids]
    if centroidsRounded == newcentroidsRounded:
        return True
    else:
        return False
    
def kMeans1D(data, k):

    data = data.sort_values()
    initialCentroids = []
    while len(initialCentroids) < k:
       initial = random.uniform(min(data),max(data))
       initialCentroids.append(initial)
    
    centroids = list(initialCentroids)
    
    clusters = divideClusters(data, initialCentroids)    
    newcentroids = calculateAverages(data, clusters)
    
    while same(centroids, newcentroids) == False:
        clusters = divideClusters(data, centroids)
        centroids = list(newcentroids)
        newcentroids = calculateAverages(data, clusters)
    return clusters


def closestCentroid2D(i, centroids1, centroids2):
    distances = []
    for x, y in zip(centroids1, centroids2):
            distance = ((y - data2[i])**2 + (x - data[i])**2)**0.5
            distances.append(distance)
    minvalue = min(distances)
    return distances.index(minvalue)

def divideClusters2D(data, centroids1, centroids2):
    clusters = [[] for i in range(len(centroids1))] 
    for i in data.index:
        clusters[closestCentroid2D(i, centroids1, centroids2)].append(i)
    return clusters

def makeCoords(list1, list2):
    coords = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return coords

def kMeans2D(data, data2, k):
    initialCentroids1 = []
    while len(initialCentroids1) < k:
        initial1 = random.uniform(min(data),max(data))
        initialCentroids1.append(initial1)
    initialCentroids2 = []
    while len(initialCentroids2) < k:
        initial2 = random.uniform(min(data2),max(data2))
        initialCentroids2.append(initial2)
    
    centroids1 = list(initialCentroids1)
    centroids2 = list(initialCentroids2)
    
    clusters = divideClusters2D(data, centroids1, centroids2)
    
    newcentroids1 = calculateAverages(data, clusters)
    newcentroids2 = calculateAverages(data2, clusters)

    
    while same(centroids1, newcentroids1) == False and same(centroids2, newcentroids2) == False:
        clusters = divideClusters2D(data, centroids1, centroids2)
        centroids1 = list(newcentroids1)
        centroids2 = list(newcentroids2)
        newcentroids1 = calculateAverages(data, clusters)
        newcentroids2 = calculateAverages(data2, clusters)
    return clusters
        
        

### Start Program and open file
print("\nJin's Clustering Program.\n")
filename = input("Please enter the data-file's name: ")
dataFile = pd.read_csv(filename, index_col = 0)

### Allow User to select number of dimensions (continued below)
print("\nHow many dimensions would you like to use?")
dimension = int(input())
if dimension == 1:
    
### Allow User to select attribute
    print("Here is a list of attributes:")
    for name in dataFile.columns:
        print(name, end = "    ")
    attribute = input("\nWhich attribute would you like to cluster?  ")
    data = dataFile.loc[:][attribute]

### Potentially plot data
    toPlot = input("Would you like to plot this data? (y,n)  ")
    if toPlot.lower()[0] == 'y':
        plt.hist(data)
        plt.show()
    
### Select the Clustering Technique
    print("\nWhich clustering technique would you like to use?")
    print("(S)ingle linkage\n(C)omplete linkage\n(A)verage linkage\n(K)-means")
    clusterTechnique = input().lower()
    k = int(input("How many clusters? "))
    if clusterTechnique == 's':
        groups = singleLinkage1D(data, k)
    elif clusterTechnique == 'c':
        groups = completeLinkage1D(data, k)
    elif clusterTechnique == 'a':
        groups = averageLinkage1D(data, k)
    elif clusterTechnique == 'k':
        groups = kMeans1D(data, k)
        
    print("The groups are:")
    for g in groups:
        print()
        for name in g:
            print(name + ":", data[name])
    toPlot = input("Would you like to plot the groups? (y/n)  ")
    toPlot = toPlot.lower()[0]

    if toPlot == 'y':  
        for g in groups:
            groupData = [data[name] for name in g]
            plt.hist(groupData)
        plt.show()
            
if dimension == 2:
    print("Here is a list of attributes:")
    for name in dataFile.columns:
        print(name, end = "    ")
    attribute = input("\nWhich attribute would you like to cluster?  ")
    data = dataFile.loc[:][attribute]
    attribute2 = input("\nWhich other attribute would you like to cluster?  ")
    data2 = dataFile.loc[:][attribute2]

### Potentially plot data
    toPlot = input("Would you like to plot this data? (y,n)  ")
    if toPlot.lower()[0] == 'y':
        plt.scatter(data,data2)
        plt.show()
        
    print("\nWhich clustering technique would you like to use?")
    print("\n(K)-means")
    clusterTechnique = input().lower()
    k = int(input("How many clusters? "))
    if clusterTechnique == 'k':
        groups = kMeans2D(data, data2, k)
        
    print("The groups are:")
    for g in groups:
        print()
        for name in g:
            print(name + ":", (data[name],data2[name]))
    toPlot = input("Would you like to plot the groups? (y/n)  ")
    toPlot = toPlot.lower()[0]
    
    if toPlot == 'y':
        for g in groups:
            groupData = [data[name] for name in g]
            groupData2 = [data2[name] for name in g]
            plt.scatter(groupData, groupData2)
        plt.show()

        
        
  





    