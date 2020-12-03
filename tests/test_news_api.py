''' This function is to test the program functions of the smart alarm

    Each function is tested with a single test case and the result is
    printed to the user in the stdout'''

from news_api import get_top_stories


def test_news():
    ''' test get top stories function of the module '''

    news_return = get_top_stories()
    assert type(news_return) is list, 'News Return Function: FAILED'
