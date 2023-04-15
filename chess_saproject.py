import matplotlib.pyplot as plt 
import csv
import numpy as np
import berserk

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
    fieldNames = reader.fieldnames
    for row in reader:
    
        id = row[fieldNames[0]]
        name = row[fieldNames[1]]
        federation = row[fieldNames[2]]
        gender = row[fieldNames[3]]
        title = row[fieldNames[4]]
        yob = int(row[fieldNames[5]]) if row[fieldNames[5]] else None
        new_player = ChessPlayer(name, yob, gender, federation, id) #fide_id
        player_info = []
        player_info.append(new_player)
        
        idToPlayers[id] = player_info
     
     
     
     

#Q1 - What is the relationship between age and chess elo? Here, we are plotting every player's elo value against their year of birth
#     and seeing if there is correlation
all_yob_to_elo = []
with open('ratings_2021_condensed.csv', 'r') as file:
    
    reader = csv.DictReader(file)
    fieldNames = reader.fieldnames
    for row in reader:
        id = row[fieldNames[0]]
        elo_2021 = int(row[fieldNames[3]]) if row[fieldNames[3]] else None
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

# Extracting the top 100 male and female players based on Elo ratings
male_players = []
female_players = []
for player in idToPlayers.values():
    if player[0].gender == 'M' and len(player) > 1 and player[1] is not None:
        male_players.append(player)
    elif player[0].gender == 'F' and len(player) > 1 and player[1] is not None:
        female_players.append(player)

male_players.sort(key=lambda x: x[1], reverse=True)
female_players.sort(key=lambda x: x[1], reverse=True)

top_100_male_elo = male_players[:100]
top_100_female_elo = female_players[:100]

# Extracting Elo ratings for top 100 male and female players
male_elo = [player[1] for player in top_100_male_elo]
female_elo = [player[1] for player in top_100_female_elo]

# Plotting Elo ratings for top 100 male and female players in a bar chart
plt.figure(figsize=(12, 6))
plt.bar(np.arange(100), male_elo, alpha=0.75, label='Male')
plt.bar(np.arange(100), female_elo, alpha=0.75, label='Female')
plt.xlabel('Rank')
plt.ylabel('Elo Rating')
plt.title('Elo Ratings of Top 100 Male and Female Players')
plt.legend()
plt.show()  # display the bar chart

# Plotting a box plot to compare the distribution of Elo ratings between top 100 male and female players
plt.figure(figsize=(8, 6))
plt.boxplot([male_elo, female_elo], labels=['Male', 'Female'])
plt.xlabel('Gender')
plt.ylabel('Elo Rating')
plt.title('Distribution of Elo Ratings: Top 100 Male vs Female Players')
plt.show()  # display the box plot

# Computing and printing statistics
male_elo_np = np.array(male_elo)
female_elo_np = np.array(female_elo)
male_mean_elo = np.mean(male_elo_np)
female_mean_elo = np.mean(female_elo_np)
male_median_elo = np.median(male_elo_np)
female_median_elo = np.median(female_elo_np)
male_std_elo = np.std(male_elo_np)
female_std_elo = np.std(female_elo_np)

print('Statistics for top 100 male players:')
print(f'Mean Elo rating: {male_mean_elo:.2f}')
print(f'Median Elo rating: {male_median_elo:.2f}')
print(f'Standard deviation of Elo rating: {male_std_elo:.2f}')

print('\nStatistics for top 100 female players:')
print(f'Mean Elo rating: {female_mean_elo:.2f}')
print(f'Median Elo rating: {female_median_elo:.2f}')
print(f'Standard deviation of Elo rating: {female_std_elo:.2f}')

#Q3. How much does the average elo rating vary according to federations? Would players from, for example, the Russian federation, 
#    have a higher average rating than players from the Irish federation? How much?

countryFedCodes = {}
with open('chessFederationCodes.csv', 'r') as file:
    reader = csv.DictReader(file)
    fieldNames = reader.fieldnames
    for row in reader:
        federation = row[fieldNames[0]]
        country = row[fieldNames[1]]
        normCountry = country.replace(" ", "")
        countryFedCodes[normCountry.lower()] = federation

IDsToFederations = {}

