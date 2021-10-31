# 1830 Game Log Scraper:

The goal of this repository is to build a package to scrape game data for 1830 games from the 18xx.games api. 

## Installation Instructions:

`conda env create --file=environment.yml`

## Implemented Features:

1. An attribute recording the list of players in the game in initial turn order.
2. Methods that record the distribution of privates, the player with priority in stock round 1 and the final player scores. 

## Upcoming Features:

Here are some features that are planned to be added to this scraper:

1. A table recording the player scores at the end of each stock round and operating round, along with their share counts.
2. A dictionary that records when a private is sold in to a company or closes and how much it is sold for, or for the B&O private, when the private closes.
3. Graphical representations of the data.
4. Representations of the data in a 2d pandas array.



## Planned Applications of the Scraper:

There are two main applications in mind:

1. Build a package that allows users to input game ids and obtain tables and graphs representing their game history.
2. Scrape a large number of finished 1830 games to build a model that predicts player win probabilities from the results of the private auction.
