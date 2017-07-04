# Eight Puzzle 

Solver for 8-puzzle problem.
Smaller version of the [15-puzzle problem](https://en.wikipedia.org/wiki/15_puzzle).

## Running 

```
python3 driver_3.py <strategy> <comma-separted-tiles>
```

Example:

```
python3 driver_3.py dfs 1,0,2,3,4,5,6,7,8
```

It outputs the solution to `output.txt`.

## Strategies

- `bfs`: Breadth First Search
- `dfs`: Depth First Search
- `ast`: [A\* Search](https://en.wikipedia.org/wiki/A*_search_algorithm)

