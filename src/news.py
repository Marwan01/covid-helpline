

from newsapi import NewsApiClient
from keys import news_api_key

newsapi = NewsApiClient(api_key=news_api_key)


def return_news():
    top_headlines = newsapi.get_top_headlines(q='corona virus',
                                          category='health',
                                          language='en',
                                          country='us')
    NEWS  ="Today's most popular article about Covid-19: \n\n"
    el = top_headlines['articles'][0]
    NEWS += "- Title: "+ el['title'] + '\n'
    NEWS += "- Content:"+ el['description'] + '\n'
    NEWS += "- Source: "+ el['url'] + '\n'
    NEWS += el['urlToImage'] + '\n'

    NEWS
    return NEWS
