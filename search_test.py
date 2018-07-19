import requests
import settings


URL = 'https://www.googleapis.com/customsearch/v1?key=' + settings.API_key + '&cx=' + settings.cx + '&q='

def search_f(search_q):
    r=requests.get(URL + search_q).json()

    for names in r['items']:
        print(names['title'], names['link'])

print('Input search term(s): ')
search = str(input())

search_f(search)