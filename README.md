# FXscraper
A web scraper written entirely in Python that periodically extracts the value of the dollar-euro exchange rate from Xrates.com, stores it in a database, and shows a graph with the exchange value evolution over time.
The purpose of this project was to exercise my Python skills, that's why I used lot of libraries, I wanted to do everything with Python. You can find the precise version of the libraries in the requirements.txt file.

The web scraper first creates the database, then executes periodically two cycles, one for extracting and storing the value, and another one for creating and showing the graph. The whole program is heavily commented,
so you can find the details there.
