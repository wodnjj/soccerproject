import requests
from bs4 import BeautifulSoup
import sqlite3

naver_wfootball = "https://sports.news.naver.com/wfootball/index.nhn"
premi_team_rank = requests.get(naver_wfootball)
premi_team_rank_list = BeautifulSoup(premi_team_rank.content, "html.parser", from_encoding='utf-8')

team_rank_list = premi_team_rank_list.select('#_team_rank_epl > table > tbody > tr')

# SQLite database에 연결
conn = sqlite3.connect('team_data.db')
cursor = conn.cursor()

# 테이블이 없는 경우 테이블 만들기
cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_data (
        rank INTEGER,
        team_name TEXT,
        points INTEGER
    )
''')

# team_rank_list를 반복하여 SQLite 테이블에 데이터를 삽입
for i, o in enumerate(team_rank_list):
    if i >= 7:
        break
    rank = o.select('.blind')[0].text
    team = o.select('.name')[0].text
    points = o.select('td:last-child > span')[0].text

    # Insert the data into the SQLite table
    cursor.execute('INSERT INTO team_data (rank, team_name, points) VALUES (?, ?, ?)', (rank, team, points))

# 변경 내용 commit 및 연결 닫기
conn.commit()
conn.close()

# 팀 이름으로 검색
search_team = input("팀명을 검색하세요: ")

# SQLite 데이터베이스에 연결
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

# 연결 닫기
conn.close()