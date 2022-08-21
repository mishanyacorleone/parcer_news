import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

agent = UserAgent()

response = requests.get(url='https://www.ninefornews.nl/page/2/', headers={
    'user-agent': f'{agent.random}'
}).text
new = BeautifulSoup(response, 'lxml').find_all('div', class_='mag-box-container clearfix')[1].find('a').get('href')
title = BeautifulSoup(response, 'lxml').find_all('div', class_='mag-box-container clearfix')[1].find('h2', class_='post-title').text
response_new = requests.get(url=new, headers={
    'user-agent': f'{agent.random}'
}).text
soup = BeautifulSoup(response, 'lxml')
count_comments = soup.find('span', class_='meta-comment tie-icon meta-item fa-before').get_text()
count_views = soup.find('span', class_='meta-views meta-item').get_text()
with open('data.csv', 'w', encoding='utf-8') as F:
    writer = csv.writer(F)
    writer.writerow([
        'title', 'count_comments', 'count_views'
    ])
    writer.writerow([
        title, count_comments, count_views
    ])

# with open('new_data.csv', 'w', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow([
#         'title', 'count_comments', 'count_views'
#     ])


def parse(agent=agent):
    for page in range(2, 203):
        response = requests.get(url=f'https://www.ninefornews.nl/page/{page}/', headers={
            'user-agent': f'{agent.random}'
        }).text
        try:
            soup = BeautifulSoup(response, 'lxml').find_all('div', class_='main-content tie-col-md-8 tie-col-xs-12')[0].find('div', id='tie-block_2154')
            news = soup.find_all('li', class_='post-item tie-standard')
            news_not_full_tag = soup.find_all('li', class_='post-item')
            # if len(news) != 0:
            #     for new in news:
            #         title_new = new.find('h2', class_='post-title').text
            #         count_comments_new = new.find('span', class_='meta-comment tie-icon meta-item fa-before').text
            #         count_views_new = ''
            #         if new.find('span', class_='meta-views meta-item') != None:
            #             count_views_new = new.find('span', class_='meta-views meta-item').text
            #         elif new.find('span', class_='meta-views meta-item warm') != None:
            #             count_views_new = new.find('span', class_='meta-views meta-item warm').text
            #         elif new.find('span', class_='meta-views meta-item hot') != None:
            #             count_views_new = new.find('span', class_='meta-views meta-item hot').text
            #         else:
            #             count_views_new = new.find('span', class_='meta-views meta-item very-hot').text
            #         with open('data.csv', 'a', encoding='utf-8') as file:
            #             writer = csv.writer(file)
            #             writer.writerow([
            #                 title_new, count_comments_new, count_views_new
            #             ])
            if len(news_not_full_tag) != 0:
                for new in news_not_full_tag:
                    title_new = new.find('h2', class_='post-title').text
                    count_comments_new = new.find('span', class_='meta-comment tie-icon meta-item fa-before').text
                    count_views_new = ''
                    if new.find('span', class_='meta-views meta-item') != None:
                        count_views_new = new.find('span', class_='meta-views meta-item').text
                    elif new.find('span', class_='meta-views meta-item warm') != None:
                        count_views_new = new.find('span', class_='meta-views meta-item warm').text
                    elif new.find('span', class_='meta-views meta-item hot') != None:
                        count_views_new = new.find('span', class_='meta-views meta-item hot').text
                    else:
                        count_views_new = new.find('span', class_='meta-views meta-item very-hot').text
                    with open('data.csv', 'a', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            title_new, count_comments_new, count_views_new
                        ])
            else:
                print('Error error error')
            print(page)
        except Exception as ex:
            print(page, ex)


def main():
    parse()


if __name__ == '__main__':
    main()