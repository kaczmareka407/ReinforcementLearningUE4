import json
import sys
from matplotlib import pyplot as plt
import os

def main():
    print()
    filename = f'example.json'
    if len(sys.argv) > 1:
        filename = str(sys.argv[1])

    with open(filename) as file:
        data = json.load(file)
   
    print(f'Algorithm: {data["algorithm"]}')
    print(f'Learning episodes: {data["numLearning"]}')
    print(f'Evaluation episodes: {data["numEvalutation"]}')
    print('==========================')
    print(f'Algorithm parameters:')
    for key, value in data["parameters"].items():
        print(f'{key}: {value}')
    print('==========================')

    plot_x = [x for x in range(len(data['trainingRewards']))]
    plot_y = data['trainingRewards']

    print(f'X len = {len(plot_x)}')
    print(f'Y len = {len(plot_y)}')

    plt.plot(plot_y)
    plt.xlabel('# episode')
    plt.ylabel('reward')
    plt.title(f'Accumulated reward in the following episodes \nLevel: {data["level"]} \nAlgorithm: {data["algorithm"]}')
    plt.grid(color = 'green', linestyle = '--')

    #add point
    plt.plot(5,5,'go')

    plt.show()


if __name__ == "__main__":
    main()