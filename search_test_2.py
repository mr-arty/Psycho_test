import requests
import settings



def search_f(search_q, pn_q):    #Функция поиска
    page = (pn_q - 1) * 10 + 1
    URL = 'https://www.googleapis.com/customsearch/v1'
    payload = {'key':settings.API_key, 'cx':settings.cx, 'q':search_q, 'start':page}

    r=requests.get(URL, params = payload)  #get-запрос
    r=r.json()
    
    for names in r['items']:   #цикл для перебора элементов списка
        print(names['title'], names['link'])

pn = 1

def new_search():    #Новый поиск
    global search
    global pn
    print('Input search term(s): ')
    search = str(input())
    pn = 1
	
new_search()

while pn != 0:
    if pn == 101:    #Если номер страницы 101, начинаем поиск заново
	    new_search()

    search_f(search, pn)
    print('Input page number or 101 for new query: ')
    pn = int(input())