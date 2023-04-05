import datetime as dt
import csv

class ChessPlayer:
    def __init__(self, name, yob, gender, federation):
        self.yob = yob
        self.federation = federation
        self.gender = gender
        self.name = name
        #self.fide_id = fide_id

players_data = []
players_to_elo = {}
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
    
print('success')
size = len(players_data)
print(size)



with open('ratings_2021.csv', 'r') as file:
    
    reader = csv.DictReader(file)
    count = 0
    for row in reader:
        elo_2021 = row['rating_standard']
        players_to_elo[players_data[count]] = elo_2021
        count += 1
        
    print('lets go')


    
