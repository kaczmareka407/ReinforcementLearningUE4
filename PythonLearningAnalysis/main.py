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


    print(f'Num training episodes = {len(data["trainingRewards"])}')

    plt.plot(data['trainingRewards'], label='training reward')
    plt.xlabel('# episode')
    plt.ylabel('reward')
    plt.title(f'Accumulated reward in the following episodes \nLevel: {data["level"]} \nAlgorithm: {data["algorithm"]}')
    plt.grid(color = 'green', linestyle = '--')


    #add evaluation line
    eval_line = data['evalutationRewards']
    highest_training_reward = data['trainingRewards'][-1]
    eval_line = [x-highest_training_reward for x in eval_line]
    plt.plot(eval_line, label='evaluation reward')

    #add end_of_level locations
    wins_points = data['wonEpisodes']
    for x in wins_points:
        if x < data["numLearning"]:
            plt.plot(x,data["trainingRewards"][x],'bo')
        else:
            plt.plot(x-data["numLearning"],eval_line[x-data["numLearning"]],'rh')

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()