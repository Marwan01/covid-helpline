

from newsapi import NewsApiClient
from keys import news_api_key

newsapi = NewsApiClient(api_key=news_api_key)


def return_news():
    top_headlines = newsapi.get_top_headlines(q='corona virus',
                                          category='health',
                                          language='en',
                                          country='us')
    NEWS  ="Today's most popular news headlines about Covid-19: \n\n"
    for el in top_headlines['articles'][:5]:
        NEWS += "- "+ el['title'] + '\n'
    NEWS
    return NEWS
