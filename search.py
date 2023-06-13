import requests
from bs4 import BeautifulSoup
import sqlite3

naver_wfootball = "https://sports.news.naver.com/wfootball/index.nhn"
premi_team_rank = requests.get(naver_wfootball)
premi_team_rank_list = BeautifulSoup(premi_team_rank.content, "html.parser", from_encoding='utf-8')

team_rank_list = premi_team_rank_list.select('#_team_rank_epl > table > tbody > tr')

# Connect to the SQLite database
conn = sqlite3.connect('team_data.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_data (
        rank INTEGER,
        team_name TEXT,
        points INTEGER
    )
''')

# Iterate through the team_rank_list and insert the data into the SQLite table
for i, o in enumerate(team_rank_list):
    if i >= 7:
        break
    rank = o.select('.blind')[0].text
    team = o.select('.name')[0].text
    points = o.select('td:last-child > span')[0].text

    # Insert the data into the SQLite table
    cursor.execute('INSERT INTO team_data (rank, team_name, points) VALUES (?, ?, ?)', (rank, team, points))

# Commit changes and close the connection
conn.commit()
conn.close()

# Search for a team by name
search_team = input("팀명을 검색하세요: ")

# Connect to the SQLite database
conn = sqlite3.connect('team_data.db')
cursor = conn.cursor()

cursor.execute("SELECT rank, team_name, points FROM team_data WHERE team_name = ?", (search_team,))
result = cursor.fetchone()

if result:
    rank, team, points = result
    print("Rank:", rank)
    print("Team:", team)
    print("Points:", points)
else:
    print("Team not found.")

# Close the connection
conn.close()