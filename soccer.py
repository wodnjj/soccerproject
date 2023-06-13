import requests
from bs4 import BeautifulSoup

naver_wfootball = "https://sports.news.naver.com/wfootball/index.nhn"
premi_team_rank = requests.get(naver_wfootball)
premi_team_rank_list = BeautifulSoup(premi_team_rank.content, "html.parser", from_encoding='utf-8')

team_rank_list = premi_team_rank_list.select('#_team_rank_epl > table > tbody > tr')
# 유럽대항전 나갈 수 있는 제한 된 순위
for i, o in enumerate(team_rank_list):
    if i >= 7:
        break
    rank = o.select('.blind')[0].text
    team = o.select('.name')[0].text
    points = o.select('td:last-child > span')[0].text
    print(rank, team, points)