#Creating a map of player IDs to federations
with open('players.csv', 'r') as file:

    reader = csv.DictReader(file)

    for row in reader:
        federation = row['federation']
        id = row['\ufefffide_id']
        IDsToFederations[id] = federation


federationsToElo = {}      
elosFound = []

#Iterating through the data of standard ratings, and only processing it if we have this data in the previous 'IDsToFederations' map
#If this player's ID exists in our database, we're extracting their elo and appending it to the player's federation's list of elo ratings
with open('ratings_2021_condensed.csv', 'r') as file:
    
    reader = csv.DictReader(file)
    fieldNames = reader.fieldnames
    for row in reader:
        id = row[fieldNames[0]]
        if row['rating_standard']:
            elo = int(row[fieldNames[3]])
        else:
            elo = 0
        if elo > 0:     
            if id in IDsToFederations:
                federation = IDsToFederations[id]
                if federation in federationsToElo:
                    federationsToElo[federation].append(elo)
                else:
                    elos = []
                    elos.append(elo)
                    federationsToElo[federation] = elos
                

print('Let us analyse the elo rating of the top 100 players across different chess federations!')
federationOne = input("Please type in a country name, for example Ireland, India, Russia etc ! \n(Please don't mess with us here Fergal)")
federationOne_noSpaces = federationOne.replace(" ", "")
while federationOne_noSpaces.lower() not in countryFedCodes:
    federationOne = input("Please.....type in a full country name \n(You can type in 'fide federation codes' in Google to see what the country is called in the chess world )")
    federationOne_noSpaces = federationOne.replace(" ", "")

federationTwo = input("Perfect, now type in a second country! ")
federationTwo_noSpaces = federationTwo.replace(" ", "")
while federationTwo_noSpaces.lower() not in countryFedCodes:
    federationTwo = input("C'mon man, please \n(You can type in 'fide federation codes' in Google to see what the country is called in the chess world) ")
    federationTwo_noSpaces = federationTwo.replace(" ", "")
    
    
fedOne_elos = federationsToElo[countryFedCodes[federationOne_noSpaces.lower()]]
fedTwo_elos = federationsToElo[countryFedCodes[federationTwo_noSpaces.lower()]]

fedOne_elos.sort(reverse=True)
fedTwo_elos.sort(reverse=True)

top100_fedOne = fedOne_elos[:100]
top100_fedTwo = fedTwo_elos[:100]

plt.figure(figsize=(12, 6))
fedOne_average = sum(top100_fedOne)/100
fedTwo_average = sum(top100_fedTwo)/100

if fedOne_average > fedTwo_average:
    plt.bar(np.arange(100), top100_fedOne, alpha = 0.75, label = federationOne)
    plt.bar(np.arange(100), top100_fedTwo, alpha=0.75, label=federationTwo)
else:
    plt.bar(np.arange(100), top100_fedTwo, alpha=0.75, label=federationTwo)
    plt.bar(np.arange(100), top100_fedOne, alpha = 0.75, label = federationOne)

plt.xlabel('Rank')
plt.ylabel('Elo Rating')
plt.title("Top 100 Players in " + federationOne +" vs " + federationTwo)
plt.legend()
plt.show()  # display the bar chart

#Q5. Is there a way to show the stats of all Live LiChess chess streamers, for example their rating as well as total games played on the website?
session=berserk.TokenSession("lip_BqpyFevAtwnkbYNlJMFB")
client=berserk.Client(session=session)
info=client.users.get_live_streamers()
list=[]
games=[]
rating=[]
for dict in info:
    for key in dict:
        if key=="id":
            list.append(dict[key])


for name in list:
    
    bigdict=client.users.get_public_data(name)
    
    for key in bigdict:
        if key=="perfs":
            smallerdict=bigdict[key]
            for keyster in smallerdict:
                
                if keyster =="blitz":
                    smallestdict=smallerdict[keyster]
                    for ke in smallestdict:
                        if ke=="games":
                            games.append(smallestdict[ke])
                        if ke=="rating":
                            rating.append(smallestdict[ke])


plt.scatter(games,rating)
plt.xlabel("Number of Games Played",fontsize=16)
plt.ylabel("Player Rating",fontsize=16)
plt.title("All Live LiChess Streamers' Elo Rating vs Number of Games Played")
plt.show()
