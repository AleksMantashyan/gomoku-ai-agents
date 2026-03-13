# GomokuAI_Project

This project contains all code, AI agents, and experiments used to run and analyze
Gomoku matches. It includes three AI agents (Alpha–Beta, Minimax, Random),
a playable web interface built with Flask, and experiment CSV files used for analysis.

------------------------------------------------------------

## Folder Structure

GomokuAI_Project/
│
├── app.py                       # Flask web interface
├── Board.py                     # Board representation and game logic
├── Evaluation.py                # Pattern-based evaluation function
├── MoveFilter.py                # Move filtering (proximity search)
├── AlphaBetaAgent.py            # Alpha–Beta pruning agent
├── HeuristicMinimaxAgent.py     # Minimax agent with heuristics
├── RandomAgent.py               # Random agent
│
├── templates/
│     └── index.html             # Web UI for the Gomoku board
│
├── game_results/
│     └── CSV files for all experiments
│
├── *.py                         # Additional scripts used to run experiments
├── *.Rmd                        # R Markdown files for visualizations
│
└── lib/, bin/, __pycache__/     # Environment/cached files

------------------------------------------------------------

## How to Run the App from Terminal

1. Open a terminal (Command Prompt, PowerShell, or macOS Terminal).

2. Navigate to the project folder using `cd`. For example:

cd path/to/GomokuAI_Project

3. Install Flask (only needed once):

pip install flask

4. Run the application:

python app.py

5. After running the command, Flask will show an address such as:

 * Running on http://127.0.0.1:5000/

6. Open your web browser and go to:

http://127.0.0.1:5000/

You can now play the Gomoku game directly in your browser.

------------------------------------------------------------

## How to Run the Game (Flask Web App)

### 1. Install Requirements

Open a terminal inside the GomokuAI_Project folder and run:

pip install flask

### 2. Start the App

Run the following command inside the project folder:

python app.py

If successful, Flask will display something like:

 * Running on http://127.0.0.1:5000/

### 3. Open the Game in Your Browser

Go to:

http://127.0.0.1:5000/

You will see the interactive Gomoku board where you can choose:

- Human vs AI  
- Random Agent  
- Minimax Agent  
- Alpha–Beta Agent  

The board updates automatically and shows moves in real time.

------------------------------------------------------------

## Running the Experiments (Optional)

All experiment CSV files are already available in:

game_results/

If you want to re-run experiments or generate new CSV files, simply run the corresponding Python scripts such as:

python alpha_beta_d2_vs_minimax_d2.py
python alpha_beta_d3_vs_alpha_beta_d2.py
python random_tests_&_AB_d2_vs_max_d1.py

Each script outputs a CSV into game_results/.

------------------------------------------------------------

## Visualizations (Optional)

R Markdown files (*.Rmd) produce all plots used in the report.

To render a visualization:

1. Open the .Rmd file in RStudio  
2. Click Knit  
3. The plots will be generated automatically

Required R packages:

tidyverse
ggplot2
readr

------------------------------------------------------------

## Documentation

The `docs/` folder contains the final project report and presentation slides.

------------------------------------------------------------

## Summary

- Run the game → python app.py  
- Play in browser → http://127.0.0.1:5000  
- All experiment output → in game_results/  
- Visualizations → via .Rmd files  

Everything needed to test, run, or evaluate the AI agents is included in this folder.
