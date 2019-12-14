'''
    This file is used for graph constructing
    because I found it time consuming to calculate btwness everytime
    Betweenness will be calculated and stored in plain text
    so that it won't need to do Girvan-Newman everytime
    when we want to test different inputs in the same graph
    
    For every new graph or updated graph
    Run setup.py before run main.py
'''

import utils as g

def main():
    # Construct the graph:
    graph = g.Graph('../data/facebook_combined.txt')

    # Needs some statistics:
    max = 0.0
    min = 1000.0
    total = 0.0
    i = 0

    # Store betweenness:
    file = open('../data/btwness.txt', 'w+')
    for edge in graph.betweenness:
        n1 = edge[0]
        n2 = edge[1]
        btwness = graph.betweenness[edge]
        string = str(n1) + ',' + str(n2) + ',' + str(btwness) + '\n'
        file.write(string)
        # Do something with statistics:
        i = i + 1
        total = total + btwness
        if btwness > max:
            max = btwness
        if btwness < min:
            min = btwness
    file.close()

    # Store statistics:
    avg = total / i
    file2 = open('../data/stat.txt', 'w+')
    file2.write(f'max btwness: {max}')
    file2.write('\n')
    file2.write(f'min btwness: {min}')
    file2.write('\n')
    file2.write(f'avg btwness: {avg}')
    file2.close()

if __name__ == '__main__':
    main()
