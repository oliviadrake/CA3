''' gets information from a news api and returns relevant data

    gets top stories and returns headlines, descriptions and URLS'''

import requests
from config_file import return_news_api_key, return_news_url


def get_top_stories():
    ''' Reads the top stories from BBC news

        Returning a list of dictionaries '''

    api_key = return_news_api_key()

    base_url = return_news_url()
    complete_url = base_url + 'sources=bbc-news&' + "apiKey=" + api_key
    response = requests.get(complete_url)

    json_response = response.json()
    list_of_articles = json_response['articles']

    for each_article in list_of_articles:
        del each_article['source']
        del each_article['author']
        del each_article['urlToImage']
        del each_article['content']

    return list_of_articles
