# Quagsire

Quagsire is a desktop application designed to assist players of the Pokémon minigame **Voltorb Flip** by solving the game board using a backtracking algorithm combined with entropy-based probability analysis. It helps players make informed decisions by calculating the likelihood of each cell being safe or a bomb, thus improving their chances to maximize points and minimize risks.

This project was originally developed as the final assignment for my Differential Equations subject during my Masters program. The final version implemented a combination of a logistic Ordinary Differential Equation (ODE) and the Euler method to model the agent’s reliability progression based on the maximum entropy values on the board after each move that I developed myself.

The idea was to dynamically adjust the agent’s behavior as the game progressed, using the mathematical model to reflect increasing environmental complexity. However, for the final version presented here — aimed at a more practical and straightforward implementation — this feature was removed, as it was no longer considered a core element of the project.

## Features

- **Backtracking solver:** Enumerates all valid board configurations based on row/column sums and bomb counts.
- **Probability calculation:** Computes the probability distribution for each cell value (1, 2, 3, or Bomb).
- **Entropy-based suggestions:** Highlights cells where revealing them reduces uncertainty the most.
- **Point-maximizing hints:** Suggests the best cells to reveal based on expected point gain.
- **User-friendly GUI:** Interactive grid input with editable cells and automatic color-coded feedback.

## How to use

1. **Input the board data:**
   - Enter the known or assumed values (1, 2, 3, or B for bomb) in the 5x5 grid.
   - Fill the row and column hints in the last row and column (format: `sum,bombs`).
2. **Click "Solve"** to analyze the board.
3. **Interpret the results:**
   - Green cells are safe (non-bomb).
   - Red cells are bombs.
   - Blue and yellow highlights indicate suggested cells to reveal based on entropy and point maximization.
4. **Click "Clear"** to reset the board.


