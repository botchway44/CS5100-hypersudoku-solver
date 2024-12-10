# Hyper HyperSudoku Solver using Dancing Links

## Table of Contents

- [Project Overview](#project-overview)
- [Implementation](#implementation)
  - [Algorithm Selection](#algorithm-selection)
  - [Caveats and Additional Constraints](#caveats-and-additional-constraints)
  - [Visualization](#visualization)
- [Input Specifications](#input-specifications)
  - [Input Format](#input-format)
  - [Providing Inputs](#providing-inputs)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Solver](#running-the-solver)
  - [Example](#example)
- [Dependencies](#dependencies)


## Project Overview

This project implements a **Hyper HyperSudoku Solver** using the **Dancing Links** algorithm, an efficient technique for solving exact cover problems. The solver not only handles standard HyperSudoku puzzles but also incorporates additional constraints specific to Hyper HyperSudoku, providing a more challenging and comprehensive solving experience.

## Implementation

### Algorithm Selection

The core of this project is based on **Donald Knuth's Dancing Links (DLX)** algorithm, renowned for its efficiency in solving exact cover problems such as HyperSudoku. The DLX algorithm employs a clever data structure that allows for rapid backtracking and solution finding.

- **Dancing Links (DLX):** Utilizes a sparse matrix representation with circular doubly-linked lists to represent constraints and possible assignments. This structure enables efficient covering and uncovering of constraints during the search process.

### Caveats and Additional Constraints

- **Hyper HyperSudoku Support:** Unlike standard HyperSudoku, Hyper HyperSudoku includes four additional 3x3 regions that must also contain all digits from 1 to 9 without repetition. The solver accommodates these extra constraints by dynamically adjusting the exact cover matrix based on provided hyper box positions.
  
- **Dynamic Hyper Boxes:** Users can define the positions of hyper boxes, allowing flexibility in solving various HyperSudoku variants that incorporate different additional regions.

### Visualization

The current implementation provides console-based visualization by printing the solved HyperSudoku grid in a readable format. Each cell is displayed with its corresponding number, and empty cells (if any) are represented by dots (`.`). 

The graphical visualization implemented using matplotlib opens a pop-up window to first show the input puzzle and then begins by displaying the code execute, solving the HyperSudoku puzzle in a step by step manner.

## Input Specifications

### Input Format

- **Grid Representation:** The HyperSudoku puzzle is represented as a 9x9 grid.
- **File Format:** Inputs are provided via a text file where each line corresponds to a row in the HyperSudoku grid.
- **Cell Delimiter:** Cells within a row are separated by spaces.
- **Empty Cells:** Represented by `0`.

**Example:**
```
0 0 0 0 0 0 0 3 0
3 0 9 0 0 0 0 2 0
8 0 7 0 0 0 9 6 0
0 1 0 0 0 4 3 0 6
0 0 6 0 0 0 0 0 0
0 7 5 1 0 0 0 0 9
0 8 0 0 4 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 2
```

### Providing Inputs

- **File Input:** Users must create a text file (`.txt`) following the format described above.
- **Command-Line Argument:** The file path is provided as a command-line argument when running the program.

**Example File Name:** `grid_1.txt`

## Installation

### Prerequisites

- **Python 3.6 or higher** is required to run the solver.

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/botchway44/CS5100-hypersudoku-solver
   cd CS5100-hypersudoku-solver
   ```

2. **(Optional) Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Matplotlib Library needs to be installed for the code to run
   Command for Python 3 users - 
   ```bash
   pip3 install matplotlib
   ```

## Usage

### Running the Solver

Execute the script via the command line, providing the path to your HyperSudoku puzzle file as an argument.

```bash
python3 HyperSudoku.py grids/grid_1.txt
```

### Example

Given an input file named `grid_1.txt` located in the project directory, run:

```bash
python3 HyperSudoku.py grid_1.txt
```

**Sample Output:**
```
5 6 2 4 7 9 8 3 1
3 4 9 8 6 1 5 2 7
8 1 7 2 3 5 9 6 4
2 1 8 7 9 4 3 5 6
4 3 6 9 2 8 7 1 5
9 7 5 1 8 3 4 6 2
1 8 3 6 4 2 2 9 8
6 4 1 3 5 7 2 8 9
7 9 4 5 1 6 6 4 2
```

[r5](https://user-images.githubusercontent.com/35941942/173422917-676eb4ed-28a5-4817-ab94-f2ab4ebfb101.png)

## Dependencies

This project utilizes Python's standard libraries:

- `argparse`: For parsing command-line arguments.
- `pathlib`: For handling file paths.
- `time` : For timing the visualization

No external libraries are required, ensuring ease of installation and compatibility.
Except
- `Matplotlib` : For visualization
