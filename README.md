# Snake Game AI

Snake AI is a Python-based implementation of the classic Snake game with an AI agent that learns to play the game using Q-learning. This project is designed to showcase how reinforcement learning techniques can be applied to train an AI agent to perform tasks.

## Table of Contents
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Training the AI Agent](#training-the-ai-agent)
  - [Hyperparameters](#hyperparameters) 
  - [Training Progress](#training-progress)

## Getting Started
### Prerequisites
- Pygame (for the game interface)
- PyTorch (for the neural network)
- Matplotlib (for plotting graphs)
### How To Run
- Open cmd in current directory
- run 'python agent.py'
## Project Structure
- agent.py: Entry Point of the program which call all other classes
- game.py: Contains Game logic and Snake game class
- model.py: Defines the neural network used for Q-learning.
- plotting.py: Provides functions for plotting game statistics.
- model.pth: Pre-trained model weights './model./model.pth'
## Training The AI Agent
### Hyperparameters
You can adjust the AI agent's learning behavior by modifying hyperparameters in the agent.py file. Experiment with different values to see how they affect learning speed and performance.
### Training Progress
- During training, the AI agent's progress is displayed in the console.
- The training progress can be visualized using the provided plotting functions.
- At Learning Rate = 0.001, Batch Size = 1000, Epochs = 1000 model attained a score of 84 (at around 600ish epoch)



