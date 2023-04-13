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

countryFedCodes = {}
with open('chessFederationCodes.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        federation = row['\ufeffFed']
        country = row['Country']
        normCountry = country.replace(" ", "")
        countryFedCodes[normCountry.lower()] = federation

IDsToFederations = {}

print(len(countryFedCodes))

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
    for row in reader:
        id = row['fide_id']
        if row['rating_standard']:
            elo = int(row['rating_standard'])
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


     

