# 2D Non-Rotational Bin Packing with Greedy Heuristics

This project implements a 2D non-rotational bin packing algorithm for placing rectangular gates into a bounding box, using different greedy strategies. The objective is to minimize wasted space and optimize packing efficiency.

## Features
- **Three Greedy Heuristics**:
  1. Sum of dimensions and area.
  2. Maximum of width or height.
  3. Sum of width and height.
- Compares packing efficiencies across strategies.
- Time complexity evaluation with performance plotted against increasing number of gates.
- Optional visual output of the packing arrangement.

## Usage

### 1. Generate Test Cases  
Use the packing tester to generate random gate dimensions with `testcase_generate()`.

```python
testcase_generate("rand_input.txt", 100, 100)
```

### 2. Run the Algorithm  
To run the packing algorithm on an input file:

```bash
python packer.py <input_file> <output_file> [visualizer]
```

The script will compute and output the packing efficiency.

### 3. Visualize Results  
Enable the visualizer when calling `main()` or use the tester:

```python
visualize_gates("output.txt", "input.txt", (300, 300))
```

### 4. Plotting Performance  
The `plot_efficiency_vs_n()` function plots average runtime against the number of gates, comparing empirical results with theoretical time complexities (O(n²) and O(n³)).

```python
plot_efficiency_vs_n()
```

## Example Input Format
```
g1 20 30
g2 40 50
...
```

## Requirements
- `matplotlib`
- `time`
- `random`

---
