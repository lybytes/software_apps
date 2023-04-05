import pandas as pd
import matplotlib.pyplot as plt 
import csv
from scipy.stats import norm # For fitting
from scipy.stats import rayleigh

class ChessPlayer:
    def __init__(self, name, yob, gender, federation):
        self.yob = yob
        self.federation = federation
        self.gender = gender
        self.name = name
        #self.fide_id = fide_id

players_data = []
yob_data = []
elo = {}
elos = []
# Open the CSV file
with open('players.csv', 'r') as file:

    # Create a CSV reader object
    reader = csv.DictReader(file)

    # Create an empty list to store the data
    
    for row in reader:
    
        yob = int(row['yob']) if row['yob'] else None
        federation = row['federation']
        gender = row['gender']
        #fide_id = int(row['fide_id']) if row['fide_id'] else None
        name = row['name']
        new_player = ChessPlayer(name, yob, gender, federation) #fide_id
        players_data.append(new_player)
        yob_data.append(yob)
    

with open('ratings_2021_condensed.csv', 'r') as file:
    
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        elo_2021 = row['rating_standard']
        elo[players_data[count]] = elo_2021
        elos.append(elo_2021)
        count += 1
        
plt.plot(yob_data, elos)
plt.show()



    
