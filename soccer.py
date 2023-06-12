import requests
from bs4 import BeautifulSoup

naver_wfootball = "https://sports.news.naver.com/wfootball/index.nhn"
premi_team_rank = requests.get(naver_wfootball)
premi_team_rank_list = BeautifulSoup(premi_team_rank.content, "html.parser", from_encoding='utf-8')

team_rank_list = premi_team_rank_list.select('#_team_rank_epl > table > tbody > tr')

for i, o in enumerate(team_rank_list):
    if i >= 7:
        break
    rank = o.select('.blind')[0].text
    team = o.select('.name')[0].text
    print(rank, team)
