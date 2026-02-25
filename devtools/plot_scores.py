"""This module imports every saved player score and plots all of them"""
from matplotlib import pyplot as plt

log_location_scores ="./highscores/scores_human.csv"

with open(log_location_scores, "r") as highscores_file:
    scores_list = highscores_file.readlines()

scores_list = [int(s.strip()) for s in scores_list]

#plot
plt.plot(scores_list, marker='o') 
plt.title("Player Scores")
plt.xlabel("Attempt")
plt.ylabel("Score")
plt.grid(True)
plt.show()