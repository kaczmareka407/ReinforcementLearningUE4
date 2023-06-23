import json
import sys
from matplotlib import pyplot as plt
import os
import argparse

plt.rcParams['savefig.dpi'] = 600

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input filename", type=str)
    parser.add_argument("-c", "--compare", help="Filename to be compared", type=str)
    parser.add_argument("-s", "--save", action='store_true', help="Save plots")
    args = parser.parse_args()

    json_path = '.'
    json_files = [filename for filename in os.listdir(json_path) if filename.endswith('.json')]
    print(f'jsons: {json_files}')

    if args.file:
            json_files = [str(args.file)]
    if not args.file and args.compare:
        raise('To use --compare flag, --file must be set')
    

    for filename in json_files:
        print(f'\n==============================')
        print(f'GENERATING PLOT FOR: {filename}')
        print(f'==============================')
        plt.clf()

        try:
            with open(filename) as file:
                data = json.load(file)
        except Exception:
            print(f'FILE {filename} NOT FOUND')
            continue
    
        print(f'Algorithm: {data["algorithm"]}')
        print(f'Learning episodes: {data["numLearning"]}')
        print(f'Evaluation episodes: {data["numEvalutation"]}')
        print('==========================')
        print(f'Algorithm parameters:')
        for key, value in data["parameters"].items():
            print(f'{key}: {value}')
        print('==========================')


        print(f'Num training episodes = {len(data["trainingRewards"])}')
        print(f'Num won episodes = {len(data["wonEpisodes"])}')
        label = 'reward'
        title = f'Accumulated reward in the following episodes \nLevel: {data["level"]} \nAlgorithm: {data["algorithm"]}'

        if args.compare:
            if 'PPO2' in filename:
                label = 'PPO2'
            else:
                label = 'ACER'

            title = f'Accumulated reward in the following episodes \nLevel: {data["level"]}'
        plt.plot(data['trainingRewards'], label=label)
        plt.xlabel('# episode')
        plt.ylabel('reward')
        plt.title(title)
        plt.grid(color = 'green', linestyle = '--')

        #add end_of_level locations
        wins_points = data['wonEpisodes']
        try:
            for x in wins_points:
                if x < data["numLearning"]:
                    plt.plot(x,data["trainingRewards"][x],'bo', markersize=2)
        except IndexError:
            ...
        

        if args.compare:
            try:
                with open(args.compare) as file:
                    data2 = json.load(file)
            except Exception:
                print(f'FILE {args.compare} NOT FOUND')
                continue
            
            if 'PPO2' in args.compare:
                label = 'PPO2'
            else:
                label = 'ACER'
            plt.plot(data2['trainingRewards'], label=label)

            wins_points = data2['wonEpisodes']
            try:
                for x in wins_points:
                    if x < data2["numLearning"]:
                        plt.plot(x,data2["trainingRewards"][x],'go', markersize=2, color='orange')
            except IndexError:
                ...

        
        
        if args.compare:
            marker1 = plt.Line2D([], [], marker='o', color='blue', linestyle='None', label = f'Finished scenarios {data["algorithm"]}')
            marker2 = plt.Line2D([], [], marker='o', color='orange', linestyle='None', label = f'Finished scenarios {data2["algorithm"]}')

            legend = plt.legend(loc='upper left')
            legend.legendHandles.append(marker1)
            legend.legendHandles.append(marker2)
        else:
            marker1 = plt.Line2D([], [], marker='o', color='blue', linestyle='None', label = 'Finished scenarios')
            legend = plt.legend(loc='upper left')
            legend.legendHandles.append(marker1)

        plt.legend(handles = legend.legendHandles )
        if args.save:
            if args.compare:
                plt.savefig(f'plots/plots_comparison_{data["level"]}_{data["algorithm"]}-{data2["algorithm"]}-episode_rewards', bbox_inches='tight')
            else:
                plt.savefig(f'plots/{filename}'+'-reward.png', bbox_inches='tight')
        else:
            plt.show()

        #===========================SECOND PLOT===========================
        plt.clf()

        if args.compare:
            figure, axis = plt.subplots(2, 1)
            plt.suptitle(data['level'])
            plt.subplots_adjust(hspace=0.5)

            index = 0
            figure.suptitle(data['level'])
            for data_set in [data, data2]:
                scenario_rewards = data_set['scenarioRewards']

                axis[index].set_title(data_set['algorithm'])
                axis[index].grid(color = 'green', linestyle = '--')
                axis[index].set_ylabel('reward')
                maximum_reward = max([max(data['scenarioRewards']),max(data2['scenarioRewards'])])
                ticks = [x for x in range(0,maximum_reward,4)]

                axis[index].set_yticks(ticks)
                plt.ylabel('reward')

                x = [x for x in range(len(scenario_rewards))]
                one_third_max = max(scenario_rewards)/3
                two_third_max = (max(scenario_rewards)/3) * 2

                bar_color = [{l<one_third_max: 'red', one_third_max<=l<=two_third_max: 'orange', l>two_third_max: 'green'}[True] for l in scenario_rewards]

                axis[index].bar(x, scenario_rewards, color=bar_color)
                index = index+1

            if args.save:
                figure.savefig(f'plots/plots_comparison_{data["level"]}_{data["algorithm"]}-{data2["algorithm"]}-scenario_rewards', bbox_inches='tight')
            else:
                plt.show()
        else:
            plt.title(f'Accumulated reward in the following scenarios \nLevel: {data["level"]}\nAlgorithm: {data["algorithm"]}')
            #plot avg scenario reward
            scenario_rewards = data['scenarioRewards']
            
            
            plt.grid(color = 'blue', linestyle = '--')
            plt.xlabel('# scenario')
            plt.ylabel('reward')
            plt.yticks([x for x in range(0,max(scenario_rewards),2)])

            x = [x for x in range(len(scenario_rewards))]
            one_third_max = max(scenario_rewards)/3
            two_third_max = (max(scenario_rewards)/3) * 2

            bar_color = [{l<one_third_max: 'red', one_third_max<=l<=two_third_max: 'orange', l>two_third_max: 'green'}[True] for l in scenario_rewards]

            plt.bar(x, scenario_rewards, color=bar_color)

            if args.save:
                plt.savefig(f'plots/{filename}'+'-scenario-rewards.png', bbox_inches='tight')
            else:
                plt.show()

        plt.clf()


if __name__ == "__main__":
    main()