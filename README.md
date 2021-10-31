# 1830 Game Log Scraper:

The goal of this repository is to build a package to scrape game data for 1830 games from the 18xx.games api. 

## Implemented Features:

1. An attribute recording the list of players in the game in initial turn order.
2. Methods that record the distribution of privates, the player with priority in stock round 1 and the final player scores. 
3. Methods to record the round by round score history of the game.
3. A Python package that plots a graph of the round by round score history and can be run in the command line. Pypi link: https://pypi.org/project/scraper1830/

## Installation Instructions for scraper1830 package:

Using pip:
1. pip install scraper1830 to install all the dependencies.
2. Download geckodriver (from https://github.com/mozilla/geckodriver/releases for example)
3. Download Firefox

Using conda:

1. Download the source code and the environment.yml file and make a new environment using the command `conda env create --file=environment.yml` This will install geckodriver for you.

## Running the package in the command line:
1. Run the command `python -m scraper1830.scraper_cli plot-history --id <GAME_ID>`, where GAME_ID is the id number of the game on 18xx.games.
2. This will save the score history graph of your game as 1830-<GAME_ID>.png.



## Upcoming Features:

Here are some features that are planned to be added to this scraper:

1. Add more features to the score graph, showing where privates were bought in and where the phase changes occur.
2. Representations of the data in a 2d pandas array.



## Planned Applications of the Scraper:

There are two main applications in mind:

1. Build a package that allows users to input game ids and obtain tables and graphs representing their game history.
2. Scrape a large number of finished 1830 games to build a model that predicts player win probabilities from the results of the private auction.
