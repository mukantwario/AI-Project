import argparse
from mazegen import get_maze, ALL_MAZES, print_maze
from agents import get_agent, ALL_AGENTS
from util import Problem
import time

ALL = 'all'


def trunc(num):
    return round(num * 1000) / 1000


def mean(list):
    sum = 0
    for item in list:
        sum += item
    return trunc(sum / len(list))


def run(mazeType, ai, trials, width, height):
    # setup some data structure for reporting results
    results = []

    # for each trial
    for trial in range(trials):
        result = {}

        # create a list of agents, will only be one if `all` is not selected
        agents = []
        if ai == ALL:
            for agent in ALL_AGENTS:
                agents.append((get_agent(agent), agent))
        else:
            agents.append((get_agent(ai), ai))

        # create a list of mazes, will only be one if `all` is not selected
        mazes = []
        if mazeType == ALL:
            for maze in ALL_MAZES:
                mazes.append((get_maze(maze, width, height), maze))
        else:
            mazes.append((get_maze(mazeType, width, height), mazeType))

        # for each maze
        for mazeTuple in mazes:
            maze = mazeTuple[0]
            mazeName = mazeTuple[1]

            result[mazeName] = {}

            # for each agent
            for agentTuple in agents:
                agentName = agentTuple[1]
                agent = agentTuple[0]

                # create a problem object for this maze, corner to corner

                problem = Problem((1, 1), (width - 2, height - 2), maze, width, height)

                result[mazeName][agentName] = {}

                time_zero = time.time()
                # get a plan from this agent
                plan = agent.getPlan(problem)

                # record results of this agent-maze pair into the reporting data structure
                result[mazeName][agentName]['time'] = time.time() - time_zero
                result[mazeName][agentName]['length'] = len(plan)
                result[mazeName][agentName]['nodes'] = problem.nodes_explored

        results.append(result)

    # print tabulated results
    by_maze = {}
    by_ai = {}
    time_table = {}
    length_table = {}
    nodes_table = {}

    for result in results:
        for mazeName in result:
            if mazeName not in by_maze:
                by_maze[mazeName] = {
                    "times": [],
                    "lengths": [],
                    "nodes": []
                }
            if mazeName not in time_table:
                time_table[mazeName] = {}
            if mazeName not in length_table:
                length_table[mazeName] = {}
            if mazeName not in nodes_table:
                nodes_table[mazeName] = {}

            for agentName in result[mazeName]:
                if agentName not in by_ai:
                    by_ai[agentName] = {
                        "times": [],
                        "lengths": [],
                        "nodes": []
                    }
                if agentName not in time_table[mazeName]:
                    time_table[mazeName][agentName] = []
                if agentName not in length_table[mazeName]:
                    length_table[mazeName][agentName] = []
                if agentName not in nodes_table[mazeName]:
                    nodes_table[mazeName][agentName] = []

                by_maze[mazeName]['times'].append(result[mazeName][agentName]['time'])
                by_maze[mazeName]['lengths'].append(result[mazeName][agentName]['length'])
                by_maze[mazeName]['nodes'].append(result[mazeName][agentName]['nodes'])

                by_ai[agentName]['times'].append(result[mazeName][agentName]['time'])
                by_ai[agentName]['lengths'].append(result[mazeName][agentName]['length'])
                by_ai[agentName]['nodes'].append(result[mazeName][agentName]['nodes'])

                time_table[mazeName][agentName].append(result[mazeName][agentName]['time'])
                length_table[mazeName][agentName].append(result[mazeName][agentName]['length'])
                nodes_table[mazeName][agentName].append(result[mazeName][agentName]['nodes'])

    maze_list = [mazeName for mazeName in by_maze]
    ai_list = [agentName for agentName in by_ai]
    heuristic_list = ['time', 'length', 'nodes']

    print('\nMean Results by Maze:\n')
    print("\t\t\tTime\tLength\tNodes")
    for mazeName in by_maze:
        print('{maze: <16}'.format(maze=mazeName) + '\t' + str(mean(by_maze[mazeName]['times'])) + '\t' + str(
            mean(by_maze[mazeName]['lengths'])) + '\t' + str(mean(by_maze[mazeName]['nodes'])))

    print('\nMean Results by Agent:\n')
    print("\t\t\tTime\tLength\tNodes")
    for agentName in by_ai:
        print('{agent: <16}'.format(agent=agentName) + '\t' + str(mean(by_ai[agentName]['times'])) + '\t' + str(
            mean(by_ai[agentName]['lengths'])) + '\t' + str(mean(by_ai[agentName]['nodes'])))

    print('\nMean Times by Agent Maze combinations:\n')
    print('{a:<16}'.format(a='') + '\t'.join(map(lambda x: '{item: <16}'.format(item=x), maze_list)))
    for agentName in by_ai:
        print('{agent: <16}'.format(agent=agentName) + '\t'.join(
            map(lambda x: '{a:<16}'.format(a=mean(time_table[x][agentName])), maze_list)))

    print('\nMean Length by Agent Maze combinations:\n')
    print('{a:<16}'.format(a='') + '\t'.join(map(lambda x: '{item: <16}'.format(item=x), maze_list)))
    for agentName in by_ai:
        print('{agent: <16}'.format(agent=agentName) + '\t'.join(
            map(lambda x: '{a:<16}'.format(a=mean(length_table[x][agentName])), maze_list)))

    print('\nMean Nodes Explored by Agent Maze combinations:\n')
    print('{a:<16}'.format(a='') + '\t'.join(map(lambda x: '{item: <16}'.format(item=x), maze_list)))
    for agentName in by_ai:
        print('{agent: <16}'.format(agent=agentName) + '\t'.join(
            map(lambda x: '{a:<16}'.format(a=mean(nodes_table[x][agentName])), maze_list)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--maze', default='perfect')
    parser.add_argument('--ai', default='astar')
    parser.add_argument('--trials', type=int, default=1)
    parser.add_argument('--width', type=int, default=21)
    parser.add_argument('--height', type=int, default=21)
    args = parser.parse_args()

    run(args.maze, args.ai, args.trials, args.width, args.height)