import pandas as pd
import matplotlib.pyplot as plt 
import csv
import numpy as np
from scipy.stats import norm # For fitting
from scipy.stats import rayleigh

class ChessPlayer:
    def __init__(self, name, yob, gender, federation, id):
        self.yob = yob
        self.federation = federation
        self.gender = gender
        self.name = name
        self.id = id
        #self.fide_id = fide_id

idToPlayers = {}
yob_data = []
elo_data = []
# Open the CSV file
print('We made it out lol')
with open('players.csv', 'r') as file:

    # Create a CSV reader object
    reader = csv.DictReader(file)
    #print(reader.fieldnames)

    # Create an empty list to store the data
    for row in reader:
    
        yob = int(row['yob']) if row['yob'] else None
        federation = row['federation']
        gender = row['gender']
        id = row['\ufefffide_id']
        name = row['name']
        new_player = ChessPlayer(name, yob, gender, federation, id) #fide_id
        player_info = []
        player_info.append(new_player)
        
        idToPlayers[id] = player_info
     

print('Round One Complete')


with open('ratings_2021_condensed.csv', 'r') as file:
    
    reader = csv.DictReader(file)
    #print(reader.fieldnames)
    for row in reader:
        id = row['fide_id']
        elo_2021 = row['rating_standard']
        if id in idToPlayers:
            idToPlayers[id].append(elo_2021)

yob_data = []
elo_data = []
for player_info in idToPlayers.values():
    if len(player_info) > 1:
        player = player_info[0]
        elo = player_info[1] # Assuming elo is an integer
        if player.yob is not None and elo is not None and player.yob >= 1950 and player.yob <= 2025:
            yob_data.append(player.yob)
            elo_data.append(elo)


print('success')

print('Max of elo data', np.amax(elo_data))    # Some descriptive statistics 
print('Min of elo data', np.amin(elo_data))
print('Mean of elo', np.mean(elo_data))
print('Std. dev. of elo', np.std(elo_data))


"""
plt.scatter(yob_data, elo_data)
plt.xlim(1950, 2023)
plt.ylim(500,2500)
plt.xlabel('Year of Birth')
plt.ylabel('Elo Rating')
plt.title('Elo Rating vs. Year of Birth')
plt.show()
"""
