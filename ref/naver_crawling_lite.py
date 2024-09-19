import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

now = datetime.now() #save file name to current time
queries = set() #keywords to search
visited_urls = set()
source_list = []
data = []

def crawler():
  base_url = "https://search.naver.com/search.naver?where=news&query="

  for query in queries:
    #request search result page
    response = requests.get(base_url + query)
    if response.status_code != 200:
      print(f'페이지 로딩 오류: {response.status_code}')
      continue

    #HTML parsing using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    #newspaper publishers
    sources = soup.find_all('a', 'info press')
    for source in sources:
      source_list.append(source.text)

    #news titles and url
    articles = soup.find_all('a', class_='news_tit')
    for article in articles:
      url = article['href']
      title = article.get('title')

      #avoid duplicates
      if url not in visited_urls:
        visited_urls.add(url)
        data.append({'query': query, 'source': source_list[articles.index(article)], 'title': title, 'url': url})
    
  df = pd.DataFrame(data)
  print(df) #debug

  # output to csv
  output_name = 'result_%s-%s-%s %s-%s-%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
  df.to_csv(f'{output_name}.csv', index=False, encoding='cp949', errors='ignore')
  print(f'크롤링 완료! {output_name}.csv 이름으로 저장됩니다.')

while True:
  query = input('>> 검색할 키워드를 입력하세요. 다음으로 넘어가려면 엔터를 한번 더 누르세요: ')
  if query == '':
    break
  else:
    queries.add(query)
print('검색할 키워드: ', queries)

crawler()