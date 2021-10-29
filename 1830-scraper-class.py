#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 15:22:10 2021

@author: siddharthvenkatesh

This script aims to construct a class with  methods for scraping and storing data from the 18xx.games api for 1830 games.
"""

import requests
import pathlib
import bs4
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class Scraper1830(object):
    
    def __init__(self, ID):
        # ID is a string representing the game ID on 18xx.games
        
        #General api url for website
        api_url = 'https://18xx.games/api/game/'
        #Game ID number
        self.id = ID
        # Link to the API for the game
        self.api = api_url + self.id
        # Json file consisting of the players, results and game actions.
        self.log = requests.get(self.api).json()
        
        #URL for finished game page
        self.url = "https://18xx.games/game/" + self.id
       
        # Game Title
        self.title = self.log['title']
        
        #Raise error if game id belongs to a game not in scope of scraper
        if self.title !='1830':
            raise TypeError('Game ID must belong to a finished 1830 game, the scraper is not designed for other games or unfinished games.')
        
        # List of the privates in increasing order of base price.
        self.privates = ['SV', 'CS', 'DH', 'MH', 'CA', 'BO']
        
        # List of players in initial turn order
        
        self.players = self.log['players']
        
        
    def get_player_dict(self):
        """
        This function takes a scraper, parses the log and returns a dictionary whose 
         keys are player id numbers as ints and whose values are player name strings.

        """
        
        players = dict([d.values() for d in self.players])
        
        return players
    
    def get_private_auction(self):
        """
        This function takes a scraper, parses the log and returns a dictionary whose keys are the 
         private companies in the game and whose values are tuples (player name string, int representing price paid).


        """
        
        prices = {}
        
        # The next block of code iterates through the 'actions' field of the game log. Any time it encounters a 'bid' action
        # representing a bid on a private company, it updates that company's price with the new bid and updates the person 
        # winning the bid . Since the last 'bid' action records the final purchase of the private, the tuple at the end 
        # records the winner and the price paid.
        
        for action in self.log["actions"]:
            if action["type"] != "bid":
                continue
            prices[action["company"]] = (self.get_player_dict()[action["entity"]], action["price"])
        
        return prices
    
    def get_priority(self):
        """
        This function takes a scraper and returns the player name string of the player who had priority in stock round 1. 

        """
        
        action_counter = 0
        for action in self.log['actions']:
            
            if not (action['type'] =='par' and action['corporation'] == 'B&O'):
                action_counter+=1
                continue
            else: 
                action_counter +=1
                break
        print(action_counter)
        
        priority_id = self.log['actions'][action_counter]['entity']      
        
        return self.get_player_dict()[priority_id]


    def get_result(self):
        """
        This funtion takes a scraper and returns a dictionary whose keys are player ids and
         returns a dictionary whose keys are player name strings and whose values are their final scores as ints.

        """
        
        result = self.log['result']
        
        return result
    
    
    def get_player_history(self):
         """
         This function takes a scraper and returns a dictionary with keys strings representing player names and round numbers and values
          representing the player names and their scores at the end of each round.

         """
         
         def start_firefox_driver():
             """
             This function loads a headless copy of Firefox in Python. It is needed to load the javascript on a webpage to scrape 
              html output.
             """
             options = Options()
             options.add_argument("-headless")
             firefox = Firefox(options=options)
             return firefox    
    
         def ready(driver):
             """
             Driver is a firefox driver loaded via Selenium. This function tests that a particular table "player_table" has 
             loaded on self.url and returns a boolean (true if the table has loaded and false if not).

             """
             return driver.execute_script("return !!document.querySelector('#player_or_history');")
        
         print("Firefox Driver Loading:")
         
         # Initialize driver
         firefox = start_firefox_driver()
         
         print("Driver loaded, loading game page:")
         
         # Get the page on self.url
         firefox.get(self.url)
         # Wait till the javascript on the page runs and loads the tables.
         WebDriverWait(firefox, 5).until(ready)
         # Grab the body of the game page
         html_string = firefox.execute_script("return document.body.outerHTML")
         
         print("Page loaded, parsing html")
         
         # Use Beautiful Soup to parse the html.
         soup = bs4.BeautifulSoup(html_string, 'lxml')
         
         # Write entries into a dictionary
         dictionary = {}
         # Find the table containing the player names.
         table = soup.select('#player_table')[0]
         # Find the player names and write them to the dictionary
         names = [entry.get_text() for entry in table.find_all('th', {'class': 'name nowrap'})]
         dictionary['player_order'] = names
         # Find the table containing the player score history
         score_table = soup.select('#player_or_history')[0]
         # Enter the player scores into the dictionary
         for row in score_table.children:
             if isinstance(row, bs4.NavigableString):
                 continue
             else:
                 key = row.select('th')[0].get_text()
                 value = [c.get_text() for c in row.select('td')]
                 dictionary[key] = value
        
        
         return dictionary
     
    def player_history_table(self):
         """
         Returns the result from get_player_history as a pandas dataframe with the keys as the row index.

         """
         dictionary = self.get_player_history()
         
         return pd.DataFrame.from_dict(dictionary, orient='index')
     
    
    
            

def test1(): #test the class on game number 60001. test comparisons are obtained by looking at the self.log json directly.
    if __name__ == '__main__':
        scraper = Scraper1830('60001')
        assert scraper.id == '60001'
        assert scraper.api == 'https://18xx.games/api/game/60001'
        assert scraper.get_player_dict()[1903] == 'tango sucka'
        
        print(scraper.get_priority())
        
        # assert scraper.get_priority() ==  'lilyh'
        
        assert scraper.get_private_auction() == {'DH': ('lilyh', 100), 'CS': ('JoonGloom', 45), 'MH': ('The Beerguard', 155), 
                                                 'CA': ('MiroungaExpress', 200), 'SV': ('JoonGloom', 20), 'BO': ('tango sucka', 220)}
        
        assert scraper.log['result']['JoonGloom']==1524
        
        print(scraper.get_player_history())
        
        print(scraper.player_history_table())
        
        
test1()
        