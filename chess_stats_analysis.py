import pandas as pd
import matplotlib.pyplot as plt 
import csv
import numpy as np
import random
from scipy.stats import norm # For fitting
from scipy.stats import rayleigh

class ChessPlayer:
    def __init__(self, name, yob, gender, federation, id):
        self.yob = yob
        self.federation = federation
        self.gender = gender
        self.name = name
        self.id = id

idToPlayers = {}
yob_data = []
elo_data = []
with open('players.csv', 'r') as file:

    reader = csv.DictReader(file)

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
     
     
     
     

#Q1 - What is the relationship between age and chess elo? Here, we are plotting every player's elo value against their year of birth
#     and seeing if there is correlation
all_yob_to_elo = []
with open('ratings_2021_condensed.csv', 'r') as file:
    
    reader = csv.DictReader(file)
    for row in reader:
        id = row['fide_id']
        elo_2021 = int(row['rating_standard']) if row['rating_standard'] else None
        if id in idToPlayers:
            idToPlayers[id].append(elo_2021)
            yob_to_elo = []
            yob_to_elo.append(idToPlayers[id][0].yob)
            yob_to_elo.append(idToPlayers[id][1])
            all_yob_to_elo.append(yob_to_elo)
            

all_yob_to_elo = [yob_elo for yob_elo in all_yob_to_elo if yob_elo[1] is not None]
sorted(all_yob_to_elo, key=lambda x: x[0])

x = [item[0] for item in all_yob_to_elo]
y = [item[1] for item in all_yob_to_elo]
# Filtering out elements in x that are less than 1950
x_filtered = [year for year in x if year >= 1950]
y_filtered = [y[i] for i in range(len(x)) if x[i] >= 1950]

# Find the minimum and maximum year of birth in the data and using that as axis scales
min_yob = min(x_filtered)
max_yob = max(x_filtered)
yob_range= range(min_yob, max_yob+1, 10)

slope, intercept = np.polyfit(x_filtered, y_filtered, 1)
line_x = [min_yob, max_yob]
line_y = [slope * xi + intercept for xi in line_x]

plt.scatter(x_filtered, y_filtered , s = 1)
plt.plot(line_x, line_y, color='r')
plt.xlabel('Year of Birth')
plt.ylabel('Elo Rating')
plt.title('Elo Rating vs. Year of Birth')
plt.yticks(np.arange(800, 2900, 200))
plt.xticks(yob_range)
plt.show()
#It would seem that, naturally, there is a negative relationship between a player's year of birth and their chess elo rating, 



#Q2. How big a difference is there between the top 100 rated male players, and the top 100 rated female players?



#Q3. How does the elo rating of top players overtime change (in this particular experiment, from 2015 to 2021)


#Q4. How much does the average elo rating vary according to federations? Would players from, for example, the Russian federation, 
#    have a higher average rating than players from the Irish federation? How much?


#Q5. Is there a relationship between a person's IQ and their chess elo rating?

