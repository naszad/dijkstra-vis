# Dijkstra Graph Visualization and Animation

This project demonstrates Dijkstra's shortest-path algorithm in two flavors:

1. **C++ Command-Line Version** (`dijkstra.cpp`)
2. **Python/Tkinter GUI Version** (`gui.py`)

Additionally, a sample graph file (`graph_input.txt`) and a built-in random graph generator are provided.

---

## Files

- **dijkstra.cpp**  
  C++ implementation that reads a graph from `graph_input.txt`, computes shortest paths from a source, and prints each path and cost.

- **gui.py**  
  Python/Tkinter application that:
  - Loads any `.txt` graph in the same format
  - Displays the graph in a circular layout
  - Lets you click two nodes to animate Dijkstra step-by-step
  - Adjusts animation speed with a slider
  - Generates random connected graphs via UI controls

- **graph_input.txt**  
  Sample input with 6 vertices (U–Z) and 10 edges.

- **README.md**  
  This documentation.

---

## Requirements

- Python 3.x  
  - `tkinter` (usually included in standard library)
- A C++11-compatible compiler  
  - e.g. `g++`, `clang++`

---

## Graph File Format

Each input file must follow this structure:

```
N M               # number of vertices and edges
v1
v2
...
vN               # N distinct vertex names (one per line)
u1 v2 w          # M lines: edge between u1-v2 with weight w
...               # (undirected graph, each edge listed once)
SOURCE            # name of the source vertex for Dijkstra
```


## Command-Line (C++) Usage

1. **Compile**:
   ```sh
   g++ -std=c++11 -O2 -o dijkstra dijkstra.cpp
   ```
2. **Run** (reads `graph_input.txt` by default):
   ```sh
   ./dijkstra
   ```
3. **Output**:
   Prints paths and costs for every vertex from the source.

---

## GUI (Python) Usage

1. **Launch**:
   ```sh
   python gui.py
   ```
2. **Load a Graph**:
   - Click **Load & Run**, select any `.txt` file in the format above.
3. **Generate Random Graph**:
   - Use the **Vertices** and **Max Conn** spinboxes, then click **Generate Graph**
   - A new `random_graph.txt` is created and loaded automatically.
4. **Animate**:
   - Click a node (turns **green**) to choose the source.
   - Click a second node (turns **red**) to choose the target.
   - Watch Dijkstra visit, consider, relax, and highlight the final shortest path.
5. **Speed Slider**:
   - Adjust **Speed (ms)** to change the delay between animation steps.

---

## Example

Using the provided `graph_input.txt`:
```
6 10
U
V
W
X
Y
Z
U V 5
U X 5
U W 9
V W 8
V X 8
W X 3
W Y 7
W Z 5
X Y 7
Y Z 5
U
```
- Load it in the GUI or run the C++ binary to see the shortest paths from `U`.


---

Feel free to explore and modify the code for different layouts, color schemes, or alternative algorithms! Contributions and feedback are welcome. 