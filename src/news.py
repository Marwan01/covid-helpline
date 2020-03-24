

from newsapi import NewsApiClient
from keys import news_api_key

newsapi = NewsApiClient(api_key=news_api_key)


def return_news():
    top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                          category='health',
                                          language='en',
                                          country='us')
    NEWS  ="Today's most popular news article about Covid-19: \n\n"
    el = top_headlines['articles'][0]
    NEWS += "Title: "+ el['title'] + '\n\n'
    NEWS += "Content:\n"+ el['description'] + '\n\n'
    NEWS += "- Source: "+ el['url'] + '\n'

    NEWS
    return NEWS
