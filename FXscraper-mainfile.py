# IMPORT OF THE LIBRARIES
import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import datetime
import matplotlib.pyplot as plt
import schedule
import time

# DEFINITION OF THE WEBSITE URL
url = "https://www.x-rates.com/calculator/?from=USD&to=EUR&amount=1"

# CREATE THE SQLite DATABASE
db_path = os.path.join("fxscraper", "Dollar-Euro.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# CREATION OF THE DATABASE TABLE
c.execute('''CREATE TABLE IF NOT EXISTS Dollar_Euro
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              rate REAL,
              timestamp TEXT)''')

# DEFINITION OF THE FUNCTION TO EXTRACT THE EXCHANGE RATE AND STORE IT IN A DATABASE
def get_rate():

    # execution of the http request and extraction of the exchange rate from the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    rate = soup.find("span", {"class": "ccOutputRslt"}).text

    # set date and time
    timestamp = str(datetime.datetime.now())

    # database storing
    c.execute("INSERT INTO Dollar_Euro (rate, timestamp) VALUES (?, ?)",
              ((rate), timestamp))
    conn.commit()
    print("Exchange rate stored in the database")

# DEFINITION OF THE FUNCTION TO CREATE A GRAPH ON THE EVOLUTION OF THE EXCHANGE RATE OVER TIME
def plot_rate():

    # query to get data from the database
    c.execute("SELECT * FROM Dollar_Euro")
    data = c.fetchall()

    # parsing of the data in different lists for the exchange value and the timestamps
    rates = [row[1] for row in data]
    timestamps = [datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f") for row in data]

    # graph creation
    fig, ax = plt.subplots()
    ax.plot(timestamps, rates)
    ax.set_xlabel("Date and time")
    ax.set_ylabel("Exchange rate")
    ax.set_title("Dollar-Euro exchange rate")
    plt.show()

# PROGRAMMED FUNCTIONS EXECUTION EVERY ONE MINUTE
schedule.every(1).minutes.do(get_rate)
schedule.every(1).minutes.do(plot_rate)

while True:
    schedule.run_pending()
    time.sleep(1)