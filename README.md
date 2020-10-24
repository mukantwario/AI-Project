# CS5100-Project
 
This is our group project for CS5100, Fall 2020 Semester.

## Running the Project

To run the project, just use:
`python main.py`

We have three CLI args, `maze`, `ai`, and `trials`.

The `maze` arg defines which maze generator we will use. If this is missing, we will default to `perfect`. These are the valid options:
- `perfect`
- `braid`
  
The `ai` arg defines which ai agent we will use. If this is missing, we will default to `all` These are the valid options:
- `dfs`
- `bfs`
- `astar`
- `all`*

*All is unique because it will run all algorithms and create a report. 

The `trials` arg defines how many trials will be run for each agent-maze pair. If this is missing, we will default to `1`.

### Example Usage
`python main.py --maze perfect --ai astar --trials 5`
This will run the A* agent through 5 perfect mazes and provide us a report of the results.

## Testing Maze Generation
To test maze generation, use:
`python mazegen.py`

There is only one CLI arg: `maze`. This is from the same list as above. This will

### Example Usage
`python mazegen.py --braid`
This will print a braid maze to the console output.